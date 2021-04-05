
# Change Log
All notable changes to this project will be documented in this file.
 
The format is based on [Keep a Changelog](http://keepachangelog.com/)
and this project adheres to [Semantic Versioning](http://semver.org/).

## [2.1.1] - 2021-04-05
 
### Changed

- changed login.wxopenid to login.email in config
 
### Fixed 

- fixed [#3](https://github.com/jaris58/joox_dl/issues/3#issue-849974043) error Invalid cookie

## [2.1.0] - 2021-04-01
 
### Added

- added app.music_folder config
 
### Fixed 

- fixed error generate wpl
- fixed error mutagen.MutagenError: [Errno 13] Permission denied
- fixed error KeyError: 'genre'

## [2.0.0] - 2021-03-30
 
### Added

- added support chart link
- added support m4a high quality
- added track number tag
- added generate .wpl base on album, playlist, artist and chart
   
### Changed

- change parameter to [-h] [-u URL] [-m4a] [-hq]
- change link artist
- change comment tag with link single
- change clean_text function replace 'â' to 'a', '.' to ''
- change time session to 60 sec backward

 
### Fixed 

- fixed url_additional_data_track link