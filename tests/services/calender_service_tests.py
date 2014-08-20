from tests.mock_data.mock_data import MockData
from shuffle.services.calender_service import CalenderService


def test_get_all_accepted_users():
    calender_service = CalenderService(MockData.GOOGLE_API_SERVICE)
    accepted_attendees = calender_service.get_all_accepted_attendees("k3v5q8ion1adkil0fjl4nidtt4", "all@simplymeasured.com")
    # assert len(accepted_attendees) is len(MockData.ATTENDEES_ACCEPTED)