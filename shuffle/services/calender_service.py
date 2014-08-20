from datetime import datetime
from shuffle.models.user_model import UserModel


class CalenderService:
    def __init__(self, google_api_service):
        self.__google_calender_api = google_api_service.calender
        self.__google_admin_api = google_api_service.admin

    def get_all_accepted_attendees(self, recurring_event_id, calender_group_alias):
        all_accepted = []
        users = self.__google_admin_api.members().list(groupKey=calender_group_alias).execute()

        # TODO: Loop through all the emails in the 'all' alias and get each event to see if they have accepted
        for user in users["members"]:
            # event_id = self.__compose_event_id(recurring_event_id)
            user_email = user["email"]
            event_id = recurring_event_id + "_" + "20140828T190000Z"
            event = self.__google_calender_api.events().get(calendarId=user_email, eventId=event_id).execute()
            # If attendees is not present then the user has deleted the event from their calendar
            if "attendees" not in event:
                continue

            attendees = event['attendees']
            accepted = self.__get_accepted_attendee(user_email, attendees)
            if accepted is not None:
                all_accepted.append(UserModel(accepted["email"]))
                print accepted["email"]

        return all_accepted

    @staticmethod
    def __compose_event_id(recurring_event_id):
        current_date = datetime.utcnow().strftime("%Y%m%dT190000Z")
        return recurring_event_id + "_" + current_date

    @staticmethod
    def __get_accepted_attendee(users_email, attendees):
        # NOTE: This should actually only return one name
        for attendee in attendees:
            if attendee['email'] == users_email:
                response_status = attendee['responseStatus']
                if response_status == 'accepted':
                    return attendee


        return None