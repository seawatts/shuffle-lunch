from shuffle.models.email_model import EmailModel


class ShuffleModel:
    def __init__(self, email_model, group_size, calender_group_alias, recurring_event_id):
        self.recurring_event_id = recurring_event_id
        self.calender_group_alias = calender_group_alias
        self.group_size = group_size
        self.email_model = email_model

    @staticmethod
    def from_json(shuffle_json):
        email_model = EmailModel.from_json(shuffle_json["email"])
        return ShuffleModel(email_model, shuffle_json["groupSize"], shuffle_json["calenderGroupAlias"], shuffle_json["recurringEventId"])
