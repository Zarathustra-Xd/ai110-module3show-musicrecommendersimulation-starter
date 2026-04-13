"""
Command line runner for the Music Recommender Simulation.

Run from the project root with:
    python src/main.py
"""

from tabulate import tabulate
from recommender import load_songs, recommend_songs


PROFILES = [
    {
        "label": "Profile 1 — High-Energy Pop Fan",
        "prefs": {"genre": "pop", "mood": "happy", "energy": 0.9, "valence": 0.85},
    },
    {
        "label": "Profile 2 — Chill Lofi Listener",
        "prefs": {"genre": "lofi", "mood": "chill", "energy": 0.35, "valence": 0.6},
    },
    {
        "label": "Profile 3 — Deep Intense Rock",
        "prefs": {"genre": "rock", "mood": "intense", "energy": 0.95, "valence": 0.3},
    },
    {
        # Adversarial: user wants high energy but also melancholic blues — conflicting signals
        "label": "Profile 4 (Adversarial) — High-Energy Blues Melancholic",
        "prefs": {"genre": "blues", "mood": "melancholic", "energy": 0.9, "valence": 0.2},
    },
    {
        # Edge case: genre does not exist in the catalog at all
        "label": "Profile 5 (Edge Case) — Unknown Genre Jazz-Fusion",
        "prefs": {"genre": "jazz-fusion", "mood": "relaxed", "energy": 0.5, "valence": 0.65},
    },
]


def print_profile_table(label: str, prefs: dict, recommendations: list) -> None:
    """Print a profile's preferences and its top recommendations as a formatted ASCII table."""
    width = 90
    print("\n" + "=" * width)
    print(f"  {label}")
    print("=" * width)

    # Preferences summary as a compact inline row
    pref_headers = list(prefs.keys())
    pref_values = [str(v) for v in prefs.values()]
    print(tabulate([pref_values], headers=pref_headers, tablefmt="grid"))

    # Recommendations table — one row per song, reasons in the last column
    headers = ["#", "Title", "Artist", "Genre", "Mood", "Energy", "Score", "Reasons"]
    rows = []
    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        # Wrap reasons onto separate lines so the table stays readable
        reasons_wrapped = "\n".join(explanation.split(", "))
        rows.append([
            rank,
            song["title"],
            song["artist"],
            song["genre"],
            song["mood"],
            f"{song['energy']:.2f}",
            f"{score:.2f}",
            reasons_wrapped,
        ])

    print()
    print(tabulate(rows, headers=headers, tablefmt="grid"))
    print()


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")

    for profile in PROFILES:
        recs = recommend_songs(profile["prefs"], songs, k=5)
        print_profile_table(profile["label"], profile["prefs"], recs)


if __name__ == "__main__":
    main()
