from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from datetime import datetime, timedelta
from os.path import join, dirname, abspath

SCOPES = [
    'https://www.googleapis.com/auth/calendar', # Full control of calendars
    'https://www.googleapis.com/auth/gmail.modify' # Read, send, delete, and manage email, and manage drafts
]

OAUTH_PORT = 4567

class GoogleCalendar:
    """
    Functions for interacting with the Google Calendar API.
    """
    
    def __get_credentials(self):
        """
        Function to retrieve credentials for accessing a service.
        No parameters.
        Returns the credentials object.
        """
        
        creds = None
        
        flow = InstalledAppFlow.from_client_secrets_file(
        join(dirname(dirname(dirname(abspath(__file__)))), 'credentials.json'), 
        SCOPES
        )
        
        flow.authorization_url(prompt='consent', approval_prompt='force', access_type='offline')
        creds = flow.run_local_server(port=OAUTH_PORT)
        
        return creds
    
    def get_calendar_events(
        self,
        starting_from=datetime.utcnow().isoformat() + 'Z', 
        until=(datetime.utcnow() + timedelta(weeks=2)).isoformat() + 'Z',
        calendar_id='primary',
        order_by='startTime',
        single_events=True,
        max_results=2500):
        """
        Get calendar events within a specific time range for a given calendar ID.
        
        Args:
            starting_from (str): The start time for fetching events in ISO format.
            until (str): The end time for fetching events in ISO format.
            calendar_id (str): The ID of the calendar to fetch events from.
            order_by (str): The order in which to return events.
            single_events (bool): Whether to expand recurring events into single instances.
            max_results (int): The maximum number of events to return.

        Returns:
            list: A list of formatted event strings.
        """
    
        creds = self.__get_credentials()

        service = build('calendar', 'v3', credentials=creds)

        if calendar_id != 'primary':
            # List all calendars
            calendar_list = service.calendarList().list().execute().get('items', [])
    
            found_calendar_id = None
            for calendar in calendar_list:
                if calendar['id'] == calendar_id:
                    found_calendar_id = calendar['id']
                    break

            if found_calendar_id is None:
                print(f'Calendar with ID {calendar_id} not found.')
                return
            else:
                # Update calendar_id with the found_calendar_id
                calendar_id = found_calendar_id

        # Call the Calendar API with the specific calendar ID and time range
        events_result = service.events().list(
            calendarId=calendar_id,
            timeMin=starting_from,
            timeMax=until,
            maxResults=max_results,
            singleEvents=single_events,
            orderBy=order_by
        ).execute()

        events = events_result.get('items', [])
        if not events:
            print(f'No upcoming events found for calendar with ID {calendar_id}.')
            return []

        formatted_events = map(
            lambda event: None if 'date' in event['start'] else (
                event_name := event['summary'],
                event_date := datetime.fromisoformat(event['start']['dateTime']).strftime('%Y-%m-%d'),
                event_start_time := datetime.fromisoformat(event['start']['dateTime']).strftime('%H:%M:%S'),
                event_end_time := datetime.fromisoformat(event['end']['dateTime']).strftime('%H:%M:%S'),
                event_location := 'In-Person' if ('location' in event and not event['location'].lower().startswith('http')) else 'Remote',
                f"{event_name} - {event_date}: {event_start_time} - {event_end_time} - {event_location}"
            )[-1],
            events  
        )

        formatted_events = [event for event in formatted_events if event is not None]

        return formatted_events

    @staticmethod
    def functions():
        return [
            {
                "type": "function",
                "function": {
                    "name": "get_calendar_events",
                    "description": "Get upcoming events in my Google Calendar",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "starting_from": {
                                "type": "string",
                                "format": "date-time",
                                "description": "The start date and time for the events query in ISO 8601 format."
                            },
                            "until": {
                                "type": "string",
                                "format": "date-time",
                                "description": "The end date and time for the events query in ISO 8601 format."
                            },
                            "calendar_id": {
                                "type": "string",
                                "description": "The calendar ID from which to retrieve events."
                            },
                            "order_by": {
                                "type": "string",
                                "enum": ["startTime", "updated"],
                                "description": "The order of the events returned in the result, either by start time or last updated time."
                            },
                            "single_events": {
                                "type": "boolean",
                                "description": "Whether to expand recurring events into instances and only return single one-off events and instances of recurring events."
                            },
                            "max_results": {
                                "type": "integer",
                                "minimum": 1,
                                "maximum": 2500,
                                "description": "Maximum number of events returned on one result page, with a maximum allowed value of 2500."
                            }
                        }
                    },
                },
            }
        ]   