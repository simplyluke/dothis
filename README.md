#Do This

This is just a project I'm doing to better understand python and the Flask framework. It is *not* intended for public use, though you're more than welcome to try it out locally.

[Flask](http://flask.pocoo.org) is a python microframework.

## Running Do This

To get it running on your machine you need access to virtualenv and sqlite.


	$ git clone https://github.com/simplyluke/dothis.git  # Get the files
	$ cd dothis
	$ virtualenv venv # Set up your virtual environment
	$ . venv/bin/activate # Start the virtual environment
	$ pip install Flask # Get flask
	$ sqlite3 /tmp/dothis.db < schema.sql # Set up the database
	$ python dothis.py # Start Do This

Now simply navigate to 127.0.0.1:5000/ in your web browser and log in using 
<br />Username: Admin 
<br />Password: dev

The log in credentials can be changed to your liking by editing the configuration in dothis.py
