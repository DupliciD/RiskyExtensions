import requests
import os

id_list = [  # top 3
    'lidmdigdjdmkncijlceoohlffbnaeomb',  # the bible - 11193
    'ddfggnpadelhnkhiimnmfaappkbjnaan',  # Turbo Chrome - 8206
    'ahbkhnpmoamidjgbneafjipbmdfpefad',  # Web boost - 7527
]

# id_list = [  # Everything else above 2000 risk.
#     'conoainidgmlpjihapjpjgmmciigmhlk',
#     'pchphbfeejhdhpclfgeaomnljoiepedl',
#     'bkagcmloachflbbkfmfiggipaelfamdf',
#     'ooppcohacjcoekjgiajkkjgepofncbdl',
#     'hkcgfmboahoaaafjdfdanijmdbamaiaf',
#     'fcagpljdkekieoaacpcnjpidlibopabp',
#     'kalnennlfaffhbdbnoakkiiciifmmohk',
#     'ninghifmkkhjngngnmdnebngakiamgdl',
#     'bmihblnpomgpjkfddepdpdafhhepdbek',
#     'imofnopodmphgihdnpjgnfinpfkilkge',
#     'aianhbkhjjkbelhcalmjemdbgeeblian',
#     'kgdaiemkhdbklnlbjmgpmojklhbddaaf',
#     'nlkgdjpnhddefnomcahnffcegbnlakdf',
#     'dnaendaceojlbdjbfnkcfjdgdklhnaka',
#     'mlddgfopobkcdldadhiamagfcehbhoei',
#     'ehlmnfeohfahemdjnakciaheggkojchf',
#     'gkiemgpihainopbepilmjgmolgdlmlih',
#     'pjcpffkncpkafpbjkejnpefoihacckld',
#     'chjoanbbbllaihmkkcokfkaojegehmaa',
#     'gjcgnoednebkdcnidoicdpfnenbbaphd',
#     'nhopcoeofhlmimjafafcglbeafebbmdo',
#     'hfaokbpplplaeglmcpmjacghbnidjnll',
#     'eefingeokaijnkgahbmcpenkidbohafh',
#     'ieimachclakgpglmhafclnfklklomfeh',
#     'laeniddpnkhffoidjeddcbefopdomael',
#     'onlpodkdakgonlmodbgapcbigpcimokd',
#     'mnicfonfoiffhekefgjlaihcpnbchdbc',
#     'bhfhaohjmlicimihnipmfjpdmjcehdmg',
#     'kcllaeaafnmkadnpkmamoelibejcibfd',
#     'odgdknbigjpolbjkmpgdibnjodplgdjp'
# ]


for ext_id in id_list:
    url = f'https://clients2.google.com/service/update2/crx?response=redirect&os=cros&arch=x86-64&nacl_arch=' \
        f'x86-64&prod=chromiumcrx&prodchannel=unknown&prodversion=9999&x=id%3D{ext_id}%26uc'

    response = requests.get(url)
    if response.status_code == 200:
        with open(os.path.join(os.environ['HOME'], f'crx/{ext_id}.zip'), 'wb') as f:
            f.write(response.content)

