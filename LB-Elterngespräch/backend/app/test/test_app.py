import pytest
from app import app, db
from model.models import Termin, User
from flask import url_for

@pytest.fixture
def client():
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"  # Test-Datenbank
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            # Testbenutzer erstellen
            admin = User(username="admintest", password="rootroot", role="admin")
            teacher = User(username="teachertest", password="BesstesProjekt2025", role="teacher")
            parent = User(username="parenttest", password="BesstesProjekt2025", role="parent")
            db.session.add_all([admin, teacher, parent])
            db.session.commit()
        yield client
        with app.app_context():
            db.drop_all()

# Helper Funktionen
def login(client, username, password):
    return client.post("/login", data={"username": username, "password": password}, follow_redirects=True)

# 1. Routentests
def test_admin_dashboard_termine(client):
    # Admin-Login
    login(client, "admintest", "rootroot")
    response = client.get("/admin/dashboard/termine")
    assert response.status_code == 200
    assert b"Terminverwaltung" in response.data

def test_unauthorized_access_admin_termine(client):
    response = client.get("/admin/dashboard/termine", follow_redirects=True)
    assert response.status_code == 200
    assert b"Access denied!" in response.data

def test_parent_dashboard_termine(client):
    # Parent-Login
    login(client, "parenttest", "BesstesProjekt2025")
    response = client.get("/parent/dashboard")
    assert response.status_code == 200
    assert b"verfuegbare termine" in response.data

def test_parent_claim_termin(client):
    login(client, "admintest", "rootroot")
    # Termin erstellen
    termin = Termin(title="Test Termin", date="2025-01-01", time="10:00:00", teacher_id=1)
    db.session.add(termin)
    db.session.commit()

    # Parent claimt Termin
    login(client, "parenttest", "BesstesProjekt2025")
    response = client.post(f"/parent/claim_termin/{termin.id}", follow_redirects=True)
    assert response.status_code == 200
    assert b"Termin erfolgreich geclaimed" in response.data
    claimed_termin = Termin.query.get(termin.id)
    assert claimed_termin.parent_id == 3  # Parent ID von Timo.Schreiber

# 2. Datenbanktests
def test_create_termin(client):
    login(client, "admintest", "rootroot")
    response = client.post(
        "/admin/dashboard/create_termin",
        data={"title": "Test Termin", "date": "2025-01-01", "time": "10:00:00", "description": "Test Beschreibung", "teacher_id": 2},
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert Termin.query.filter_by(title="Test Termin").first() is not None

def test_edit_termin(client):
    login(client, "admintest", "rootroot")
    # Termin erstellen
    termin = Termin(title="Test Termin", date="2025-01-01", time="10:00:00", teacher_id=1)
    db.session.add(termin)
    db.session.commit()

    # Termin bearbeiten
    response = client.post(
        f"/admin/dashboard/edit_termin/{termin.id}",
        data={"title": "Updated Termin", "date": "2025-01-02", "time": "11:00:00", "description": "Updated Beschreibung"},
        follow_redirects=True,
    )
    assert response.status_code == 200
    updated_termin = Termin.query.get(termin.id)
    assert updated_termin.title == "Updated Termin"
    assert updated_termin.date.strftime("%Y-%m-%d") == "2025-01-02"
    assert updated_termin.time.strftime("%H:%M:%S") == "11:00:00"

def test_delete_termin(client):
    login(client, "admintest", "rootroot")
    # Termin erstellen
    termin = Termin(title="Test Termin", date="2025-01-01", time="10:00:00", teacher_id=1)
    db.session.add(termin)
    db.session.commit()

    # Termin löschen
    response = client.post(f"/admin/dashboard/delete_termin/{termin.id}", follow_redirects=True)
    assert response.status_code == 200
    assert Termin.query.get(termin.id) is None

# 3. Berechtigungstests
def test_teacher_access_admin_dashboard(client):
    login(client, "teachertest", "BesstesProjekt2025")
    response = client.get("/admin/dashboard", follow_redirects=True)
    assert response.status_code == 200
    assert b"Access denied!" in response.data

def test_admin_access_all_routes(client):
    login(client, "admintest", "rootroot")
    response = client.get("/admin/dashboard")
    assert response.status_code == 200
    assert b"Admin Dashboard" in response.data

# 4. End-to-End-Tests
def test_full_workflow(client):
    login(client, "admintest", "rootroot")
    # Admin erstellt Termin
    client.post(
        "/admin/dashboard/create_termin",
        data={"title": "Workflow Termin", "date": "2025-01-01", "time": "10:00:00", "description": "Workflow Beschreibung", "teacher_id": 2},
        follow_redirects=True,
    )
    termin = Termin.query.filter_by(title="Workflow Termin").first()
    assert termin is not None

    # Parent claimt Termin
    login(client, "parenttest", "BesstesProjekt2025")
    response = client.post(f"/parent/claim_termin/{termin.id}", follow_redirects=True)
    assert response.status_code == 200
    assert b"Termin erfolgreich geclaimed" in response.data
    assert termin.parent_id == 3  # Parent ID von Timo.Schreiber
