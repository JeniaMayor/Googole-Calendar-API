import json
import os
import pickle
from datetime import datetime
from typing import List

from google.auth.transport.requests import Request
from google.oauth2 import service_account
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from jsonschema import validate

dir_path = os.path.dirname(os.path.abspath(__file__))


class GoogleCalendar:
    __CONFIG_SCHEMA: dict = {
        "type": "object",
        "properties": {
            "SCOPES": {
                "type": "array",
                "items": {
                    "type": "string"
                }
            },
            "SERVICE_NAME": {
                "type": "string"
            },
            "VERSION": {
                "type": "string"
            },
            "TIME_ZONE": {
                "type": "string"
            },
            "DEFAULT_LOCATION": {
                "type": "string"
            },
        }
    }
    __SCOPES: list
    __SERVICE_NAME: str
    __VERSION: str
    __TIME_ZONE: str
    __LOCATION: str

    __credentials: any
    __service: any
    __calendar_id: str

    def __init__(self, calendar_id: str, api_keys_path: str = None):
        try:
            with open(os.path.join(dir_path, 'configs', 'Calendar.json'), "r") as configs:
                target = json.load(configs)
                validate(target, self.__CONFIG_SCHEMA)
                self.__SCOPES = target["SCOPES"]
                self.__SERVICE_NAME = target["SERVICE_NAME"]
                self.__VERSION = target["VERSION"]
                self.__TIME_ZONE = target["TIME_ZONE"]
                self.__LOCATION = target["DEFAULT_LOCATION"]

                self.__calendar_id = calendar_id

            if api_keys_path:
                self.__credentials = self.__authenticate(api_keys_path)
            else:
                self.__credentials = self.__authenticate_OAuth()

            self.__service = self.__create_service()

        except Exception as err:
            print(f"Bug ;): {err}")

    def __authenticate(self, api_keys_path: str):
        try:
            return service_account.Credentials.from_service_account_file(
                api_keys_path, scopes=self.__SCOPES)

        except Exception as err:
            print(f'[X]: {err}')
            raise err

    def __authenticate_OAuth(self):
        token_path = os.path.join(dir_path, '..', 'secrets', 'token.pickle')
        credentials_path = os.path.join(dir_path, '..', 'secrets', 'token.pickle')

        creds = None

        if os.path.exists(token_path):
            with open(token_path, 'rb') as token:
                creds = pickle.load(token)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    credentials_path, self.__SCOPES)
                creds = flow.run_local_server(port=0)

            with open(token_path, 'wb') as token:
                pickle.dump(creds, token)

        return creds

    def __create_service(self):
        try:
            return build(
                serviceName=self.__SERVICE_NAME,
                version=self.__VERSION,
                credentials=self.__credentials
            )

        except Exception as err:
            print(f'{err}')

    def get_events_list(self, max_result: int = 5) -> []:
        events_result: [] = self.__service.events().list(
            calendarId=self.__calendar_id,
            maxResults=max_result,
            singleEvents=True,
            orderBy='startTime'
        ).execute()

        events = events_result.get('items', [])

        if not events:
            return []

        return events

    def create_event(self,
                     summery: str,
                     description: str,
                     start_time: datetime,
                     end_time: datetime,
                     invitations: [str] = None):

        if invitations is None:
            invitations = []

        event = {
            'summary': summery,
            'location': self.__LOCATION,
            'description': description,
            'start': {
                'dateTime': start_time.isoformat(),
                'timeZone': self.__TIME_ZONE,
            },
            'end': {
                'dateTime': end_time.isoformat(),
                'timeZone': self.__TIME_ZONE,
            },
            'attendees': list(map(lambda item: {"email": item}, invitations)),
            'reminders': {
                'useDefault': False,
                'overrides': [
                    {'method': 'email', 'minutes': 30},
                    {'method': 'popup', 'minutes': 30},
                ],
            }
        }

        try:
            self.__service.events().insert(
                calendarId=self.__calendar_id,
                body=event
            ).execute()

        except Exception as err:
            print(err)
