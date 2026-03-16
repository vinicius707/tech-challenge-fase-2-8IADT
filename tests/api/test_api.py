import time
import os
import json
from fastapi.testclient import TestClient
from src.api import app
from src.ga import representation

client = TestClient(app.app)


def test_optimize_job_lifecycle(tmp_path):
    # submit job
    payload = {"instance": "data/instances/hospital_points.csv", "num_vehicles": 2, "population": 10, "generations": 5}
    r = client.post("/optimize", json=payload)
    assert r.status_code == 202
    body = r.json()
    job_id = body["job_id"]
    assert body["status"] == "queued"

    # wait for job to be created and run (engine runs in background thread)
    time.sleep(1)

    # check job exists
    r2 = client.get(f"/jobs/{job_id}")
    assert r2.status_code == 200
    status = r2.json().get("status")
    assert status in ("queued", "running", "finished", "failed")

    # poll until finished or timeout
    timeout = time.time() + 10
    while time.time() < timeout:
        r3 = client.get(f"/jobs/{job_id}")
        st = r3.json().get("status")
        if st == "finished":
            break
        if st == "failed":
            err = r3.json().get('error')
            assert False, "job failed: {}".format(err)
        time.sleep(0.5)

    # now get routes
    r4 = client.get(f"/routes/{job_id}")
    assert r4.status_code == 200
    body = r4.json()
    assert body["status"] in ("finished",)
    artifacts = body.get("artifacts", {})
    assert "history" in artifacts and "best" in artifacts

    # request instructions
    r5 = client.post(f"/instructions/{job_id}")
    assert r5.status_code == 200
    body5 = r5.json()
    assert "instruction" in body5

