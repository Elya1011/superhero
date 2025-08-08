import pytest, json, os
from main import get_the_tallest_hero

@pytest.fixture
def mock_heros():
    tests_dir = os.path.dirname(os.path.abspath(__file__))
    data_for_test = os.path.join(tests_dir, 'data_for_test.json')
    with open(data_for_test) as f:
        return json.load(f)

@pytest.fixture
def mock_api(mocker, mock_heros):
    mock_get = mocker.patch('main.requests.get')
    mock_response = mocker.Mock()
    mock_response.json.return_value = mock_heros
    mock_get.return_value = mock_response
    return mock_get

def test_get_tallest_male_with_work(mock_api, mock_heros):
    result = get_the_tallest_hero('Male', True)
    assert result == 'Oleg'

def test_get_tallest_male_without_work(mock_api, mock_heros):
    result = get_the_tallest_hero('Male', False)
    assert result == 'Misha'

def test_get_tallest_female_with_work(mock_api, mock_heros):
    result = get_the_tallest_hero('Female', True)
    assert result == 'Miky'

def test_get_tallest_female_without_work(mock_api, mock_heros):
    result = get_the_tallest_hero('Female', False)
    assert result == 'Mona'

def test_get_tallest_no_gender_with_work(mock_api, mock_heros):
    result = get_the_tallest_hero('-', True)
    assert result == 'NoGender'

def test_get_tallest_no_gender_without_work(mock_api, mock_heros):
    result = get_the_tallest_hero('-', False)
    assert result == 'NoGenderNoWork2'

def test_with_incorrect_param_gender(mock_api, mock_heros):
    valid_genders = {'Male', 'Female', '-'}
    with pytest.raises(ValueError) as exc_info:
        get_the_tallest_hero('no gender', True)
    exc_msg = f"Invalid gender. Use: {', '.join(valid_genders)}"
    assert exc_msg == str(exc_info.value)

def test_with_incorrect_param_work(mock_api, mock_heros):
    with pytest.raises(TypeError) as exc_info:
        get_the_tallest_hero('-', 'mua')
    exc_msg = 'work must be a boolean value: True or False'
    assert exc_msg == str(exc_info.value)

def test_with_two_incorrect_param(mock_api, mock_heros):
    valid_genders = {'Male', 'Female', '-'}
    with pytest.raises(ValueError) as exc_info:
        get_the_tallest_hero('no gender', 0)
    exc_msg = f"Invalid gender. Use: {', '.join(valid_genders)}"
    assert exc_msg == str(exc_info.value)