#!/usr/bin/env python

"""PyClass.py: Daily homework reminder via email using Google Classroom's API and smtp."""

__author__  = "Nolan Clement"
__version__ = "1.0.0"
__email__   = "nolangclement@gmail.com"
__status__  = "Development"


from __future__ import print_function
import pickle
import os.path
import datetime
import smtplib, ssl
import time
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/classroom.courses.readonly', 'https://www.googleapis.com/auth/classroom.coursework.students']

# *CONFIG*
email = "600021071@fjuhsd.org" # Email that will recieve the summary
password = "nkRPL54z" # Summary will be sent from the recipients email
show_description = True # Description of due assignments is included in the summary 
show_overdue = True # Previously shown assignments are included in the summary

#Empty string to build message body
out = ""
dt = datetime.datetime.today()

#Creds are stored in token.pickle, delete this file to establish new creds
def establish_creds():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('classroom', 'v1', credentials=creds)
    return service


def due_assignments(service, out):
    classes = service.courses().list(pageSize=10).execute().get('courses', [])
    #Iterates over each class
    for c in classes:
        out += (c['name'] + "\n")
        course_work = []
        #Interface with classroom api
        response = service.courses().courseWork().list(courseId=c['id'], pageSize=100).execute()
        course_work.extend(response.get('courseWork', []))
        #Iterate over every assignment
        for work in course_work:
            try:
                #Check for assignments due today
                if(dt.year == work['dueDate']['year'] and dt.month == work['dueDate']['month'] 
                    and dt.day == work['dueDate']['day'] - 1):
                    #Assignment is due today
                    dueIn = int(time.strftime('%H')) - work['dueTime']['hours'] #TODO finish functionality 

                    if(show_description):
                        out += (work['title'] + " - " + work['description'] + " | due in " + str(dueIn) + " hours.\n")
                    else:
                        out += (work['title'] + " - " + " due in " + str(dueIn) + " hours.")
            except KeyError:
                pass
                #print("Assignment '" + work['title'] +  "' has no due date.")
    out += ("\n\n")
    return out



def overdue_assignments():
    #TODO ADD THIS FUNCTIONALITY
    pass

def send_email(text):
    msg = MIMEMultipart("alternative")
    msg["Subject"] = "PyClass Daily Summary"
    msg["From"] = email
    msg["To"] = email
    t = open("template.html", "r")
    template = t.read()
    h = ("Daily summary for " + str(dt.month) + "/" + str(dt.day) + "/" + str(dt.year) + ":\n\n")
    template = template.replace("[HEADER]", h)
    template = template.replace("[BODY]", text)
    final = MIMEText(template, "html")
    #Attach text body
    msg.attach(final)

    #Attach images
    #TODO refactor image names to be descriptive
    with open("images/thinking.png", "rb") as f:
        data = f.read()
    img = MIMEImage(data)
    f.close()
    img.add_header('Content-ID', '<image1>')
    msg.attach(img)

    with open("images/topgif.gif", "rb") as f:
        data2 = f.read()
    img2 = MIMEImage(data2)
    f.close()
    img2.add_header('Content-ID', '<image2>')
    msg.attach(img2)

    with open("images/bottom.png", "rb") as f:
        data3 = f.read()
    img3 = MIMEImage(data3)
    f.close()
    img3.add_header('Content-ID', '<image3>')
    msg.attach(img3)

    with open("images/top.png", "rb") as f:
        data4 = f.read()
    img4 = MIMEImage(data4)
    f.close()
    img4.add_header('Content-ID', '<image4>')
    msg.attach(img4)

    #Send email with smtp
    context = ssl.create_default_context()
    server = smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context)
    server.ehlo()
    server.login(email, password)
    server.sendmail(email, email, msg.as_string())
    server.quit() 

def main():
    service = establish_creds()
    msg = due_assignments(service, out)
    if(show_overdue):
        overdue_assignments()
    send_email(msg)


if __name__ == '__main__':
    main()