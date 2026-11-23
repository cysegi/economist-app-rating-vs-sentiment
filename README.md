# Star Ratings vs. User Sentiment: The Economist App (Google Play)

Do star ratings reflect what users actually write? This project scores 5,100 Google Play reviews of The Economist Android app (`com.economist.lamarr`) with VADER and tests how well sentiment polarity explains the star rating.

Course project for ABM503D Web and Social Media Analytics, Universiti Sains Malaysia (Semester 1, 2025/2026). Two-person team: Chew Yoong Chang and Felicia Yeow Kar Mun.

## Research questions

1. RQ1. What is the sentiment polarity distribution of the reviews?
2. RQ2. How are star ratings distributed?
3. RQ3. How strongly does sentiment polarity relate to the star rating?

## Data

- Source: Google Play Store, collected with `google-play-scraper` (English, Malaysia storefront).
- Window: 2019-12-09 to 2025-11-28.
- 5,114 reviews collected; 5,100 retained after cleaning.
- Raw review data is not included in this repository because it contains reviewer names and profile images. Run `notebooks/00_collect_google_play_reviews.ipynb` to rebuild it. See `data/README.md`.

## Method

1. Collection: `notebooks/00_collect_google_play_reviews.ipynb`.
2. Cleaning and scoring: `notebooks/01_vader_sentiment.ipynb`.
   - Steps: language check with translation to English when needed, lowercase, remove links, emojis, mentions and punctuation, tokenize, remove stopwords (keeping not, no and nor), lemmatize.
   - NLTK VADER compound score, labeled Positive (> 0.05), Negative (< -0.05), otherwise Neutral.
   - Outputs: pie chart, word clouds, top-word bars, and daily, monthly and yearly trends.
3. Statistics: `src/rating_vs_sentiment.py`. This is an OLS regression of star rating on sentiment category, with Positive as the reference, plus a Spearman correlation between stars and the compound score. The course paper ran this regression in an Excel add-in; this script reproduces it in Python with the same coefficients.

## Results

| Sentiment | Reviews | Share | Mean stars | Mean compound |
|---|---:|---:|---:|---:|
| Positive | 2,892 | 56.7% | 3.85 | 0.565 |
| Negative | 1,328 | 26.0% | 1.79 | -0.474 |
| Neutral | 880 | 17.3% | 3.08 | 0.000 |

- Star ratings are polarized: 1,919 five-star (37.6%) and 1,417 one-star (27.8%) reviews; mean 3.18.
- Regression: F(2, 5097) = 927.36, p < .001, R² = 0.267. Relative to Positive reviews:
  - Negative reviews average 2.06 fewer stars (β = -2.057).
  - Neutral reviews average 0.77 fewer stars (β = -0.766).
- Spearman ρ (stars vs. compound) = 0.526.
- 82 five-star reviews scored Negative, and 380 one-star reviews scored Positive.
- Negative reviews centered on audio playback, offline access, app stability and subscription issues.

Interpretation: sentiment and rating agree only moderately. Text-level analysis surfaces technical complaints that the headline Play Store rating hides.

Charts are in `results/charts/`. Tables from the script are in `results/`.

## Limitations

- VADER is a lexicon model. It misses sarcasm and domain terms, and it does not weigh mixed reviews well.
- Reviews come from a single storefront and language, so they are not a random sample of users.
- The cleaning step `re.sub(r'rt', '', text)`, inherited from a Twitter template, also removes "rt" inside words (for example, "start" becomes "sta"). This slightly affects the word clouds and top-word charts. VADER scores were computed on the cleaned text.
- The regression treats the 1 to 5 star scale as interval data.

## Run

```bash
pip install -r requirements.txt
python src/rating_vs_sentiment.py data/output_economist_reviews2_file.xlsx
```

## Credits

- Joint work with Felicia Yeow Kar Mun.
- Cleaning and VADER notebook structure adapted from ABM503D lab material (Prof. Dr. Nor Hasliza Md Saad, USM).
- The regression script was added after the course to make the statistics reproducible in Python.
