# PyClass

Daily homework reminder via email using Google Classroom's API and smtp.

### Prerequisites

[Python 3](https://www.python.org/downloads/)

## Setup

Open terminal and run this command 

> pip3 install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib --user

Run PyClass.py locally using any suitable python environment, this will start the authentication process and generate a token.pickle file. If you have completed the authentication flow correctly you should be greeted with:

> The authentication flow has completed, you may close this window.

We will now host PyClass remotely on pythonanywhere, eliminating the need to run the service 24/7 locally.

1. First, create an account with **[here](https://www.pythonanywhere.com/registration/register/beginner/)**.
2. Navigate to **Files** in the upper right hand corner.
3. Enter a new directory name and select **New directory**

Upload the following files:
	
1. PyClass.py
2. images (create a directory called "images" and upload each file)
3. template.html
4. credentials.json
5. token.pickle

Open PyClass.py

Modify the variables under *CONFIG*

Open a bash console (green button near the bottom of your screen)

Run the following command

> pip3 install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib --user

Make a virtual env in .virtualenvs/ --- *TODO EXPLAIN THIS* ---

Navigate to *Tasks*

Make a task with the following command template
> /home/USER/.virtualenvs/VIRTUALENVNAME/bin/python /home/USER/PROJECTNAME/PyClass.py

## Running a test

Set the task to a time just after the current time, wait for an email.


