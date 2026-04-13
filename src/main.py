"""
Command line runner for the Music Recommender Simulation.

Run from the project root with:
    python -m src.main
"""

from src.recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")

    # Default "pop / happy / high-energy" taste profile
    user_prefs = {
        "genre": "pop",
        "mood": "happy",
        "energy": 0.8,
        "valence": 0.8,
    }

    print("\n--- User Profile ---")
    for key, val in user_prefs.items():
        print(f"  {key}: {val}")

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print("\n=== Top 5 Recommendations ===\n")
    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"#{rank}  {song['title']}  |  {song['artist']}")
        print(f"     Genre: {song['genre']}  |  Mood: {song['mood']}  |  Energy: {song['energy']}")
        print(f"     Score: {score:.2f}")
        print(f"     Why:   {explanation}")
        print()


if __name__ == "__main__":
    main()
