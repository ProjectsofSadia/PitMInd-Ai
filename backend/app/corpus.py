"""Sample motorsport knowledge/race-report corpus (stand-in for ingested public data).

Each doc: id, title, text, tags. The production system ingests public race
reports/regulations; retrieval + grounding logic is identical either way.
"""
DOCS = [
    {"id": "d1", "title": "Tyre degradation basics",
     "text": "Tyre degradation is the loss of grip and pace as a stint progresses, measured in milliseconds lost per lap. Softer compounds offer more initial grip but degrade faster than hard compounds."},
    {"id": "d2", "title": "Undercut strategy",
     "text": "An undercut is pitting earlier than a rival to use fresh-tyre pace and gain track position when they stop. It works best when tyre degradation is high and the pit-lane time loss is low."},
    {"id": "d3", "title": "Overcut strategy",
     "text": "An overcut is staying out longer than a rival while they struggle on old tyres or in traffic, then pitting into clear air. It favours low-degradation tracks and cooler conditions."},
    {"id": "d4", "title": "Stint analysis",
     "text": "A stint is a run of laps on one set of tyres between pit stops. Engineers analyse stint pace, the degradation slope, and consistency to plan pit windows and compound choice."},
    {"id": "d5", "title": "Lap-time consistency",
     "text": "Consistency is how repeatable a driver's lap times are, often the standard deviation of clean laps. High consistency helps tyre and fuel modelling and reduces strategy risk."},
    {"id": "d6", "title": "Sector analysis",
     "text": "A lap is split into three sectors. Comparing best sector times across drivers isolates where time is gained or lost. The sum of a driver's best sectors is their theoretical best lap."},
    {"id": "d7", "title": "Pit-stop time loss",
     "text": "Pit-stop time loss is the total time cost of pitting: pit-lane delta plus the stationary stop. It sets the break-even for undercut and overcut decisions."},
    {"id": "d8", "title": "Compound selection",
     "text": "Compound selection balances one-lap pace against degradation and stint length. Softs suit short stints and qualifying; hards suit long stints and high-degradation circuits."},
    {"id": "d9", "title": "Dirty air and following",
     "text": "Dirty air is the turbulent wake behind a car that reduces downforce for a following car, hurting cornering and increasing tyre and brake temperatures."},
    {"id": "d10", "title": "Fuel load effect",
     "text": "A heavier fuel load slows a car by roughly a few hundredths per lap per kilogram. Lap times naturally improve through a stint as fuel burns off, partly masking tyre degradation."},
    {"id": "d11", "title": "Safety car strategy",
     "text": "A safety car slows the field and shrinks the pit-stop time loss, creating a cheap pit opportunity. Teams often pit under a safety car to gain track position."},
    {"id": "d12", "title": "Track evolution",
     "text": "Track evolution is the grip increase as rubber is laid down over a session. It makes later laps faster and must be separated from tyre degradation in pace analysis."},
    {"id": "d13", "title": "Degradation vs fuel correction",
     "text": "To measure true tyre degradation, engineers fuel-correct lap times, removing the pace gained from burning fuel so the remaining trend reflects the tyres."},
    {"id": "d14", "title": "Pace benchmarking",
     "text": "Benchmarking compares a driver's best and median pace against the field to show competitive position and the gap to the fastest car in milliseconds."},
    {"id": "d15", "title": "Two-stop vs one-stop",
     "text": "A two-stop trades extra pit-stop time loss for fresher, faster tyres. It beats a one-stop when total time saved on fresher tyres exceeds the added pit loss."},
]


def load_corpus():
    """Base knowledge docs + any real ingested race docs (data/corpus.json)."""
    import json, pathlib
    docs = list(DOCS)
    extra = pathlib.Path(__file__).parent.parent.parent / "data" / "corpus.json"
    if extra.exists():
        try:
            docs += json.loads(extra.read_text())
        except Exception:
            pass
    return docs
