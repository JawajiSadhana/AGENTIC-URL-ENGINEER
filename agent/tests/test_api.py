from fastapi.testclient import TestClient
from app.main import app
client = TestClient(app)

def test_health():
 response = client.get('/health')
 assert response.status_code == 200
 assert response.json() == {'status': 'ok'}

def test_shorten_valid_url():
 response = client.post('/shorten', data={'url': 'https://google.com'})
 assert response.status_code == 200
 assert 'Success' in response.text
def test_shorten_invalid_url():
 response = client.post('/shorten', data={'url': 'ftp://hack.com'})
 assert response.status_code == 200
 assert 'SSRF Blocked' in response.text
def test_analytics_not_found():
 response = client.get('/api/v1/analytics/abcdef')
 assert response.json() == {'error': 'not found'}
