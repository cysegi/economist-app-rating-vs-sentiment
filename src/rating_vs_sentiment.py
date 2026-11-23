"""Relate Google Play star ratings to VADER sentiment for The Economist app.

Reproduces in Python the regression reported in the course paper (originally run
in an Excel add-in): star rating ~ sentiment category, Positive as reference.

Usage: python src/rating_vs_sentiment.py data/output_economist_reviews2_file.xlsx
Input must contain the columns `score`, `Sentiment` and `Compound` produced by
notebooks/01_vader_sentiment.ipynb.
"""
import sys
from pathlib import Path

import pandas as pd
import statsmodels.formula.api as smf
from scipy.stats import spearmanr

src = Path(sys.argv[1] if len(sys.argv) > 1 else "data/output_economist_reviews2_file.xlsx")
df = pd.read_excel(src) if src.suffix == ".xlsx" else pd.read_csv(src)
df = df.dropna(subset=["score", "Sentiment", "Compound"])
out = Path("results"); out.mkdir(exist_ok=True)

# RQ1: sentiment polarity distribution
polarity = df["Sentiment"].value_counts().rename("n").to_frame()
polarity["share"] = (polarity["n"] / len(df)).round(4)
polarity.to_csv(out / "sentiment_distribution.csv")

# RQ2: star rating distribution
stars = df["score"].value_counts().sort_index().rename("n").to_frame()
stars["share"] = (stars["n"] / len(df)).round(4)
stars.to_csv(out / "star_distribution.csv")

# RQ3: relationship between stars and sentiment
pd.crosstab(df["score"], df["Sentiment"]).to_csv(out / "stars_by_sentiment.csv")
summary = df.groupby("Sentiment").agg(n=("score", "size"),
                                      mean_stars=("score", "mean"),
                                      mean_compound=("Compound", "mean")).round(3)
summary.to_csv(out / "summary_by_sentiment.csv")

model = smf.ols("score ~ C(Sentiment, Treatment('Positive'))", data=df).fit()
rho, p = spearmanr(df["score"], df["Compound"])
with open(out / "regression.txt", "w") as f:
    f.write(model.summary().as_text())
    f.write(f"\n\nSpearman rho (stars vs compound) = {rho:.3f}, p = {p:.2e}, n = {len(df)}\n")

print(polarity, stars, summary, sep="\n\n")
print(f"\nR^2 = {model.rsquared:.3f}, F = {model.fvalue:.2f}")
print(model.params.round(3))
print(f"Spearman rho = {rho:.3f}")
