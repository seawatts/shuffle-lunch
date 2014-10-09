class EmailModel:
    def __init__(self, subject, from_email, from_name, template):
        self.template = template
        self.subject = subject
        self.from_name = from_name
        self.from_email = from_email

    @staticmethod
    def from_json(email_json):
        return EmailModel(email_json["subject"], email_json["fromEmail"], email_json["fromName"], email_json["template"])

