"""JSON-based storage for locations, vehicles, and deliveries."""
import os
import json
import uuid
from typing import Dict, Any, List


def _load_json(path: str, default: Any = None) -> Any:
    if default is None:
        default = {}
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as fh:
            return json.load(fh)
    return default if not isinstance(default, list) else []


def _save_json(path: str, data: Any):
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=2)


LOCATIONS_PATH = "data/locations.json"
VEHICLES_PATH = "data/vehicles.json"
DELIVERIES_PATH = "data/deliveries.json"


# --- Locations ---
def load_locations() -> List[Dict[str, Any]]:
    return _load_json(LOCATIONS_PATH, [])


def save_locations(locations: List[Dict[str, Any]]):
    _save_json(LOCATIONS_PATH, locations)


def next_location_id(locations: List[Dict[str, Any]]) -> int:
    if not locations:
        return 1
    return max(int(loc.get("id", 0)) for loc in locations) + 1


# --- Vehicles ---
def load_vehicles() -> List[Dict[str, Any]]:
    return _load_json(VEHICLES_PATH, [])


def save_vehicles(vehicles: List[Dict[str, Any]]):
    _save_json(VEHICLES_PATH, vehicles)


# --- Deliveries ---
def load_deliveries() -> List[Dict[str, Any]]:
    return _load_json(DELIVERIES_PATH, [])


def save_deliveries(deliveries: List[Dict[str, Any]]):
    _save_json(DELIVERIES_PATH, deliveries)
