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
## Usage
### Python 3
```usage python
usage: joox_dl.py [-h] [-u URL] [-m] [-hq]
```
### Windows (CMD)
```usage windows
usage: joox_dl.exe [-h] [-u URL] [-m] [-hq]
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
  -u URL, --url URL   url String
  -m, --m4a           m4a Type
  -hq, --highquality  high quality

```

## Change log
> ## [2.1.0] - 2021-04-01
>  
> ### Added
> 
> - added app.music_folder config
>  
> ### Fixed 
> 
> - fixing error generate wpl
> - fixing error mutagen.MutagenError: [Errno 13] Permission denied
> - fixing error KeyError: 'genre'

[Full Change Log](https://github.com/jaris58/joox_dl/blob/master/CHANGELOG.md)
## License
[MIT](https://en.wikipedia.org/wiki/MIT_License)