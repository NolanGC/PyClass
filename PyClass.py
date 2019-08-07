from __future__ import print_function
import pickle
import os.path
import datetime
import smtplib, ssl
import time
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

out = ""
dt = datetime.datetime.today()


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
    out += ("Daily summary for " + str(dt.month) + "/" + str(dt.day) + "/" + str(dt.year) + ":\n\n")
    for c in classes:
        out += (c['name'] + "\n")
        course_work = []
        response = service.courses().courseWork().list(courseId=c['id'], pageSize=100).execute()
        course_work.extend(response.get('courseWork', []))
        for work in course_work:
            try:
                if(dt.year == work['dueDate']['year'] and dt.month == work['dueDate']['month'] 
                    and dt.day == work['dueDate']['day'] - 1):
                    #Assignment is due today
                    dueIn = int(time.strftime('%H')) - work['dueTime']['hours']

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
    pass

def send_email(message):
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.ehlo()
    server.login(email, password)

    server.sendmail(email, email, str(message))
    server.quit() 
    #TODO FANCY EMAIL https://realpython.com/python-send-email/
def main():
    service = establish_creds()
    msg = due_assignments(service, out)
    if(show_overdue):
        overdue_assignments()
    send_email(msg)


if __name__ == '__main__':
    main()