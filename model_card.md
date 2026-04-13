# Model Card: Music Recommender Simulation

## 1. Model Name

**VibeFinder 1.0**

---

## 2. Intended Use

VibeFinder suggests 3–5 songs from a small catalog based on a user's preferred genre, mood, and energy level. It is designed for classroom exploration of how content-based filtering works — not for real-world deployment. It assumes the user can describe their current taste with a genre, a mood word, and a numeric energy target.

---

## 3. How the Model Works

VibeFinder reads through every song in its catalog and gives each one a score based on how well it matches what the user told us they like. A song earns the most points (2) if its genre matches the user's favorite genre, because genre is the strongest and most reliable taste signal. It earns a smaller bonus (1) if the mood matches too — mood is important but more subjective and overlapping (for example, "chill" and "relaxed" are almost the same).

For energy and positivity (valence), the model rewards *closeness*, not just highness or lowness. If the user wants medium-energy music, a very quiet song and a very loud song are penalized equally. The song with the energy closest to the target wins those points. After scoring every song, the model simply sorts them from highest to lowest and returns the top results, along with plain-language reasons for each pick.

---

## 4. Data

The catalog contains **18 songs** stored in `data/songs.csv`. The original 10 songs cover pop, lofi, rock, ambient, jazz, synthwave, and indie pop. Eight new songs were added to improve diversity:

| Added genre | Added mood |
|---|---|
| hip-hop | energetic |
| classical | peaceful |
| country | nostalgic |
| metal | aggressive |
| rnb | romantic |
| edm | euphoric |
| blues | melancholic |
| reggae | uplifting |

Each song has 10 attributes: id, title, artist, genre, mood, energy, tempo_bpm, valence, danceability, and acousticness. The catalog is still small and skews toward Western pop-adjacent genres — non-Western music genres (Afrobeats, K-pop, cumbia, etc.) are missing entirely.

---

## 5. Strengths

- Works well for users who have a clear genre preference, especially pop, lofi, or rock — the three most represented genres.
- The energy proximity scoring means users who prefer "medium" music are served as well as users who prefer extremes.
- Every recommendation comes with a plain-language explanation of *why* it was chosen, making the system fully transparent.
- Simple enough to audit by hand: you can trace every point back to a specific rule.

---

## 6. Limitations and Bias

- **Genre dominance**: A 2-point genre bonus means a mediocre genre-match will almost always beat a perfect mood+energy match in a different genre. The system may ignore great songs.
- **Catalog size**: With only 18 songs, many user profiles will see repeated or near-identical recommendations regardless of the energy/mood differences.
- **One-size scoring**: All users are evaluated against the same fixed rules. A user who cares mostly about danceability and not at all about genre gets a worse experience than the system was designed for.
- **Binary mood matching**: "Chill" and "relaxed" are semantically similar but score as total mismatches. The system has no concept of mood proximity.
- **Missing genres**: Any user who prefers K-pop, Afrobeats, or reggaeton will find nothing in the catalog that matches their genre — their top result will be driven entirely by energy/valence, which may feel irrelevant.
- **Western/English bias**: All songs are in an English-language, Western-pop framing.

---

## 7. Evaluation

Three user profiles were tested manually:

1. **Pop / Happy / High Energy (0.8)** — Results were intuitive: "Sunrise City" and "Gym Hero" ranked at the top, both pop/happy with high energy. Matched expectations.
2. **Lofi / Chill / Low Energy (0.4)** — "Midnight Coding" and "Library Rain" both scored at the top. System correctly prioritized the calm, acoustic tracks.
3. **Metal / Aggressive / High Energy (0.97)** — "Iron Tide" was the only metal song, so it ranked first easily. The second and third results were high-energy non-metal tracks (EDM, rock), which felt reasonable as fallbacks.

The automated tests in `tests/test_recommender.py` confirm that the pop/happy profile returns the pop song first, and that `explain_recommendation` always returns a non-empty string.

---

## 8. Future Work

- **Mood proximity**: Map moods to a similarity graph so "relaxed" and "chill" are treated as near-matches rather than total misses.
- **Catalog expansion**: Add at least 5 songs per genre so the diversity of results improves for minority-genre users.
- **Danceability and tempo weighting**: Add optional user preferences for danceability and tempo range — some users sort by how danceable a song is more than its energy.
- **Diversity penalty**: Avoid returning five songs by the same artist or five songs in the same sub-genre — add a diversity re-ranking step.
- **Collaborative layer**: Track which songs users skip or replay, and adjust future scores accordingly.

---

## 9. Personal Reflection

Building VibeFinder made it clear how much a real recommender depends on *what you measure*. Spotify has years of listening history, skip rates, and playlist co-occurrences to work with — this simulation only has a handful of floats per song. The most surprising outcome was how dominant the genre weight turned out to be: a 2-point genre bonus means a user who just wants "energetic music" but didn't pick the right genre label will get mediocre results. That mirrors a real risk in AI systems: if the most-weighted feature is also the most rigid or poorly defined, the whole model tilts toward it even when other signals would serve the user better. Human judgment still matters here — deciding *which* features to measure and *how much* to weight them is a design choice that encodes assumptions about what music listeners actually care about.
