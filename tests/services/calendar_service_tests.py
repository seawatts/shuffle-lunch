from tests.mock_data.mock_data import MockData
from shuffle.services.calendar_service import CalendarService


def test_get_all_accepted_users():
    calendar_service = CalendarService(MockData.GOOGLE_API_SERVICE)
    accepted_attendees = calendar_service.get_all_accepted_attendees("k3v5q8ion1adkil0fjl4nidtt4", "all@simplymeasured.com")
    assert len(accepted_attendees) is not 0