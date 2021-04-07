
# Change Log
All notable changes to this project will be documented in this file.
 
The format is based on [Keep a Changelog](http://keepachangelog.com/)
and this project adheres to [Semantic Versioning](http://semver.org/).

## [2.2.0] - 2021-04-07
 
### Added

- add force option to force re-download file
- add folder path while loading / download file
- login support with facebook
 
### Fixed 

- fix song with same name but diferent file
- fix re-download file if broken / un-complete file
- fix artist name if more than one
- fix generate config file if not exist
- fix configparser.NoOptionError

## [2.1.1] - 2021-04-05
 
### Added

- add login.email in config
 
### Fixed 

- fix [#3](https://github.com/jaris58/joox_dl/issues/3#issue-849974043) : Invalid cookie

### Removed

-  remove login.wxopenid in config

## [2.1.0] - 2021-04-01
 
### Added

- add app.music_folder config
 
### Fixed 

- fix error generate wpl
- fix error mutagen.MutagenError: [Errno 13] Permission denied
- fix error KeyError: 'genre'

## [2.0.0] - 2021-03-30
 
### Added

- add support chart link
- add support m4a high quality
- add track number tag
- add generate .wpl base on album, playlist, artist and chart
   
### Changed

- change parameter to [-h] [-u URL] [-m4a] [-hq]
- change link artist
- change comment tag with link single
- change clean_text function replace 'â' to 'a', '.' to ''
- change time session to 60 sec backward

 
### Fixed 

- fix url_additional_data_track link