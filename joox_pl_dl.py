import argparse
import sys
import os
import time
import datetime
import requests
from tqdm import tqdm
from pprint import pprint
import json
import re
import eyed3
from PIL import Image
from io import BytesIO
## pyinstaller --onefile --icon=logo.ico .\SKIT.py ##



def download_url(url, output_path):
    # url = "http://www.ovh.net/files/10Mb.dat" #big file test
    # Streaming, so we can iterate over the response.
    r = requests.get(url, stream=True)
    # Total size in bytes.
    total_size = int(r.headers.get('content-length', 0))
    block_size = 1024 #1 Kibibyte
    t=tqdm(total=total_size, unit='iB', unit_scale=True, desc=f'Downloading - {output_path}')
    with open(output_path, 'wb') as f:
        for data in r.iter_content(block_size):
            t.update(len(data))
            f.write(data)
    t.close()
    if total_size != 0 and t.n != total_size:
        return False
    return True
    

def main():
    parser = argparse.ArgumentParser();
    parser.add_argument('-p', '--playlistid', help='Playlist ID')
    args = parser.parse_args()
    plID = vars(args)['playlistid']

    if not plID or not periode.isnumeric():
        parser.print_help()
        parser.exit()

    # plID = "1494906408"

    urlPlaylist = "https://api-jooxtt.sanook.com/web-fcgi-bin/web_getfav?country=id&lang=id&listid="+ plID +"&reqtype=3&wmid=45970101&s=30d470dee599fb4f076a25798fcc075a"


    r = requests.get(urlPlaylist)
    data = r.json()

    for k in data['item']:
        urlTrack = "http://api.joox.com/web-fcgi-bin/web_get_songinfo?songid=" + k['gl']
        # urlTrack = "http://api.joox.com/web-fcgi-bin/web_get_songinfo?songid=TtEH_iaoAGl1dh5KsV44pg=="

        r = requests.get(urlTrack)
        dataTrackRaw = r.text
        dataTrackRaw = dataTrackRaw[18:-1]
        dataTrack = json.loads(dataTrackRaw)
        dataTrack['msong'] = dataTrack['msong'].replace('?', '');
        dataTrack['msong'] = dataTrack['msong'].replace('\'', '');
        dataTrack['msong'] = dataTrack['msong'].replace('\"', '');
        dataTrack['msong'] = dataTrack['msong'].replace(':', '');

        # with open('joox/' + dataTrack['msong']+'.json', 'w') as outfile:
        #     json.dump(dataTrack, outfile)

        # exit()

        link_track = dataTrack['mp3Url']
        fileType = link_track.split('?')
        fileType = fileType[0].split('.')
        fileType = fileType[-1]

        fileName = dataTrack['msong'] + '.' + fileType
        filePath = 'joox/' + fileName
        if(download_url(link_track, filePath)):
            audiofile = eyed3.load(filePath)

            if (audiofile.tag == None):
                audiofile.initTag()

            audiofile.tag.artist = dataTrack['msinger']
            audiofile.tag.album = dataTrack['malbum']
            audiofile.tag.album_artist = dataTrack['malbum']+' - '+ dataTrack['msinger']
            audiofile.tag.title = dataTrack['msong']

            if (dataTrack['imgSrc'] != ""):
                responseImg = requests.get(dataTrack['imgSrc'])
                mime_type = contentType = responseImg.headers['content-type']
                img = responseImg.content
                audiofile.tag.images.set(3, img, mime_type)

            audiofile.tag.save()

        # break
        
if __name__ == '__main__': 
    try:
        main() 
    except KeyboardInterrupt:
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
    except requests.ConnectionError as e:
        print("OOPS!! Connection Error. Make sure you are connected to Internet. Technical Details given below.\n")
        print(str(e))
    except requests.Timeout as e:
        print("OOPS!! Timeout Error")
        print(str(e))
    except requests.RequestException as e:
        print("OOPS!! General Error")
        print(str(e))