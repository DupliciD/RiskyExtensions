import json
import os

from ChromeExtensions import ExtensionList

# Sitemap enumerated with crawl_sitemap.py from https://github.com/mdamien/chrome-extensions-archive
sitemap_path = os.path.join(os.environ['HOME'], 'PycharmProjects/chrome-extensions-archive/crawled/sitemap/result.json')

# Read the sitemap json into a list
with open(sitemap_path, 'r') as f:
    contents = f.read()
sitemap_json = json.loads(contents)
ext_id_list = []
for ext_url in sitemap_json:
    ext_id_list.append(os.path.split(ext_url)[1])

# # Code snippet for making CRXcavator attempt to scan every extension in our list
# scan_crx = ExtensionList(ext_id_list, pool_size=25)
# scan_crx.submit_for_scans()

# Code snippet for retrieving extension data from CRXcavator
idx = 0
inc = 10000
while idx < len(ext_id_list)/10000:
    if f'dump{idx}.csv' not in os.listdir(os.path.join(os.environ['HOME'], 'csvs')):
        crx = ExtensionList(ext_id_list[idx*inc:(idx+1)*inc], pool_size=25)
        crx.to_csv(os.path.join(os.environ['HOME'], f'csvs/dump{idx}.csv'))
        print(f'{idx*inc}-{(idx+1)*inc}: Saved to {os.environ["HOME"]}/csvs/dump{idx}.csv')
    else:
        print(f'Skipping {idx*inc}-{(idx+1)*inc} because dump{idx}.csv already exists...')
    idx += 1

print('Script complete')
