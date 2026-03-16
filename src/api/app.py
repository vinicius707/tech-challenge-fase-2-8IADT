from datetime import datetime
from fastapi import FastAPI, BackgroundTasks, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
import uuid
import os
import json
import time
from concurrent.futures import ThreadPoolExecutor
from src.api.storage import (
    load_locations, save_locations, next_location_id,
    load_vehicles, save_vehicles,
    load_deliveries, save_deliveries,
)


def _model_to_dict(model, exclude_unset: bool = False) -> dict:
    """Compatível com Pydantic v1 (.dict) e v2 (.model_dump)."""
    if hasattr(model, "model_dump"):
        return model.model_dump(exclude_unset=exclude_unset)
    return model.dict(exclude_unset=exclude_unset)
from src.ga import engine, representation, fitness
from src.llm.adapter import LLMAdapter
from src.viz import map as viz_map
import csv

app = FastAPI(title="Tech Challenge - Routes Optimization API")

app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"], allow_methods=["*"], allow_headers=["*"])

JOBS_PATH = "experiments/jobs.json"
EXPERIMENTS_DIR = "experiments"


def _mount_static():
    if os.path.isdir(EXPERIMENTS_DIR):
        app.mount("/artifacts", StaticFiles(directory=EXPERIMENTS_DIR), name="artifacts")
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


# --- Pydantic models for CRUD ---
class LocationCreate(BaseModel):
    address: str
    lat: float
    lon: float
    priority: str  # ALTA, MÉDIA, BAIXA
    notes: Optional[str] = ""


class LocationUpdate(BaseModel):
    address: Optional[str] = None
    lat: Optional[float] = None
    lon: Optional[float] = None
    priority: Optional[str] = None
    notes: Optional[str] = None


class VehicleCreate(BaseModel):
    name: str
    capacity_kg: float
    autonomy_km: float
    active: Optional[bool] = True


class VehicleUpdate(BaseModel):
    name: Optional[str] = None
    capacity_kg: Optional[float] = None
    autonomy_km: Optional[float] = None
    active: Optional[bool] = None


class DeliveryCreate(BaseModel):
    location_id: int
    priority: str  # CRÍTICA, ALTA, MÉDIA, BAIXA
    volume_kg: Optional[float] = 0.0
    notes: Optional[str] = ""


# --- Locations CRUD ---
@app.get("/locations")
def list_locations():
    return {"locations": load_locations()}


@app.post("/locations", status_code=201)
def create_location(req: LocationCreate):
    locations = load_locations()
    loc = {
        "id": next_location_id(locations),
        "address": req.address,
        "lat": req.lat,
        "lon": req.lon,
        "priority": req.priority,
        "notes": req.notes or "",
        "created_at": time.time(),
    }
    locations.append(loc)
    save_locations(locations)
    return loc


@app.get("/locations/{loc_id}")
def get_location(loc_id: int):
    locations = load_locations()
    for loc in locations:
        if loc.get("id") == loc_id:
            return loc
    raise HTTPException(status_code=404, detail="location not found")


@app.put("/locations/{loc_id}")
def update_location(loc_id: int, req: LocationUpdate):
    locations = load_locations()
    for i, loc in enumerate(locations):
        if loc.get("id") == loc_id:
            upd = {k: v for k, v in _model_to_dict(req, exclude_unset=True).items() if v is not None}
            locations[i] = {**loc, **upd}
            save_locations(locations)
            return locations[i]
    raise HTTPException(status_code=404, detail="location not found")


@app.delete("/locations/{loc_id}", status_code=204)
def delete_location(loc_id: int):
    locations = [l for l in load_locations() if l.get("id") != loc_id]
    if len(locations) == len(load_locations()):
        raise HTTPException(status_code=404, detail="location not found")
    save_locations(locations)
    return None


# --- Vehicles CRUD ---
def _next_vehicle_id(vehicles):
    if not vehicles:
        return 1
    return max(int(v.get("id", 0)) for v in vehicles) + 1


@app.get("/vehicles")
def list_vehicles():
    return {"vehicles": load_vehicles()}


@app.post("/vehicles", status_code=201)
def create_vehicle(req: VehicleCreate):
    vehicles = load_vehicles()
    v = {
        "id": _next_vehicle_id(vehicles),
        "name": req.name,
        "capacity_kg": req.capacity_kg,
        "autonomy_km": req.autonomy_km,
        "active": req.active if req.active is not None else True,
    }
    vehicles.append(v)
    save_vehicles(vehicles)
    return v


@app.get("/vehicles/{v_id}")
def get_vehicle(v_id: int):
    for v in load_vehicles():
        if v.get("id") == v_id:
            return v
    raise HTTPException(status_code=404, detail="vehicle not found")


@app.put("/vehicles/{v_id}")
def update_vehicle(v_id: int, req: VehicleUpdate):
    vehicles = load_vehicles()
    for i, v in enumerate(vehicles):
        if v.get("id") == v_id:
            upd = {k: v for k, v in _model_to_dict(req, exclude_unset=True).items() if v is not None}
            vehicles[i] = {**v, **upd}
            save_vehicles(vehicles)
            return vehicles[i]
    raise HTTPException(status_code=404, detail="vehicle not found")


@app.delete("/vehicles/{v_id}", status_code=204)
def delete_vehicle(v_id: int):
    vehicles = [v for v in load_vehicles() if v.get("id") != v_id]
    if len(vehicles) == len(load_vehicles()):
        raise HTTPException(status_code=404, detail="vehicle not found")
    save_vehicles(vehicles)
    return None


# --- Deliveries CRUD ---
def _next_delivery_id(deliveries):
    if not deliveries:
        return 1
    return max(int(d.get("id", 0)) for d in deliveries) + 1


@app.get("/deliveries")
def list_deliveries():
    return {"deliveries": load_deliveries()}


@app.post("/deliveries", status_code=201)
def create_delivery(req: DeliveryCreate):
    deliveries = load_deliveries()
    loc_lookup = {l["id"]: l for l in load_locations()}
    if req.location_id not in loc_lookup:
        raise HTTPException(status_code=400, detail="location not found")
    d = {
        "id": _next_delivery_id(deliveries),
        "location_id": req.location_id,
        "priority": req.priority,
        "volume_kg": req.volume_kg or 0.0,
        "notes": req.notes or "",
        "created_at": time.time(),
        "status": "pendente",
    }
    deliveries.append(d)
    save_deliveries(deliveries)
    return d


class OptimizeRequest(BaseModel):
    instance: Optional[str] = "data/instances/hospital_points.csv"
    num_vehicles: Optional[int] = 3
    population: Optional[int] = 50
    generations: Optional[int] = 100
    mutation_rate: Optional[float] = 0.05
    elitism: Optional[int] = 1
    init_method: Optional[str] = "random"  # random, nearest_neighbor, clarke_wright
    fitness_weights: Optional[Dict[str, Any]] = None
    locations_ids: Optional[List[int]] = None
    delivery_ids: Optional[List[int]] = None
    vehicle_ids: Optional[List[int]] = None


def _build_points_from_config(cfg: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Build points list from delivery_ids+locations or locations_ids or instance CSV."""
    delivery_ids = cfg.get("delivery_ids")
    locations_ids = cfg.get("locations_ids")
    instance = cfg.get("instance", "data/instances/hospital_points.csv")

    if delivery_ids:
        deliveries = [d for d in load_deliveries() if d.get("id") in delivery_ids]
        loc_by_id = {l["id"]: l for l in load_locations()}
        points = []
        for d in deliveries:
            loc = loc_by_id.get(d["location_id"])
            if not loc:
                continue
            points.append({
                "id": d["id"],
                "lat": loc["lat"],
                "lon": loc["lon"],
                "priority": d.get("priority", "medium"),
                "volume": d.get("volume_kg", 0.0),
                "notes": d.get("notes", "") or loc.get("address", ""),
            })
        return points

    if locations_ids:
        locations = [l for l in load_locations() if l.get("id") in locations_ids]
        return [{
            "id": l["id"],
            "lat": l["lat"],
            "lon": l["lon"],
            "priority": l.get("priority", "medium"),
            "volume": 0.0,
            "notes": l.get("notes", "") or l.get("address", ""),
        } for l in locations]

    return representation.parse_instance_csv(instance)


def _build_weights_from_config(cfg: Dict[str, Any]) -> Dict[str, Any]:
    """Build fitness weights, including vehicle capacities and autonomies from vehicle_ids."""
    weights = dict(cfg.get("fitness_weights") or {})
    weights.setdefault("distance", 1.0)
    weights.setdefault("capacity_penalty", 1.0)
    weights.setdefault("priority_penalty", 1.0)
    weights.setdefault("autonomy_penalty", 1.0)

    vehicle_ids = cfg.get("vehicle_ids")
    if vehicle_ids:
        vehicles = [v for v in load_vehicles() if v.get("id") in vehicle_ids and v.get("active", True)]
        if vehicles:
            weights["vehicle_capacities"] = [v["capacity_kg"] for v in vehicles]
            weights["vehicle_autonomies"] = [v["autonomy_km"] for v in vehicles]
        cap = (cfg.get("fitness_weights") or {}).get("vehicle_capacity")
        if cap is not None and "vehicle_capacities" not in weights:
            weights["vehicle_capacity"] = cap
    elif "vehicle_capacity" not in weights:
        weights["vehicle_capacity"] = 100.0

    return weights


def run_job(job_id: str, cfg: Dict[str, Any], out_dir: str):
    jobs = load_jobs()
    jobs[job_id]["status"] = "running"
    save_jobs(jobs)

    try:
        points = _build_points_from_config(cfg)
        if not points:
            raise ValueError("No points to optimize")
        num_vehicles = cfg.get("num_vehicles", 3)
        vehicle_ids = cfg.get("vehicle_ids")
        if vehicle_ids:
            vehicles = [v for v in load_vehicles() if v.get("id") in vehicle_ids and v.get("active", True)]
            if vehicles:
                num_vehicles = len(vehicles)
        weights = _build_weights_from_config(cfg)
        generations = cfg.get("generations", 10)

        def on_progress(current: int, total: int):
            j = load_jobs()
            if job_id in j:
                j[job_id]["progress"] = {"current": current, "total": total}
                save_jobs(j)

        depot = None
        if points:
            lats = [p["lat"] for p in points]
            lons = [p["lon"] for p in points]
            depot = {"lat": sum(lats) / len(lats), "lon": sum(lons) / len(lons)}

        res = engine.run_ga(points,
                            num_vehicles=num_vehicles,
                            population_size=cfg.get("population", 30),
                            generations=generations,
                            elitism=cfg.get("elitism", 1),
                            mutation_rate=cfg.get("mutation_rate", 0.05),
                            weights=weights,
                            depot=depot,
                            init_method=cfg.get("init_method", "random"),
                            out_dir=out_dir,
                            on_progress=on_progress)
        # try to export geojson/html/results from best_solution
        best_csv = res.get("best")
        try:
            # load best_solution.csv
            routes = []
            if best_csv and os.path.exists(best_csv):
                with open(best_csv, newline='', encoding='utf-8') as fh:
                    reader = csv.DictReader(fh)
                    for row in reader:
                        seq = [int(x) for x in row['sequence'].split('|') if x]
                        routes.append(seq)
                points = _build_points_from_config(cfg)
                lookup = representation.build_points_lookup(points)
                decoded = representation.decode_chromosome(routes, lookup)
                depot = None
                if decoded:
                    lats = [p["lat"] for r in decoded for p in r]
                    lons = [p["lon"] for r in decoded for p in r]
                    if lats and lons:
                        depot = {"lat": sum(lats) / len(lats), "lon": sum(lons) / len(lons)}
                vehicle_reports = []
                for vid, route in enumerate(decoded):
                    load_kg = sum(p.get("volume", 0.0) for p in route)
                    stops = [{"id": p["id"], "endereco": p.get("notes", "") or f"Ponto {p['id']}"} for p in route]
                    distance_km = round(fitness.total_distance_for_route(route, depot=depot), 2)
                    vehicle_reports.append({
                        "vehicle_id": vid,
                        "load_kg": load_kg,
                        "stops": stops,
                        "distance_km": distance_km,
                    })
                res["vehicle_reports"] = vehicle_reports
                geojson_obj = viz_map.routes_to_geojson(decoded)
                geojson_path = os.path.join(out_dir, "routes.geojson")
                viz_map.save_geojson(geojson_obj, geojson_path)
                html_path = os.path.join(out_dir, "route_map.html")
                viz_map.generate_simple_html_map(decoded, html_path)
                # simple results.csv
                results_csv = os.path.join(out_dir, "results.csv")
                with open(results_csv, "w", newline="", encoding="utf-8") as rfh:
                    rfh.write("total_distance,total_load,vehicles\n0.0,0.0,{}".format(len(decoded)))
                res["routes_geojson"] = geojson_path
        except Exception:
            # non-fatal
            pass
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
    jobs[job_id] = {"status": "queued", "request": _model_to_dict(req), "out_dir": out_dir, "created_at": time.time()}
    save_jobs(jobs)
    # schedule background run
    EXECUTOR.submit(run_job, job_id, _model_to_dict(req), out_dir)
    return {"job_id": job_id, "status": "queued"}


@app.get("/jobs")
def list_jobs():
    jobs = load_jobs()
    return {"jobs": {k: {"status": v.get("status"), "job_id": k} for k, v in jobs.items()}}


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


class AskRequest(BaseModel):
    question: str


def _build_job_context_for_qa(job: Dict[str, Any]) -> str:
    """Build context string for Q&A from job artifacts and request."""
    ctx_parts = []
    req = job.get("request", {})
    ctx_parts.append(f"Configuração: num_vehicles={req.get('num_vehicles', 3)}, "
                     f"delivery_ids={req.get('delivery_ids')}, locations_ids={req.get('locations_ids')}")
    artifacts = job.get("artifacts", {})
    vr = artifacts.get("vehicle_reports") or []
    if not vr:
        vr = _reconstruct_vehicle_reports_from_job(job)
    total_dist = sum(r.get("distance_km", 0) for r in vr)
    total_load = sum(r.get("load_kg", 0) for r in vr)
    ctx_parts.append(f"Métricas: total_distance_km={round(total_dist, 2)}, total_load_kg={round(total_load, 2)}, "
                     f"vehicles_used={len(vr)}")
    for i, r in enumerate(vr):
        stops = r.get("stops", [])
        addrs = [s.get("endereco", f"Ponto {s.get('id')}") for s in stops]
        ctx_parts.append(f"Veículo {i + 1}: {r.get('distance_km', 0)} km, carga {r.get('load_kg', 0)} kg; paradas: {', '.join(addrs)}")
    return "\n".join(ctx_parts)


def _reconstruct_vehicle_reports_from_job(job: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Reconstruct vehicle_reports from best_solution.csv when artifacts lack them."""
    artifacts = job.get("artifacts", {})
    out_dir = artifacts.get("out_dir") or job.get("out_dir")
    if not out_dir or not os.path.isdir(out_dir):
        return []
    best_csv = os.path.join(out_dir, "best_solution.csv")
    if not os.path.exists(best_csv):
        return []
    try:
        points = _build_points_from_config(job.get("request", {}))
        lookup = representation.build_points_lookup(points)
        routes = []
        with open(best_csv, newline="", encoding="utf-8") as fh:
            reader = csv.DictReader(fh)
            for row in reader:
                seq = [int(x) for x in row.get("sequence", "").split("|") if x]
                routes.append(seq)
        decoded = representation.decode_chromosome(routes, lookup)
        depot = None
        if decoded:
            lats = [p["lat"] for r in decoded for p in r]
            lons = [p["lon"] for r in decoded for p in r]
            if lats and lons:
                depot = {"lat": sum(lats) / len(lats), "lon": sum(lons) / len(lons)}
        vehicle_reports = []
        for vid, route in enumerate(decoded):
            load_kg = sum(p.get("volume", 0.0) for p in route)
            stops = [{"id": p["id"], "endereco": p.get("notes", "") or f"Ponto {p['id']}"} for p in route]
            distance_km = round(fitness.total_distance_for_route(route, depot=depot), 2)
            vehicle_reports.append({"vehicle_id": vid, "load_kg": load_kg, "stops": stops, "distance_km": distance_km})
        return vehicle_reports
    except Exception:
        return []


@app.post("/jobs/{job_id}/ask")
def ask_about_job(job_id: str, body: AskRequest):
    """Answer natural language questions about the job's routes and deliveries."""
    jobs = load_jobs()
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail="job not found")
    job = jobs[job_id]
    if job.get("status") != "finished":
        raise HTTPException(status_code=400, detail="job not finished")
    context = _build_job_context_for_qa(job)
    adapter = LLMAdapter()
    answer = adapter.answer_question(body.question.strip(), context)
    return {"answer": answer}


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
    with open(geojson, "r", encoding="utf-8") as fh:
        gj = json.load(fh)
    cfg = jobs[job_id].get("request", {})
    points = _build_points_from_config(cfg)
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


@app.get("/reports/weekly")
def get_weekly_report(
    from_date: Optional[str] = Query(None, alias="from"),
    to_date: Optional[str] = Query(None, alias="to"),
):
    """Generate weekly logistics report with metrics and LLM summary."""
    jobs = load_jobs()
    now = time.time()
    week_sec = 7 * 24 * 3600
    from_ts = now - week_sec
    to_ts = now
    if from_date:
        try:
            from_ts = datetime.strptime(from_date, "%Y-%m-%d").timestamp()
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid 'from' date, use YYYY-MM-DD")
    if to_date:
        try:
            to_ts = datetime.strptime(to_date + " 23:59:59", "%Y-%m-%d %H:%M:%S").timestamp()
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid 'to' date, use YYYY-MM-DD")

    finished_jobs = []
    for jid, j in jobs.items():
        if j.get("status") != "finished":
            continue
        created = j.get("created_at") or 0
        if from_ts <= created <= to_ts:
            finished_jobs.append({"job_id": jid, "request": j.get("request", {}), "artifacts": j.get("artifacts", {})})

    total_jobs = len(finished_jobs)
    total_deliveries = 0
    total_distance_km = 0.0
    total_load_kg = 0.0
    total_vehicles_used = 0
    for j in finished_jobs:
        req = j.get("request") or {}
        dids = req.get("delivery_ids") or []
        lids = req.get("locations_ids") or []
        total_deliveries += len(dids) if dids else (len(lids) if lids else 0)
        reports = j.get("artifacts") or {}
        vr = reports.get("vehicle_reports") or []
        for r in vr:
            total_distance_km += r.get("distance_km", 0)
            total_load_kg += r.get("load_kg", 0)
        if vr:
            total_vehicles_used += len(vr)

    # tempo estimado (30 km/h média em ambiente urbano)
    estimated_hours = round(total_distance_km / 30.0, 2) if total_distance_km else 0

    metrics = {
        "period_from": datetime.fromtimestamp(from_ts).strftime("%Y-%m-%d"),
        "period_to": datetime.fromtimestamp(to_ts).strftime("%Y-%m-%d"),
        "total_jobs_finished": total_jobs,
        "total_deliveries_planned": total_deliveries,
        "total_distance_km": round(total_distance_km, 2),
        "total_load_kg": round(total_load_kg, 2),
        "total_vehicles_used": total_vehicles_used,
        "estimated_hours": estimated_hours,
        "job_ids": [j["job_id"] for j in finished_jobs],
    }
    metrics_text = "\n".join(f"{k}: {v}" for k, v in metrics.items())
    adapter = LLMAdapter()
    summary = adapter.generate_report_summary(metrics_text)
    return {"metrics": metrics, "summary": summary}


# mount static files after routes so /artifacts doesn't conflict
try:
    _mount_static()
except RuntimeError:
    pass

