import requests
import shutil
import zipfile
import os

# Get Current ElvUI installed
addonFolder = 'C:\\World of Warcraft\\_retail_\\Interface\\AddOns\\'
elvUIURL = "https://www.tukui.org/download.php?ui=elvui"

with open(addonFolder + 'ElvUI\\ElvUI-Mainline.toc', 'r') as reader:
    line = reader.readline()
    while line != '':  # The EOF char is an empty string
        if "Version: " in line: 
            elvUIInstalledVersion = line[12:]
            elvUIInstalledVersion = elvUIInstalledVersion[:-1]
            break
        line = reader.readline()

print('Installed ElvUI Version: ' + elvUIInstalledVersion)

# Get Latest ElvUI version
downloadPage = requests.get(elvUIURL)

if "downloads/elvui-" in downloadPage.text: 
    start = downloadPage.text.index('downloads/elvui-') + 16
    newVersion = downloadPage.text[start:downloadPage.text.index('.zip')]
    print('Latest ElvUI Version: ' + newVersion)

# If Installed < Latest
if(newVersion > elvUIInstalledVersion):
    print('Downloading latest version ' + newVersion)
    # Download latest zip
    downloadURL = 'https://www.tukui.org/downloads/elvui-' + newVersion + '.zip'
    zipFile = 'elvui-' + newVersion + '.zip'

    r = requests.get(downloadURL, stream=True)
    with open(zipFile, 'wb') as fd:
        for chunk in r.iter_content(chunk_size=128):
            fd.write(chunk)

    # Delete ElvUI folder from Addons
    print('Removing old version.')
    shutil.rmtree(addonFolder + '\\ElvUI')
    shutil.rmtree(addonFolder + '\\ElvUI_OptionsUI')

    # Extract zip to Addons
    print('Unzipping new version')
    with zipfile.ZipFile(zipFile, 'r') as zip_ref:
        zip_ref.extractall(addonFolder)

    os.remove(zipFile)
else:
    print("Version up to date.")