"""Generate a synthetic bank customer dataset resembling UniversalBank.csv.

Run:  python sample_data/generate_sample.py
Produces: sample_data/bank_customers_sample.csv
"""

import os

import numpy as np
import pandas as pd

RNG = np.random.default_rng(42)
N = 5000


def main():
    age = RNG.integers(23, 67, size=N)
    experience = np.clip(age - RNG.integers(20, 26, size=N), 0, None)
    income = np.round(RNG.gamma(shape=3.0, scale=25, size=N) + 8).astype(int)
    family = RNG.integers(1, 5, size=N)
    ccavg = np.round(np.clip(income / 30 * RNG.uniform(0.3, 1.6, size=N), 0, None), 1)
    education = RNG.choice([1, 2, 3], size=N, p=[0.42, 0.28, 0.30])
    mortgage = np.where(
        RNG.random(N) < 0.3,
        RNG.integers(50, 600, size=N),
        0,
    )
    securities = (RNG.random(N) < 0.10).astype(int)
    cd_account = (RNG.random(N) < 0.06).astype(int)
    online = (RNG.random(N) < 0.6).astype(int)
    creditcard = (RNG.random(N) < 0.29).astype(int)

    # Latent propensity to accept a personal loan: driven by income, card
    # spend, education, CD account, family - matching domain intuition.
    z = (
        -7.5
        + 0.030 * income
        + 0.55 * ccavg
        + 0.45 * education
        + 1.6 * cd_account
        + 0.20 * family
        + 0.002 * mortgage
        + 0.3 * online
    )
    prob = 1 / (1 + np.exp(-z))
    personal_loan = (RNG.random(N) < prob).astype(int)

    df = pd.DataFrame({
        "ID": np.arange(1, N + 1),
        "Age": age,
        "Experience": experience,
        "Income": income,
        "ZIP Code": RNG.integers(90000, 96200, size=N),
        "Family": family,
        "CCAvg": ccavg,
        "Education": education,
        "Mortgage": mortgage,
        "Personal Loan": personal_loan,
        "Securities Account": securities,
        "CD Account": cd_account,
        "Online": online,
        "CreditCard": creditcard,
    })

    out = os.path.join(os.path.dirname(__file__), "bank_customers_sample.csv")
    df.to_csv(out, index=False)
    print(f"Wrote {out} ({len(df)} rows, acceptance rate "
          f"{df['Personal Loan'].mean():.1%})")


if __name__ == "__main__":
    main()
