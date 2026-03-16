import pytest
from fastapi.testclient import TestClient
from src.api.app import app
import src.api.app as api_app
import json
import os

client = TestClient(app)

@pytest.fixture(autouse=True)
def mock_experiments_dir(tmp_path):
    old_jobs = api_app.JOBS_PATH
    old_dir = api_app.EXPERIMENTS_DIR
    api_app.JOBS_PATH = str(tmp_path / "jobs.json")
    api_app.EXPERIMENTS_DIR = str(tmp_path)
    
    yield
    
    api_app.JOBS_PATH = old_jobs
    api_app.EXPERIMENTS_DIR = old_dir

def test_optimize_endpoint_queues_job():
    payload = {
        "num_vehicles": 2,
        "population": 10,
        "generations": 5
    }
    # It attempts to use data/instances/hospital_points.csv by default
    resp = client.post("/optimize", json=payload)
    
    assert resp.status_code == 202
    data = resp.json()
    assert "job_id" in data
    assert data["status"] == "queued"
    
    job_id = data["job_id"]
    
    # Check if job was registered
    resp2 = client.get("/jobs")
    assert resp2.status_code == 200
    jobs = resp2.json().get("jobs", {})
    assert job_id in jobs
    assert jobs[job_id]["status"] in ("queued", "running")
