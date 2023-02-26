import json

def load_current_plan(SAVE_LOCATION) -> dict:
    """Loads dict of current json object"""
    with open(SAVE_LOCATION, 'r') as f:
        return json.load(f)