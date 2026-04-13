import csv
from typing import List, Dict, Tuple
from dataclasses import dataclass


@dataclass
class Song:
    """Represents a song and its attributes."""
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float


@dataclass
class UserProfile:
    """Represents a user's taste preferences."""
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool


def load_songs(csv_path: str) -> List[Dict]:
    """Load songs from a CSV file and return a list of dicts with numeric fields converted."""
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            row["id"] = int(row["id"])
            row["energy"] = float(row["energy"])
            row["tempo_bpm"] = float(row["tempo_bpm"])
            row["valence"] = float(row["valence"])
            row["danceability"] = float(row["danceability"])
            row["acousticness"] = float(row["acousticness"])
            songs.append(row)
    return songs


def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score a single song against user preferences and return (score, reasons)."""
    score = 0.0
    reasons = []

    # Genre match: +2.0 points (highest weight — genre is the clearest taste signal)
    if song["genre"] == user_prefs.get("genre", ""):
        score += 2.0
        reasons.append("genre match (+2.0)")

    # Mood match: +1.0 point
    if song["mood"] == user_prefs.get("mood", ""):
        score += 1.0
        reasons.append("mood match (+1.0)")

    # Energy similarity: up to +1.0 — reward closeness to target, not just high/low values
    target_energy = user_prefs.get("energy", 0.5)
    energy_sim = round(1.0 - abs(song["energy"] - target_energy), 2)
    score += energy_sim
    reasons.append(f"energy similarity ({energy_sim:.2f})")

    # Valence similarity: up to +0.5 — valence reflects positivity/"vibe"
    target_valence = user_prefs.get("valence", 0.5)
    valence_sim = round(0.5 * (1.0 - abs(song["valence"] - target_valence)), 2)
    score += valence_sim
    reasons.append(f"valence similarity ({valence_sim:.2f})")

    return round(score, 2), reasons


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Score every song, then return the top-k as (song, score, explanation) tuples sorted highest first.

    Uses sorted() (returns a new list) rather than list.sort() (in-place mutation)
    so the original catalog order is preserved for repeated calls.
    """
    scored = [(song, *score_song(user_prefs, song)) for song in songs]
    ranked = sorted(scored, key=lambda x: x[1], reverse=True)
    return [(song, score, ", ".join(reasons)) for song, score, reasons in ranked[:k]]


class Recommender:
    """OOP wrapper around the scoring logic; works with Song and UserProfile dataclasses."""

    def __init__(self, songs: List[Song]):
        self.songs = songs

    def _score(self, user: UserProfile, song: Song) -> Tuple[float, List[str]]:
        """Compute a numeric score and reasons list for one Song against a UserProfile."""
        score = 0.0
        reasons = []

        if song.genre == user.favorite_genre:
            score += 2.0
            reasons.append("genre match (+2.0)")

        if song.mood == user.favorite_mood:
            score += 1.0
            reasons.append("mood match (+1.0)")

        energy_sim = round(1.0 - abs(song.energy - user.target_energy), 2)
        score += energy_sim
        reasons.append(f"energy similarity ({energy_sim:.2f})")

        if user.likes_acoustic and song.acousticness > 0.6:
            score += 0.5
            reasons.append("acoustic preference (+0.5)")

        return round(score, 2), reasons

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Return the top-k Songs for the given UserProfile, sorted by descending score."""
        scored = [(song, self._score(user, song)[0]) for song in self.songs]
        ranked = sorted(scored, key=lambda x: x[1], reverse=True)
        return [song for song, _ in ranked[:k]]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Return a human-readable explanation of why this song was recommended."""
        _, reasons = self._score(user, song)
        return ", ".join(reasons) if reasons else "No specific match found"
