import pytest
from fastapi.testclient import TestClient
from src.api.app import app
import json
import os
from src.api import storage

client = TestClient(app)

@pytest.fixture(autouse=True)
def mock_storage(tmp_path):
    """Override storage paths during tests to mock data cleanly."""
    old_locs = storage.LOCATIONS_PATH
    old_vehs = storage.VEHICLES_PATH
    old_dels = storage.DELIVERIES_PATH
    
    storage.LOCATIONS_PATH = str(tmp_path / "locations.json")
    storage.VEHICLES_PATH = str(tmp_path / "vehicles.json")
    storage.DELIVERIES_PATH = str(tmp_path / "deliveries.json")
    
    yield
    
    storage.LOCATIONS_PATH = old_locs
    storage.VEHICLES_PATH = old_vehs
    storage.DELIVERIES_PATH = old_dels


def test_location_crud():
    # Create
    resp = client.post("/locations", json={
        "address": "Hospital Base",
        "lat": -23.55,
        "lon": -46.63,
        "priority": "ALTA"
    })
    assert resp.status_code == 201
    loc_id = resp.json()["id"]

    # Read
    resp2 = client.get("/locations")
    assert resp2.status_code == 200
    assert len(resp2.json()["locations"]) == 1
    assert resp2.json()["locations"][0]["id"] == loc_id

    # Update
    resp3 = client.put(f"/locations/{loc_id}", json={
        "address": "Hospital Base Atualizado"
    })
    assert resp3.status_code == 200
    assert resp3.json()["address"] == "Hospital Base Atualizado"

    # Delete
    resp4 = client.delete(f"/locations/{loc_id}")
    assert resp4.status_code == 204

    resp5 = client.get("/locations")
    assert len(resp5.json()["locations"]) == 0


def test_vehicle_crud():
    # Create
    resp = client.post("/vehicles", json={
        "name": "Van Resfriada",
        "capacity_kg": 500,
        "autonomy_km": 400
    })
    assert resp.status_code == 201
    vid = resp.json()["id"]

    # Read
    resp2 = client.get("/vehicles")
    assert resp2.status_code == 200
    assert len(resp2.json()["vehicles"]) == 1

    # Delete
    resp3 = client.delete(f"/vehicles/{vid}")
    assert resp3.status_code == 204
