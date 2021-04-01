import argparse
import base64
import configparser
import html
import json
import os
import sys
import time
from string import Template

import music_tag
import requests
from tqdm import tqdm

# pyinstaller --onefile --icon=logo.ico --add-data="data_files/template.wpl;data_files" .\joox_dl.py
configName = 'joox_dl.cfg'

if getattr(sys, 'freeze', False):
    applicationPath = os.path.dirname(sys.executable)
else:
    applicationPath = os.path.dirname(__file__)

configPath = os.path.join(applicationPath, configName)
configParser = configparser.RawConfigParser()
configParser.read(configPath)

m4a = None
hq = None
url_str = None
counter = 0
music_folder = configParser.get('app', 'music_folder')
wxopenid = configParser.get('login', 'wxopenid')
password = configParser.get('login', 'password')


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


# download funtion
def download_url(url, output_path):
    # url = "http://www.ovh.net/files/10Mb.dat" #big file test
    # Streaming, so we can iterate over the response.
    r = requests.get(url, stream=True)
    # Total size in bytes.
    total_size = int(r.headers.get('content-length', 0))
    block_size = 1024  # 1 Kibibyte
    t = tqdm(total=total_size, unit='iB', unit_scale=True, desc=f'Downloading - {get_last_segment(output_path)}')
    with open(output_path, 'wb') as f:
        for data in r.iter_content(block_size):
            t.update(len(data))
            f.write(data)
    t.close()
    if total_size != 0 and t.n != total_size:
        return False
    return True


# clean value from restricted symbol create folder name etc.
def clean_text(text_raw):
    return text_raw.replace('?', '').replace('\'', '').replace('\"', '').replace(':', '').replace('®', '') \
        .replace('ñ', 'n').replace('Ã±', 'n').replace('/', '-').replace('|', '-').replace('â', 'a').replace('.', '')


def get_track(url):
    song_id = url.split("/")[-1]
    with requests.Session() as s:
        epoch = int(time.time()) - 60
        s.get(
            "https://api.joox.com/web-fcgi-bin/web_wmauth?country=id&lang=id&wxopenid=" +
            wxopenid + "&password=" +
            password + "&wmauth_type=0&authtype=2" +
            "&time=" + str(epoch) + "294&_=" + str(epoch) + "295&callback=axiosJsonpCallback1")
        url_track = "http://api.joox.com/web-fcgi-bin/web_get_songinfo?songid=" + song_id

        r = s.get(url_track)

        data_track_raw = r.text
        data_track_raw = data_track_raw[data_track_raw.find("(") + 1:-1]

        data_track = json.loads(data_track_raw)

        if data_track['msg'] == "invaid cookie":
            print("Invalid cookie.")
            sys.exit(0)

        data_track['msinger'] = clean_text(data_track['msinger'])
        data_track['malbum'] = clean_text(data_track['malbum'])
        data_track['msong'] = clean_text(data_track['msong'])

        url_additional_data_track = "https://api-jooxtt.sanook.com/page/single?" + \
                                    "regionURI=id-id&country=id&lang=id&id=" + \
                                    str(song_id) + "&device=desktop"
        r = s.get(url_additional_data_track)
        additional_data_track_raw = json.loads(r.text)
        if 'single' in additional_data_track_raw and additional_data_track_raw['single']['status_code'] == 0:
            additional_data_track = additional_data_track_raw['single']
        else:
            additional_data_track = None

        global counter
        counter += 1
        data_track['tracknumber'] = counter

        link_track = get_link_track(data_track)
        if link_track:
            file_type = link_track.split('?')
            file_type = file_type[0].split('.')
            file_type = file_type[-1]

            file_name = data_track['msong'] + '.' + file_type
            data_track['fpath'] = get_full_path_music(data_track, file_name)

            if not os.path.exists(data_track['fpath']):
                if download_url(link_track, data_track['fpath']):
                    set_tag(s, data_track, additional_data_track)
            else:
                print(get_info(data_track) + ' - sudah ada.')
                set_tag(s, data_track, additional_data_track)

            data_track['apath'] = os.path.abspath(data_track['fpath'])
            data_track['spath'] = '../' + data_track['fpath'][len(music_folder):]

            return data_track
        if m4a:
            file_type = 'm4a'
        else:
            file_type = 'mp3'
        file_name = data_track['msong'] + '.' + file_type
        data_track['fpath'] = get_full_path_music(data_track, file_name)

        if os.path.exists(data_track['fpath']):
            print(get_info(data_track) + ' - sudah ada.')
            data_track['apath'] = os.path.abspath(data_track['fpath'])
            data_track['spath'] = '../' + data_track['fpath'][len(music_folder):]
            return data_track

        print(get_info(data_track) + ' - link rusak.')
        return None


def get_info(data_track):
    return data_track['msinger'] + '/' + data_track['malbum'] + '/' + data_track['msong']


def get_full_path_music(data_track, file_name):
    if not os.path.exists(music_folder):
        os.makedirs(music_folder)

    artist_folder = music_folder + 'Artists/' + data_track['msinger'] + '/'
    if not os.path.exists(artist_folder):
        os.makedirs(artist_folder)

    album_folder = artist_folder + data_track['malbum'] + '/'
    if not os.path.exists(album_folder):
        os.makedirs(album_folder)

    return album_folder + file_name


def get_link_track(data_track):
    kbps_map = json.loads(data_track['kbps_map'])

    if m4a and hq and kbps_map['192'] > 0:
        return data_track['r192Url']
    elif m4a and kbps_map['96'] > 0:
        return data_track['m4aUrl']
    elif hq and kbps_map['320'] > 0:
        return data_track['r320Url']
    elif kbps_map['128'] > 0:
        return data_track['mp3Url']
    else:
        return None


def set_tag(session, data_track, additional_data_track=None):
    audiofile = music_tag.load_file(data_track['fpath'])
    audiofile['artist'] = data_track['msinger']
    audiofile['album'] = data_track['malbum']
    audiofile['albumartist'] = data_track['msinger']
    audiofile['tracktitle'] = data_track['msong']
    audiofile['comment'] = 'Generated By j4r1s \n' + \
                           get_single_link(data_track['encodeSongId']) + '\n' + \
                           str(url_str)
    if get_mode(str(url_str)) == 'album':
        audiofile['tracknumber'] = data_track['tracknumber']

    if additional_data_track:
        audiofile['genre'] = additional_data_track['genre'] if 'genre' in additional_data_track else None
        audiofile['year'] = str(additional_data_track['release_time']) \
            if 'release_time' in additional_data_track else None
        if additional_data_track['lrc_exist'] == 1:
            audiofile['lyrics'] = str(base64.b64decode(additional_data_track['lrc_content'])) \
                if 'lrc_content' in additional_data_track else None
        else:
            audiofile['lyrics'] = None
    else:
        audiofile['genre'] = None
        audiofile['year'] = None
        audiofile['lyrics'] = None

    if data_track['imgSrc'] != "":
        response_img = session.get(data_track['imgSrc'])
        audiofile['artwork'] = response_img.content
    try:
        audiofile.save()
    except Exception:
        print("Skipped " + get_info(data_track) + " in use.")


def get_last_segment(url):
    return url.split("/")[-1]


def get_uri(url, index=0, num=30):
    if get_mode(url) == 'playlist':
        return "https://api-jooxtt.sanook.com/openjoox/v1/playlist/" + \
               str(get_last_segment(url)) + "/tracks?country=id&lang=id&index=" + str(index) + "&num=" + str(num)
    elif get_mode(url) == 'album':
        return "https://api-jooxtt.sanook.com/openjoox/v1/album/" + \
               str(get_last_segment(url)) + "/tracks?country=id&lang=id&index=" + str(index) + "&num=" + str(num)
    elif get_mode(url) == 'artist':
        return "https://api-jooxtt.sanook.com/openjoox/v1/artist/" + \
               str(get_last_segment(url)) + "/tracks?country=id&lang=id&index=" + str(index) + "&num=" + str(num)
    elif get_mode(url) == 'chart':
        return "https://api-jooxtt.sanook.com/page/chartDetail?country=id&lang=id&id=" + \
               str(get_last_segment(url))
    return None


def get_mode_text(url):
    if get_mode(url) == 'playlist':
        return "Playlist"
    elif get_mode(url) == 'album':
        return "Album"
    elif get_mode(url) == 'artist':
        return "Artist"
    elif get_mode(url) == 'chart':
        return "Chart"
    return ""


def get_artist_detail_uri(url):
    return "https://api-jooxtt.sanook.com/page/artistDetail?id=" + \
           str(get_last_segment(url)) + "&lang=id&country=id"


def get_mode(url):
    if 'playlist' in url:
        return "playlist"
    elif 'album' in url:
        return "album"
    elif 'artist' in url:
        return "artist"
    elif 'single' in url:
        return "single"
    elif 'chart' in url:
        return "chart"
    return None


def get_single_link(encodestr):
    return 'https://www.joox.com/id/single/' + encodestr.replace('/', '_')


def generate_wpl(title, pathlist):
    medialist = []
    for path in pathlist:
        medialist.append('<media src="' + html.escape(path) + '"/>')

    # Data Playlist
    data_playlist = {
        'title': html.escape(title),
        'medialist': '\n'.join(medialist)
    }
    file_path = resource_path('data_files/template.wpl')
    with open(file_path, 'r') as f:
        src = Template(f.read())
        result = src.substitute(data_playlist)

        playlist_folder = music_folder + 'Playlists/'
        if not os.path.exists(playlist_folder):
            os.makedirs(playlist_folder)

        playlist_fpath = playlist_folder + title + '.wpl'
        f_playlist = open(playlist_fpath, "w", encoding="utf-8")
        f_playlist.write(result)
        f_playlist.close()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--url', help='url String')
    parser.add_argument('-m', '--m4a', help='m4a Type', action='store_true')
    parser.add_argument('-hq', '--highquality', help='high quality', action='store_true')

    args = parser.parse_args()
    global url_str
    url_str = vars(args)['url']
    global hq
    hq = vars(args)['highquality']
    global m4a
    m4a = vars(args)['m4a']
    global music_folder

    if url_str is None:
        parser.print_help()
        parser.exit()

    mode = get_mode(url_str)
    if mode is None:
        print("Url tidak dikenal.")

    else:
        if mode == "single":
            # downloading track
            get_track(url_str)
            print('Selesai!')
        else:
            uri = get_uri(url_str)
            if get_mode(url_str) == "chart":
                r = requests.get("https://api-jooxtt.sanook.com/page/chartlist?country=id&lang=id&device=desktop")
                raw_data_chart_list = r.json()
                data_chart_list = raw_data_chart_list['topcharts']['data']
                chart = None
                for item in data_chart_list:
                    if str(item['id']) == get_last_segment(url_str):
                        chart = item
                        break
                if chart:
                    chart_name = chart['name'] + " - " + chart['update_time']
                else:
                    chart_name = "Chart"

                # fecthing track
                r = requests.get(uri)
                data = r.json()
                path_list = []
                for item in data['tracksItemList']['tracks']['items']:
                    # downloading track
                    infotrack = get_track(get_single_link(item['id']))
                    if infotrack:
                        # For Create Playlist
                        path_list.append(infotrack['spath'])
                # Create Playlist
                generate_wpl(clean_text(chart_name), path_list)
                print(get_mode_text(url_str) + ' - ' + str(chart_name) + ' : ' + str(counter) + "/" +
                      str(data['tracksItemList']['tracks']['total_count']) +
                      ' lagu.' + ' - Selesai!')
            else:
                total_song = None
                name = None
                if get_mode(url_str) == "artist":
                    uri_detail = get_artist_detail_uri(url_str)
                    r = requests.get(uri_detail)
                    data_detail = r.json()
                    name = clean_text(data_detail['artistInfo']['name'])

                path_list = []
                proses = True
                while proses:
                    r = requests.get(uri)
                    data = r.json()

                    total_song = data['tracks']['total_count']

                    # fecthing track
                    for item in data['tracks']['items']:
                        # downloading track
                        infotrack = get_track(get_single_link(item['id']))
                        if infotrack:
                            # For Create Playlist
                            path_list.append(infotrack['spath'])

                    if data['tracks']['next_index'] is None:
                        proses = False

                        if get_mode(url_str) != "artist":
                            name = data['name']
                        prefix_plist = ''
                        # get artist name for album playlist
                        if 'artist_list' in data:
                            if len(data['artist_list']) > 0:
                                prefix_plist += clean_text(data['artist_list'][0]['name']) + ' - '
                        pl_name = clean_text(prefix_plist + name)

                        # Create Playlist
                        generate_wpl(pl_name, path_list)
                    else:
                        uri = get_uri(url_str, data['tracks']['next_index'])
                print(get_mode_text(url_str) + ' - ' + str(name) + ' : ' + str(counter) + "/" + str(total_song) +
                      ' lagu.' + ' - Selesai!')


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
