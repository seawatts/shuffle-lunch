from shuffle.services.google_api_service import GoogleApiService


def test_get_auth():
    google_api_service = GoogleApiService()
    assert google_api_service.admin is not None
    assert google_api_service.calendar is not None
