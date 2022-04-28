import json, urllib.request, re, base64, sys, os
from PIL import Image

save_to_folder = 'images_decoded/'
encodedBytes = []
decodedBytes = []
nJsonFileName = ""

def parserJson():
    global encodedBytes, sFile_name
    jsonData = json.load(open(sFile_name, 'r'))

    counter = 3
    while True:
        try:
            sBase64 = jsonData['log']['entries'][counter]['response']['content']['text']
            sUrl = jsonData['log']['entries'][counter]['request']['url']
            bIsImage = jsonData['log']['entries'][counter]['response']['content']['mimeType'] == 'image/png'

            if bIsImage:
                encodedBytes.append([sBase64, sUrl])
            
        except IndexError:
            break
        except KeyError:
            pass
        
        counter += 1


def decodeImages():
    global encodedBytes, decodedBytes

    nCounter = 0
    for encodedImage in encodedBytes:
        try:
            decodedBytes.append([base64.b64decode(encodedImage[0]), encodedBytes[nCounter][1]])
        except Exception:
            pass

        nCounter += 1

def saveImages():
    global decodedBytes, save_to_folder

    for decoded in decodedBytes:
        sFile_name = save_to_folder + re.sub('[^0-9]','', decoded[1][-7:]) + '.png'
        
        print('Finished: ' + sFile_name)
        
        with open(sFile_name, 'wb') as img:
            img.write(decoded[0])

def imagesToPDF():
    path = os.listdir(save_to_folder)
    firstImage = Image.open(f'{save_to_folder}/01.png').convert('RGB')
    imageList = []

    for file in path:
        if file != '01.png':
            imageList.append(Image.open(f'{save_to_folder}/{file}').convert('RGB'))
        
    firstImage.save('Buch.pdf', save_all=True, append_images=imageList)  

if __name__ == '__main__':
    if len(sys.argv) > 1:
        sFile_name = sys.argv[1]

        parserJson()
        decodeImages()
        saveImages()

        if input('\nconvert images to PDF? (y/n): ').upper() == 'Y':
            imagesToPDF()

    else:
        print('please specify a file name... (westermann-ripper.py filename.har)')
