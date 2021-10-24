# WebApp.PY
Web Application with Flask. Source code and documents are from https://www.udemy.com/course/the-python-mega-course.

## Installation flask and virtualenv

Installation virtual environment:

```powershell
#pip3.9 install virtualenv
```

## Create virtual environment and need libraries for web app in Windows PowerShell

```powershell
> cd D:\Learning\Python\WebApp.PY
> python -m venv env
# OR
> virtualenv env
# Check 'env' directory are created
> dir
    Directory: D:\Learning\Python\WebApp.PY
Mode                 LastWriteTime         Length Name
----                 -------------         ------ ----
d-----        10/16/2021   9:12 PM                env
d-----        10/16/2021   9:11 PM                WebApp.PY
```

Activate the local environment and install libraries
```powershell
# Activate virtual env
> .\env\Scripts\activate.bat
# Install libraries
> pip install flask
> pip install psycopg2
> pip install Flask-SQLAlchemy
> pip install geopy
> pip install pandas
> pip install pandas_datareader
> pip install bokeh
> pip install gunicorn
# Launch welsite
> python HelloWorld.py
```

## Python hosting servers:

- https://www.heroku.com
- https://www.pythonanywhere.com

### Create Procfile
```
web: gunicorn HelloWorld:app
```

### Create runtime.txt
Check Heroku runtime support:
#https://devcenter.heroku.com/articles/python-runtimes#supported-python-runtimes
runtime.txt
```
python-3.9.7
```

### Create requirements.txt
```powershell
.\env\Scripts\pip freeze > requirement.txt 
```

## References:

- Jinja template in Flask: https://jinja.palletsprojects.com/en/2.9.x/templates/
