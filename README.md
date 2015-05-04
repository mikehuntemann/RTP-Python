Youtube-Crawler
=========================
## setup
Run program in terminal:

```
$ cd working-dir/src
$ python YouTube.py
```
### information
The youtube.db is created in its working directory.
Database can be viewed with the SQLite Browser - [download here].
[download here]: http://sqlitebrowser.org "SQLite Browser Download"

### use
Global variable *keyword* is used to specify the topic on the Youtube platform. 

### missing functions
- Subtitle analysis:
  - At what timestamp does the keyword appear in the video?
  - Print out the link including the exact timestamp when the keyword was said.