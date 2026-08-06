"""
PitMind ingestion - build a corpus from real public F1 results.

Source: Jolpica (the maintained Ergast successor, https://api.jolpi.ca), a free
public JSON API - no scraping. Each race becomes a grounded document the
assistant can retrieve over. Run on your machine (needs internet):

    python -m app.ingest --year 2024 --rounds 1 2 3

Writes data/corpus.json, which retrieval loads alongside the base knowledge docs.
"""
from __future__ import annotations
import argparse, json, pathlib

DATA_OUT = pathlib.Path(__file__).parent.parent.parent / "data" / "corpus.json"
JOLPICA = "https://api.jolpi.ca/ergast/f1"


def race_to_doc(race: dict) -> dict:
    """Ergast race JSON -> a grounded race-summary document. Pure function."""
    season, rnd = race["season"], race["round"]
    name = race["raceName"]
    results = race.get("Results", [])
    def drv(r): return f"{r['Driver']['givenName']} {r['Driver']['familyName']}"
    top = results[:3]
    podium = ", ".join(f"P{r['position']} {drv(r)} ({r['Constructor']['name']})" for r in top)
    winner = top[0] if top else None
    fl = next((r for r in results if r.get("FastestLap", {}).get("rank") == "1"), None)
    text = f"{season} {name} (round {rnd}). Podium: {podium}."
    if winner and winner.get("Time"):
        text += f" Winning time {winner['Time']['time']}."
    if fl:
        text += f" Fastest lap: {drv(fl)} ({fl['FastestLap']['Time']['time']})."
    return {"id": f"race-{season}-{rnd}", "title": f"{season} {name} result",
            "text": text, "tags": ["race-result", season]}


def fetch_jolpica(year: int, rnd: int) -> dict:
    import httpx
    r = httpx.get(f"{JOLPICA}/{year}/{rnd}/results.json", timeout=60)
    r.raise_for_status()
    races = r.json()["MRData"]["RaceTable"]["Races"]
    return races[0] if races else {}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--year", type=int, required=True)
    ap.add_argument("--rounds", type=int, nargs="+", required=True)
    args = ap.parse_args()
    docs = []
    for rnd in args.rounds:
        race = fetch_jolpica(args.year, rnd)
        if race:
            docs.append(race_to_doc(race))
            print(f"  + {race['season']} {race['raceName']}")
    DATA_OUT.parent.mkdir(parents=True, exist_ok=True)
    DATA_OUT.write_text(json.dumps(docs, indent=2))
    print(f"Wrote {len(docs)} real race documents -> {DATA_OUT}")


if __name__ == "__main__":
    main()
