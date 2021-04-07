<p align="center">
    <img alt="logo" src="https://fajar-isnandio.com/wp-content/uploads/2020/12/joox_dl.png"  height="100" style="margin-bottom: 10px;">
</p>
<p align="center">Joox DL is Joox Downloader for Python.</p>
<p align="center">
    <a href="https://www.python.org/downloads/release/python-391/"><img alt="Python" src="https://img.shields.io/badge/python-v3.9-blue"></a>
    <a href="https://github.com/jaris58/joox_dl/network"><img alt="GitHub forks" src="https://img.shields.io/github/forks/jaris58/joox_dl"></a>
    <a href="https://github.com/jaris58/joox_dl/stargazers"><img alt="GitHub stars" src="https://img.shields.io/github/stars/jaris58/joox_dl"></a>
    <a href="https://github.com/jaris58/joox_dl/blob/master/LICENSE"><img alt="GitHub license" src="https://img.shields.io/github/license/jaris58/joox_dl"></a>
    <br>
    <a href="https://fajar-isnandio.com">
        <img src="https://fajar-isnandio.com/wp-content/uploads/2015/02/fajar-isnandio-com.png" alt="Fajar Isnandio">
    </a>
</p>

----

## Installation
### Python 3
```install
pip install -r requirements.txt
```
### Windows (CMD)
> Download last application in [here](https://github.com/jaris58/joox_dl/releases/latest)
### File Config
> joox_dl.cfg
> ```config
> [app]
> music_folder=music/
> 
> [login]
> authtype=2
> email=[your-email]
> password=[your-password]
> wxopenid=[your-wxopenid]
> access_token=[your-access_token]
> ```
## Usage
### Python 3
```usage python
usage: joox_dl.py [-h] [-u URL] [-m] [-hq] [-f]
```
### Windows (CMD)
```usage windows
usage: joox_dl.exe [-h] [-u URL] [-m] [-hq] [-f]
```
### Example
```example
python joox_dl.py -m -u https://www.joox.com/id/playlist/db1J7YbWZ1LectFJqPzd5g==
python joox_dl.py -m -u https://www.joox.com/id/album/fnIkeDK++hFXaAzg7s9Etg==
python joox_dl.py -m -u https://www.joox.com/id/single/TtEH_iaoAGl1dh5KsV44pg==
python joox_dl.py -m -u https://www.joox.com/id/artist/oPx7SaQaTLhpqJP1zpTSpQ==
python joox_dl.py -m -u https://www.joox.com/id/chart/36
```

## Optional Arguments
```optar
  -h, --help          show this help message and exit
  -u URL, --url URL   Url String
  -m, --m4a           M4A file type
  -hq, --highquality  High quality
  -f, --force         Force to re-download

```

## Change log
> ## [2.2.0] - 2021-04-07
>  
> ### Added
> 
> - add force option to force re-download file
> - add folder path while loading / download file
>  
> ### Fixed 
> 
> - fix song with same name but diferent file
> - fix re-download file if broken / un-complete file
> - fix artist name if more than one
> - fix generate config file if not exist
> - fix configparser.NoOptionError

[Full Change Log](https://github.com/jaris58/joox_dl/blob/master/CHANGELOG.md)
## License
[MIT](https://en.wikipedia.org/wiki/MIT_License)