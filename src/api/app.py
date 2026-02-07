from fastapi import FastAPI, BackgroundTasks, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, Any
import uuid
import os
import json
from concurrent.futures import ThreadPoolExecutor
from src.ga import engine, representation
from src.llm.adapter import LLMAdapter

app = FastAPI(title="Tech Challenge - Routes Optimization API")

JOBS_PATH = "experiments/jobs.json"
EXECUTOR = ThreadPoolExecutor(max_workers=2)

def load_jobs() -> Dict[str, Any]:
    if os.path.exists(JOBS_PATH):
        with open(JOBS_PATH, "r", encoding="utf-8") as fh:
            return json.load(fh)
    return {}

def save_jobs(jobs: Dict[str, Any]):
    os.makedirs(os.path.dirname(JOBS_PATH) or ".", exist_ok=True)
    with open(JOBS_PATH, "w", encoding="utf-8") as fh:
        json.dump(jobs, fh, indent=2)


class OptimizeRequest(BaseModel):
    instance: Optional[str] = "data/instances/hospital_points.csv"
    num_vehicles: Optional[int] = 3
    population: Optional[int] = 50
    generations: Optional[int] = 100
    mutation_rate: Optional[float] = 0.05
    elitism: Optional[int] = 1
    fitness_weights: Optional[Dict[str, float]] = None


def run_job(job_id: str, cfg: Dict[str, Any], out_dir: str):
    jobs = load_jobs()
    jobs[job_id]["status"] = "running"
    save_jobs(jobs)

    try:
        points = representation.parse_instance_csv(cfg.get("instance"))
        weights = cfg.get("fitness_weights") or {}
        res = engine.run_ga(points,
                            num_vehicles=cfg.get("num_vehicles", 3),
                            population_size=cfg.get("population", 30),
                            generations=cfg.get("generations", 10),
                            elitism=cfg.get("elitism", 1),
                            mutation_rate=cfg.get("mutation_rate", 0.05),
                            weights=weights,
                            out_dir=out_dir)
        jobs = load_jobs()
        jobs[job_id]["status"] = "finished"
        jobs[job_id]["artifacts"] = res
        save_jobs(jobs)
    except Exception as e:
        jobs = load_jobs()
        jobs[job_id]["status"] = "failed"
        jobs[job_id]["error"] = str(e)
        save_jobs(jobs)


@app.post("/optimize", status_code=202)
def optimize(req: OptimizeRequest, background_tasks: BackgroundTasks):
    job_id = str(uuid.uuid4())
    out_dir = f"experiments/jobs/{job_id}"
    jobs = load_jobs()
    jobs[job_id] = {"status": "queued", "request": req.dict(), "out_dir": out_dir}
    save_jobs(jobs)
    # schedule background run
    EXECUTOR.submit(run_job, job_id, req.dict(), out_dir)
    return {"job_id": job_id, "status": "queued"}


@app.get("/jobs/{job_id}")
def get_job(job_id: str):
    jobs = load_jobs()
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail="job not found")
    return jobs[job_id]


@app.get("/routes/{job_id}")
def get_routes(job_id: str):
    jobs = load_jobs()
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail="job not found")
    if jobs[job_id]["status"] != "finished":
        return {"status": jobs[job_id]["status"]}
    artifacts = jobs[job_id].get("artifacts", {})
    return {"status": "finished", "artifacts": artifacts}


@app.post("/instructions/{job_id}")
def generate_instructions(job_id: str):
    jobs = load_jobs()
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail="job not found")
    if jobs[job_id]["status"] != "finished":
        raise HTTPException(status_code=400, detail="job not finished")
    artifacts = jobs[job_id].get("artifacts", {})
    out_dir = artifacts.get("out_dir") or jobs[job_id].get("out_dir")
    geojson = os.path.join(out_dir, "routes.geojson")
    if not os.path.exists(geojson):
        raise HTTPException(status_code=404, detail="routes.geojson not found for job")
    # reconstruct routes and call LLMAdapter
    from src.viz import map as viz_map
    with open(geojson, "r", encoding="utf-8") as fh:
        gj = json.load(fh)
    points = representation.parse_instance_csv("data/instances/hospital_points.csv")
    lookup = representation.build_points_lookup(points)
    decoded = []
    for feat in gj.get("features", []):
        seq = feat.get("properties", {}).get("sequence", [])
        decoded.append([lookup[int(cid)] for cid in seq])

    adapter = LLMAdapter()
    route_summary = "\n".join([f"Vehicle {i}: {len(r)} stops" for i, r in enumerate(decoded)])
    instr = adapter.generate_instructions(route_summary)
    out_path = os.path.join(out_dir, "instruction.txt")
    with open(out_path, "w", encoding="utf-8") as fh:
        fh.write(instr)
    return {"status": "ok", "instruction": out_path}

