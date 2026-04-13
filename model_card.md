# Model Card: VibeFinder 1.0

---

## 1. Model Name

**VibeFinder 1.0**

---

## 2. Goal / Task

VibeFinder's goal is to predict which songs from a small catalog a user will enjoy, based on three inputs: their preferred genre, their preferred mood, and a target energy level on a 0–1 scale. It produces a ranked list of top 5 songs and explains the reason behind each pick in plain language.

This is a simplified version of **content-based filtering** — the same general idea behind Spotify's "Radio" feature, but without any listening history or collaborative data.

---

## 3. Algorithm Summary

VibeFinder scores every song in the catalog by comparing it to what the user said they like, then returns the songs with the highest scores.

Here is how the scoring works, explained without code:

- If a song's **genre** matches the user's favorite genre, it earns 2 points. Genre is the biggest signal because most people primarily sort their music taste by genre first.
- If a song's **mood** matches the user's preferred mood, it earns 1 point.
- For **energy**, the score is based on how *close* the song's energy is to the user's target — not whether it is simply high or low. A song that is exactly on target earns 1 full point; one that is completely opposite earns 0.
- For **positivity (valence)**, the same closeness rule applies but with a smaller maximum reward of 0.5 points.
- If the user prefers acoustic music and the song is highly acoustic, it earns a small bonus of 0.5 points.

After every song is scored, they are sorted from highest to lowest. The top 5 are returned as recommendations.

---

## 4. Data Used

The catalog contains **18 songs** in `data/songs.csv`. The original 10 starter songs covered pop, lofi, rock, ambient, jazz, synthwave, and indie pop. Eight songs were added to improve genre diversity:

| Genre added | Mood added |
|---|---|
| hip-hop | energetic |
| classical | peaceful |
| country | nostalgic |
| metal | aggressive |
| R&B | romantic |
| EDM | euphoric |
| blues | melancholic |
| reggae | uplifting |

Each song has 10 attributes: id, title, artist, genre, mood, energy, tempo_bpm, valence, danceability, and acousticness.

**Limits of this dataset:**
- 18 songs is extremely small for a real recommender.
- Most genres have only one song (blues, metal, classical, reggae, etc.) — so any user who likes those genres gets essentially zero choice.
- The catalog reflects Western pop-adjacent taste. Genres like Afrobeats, K-pop, cumbia, and Bollywood are entirely absent.
- The mood vocabulary is narrow: 10 distinct moods for 18 songs. Synonyms like "chill" and "relaxed" are treated as completely different.

---

## 5. Observed Behavior / Biases

**Filter bubble — genre dominance:**
The single biggest bias is that the 2-point genre bonus makes it nearly impossible for a non-matching genre to win, even if every other preference aligns perfectly. In the adversarial test (Profile 4), a user who said they wanted high-energy (0.9) blues got "Empty Crossroads" as their #1 result — a slow, quiet blues song with energy of 0.33. The genre+mood bonus was 3.0 points, which no energy-similar song could overcome (max energy score is 1.0). This means **genre always wins**, even when the user's strongest actual preference might be energy or mood.

**Single-song genres create a dead-end:**
For blues, metal, classical, country, R&B, EDM, and reggae users, the #1 result will always be the same single song for that genre, regardless of any other preferences. The system cannot offer variety to users of minority genres.

**Mood synonyms are invisible:**
"Chill" and "relaxed" score as a complete mismatch. A user who prefers "relaxed" music will never get credit for liking "Midnight Coding" (chill lofi), even though they are nearly the same vibe. This affects jazz, lofi, and ambient listeners most.

**The cold-start floor is very low:**
Profile 5 (unknown genre "jazz-fusion") showed that when genre never matches, the system degenerates into an energy-proximity ranking. The top results included lofi and country tracks that have nothing in common with jazz-fusion except similar energy levels.

---

## 6. Evaluation Process

Five user profiles were tested:

| Profile | Genre | Mood | Energy | Type |
|---|---|---|---|---|
| 1 — High-Energy Pop Fan | pop | happy | 0.9 | Normal |
| 2 — Chill Lofi Listener | lofi | chill | 0.35 | Normal |
| 3 — Deep Intense Rock | rock | intense | 0.95 | Normal |
| 4 — High-Energy Blues Melancholic | blues | melancholic | 0.9 | Adversarial |
| 5 — Unknown Genre Jazz-Fusion | jazz-fusion | relaxed | 0.5 | Edge case |

**What matched expectations:**
- Profiles 1, 2, and 3 all returned genre-matching songs at #1, with the correct mood and closest energy. The system behaved exactly as designed for well-represented genres.
- Profile 2 achieved the maximum possible score (4.50) for "Library Rain" — a perfect genre + mood + exact energy match.

**What was surprising:**
- Profile 4 (adversarial): "Empty Crossroads" ranked #1 despite its energy (0.33) being nearly the opposite of what the user asked for (0.9). The genre+mood dominance was stronger than expected — it overrode a 0.57-point energy deficit entirely.
- Profile 5 (edge case): The system returned reasonable-feeling fallbacks (#1 "Coffee Shop Stories" — jazz/relaxed) because the mood matched, but positions 2–5 were generic mid-energy tracks with no real jazz connection.

**Automated tests** in `tests/test_recommender.py` confirm that the pop/happy profile always returns the pop song first, and that `explain_recommendation` always returns a non-empty string.

---

## 7. Intended Use and Non-Intended Use

**Intended use:**
- Classroom exploration of how content-based filtering works.
- Learning how scoring weights encode assumptions about user taste.
- A starting point for experimenting with bias in simple recommendation algorithms.

**Not intended for:**
- Real user-facing music apps. The catalog is far too small and the scoring is too rigid.
- Any situation where personalization matters — the system has no memory of past interactions.
- Users whose genre preferences are not represented in the catalog (most non-Western genres).
- Making decisions about what music is "objectively better" — the scores only reflect similarity to one pre-defined profile, not artistic quality.

---

## 8. Ideas for Improvement

1. **Mood proximity graph**: Instead of binary match/no-match, group moods into clusters (e.g., chill/relaxed/peaceful = similar; intense/aggressive/energetic = similar). Award partial points for near-matches.
2. **Per-user genre weight**: Let the user tell the system whether genre, mood, or energy matters most to them. A user who picks music purely by energy should be able to set genre weight to 0.
3. **Diversity re-ranking**: After scoring, apply a penalty if the same genre or artist appears more than once in the top 5, so recommendations stay varied even when the catalog is small.

---

## 9. Personal Reflection

**Biggest learning moment:** Building the adversarial profile (high-energy blues melancholic) made it clear that no matter how careful the scoring logic seems, a bad weight choice can produce results that feel wrong to the user. The genre bonus was designed to prioritize the most reliable taste signal — but when the catalog has only one song for a genre, that "reliability" turns into a trap.

**How AI tools helped:** Using Claude to scaffold the scoring logic and the CSV expansion saved significant time. But I had to double-check the adversarial results manually — the AI output looked correct but the scoring math needed to be verified by tracing a specific song through the formula step by step to confirm the genre+mood dominance effect was real.

**What surprised me about simple algorithms:** Even with just four scoring rules and 18 songs, the system produces results that *feel* like real recommendations for well-represented profiles. Profile 1 and Profile 2 both returned results that a human music fan would recognize as sensible. The surprise is how quickly that illusion breaks — Profile 4 exposes the brittleness immediately.

**What I would try next:** I would add a "mood distance" function that scores partial matches between similar moods, and experiment with lowering the genre weight from 2.0 to 1.5 to see if the adversarial profile improves without hurting the normal profiles. I would also try adding a fifth test profile — a user with perfectly average preferences across all features (genre: pop, mood: happy, energy: 0.5, valence: 0.5) — to see which songs float to the top when no strong signal dominates.
