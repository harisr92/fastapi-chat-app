from starlette import status
from fastapi.testclient import TestClient

def test_create_session_with_valid_data(client: TestClient):
    request_data = {
        "session_user": "testuser"
    }
    response = client.post('/sessions/', json=request_data)
    response_data = response.json()
    assert response.status_code == status.HTTP_201_CREATED
    assert response_data.get('session_user') == request_data.get('session_user')
    assert 'id' in response_data
    assert 'created_at' in response_data


def test_create_session_with_invalid_name(client: TestClient):
    request_data = {
        "session_user": ""
    }
    response = client.post('/sessions/', json=request_data)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT


def test_read_existing_session(client: TestClient):
    # First, create a session to read later
    create_request_data = {
        "session_user": "testuser"
    }
    create_response = client.post('/sessions/', json=create_request_data)
    created_session = create_response.json()
    session_id = created_session.get('id')

    # Now, read the created session
    read_response = client.get(f'/sessions/{session_id}')
    read_session = read_response.json()
    assert read_response.status_code == status.HTTP_200_OK
    assert read_session == created_session


def test_read_nonexistent_session(client: TestClient):
    response = client.get('/sessions/9999')
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': 'Session not found.'}
