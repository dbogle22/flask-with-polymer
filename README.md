# flask-with-polymer

I looked around for a while of a good example of how to set up a polymer app using flask. This is a simple example of how to set up a basic flask backend to serve polymer files. Once you clone this repo just navigate to the static folder and run 'bower install' to get everything that polymer needs. After that is done just set up flask by running export FLASK_APP=app.py. Then from the root directory which contains app.py fun flask run. Below is a list of commands you can run

```
$ cd static/
$ bower install
$ cd ..
$ export FLASK_APP=app.py
$ flask run
```

Then navigate in your browser to http://localhost:5000. 
