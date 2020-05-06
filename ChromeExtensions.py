import datetime
import json
from multiprocessing import Pool

import pandas as pd
import requests
from tqdm import tqdm


def write_log(message):
    with open('/tmp/chrome_extensions.log', 'a') as f:
        f.write(f'{datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")} -- {message}\n')


class ChromeExtension(object):
    def __init__(self, ext_id):
        self.ext_id = ext_id
        self.report = None

    @staticmethod
    def get_headers():
        with open('apikey.txt', 'r') as f:
            return {'API-Key': f.read().strip()}

    def submit_for_scan(self):
        api_url = 'https://api.crxcavator.io/v1/submit'
        try:
            response = requests.post(
                api_url,
                headers=self.get_headers(),
                json={'extension_id': f'{self.ext_id}'}
            )
            if response.status_code == 200:
                # write_log(f'Successfully submitted extension {self.ext_id} for scanning.')
                return True
            else:
                write_log(f'ERROR: Status code [{response.status_code}] while submitting extension: {self.ext_id}'
                          f'\r\n\t\tResponse:{response.text}')
                return False
        except requests.exceptions.ConnectionError as e:
            write_log(f'Connection error received when submitting {self.ext_id} to be scanned, trying again.')
            return self.submit_for_scan()

    def crxcavator_lookup(self):
        # Lookup the risk score in crxcavator as it has everything that I planned to do and more.
        api_url = f'https://api.crxcavator.io/v1/report/{self.ext_id}'
        try:
            response = requests.get(
                api_url,
                headers=self.get_headers()
            )
            if response.status_code == 200 and response.json():
                self.report = response.json()[-1]
            else:
                self.report = {}
                self.submit_for_scan()
        except requests.exceptions.ConnectionError as e:
            write_log(f'Connection error received when querying {self.ext_id}, trying again.')
            self.crxcavator_lookup()

    def get_risk_info(self, submit=False):
        if self.report is None:
            self.crxcavator_lookup()
        if self.report == {}:
            write_log(f'No data for extension {self.ext_id}')
            if submit is not False:
                self.submit_for_scan()
            return {'extension_id': self.ext_id, 'name': 'No data available.'}
        risk = self.report['data']['risk'] if 'risk' in self.report['data'].keys() else None
        report_data = {
            'extension_id': self.ext_id,
            'version': self.report['version'],
            'total_risk': risk['total'] if (risk and ('total' in risk.keys())) else None,
            'URLs': self.report['data']['extcalls'] if 'extcalls' in self.report['data'].keys() else None,
            'dangerous_fns': list(self.report['data']['dangerousfunctions'].keys()) if 'dangerousfunctions' in
                                                                                 self.report['data'].keys() else None,
            'entrypoints': self.report['data']['entrypoints'] if 'entrypoints' in self.report['data'].keys() else None,
            'csp_risk': risk['csp']['total'] if 'csp' in risk.keys() else None,
            'permissions_risk': risk['permissions']['total'] if 'permissions' in risk.keys() else None,
            'webstore_risk': risk['webstore']['total'] if 'webstore' in risk.keys() else None,
            'manifest': self.report['data']['manifest'] if 'manifest' in self.report['data'].keys() else None
        }
        webstore = self.report['data']['webstore']
        if webstore:
            report_data.update({
                'name': webstore['name'],
                'short_description': webstore['short_description'],
                'version': webstore['version'],  # available in manifest and base object
                'last_updated': webstore['last_updated'],
                'offered_by': webstore['offered_by'],  # Looks worse than mine
                'rating': webstore['rating'],
                'rating_users': webstore['rating_users'],
                'users': webstore['users'],
                'size': webstore['size'],
                'type': webstore['type'],
                'permission_warnings': webstore['permission_warnings'],
                'email': webstore['email'],
                'address': webstore['address'],
                'privacy_policy': webstore['privacy_policy']
            })
        else:
            report_data.update({
                'name': None,
                'short_description': None,
                'version': None,  # available in manifest and base object
                'last_updated': None,
                'offered_by': None,  # Looks worse than mine
                'rating': None,
                'rating_users': None,
                'users': None,
                'size': None,
                'type': None,
                'permission_warnings': None,
                'email': None,
                'address': None,
                'privacy_policy': None
            })
        return report_data


class ExtensionList(object):
    def __init__(self, ext_ids, pool_size=20):
        self.extensions = [ChromeExtension(ext_id) for ext_id in ext_ids]
        self.pool_size = pool_size

    def run_async(self, func, data, progress=True, task=None):
        with Pool(self.pool_size) as p:
            if progress:
                return_data = list(tqdm(p.imap(func, data), total=len(data), desc=task))
            else:
                return_data = list(p.imap(func, data))
        return return_data

    def get_extension_data(self):
        print(f'#### Getting CRXcavator data for {len(self.extensions)} extensions ####')
        self.extensions = self.run_async(self._lookup, self.extensions, progress=True, task='API Queries')

    @staticmethod
    def _lookup(extension) -> ChromeExtension:
        extension.crxcavator_lookup()
        return extension

    def get_data_as_df(self):
        return pd.DataFrame(self.run_async(self._export_data, self.extensions, progress=True, task='Getting CRX data'))

    @staticmethod
    def _export_data(extension) -> ChromeExtension:
        return extension.get_risk_info()

    def submit_for_scans(self):
        results = self.run_async(self._scan_crx, self.extensions, progress=True, task='Submitting CRX for scanning.')
        print(f'Submission Successes: {len([x for x in results if x is True])}')
        print(f'Submission Failures: {len([x for x in results if x is False])}')

    @staticmethod
    def _scan_crx(extension) -> ChromeExtension:
        return extension.submit_for_scan()

    def to_csv(self, csv_path):
        ext_df = self.get_data_as_df()
        columns = [
            'extension_id', 'name', 'short_description', 'version', 'last_updated', 'total_risk',
            'offered_by', 'rating', 'rating_users', 'users', 'size', 'type', 'permission_warnings', 'email',
            'address', 'privacy_policy', 'entrypoints', 'csp_risk', 'permissions_risk',
            'webstore_risk'
        ]
        ext_df.to_csv(csv_path, columns=columns, index=False, encoding='utf-8')
