from fastapi.testclient import TestClient

from routers import files
test = TestClient(files.router)

def test_get_files():
    response = test.get('/getFiles/')
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}