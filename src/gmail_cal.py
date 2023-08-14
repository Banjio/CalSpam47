from __future__ import print_function

from pathlib import Path
import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
class GmailCalSender(object):

    SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
     
    def __init__(self, token_path: str = 'token.json', cred_path: str = 'credentials.json') -> None:
        self.token_path = Path(token_path)
        self.cred_path = Path(cred_path)
        self.creds = self.build_creds()

    
    def build_creds(self):
        """
        Checks if a token.json file exsits if not logs into your account and creates it. 
        Note that you need a credentials.json file, which is generated when you set up a project
        in the google cloud developer environment. How to setup https://developers.google.com/calendar/quickstart/python
        """
        creds = None
        if self.token_path.exists():
            creds = Credentials.from_authorized_user_file('token.json', GmailCalSender.SCOPES)
    # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.cred_path, GmailCalSender.SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open(self.token_path, 'w') as token:
                token.write(creds.to_json())
        return creds

    
    def list_events(self):
        try:
            service = build('calendar', 'v3', credentials=self.creds)

            # Call the Calendar API
            now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
            print('Getting the upcoming 10 events')
            events_result = service.events().list(calendarId='primary', timeMin=now,
                                                maxResults=10, singleEvents=True,
                                                orderBy='startTime').execute()
            events = events_result.get('items', [])

            if not events:
                print('No upcoming events found.')
                return

            # Prints the start and name of the next 10 events
            for event in events:
                start = event['start'].get('dateTime', event['start'].get('date'))
                print(start, event['summary'])

        except HttpError as error:
            print('An error occurred: %s' % error)

    def create_cal_event():
        pass



if __name__ == "__main__":
    gmaili = GmailCalSender()
    gmaili.list_events()
    print("Done")