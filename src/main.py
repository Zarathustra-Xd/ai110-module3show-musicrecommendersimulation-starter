"""
Command line runner for the Music Recommender Simulation.

Run from the project root with:
    python src/main.py
"""

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


def print_profile(label: str, prefs: dict, recommendations: list) -> None:
    separator = "=" * 60
    print(f"\n{separator}")
    print(f"  {label}")
    print(separator)
    print("  Preferences:")
    for key, val in prefs.items():
        print(f"    {key}: {val}")
    print(f"\n  Top {len(recommendations)} Recommendations:\n")
    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"  #{rank}  {song['title']}  |  {song['artist']}")
        print(f"       Genre: {song['genre']}  |  Mood: {song['mood']}  |  Energy: {song['energy']}")
        print(f"       Score: {score:.2f}")
        print(f"       Why:   {explanation}")
        print()


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")

    for profile in PROFILES:
        recs = recommend_songs(profile["prefs"], songs, k=5)
        print_profile(profile["label"], profile["prefs"], recs)


if __name__ == "__main__":
    main()
