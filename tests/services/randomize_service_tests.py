from shuffle.services.randomize_service import RandomizeService
from tests.config.mock_data.mock_data import MockData


def test_get_random_groups():
    groups = RandomizeService.create_randomize_groups(MockData.ATTENDEES_ACCEPTED["attendees"], 3)
    assert len(groups) is not 0
    assert len(groups[0]) is 3
    groups2 = RandomizeService.create_randomize_groups(MockData.ATTENDEES_ACCEPTED["attendees"], 4)
    assert len(groups2) is not 0
    assert len(groups2[0]) is 4
    assert groups is not groups2
