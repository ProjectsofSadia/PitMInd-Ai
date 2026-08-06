"""Verify Ergast race -> document mapping on mock data (no network)."""
from app.ingest import race_to_doc

MOCK = {
    "season": "2024", "round": "1", "raceName": "Bahrain Grand Prix",
    "Results": [
        {"position": "1", "Driver": {"givenName": "Max", "familyName": "Verstappen"},
         "Constructor": {"name": "Red Bull"}, "Time": {"time": "1:31:44.742"},
         "FastestLap": {"rank": "1", "Time": {"time": "1:32.608"}}},
        {"position": "2", "Driver": {"givenName": "Sergio", "familyName": "Perez"},
         "Constructor": {"name": "Red Bull"}},
        {"position": "3", "Driver": {"givenName": "Carlos", "familyName": "Sainz"},
         "Constructor": {"name": "Ferrari"}},
    ],
}

def test_race_to_doc_is_grounded():
    d = race_to_doc(MOCK)
    assert d["id"] == "race-2024-1"
    assert "Verstappen" in d["text"] and "Bahrain" in d["text"]
    assert "Fastest lap: Max Verstappen" in d["text"]
    assert "Winning time 1:31:44.742" in d["text"]
