## Installation

If [`pip`](https://docs.python.org/3/library/ensurepip.html) or
[`venv`](https://docs.python.org/3/library/venv.html) are not installed,
install them first:

```
sudo apt install python3-pip
sudo apt install python3-venv
```

Create a new [virtual environment](https://docs.python.org/3/library/venv.html):

```
python3 -m venv .venv
source .venv/bin/activate
```

Install the dependencies:

```
python -m pip install -r requirements.txt
```

Create the database:

```
createdb martin		# Only necessary if martin doesn't exist yet
sudo -u martin psql
CREATE DATABASE frecuencialexicalsu WITH OWNER martin;
```

Set-up the initial state of the database:

```
python manage.py migrate
python manage.py createsuperuser
python manage.py seed --mode=refresh
```

## Starting the server

Activate the [virtual environment](https://docs.python.org/3/library/venv.html):

```
source .venv/bin/activate
```

Start a development web server on your local machine:

```
python manage.py runserver
```

## How to update the stimuli (videos)

1. Place the video files at folder `experiment/static/terms`
2. Update the CSV file at `stimuli/management/commands/seed.csv`
3. Activate the virtual environment: `source .venv/bin/activate`
4. Fill the database with the stimuli: `python manage.py seed --mode=refresh`