import json
import os


def JDataRead():
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    json_url = os.path.join(SITE_ROOT, "data", "risk_analysis.json")
    data = json.load(open(json_url))
    return data