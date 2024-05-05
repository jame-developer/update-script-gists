import os
from pytest_mock import MockerFixture

from update_install_golang_gist import extract_go_version, get_current_used_go_version, get_latest_go_version, update_gist


def test_get_latest_go_version(mocker: MockerFixture):
    response_mock = mocker.Mock()
    response_mock.status_code = 200
    response_mock.text = "go1.18.1"
    mocker.patch("requests.get", return_value=response_mock)

    assert get_latest_go_version() is True

def test_get_latest_go_version_failed(mocker: MockerFixture):
    response_mock = mocker.Mock()
    response_mock.status_code = 404
    response_mock.text = "Not Found"
    mocker.patch("requests.get", return_value=response_mock)

    assert get_latest_go_version() is False

def test_get_latest_go_version_failed_text(mocker: MockerFixture):
    response_mock = mocker.Mock()
    response_mock.status_code = 200
    response_mock.text = "Not Found"
    response_mock.return_value.split.side_effect = Exception("Failed to split")
    mocker.patch("requests.get", return_value=response_mock)

    assert get_latest_go_version() is False

def test_get_latest_go_version_invalid_version(mocker: MockerFixture):
    response_mock = mocker.Mock()
    response_mock.status_code = 200
    response_mock.text = "1.18.1"
    mocker.patch("requests.get", return_value=response_mock)

    assert get_latest_go_version() is False
    
def test_get_current_used_go_version_success(mocker: MockerFixture):
    mocker.patch.dict(os.environ, {"GITHUB_TOKEN": "dummy_token", "GIST_ID": "dummy_gist_id"})
    response_mock = mocker.Mock()
    response_mock.status_code = 200
    response_mock.json.return_value = {
        "files": {
            "install_golang.sh": {
                "content": "GO_VERSION=go1.17.2\n"
            }
        }
    }
    mocker.patch("requests.get", return_value=response_mock)

    assert get_current_used_go_version() is True

def test_get_current_used_go_version_failed(mocker: MockerFixture):
    mocker.patch.dict(os.environ, {"GITHUB_TOKEN": "dummy_token", "GIST_ID": "dummy_gist_id"})
    response_mock = mocker.Mock()
    response_mock.status_code = 404
    mocker.patch("requests.get", return_value=response_mock)

    assert get_current_used_go_version() is False
    
def test_extract_go_version(mocker):
    # Call the function with the mocked input
    result = extract_go_version('#!/bin/bash\nGO_VERSION=go1.16.3\nlinux/amd64')

    # Assert that the function returns the expected result
    assert result == 'go1.16.3'

def test_extract_go_version_no_version(mocker):
    # Call the function with the mocked input
    result = extract_go_version('#!/bin/bash\nlinux/amd64')

    # Assert that the function returns None
    assert result is None

def test_update_gist_success(mocker: MockerFixture):
    # Mock the necessary environment variables
    mocker.patch.dict(os.environ, {"GITHUB_TOKEN": "dummy_token", "GIST_ID": "dummy_gist_id"})

    # Mock the necessary requests responses
    response_get_mock = mocker.Mock()
    response_get_mock.status_code = 200
    response_get_mock.json.return_value = {
        "files": {
            "install_golang.sh": {
                "content": "#!/bin/bash\nGO_VERSION=go1.17.2\nlinux/amd64"
            }
        }
    }
    mocker.patch("requests.get", return_value=response_get_mock)

    response_patch_mock = mocker.Mock()
    response_patch_mock.status_code = 200
    mocker.patch("requests.patch", return_value=response_patch_mock)

    # Mock the file reading
    mocker.patch("builtins.open", mocker.mock_open(read_data="go1.17.2\n"))

    # Call the function
    result = update_gist()   

    # Assert the result
    assert result is True

def test_update_gist_patch_failure(mocker: MockerFixture):
    # Mock the necessary environment variables
    mocker.patch.dict(os.environ, {"GITHUB_TOKEN": "dummy_token", "GIST_ID": "dummy_gist_id"})

    # Mock the necessary requests responses
    response_get_mock = mocker.Mock()
    response_get_mock.status_code = 200
    response_get_mock.json.return_value = {
        "files": {
            "install_golang.sh": {
                "content": "#!/bin/bash\nGO_VERSION=go1.17.2\nlinux/amd64"
            }
        }
    }
    mocker.patch("requests.get", return_value=response_get_mock)

    response_patch_mock = mocker.Mock()
    response_patch_mock.status_code = 500  # Simulate a failure response
    mocker.patch("requests.patch", return_value=response_patch_mock)

    # Mock the file reading
    mocker.patch("builtins.open", mocker.mock_open(read_data="go1.17.2\n"))

    # Call the function
    result = update_gist()
    
    # Assert the result
    assert result is False

def test_update_gist_get_failure(mocker: MockerFixture):
    # Mock the necessary environment variables
    mocker.patch.dict(os.environ, {"GITHUB_TOKEN": "dummy_token", "GIST_ID": "dummy_gist_id"})

    # Mock the necessary requests responses
    response_get_mock = mocker.Mock()
    response_get_mock.status_code = 404  # Simulate a failure response
    mocker.patch("requests.get", return_value=response_get_mock)

    # Mock the file reading
    mocker.patch("builtins.open", mocker.mock_open(read_data="go1.17.2\n"))

    # Call the function
    result = update_gist()
    
    # Assert the result
    assert result is False