from shuffle.services.email_service import EmailService
from tests.mock_data.mock_data import MockData


def test_get_all_accepted_users():
    email_service = EmailService(MockData.GOOGLE_API_SERVICE)
    email_service.send_emails_to_groups(MockData.RANDOM_GROUPS, "cwatts@simplymeasured.com", "my mock test", "cool beans")