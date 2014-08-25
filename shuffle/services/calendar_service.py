from datetime import datetime
import logging
from shuffle.models.user_model import UserModel


class CalendarService:
    def __init__(self, google_api_service):
        self.__google_calendar_api = google_api_service.calendar
        self.__google_admin_api = google_api_service.admin

    def get_all_accepted_attendees(self, recurring_event_id, calendar_group_alias):
        # event_id = self.__compose_event_id(recurring_event_id)
        event_id = recurring_event_id + "_" + "20140814T190000Z"
        logging.info("Getting all accepted users from event: " + event_id)
        all_accepted = []
        users = self.__google_admin_api.members().list(groupKey=calendar_group_alias).execute()
        logging.debug("Found " + str(len(users["members"])) + " in " + calendar_group_alias + " email alias")
        for user in users["members"]:
            user_email = user["email"]
            event = self.__google_calendar_api.events().get(calendarId=user_email, eventId=event_id).execute()
            # If attendees is not present then the user has deleted the event from their calendar
            if "attendees" not in event:
                continue

            attendees = event['attendees']
            accepted = self.__get_accepted_attendee(user_email, attendees)
            if accepted is not None:
                user_model = UserModel(accepted["email"])
                all_accepted.append(user_model)
                logging.debug(user_model.get_email() + " accepted event")

        logging.info(str(len(all_accepted)) + " users accepted the event")
        return all_accepted

    @staticmethod
    def __compose_event_id(recurring_event_id):
        current_date = datetime.utcnow().strftime("%Y%m%dT190000Z")
        event_id = recurring_event_id + "_" + current_date
        logging.debug("Event id: " + event_id)
        return event_id

    @staticmethod
    def __get_accepted_attendee(users_email, attendees):
        # NOTE: This should actually only return one name
        for attendee in attendees:
            if attendee['email'] == users_email:
                response_status = attendee['responseStatus']
                if response_status == 'accepted':
                    return attendee


        return None