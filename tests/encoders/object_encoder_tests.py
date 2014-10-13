from shuffle.encoders.object_encoder import ObjectEncoder
from tests.config.mock_data.mock_data import MockData


def test_encoding_list():
    groups = MockData.RANDOM_GROUPS
    encoded_groups = ObjectEncoder().encode(groups)
    assert len(encoded_groups) != 0
