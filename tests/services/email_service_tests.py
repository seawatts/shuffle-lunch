from shuffle.models.email_model import EmailModel
from shuffle.models.shuffle_config_model import ShuffleModel
from shuffle.services.email_service import EmailService
from tests.config.mock_data.mock_data import MockData


def test_email_users():
    email_service = EmailService()
    email_model = EmailModel("my mock test", "shuffle-lunch@simplymeasured.com", "shuffle lunch", "test")
    shuffle = ShuffleModel(email_model, 5, "", "", "Shuffle Lunch Test", "")
    email_service.send_emails_to_groups_with_template(shuffle, MockData.RANDOM_GROUPS)
    # Write compiled email template to file so we can see the debug version
