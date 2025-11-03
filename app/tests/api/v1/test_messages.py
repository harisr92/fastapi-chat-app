from starlette import status
from fastapi.testclient import TestClient
import pytest

@pytest.fixture
def create_session(client: TestClient):
    request_data = {
        "session_user": "testuser"
    }
    return client.post('/sessions/', json=request_data).json()


def test_add_message_with_valid_data(client: TestClient, create_session):
    request_data = {
        "content": "Hello, this is a test message.",
        "role": "user"
    }
    response = client.post(f'/sessions/{create_session.get('id')}/messages/', json=request_data)
    response_data = response.json()
    assert response.status_code == status.HTTP_201_CREATED
    assert response_data.get('content') == request_data.get('content')
    assert response_data.get('role') == request_data.get('role')
    assert 'timestamp' in response_data


def test_add_message_to_nonexistent_session(client: TestClient):
    request_data = {
        "content": "This message should fail.",
        "role": "user"
    }
    response = client.post('/sessions/9999/messages/', json=request_data)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': 'Session not found.'}


def test_add_message_with_invalid_role(client: TestClient, create_session):
    request_data = {
        "content": "This message has an invalid role.",
        "role": "invalid_role"
    }
    response = client.post(f'/sessions/{create_session.get('id')}/messages/', json=request_data)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT


def test_add_message_with_empty_content(client: TestClient, create_session):
    request_data = {
        "content": "",
        "role": "user"
    }
    response = client.post(f'/sessions/{create_session.get('id')}/messages/', json=request_data)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT


def test_read_messages_from_existing_session(client: TestClient, create_session):
    # First, add a message to the session
    message_data = {
        "content": "Hello, this is a test message.",
        "role": "user"
    }
    client.post(f'/sessions/{create_session.get('id')}/messages/', json=message_data)

    # Now, read messages from the session
    response = client.get(f'/sessions/{create_session.get('id')}/messages/')
    response_data = response.json()
    assert response.status_code == status.HTTP_200_OK
    assert len(response_data) == 1
    assert response_data[0].get('content') == message_data.get('content')
    assert response_data[0].get('role') == message_data.get('role')


def test_read_messages_from_nonexistent_session(client: TestClient):
    response = client.get('/sessions/9999/messages/')
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': 'Session not found.'}
