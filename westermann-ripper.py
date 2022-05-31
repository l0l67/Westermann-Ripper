import json, urllib.request, re, base64, sys, os, requests
from PIL import Image

saveDestination = 'images_decoded/'

download = False

def parseJson(filename):
    jsonData = json.load(open(filename, 'r'))

    counter = 3
    while True:
        try:
            base64str = jsonData['log']['entries'][counter]['response']['content']['text']
            url = jsonData['log']['entries'][counter]['request']['url']
            isImage = jsonData['log']['entries'][counter]['response']['content']['mimeType'] == 'image/png'

            if isImage:
                image = None
                if download:
                    image = downloadImage(url)
                else:
                    image = decodeImage(base64str)
                
                saveImage(image, f"{re.sub('[^0-9]', '', url[-7:])}.png")
            
        except IndexError:
            break
        except KeyError:
            pass
        
        counter += 1


def decodeImage(encodedData):
    return base64.b64decode(encodedData)

def downloadImage(url):
    data = requests.get(url)
    return data.content


def saveImage(image, name):
    filename = saveDestination + name
        
    with open(filename, 'wb') as img:
        img.write(image)
        
    print('Finished: ' + filename)


def imagesToPDF():
    path = os.listdir(saveDestination)
    firstImage = Image.open(f'{saveDestination}/01.png').convert('RGB')
    imageList = []

    for file in path:
        if file != '01.png' and file.endswith('.png'):
            imageList.append(Image.open(f'{saveDestination}/{file}').convert('RGB'))
        
    firstImage.save('output.pdf', save_all=True, append_images=imageList)  

if __name__ == '__main__':
    argLength = len(sys.argv)
    if argLength > 1:
        download = (argLength > 2 and sys.argv[1] == '--download')
        
        parseJson(sys.argv[argLength - 1])

        if input('\nconvert images to PDF? (y/n): ').upper() == 'Y':
            imagesToPDF()

    else:
        print('please specify a file name... (python3 westermann-ripper.py [--download] filename)')
