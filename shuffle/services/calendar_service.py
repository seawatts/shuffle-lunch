from datetime import datetime
import logging

from apiclient.http import HttpError

from shuffle.models.user_model import UserModel


class CalendarService:
    def __init__(self, google_api_service):
        self.__google_calendar_api = google_api_service.calendar
        self.__google_admin_api = google_api_service.admin

    def get_today_event_id(self, recurring_event_id):
        logging.debug("Getting today's event id {0}".format(recurring_event_id))
        try:
            while True:
                page_token = None
                events = self.__google_calendar_api.events().instances(calendarId='primary', eventId=recurring_event_id, pageToken=page_token).execute()
                # event = self.__google_calendar_api.events().get(calendarId='lisa@simplymeasured.com', eventId=recurring_event_id).execute()
                today_date = datetime.today().date()
                for event in events['items']:
                    start_date = event['start']["dateTime"]
                    stripped_start_date = start_date[:10]
                    event_date = datetime.strptime(stripped_start_date, "%Y-%m-%d").date()
                    if event_date > today_date:
                        return None
                    elif event_date == today_date:
                        logging.debug("Found event id {0} for today {1}".format(str(event["id"]),  str(event_date)))
                        return event["id"]
                    page_token = events.get('nextPageToken')
                if not page_token:
                    break
        except HttpError as error:
            logging.debug("HTTP error getting calendar event: {0}".format(error))
            return None
        return None

    def get_all_accepted_attendees(self, recurring_event_id, calendar_group_alias):
        logging.info("Getting all accepted users from event")
        all_accepted = []
        try:
            users = self.__google_admin_api.members().list(groupKey=calendar_group_alias).execute()
        except HttpError as error:
            logging.error("An error occurred when trying to get members from alias. This is unrecoverable, please check the alias and try again. {0}".format(error))
            raise error

        logging.debug("Found {0} in {1} email alias".format(str(len(users["members"])), calendar_group_alias))
        for user in users["members"]:
            user_email = user["email"]
            try:
                event = self.__google_calendar_api.events().get(calendarId=user_email, eventId=recurring_event_id).execute()
            except HttpError as error:
                logging.error("An error occurred when trying the event from the specified calendar. {0}".format(error))
                raise error

            # If attendees is not present then the user has deleted the event from their calendar
            if "attendees" not in event:
                continue

            attendees = event['attendees']
            accepted = self.__get_accepted_attendee(user_email, attendees)
            if accepted is not None:
                user_model = UserModel(accepted["email"])
                all_accepted.append(user_model)
                logging.debug("{0} accepted event".format(user_model.get_email()))

        logging.info("{0} users accepted the event".format(str(len(all_accepted))))
        return all_accepted

    @staticmethod
    def __get_accepted_attendee(users_email, attendees):
        # NOTE: This should actually only return one name
        for attendee in attendees:
            if attendee['email'] == users_email:
                response_status = attendee['responseStatus']
                if response_status == 'accepted':
                    return attendee

        return None
