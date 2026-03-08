import pytest
from app import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


# ── HEALTH CHECK ──────────────────────────────────────────
def test_health_returns_200(client):
    r = client.get('/health')
    assert r.status_code == 200

def test_health_status_is_healthy(client):
    r = client.get('/health')
    assert r.get_json()['status'] == 'healthy'

def test_health_app_name(client):
    r = client.get('/health')
    assert r.get_json()['app'] == 'ACEest Fitness'


# ── PROGRAMS LIST ─────────────────────────────────────────
def test_programs_returns_200(client):
    r = client.get('/programs')
    assert r.status_code == 200

def test_programs_returns_list(client):
    r = client.get('/programs')
    assert 'programs' in r.get_json()

def test_programs_has_three_items(client):
    r = client.get('/programs')
    assert len(r.get_json()['programs']) == 3

def test_programs_contains_fat_loss(client):
    r = client.get('/programs')
    assert 'Fat Loss (FL)' in r.get_json()['programs']

def test_programs_contains_muscle_gain(client):
    r = client.get('/programs')
    assert 'Muscle Gain (MG)' in r.get_json()['programs']

def test_programs_contains_beginner(client):
    r = client.get('/programs')
    assert 'Beginner (BG)' in r.get_json()['programs']


# ── PROGRAM DETAIL ────────────────────────────────────────
def test_fat_loss_returns_200(client):
    r = client.get('/program/Fat Loss (FL)')
    assert r.status_code == 200

def test_fat_loss_has_workout(client):
    r = client.get('/program/Fat Loss (FL)')
    assert 'workout' in r.get_json()

def test_fat_loss_has_diet(client):
    r = client.get('/program/Fat Loss (FL)')
    assert 'diet' in r.get_json()

def test_fat_loss_has_calorie_factor(client):
    r = client.get('/program/Fat Loss (FL)')
    assert r.get_json()['calorie_factor'] == 22

def test_muscle_gain_returns_200(client):
    r = client.get('/program/Muscle Gain (MG)')
    assert r.status_code == 200

def test_muscle_gain_calorie_factor(client):
    r = client.get('/program/Muscle Gain (MG)')
    assert r.get_json()['calorie_factor'] == 35

def test_beginner_returns_200(client):
    r = client.get('/program/Beginner (BG)')
    assert r.status_code == 200

def test_invalid_program_returns_404(client):
    r = client.get('/program/InvalidProgram')
    assert r.status_code == 404

def test_invalid_program_returns_error_key(client):
    r = client.get('/program/InvalidProgram')
    assert 'error' in r.get_json()


# ── CALORIE CALCULATOR ────────────────────────────────────
def test_calories_fat_loss_70kg(client):
    r = client.post('/calories', json={'weight': 70, 'program': 'Fat Loss (FL)'})
    assert r.status_code == 200
    assert r.get_json()['calories'] == 1540   # 70 * 22

def test_calories_muscle_gain_80kg(client):
    r = client.post('/calories', json={'weight': 80, 'program': 'Muscle Gain (MG)'})
    assert r.status_code == 200
    assert r.get_json()['calories'] == 2800   # 80 * 35

def test_calories_beginner_60kg(client):
    r = client.post('/calories', json={'weight': 60, 'program': 'Beginner (BG)'})
    assert r.status_code == 200
    assert r.get_json()['calories'] == 1560   # 60 * 26

def test_calories_returns_weight_and_program(client):
    r = client.post('/calories', json={'weight': 70, 'program': 'Fat Loss (FL)'})
    data = r.get_json()
    assert data['weight'] == 70
    assert data['program'] == 'Fat Loss (FL)'

def test_calories_invalid_program_returns_400(client):
    r = client.post('/calories', json={'weight': 70, 'program': 'Invalid'})
    assert r.status_code == 400

def test_calories_zero_weight_returns_400(client):
    r = client.post('/calories', json={'weight': 0, 'program': 'Fat Loss (FL)'})
    assert r.status_code == 400

def test_calories_no_body_returns_400(client):
    r = client.post('/calories', content_type='application/json', data='')
    assert r.status_code == 400