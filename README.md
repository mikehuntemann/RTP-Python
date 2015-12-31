#Youtube-Crawler


## setup
install [homebrew](https://www.brew.sh) with:

```
ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
```

then install python, mongodb, ffmpeg & youtube-dl with brew:

```
brew install python
brew install mongodb
brew install ffmpeg
```

in addition we need two python libraries:  
- [Requests 2.8.1](https://pypi.python.org/pypi/requests) - Python HTTP for Humans.   
- [pymongo 3.2](https://pypi.python.org/pypi/pymongo) - Mongodb for Python

```
pip install pymongo
```

## config
open the settings.json file in your editor of choise.
change the _API_KEY_ (if you don't have one, check out [developer.google.com](developer.google.com) and register your project).
change _SEARCH_KEY_ and _DB_KEY_ for your topic.


## run programm
run mongod in your terminal

```
mongod
```

make a new terminal window:
go to the project folder in your terminal and start YoutubeSearch.py

```
cd /your/project/directory
python YoutubeSearch.py
```

## output
the created metadata / subtitle database can be viewed with [MongoHub](https://github.com/jeromelebel/MongoHub-Mac/)
