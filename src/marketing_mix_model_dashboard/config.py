"""Project configuration for the Meridian marketing mix model."""
from pathlib import Path

# --- Paths -----------------------------------------------------------------
ROOT = Path(__file__).resolve().parents[2]
DATA_PATH = ROOT / "data" / "geo_all_channels.csv"
OUTPUT_DIR = ROOT / "outputs"
TABLEAU_DIR = OUTPUT_DIR / "tableau"
REPORTS_DIR = OUTPUT_DIR / "reports"
MODELS_DIR = OUTPUT_DIR / "models"
MODEL_PATH = MODELS_DIR / "mmm_main.pkl"
DATA_DICTIONARY_SRC = ROOT / "docs" / "tableau_data_dictionary.md"

# --- Run settings ----------------------------------------------------------
SEED = 42
SAMPLING_PRESET = "full"      # "smoke" | "standard" | "full"
RUN_SENSITIVITY = True        # refit alternative specs to test ROI robustness
LOAD_SAVED_MODEL = False      # reuse MODEL_PATH instead of sampling

SAMPLING_PRESETS = {
    "smoke":    dict(n_chains=2, n_adapt=20,   n_burnin=20,  n_keep=20,   n_prior=50),
    "standard": dict(n_chains=4, n_adapt=1000, n_burnin=500, n_keep=500,  n_prior=500),
    "full":     dict(n_chains=4, n_adapt=2000, n_burnin=500, n_keep=1000, n_prior=1000),
}
SENSITIVITY_PRESET = dict(n_chains=4, n_adapt=500, n_burnin=250, n_keep=250, n_prior=0)

# --- Model specification -----------------------------------------------------
KNOTS = 13                    # int, "aks" or None (one knot per week)
MAX_LAG = 8
HOLDOUT_FRACTION = 0.10
CONFIDENCE_LEVEL = 0.90

# Alternative specs refit in the sensitivity analysis: (name, knots, include_promo, include_organic)
SENSITIVITY_VARIANTS = [
    ("aks_knots", "aks", True, True),
    ("fixed_26_knots", 26, True, True),
    ("no_promo_no_organic", KNOTS, False, False),
    ("v1_replica", None, False, False),
]

# --- Budget optimization -----------------------------------------------------
SPEND_BOUND = 0.30            # max relative change per channel at fixed budget
BREAKEVEN_BOUNDS = (0.5, 1.0) # (lower, upper) spend constraints for the target-mROI run
BUDGET_MULTIPLIERS = [0.8, 0.9, 1.0, 1.1, 1.2]
OPTIMIZER_DRAWS = 250         # posterior draws used by the optimizer (runtime scales linearly)
ACTION_THRESHOLD_PCT = 5.0    # |spend change| below this is labelled "Maintain"
TRANCHE_PCT = 0.20            # size of the +/- spending tranche in the scorecard

# --- Channels ----------------------------------------------------------------
CHANNEL_MAP = {               # raw column prefix -> (display name, channel family)
    "Channel0": ("Goobly Search", "Paid Search"),
    "Channel1": ("Facepage Ads", "Paid Social"),
    "Channel2": ("Instaview Ads", "Paid Social"),
    "Channel3": ("LinkdUp Ads", "B2B Social"),
    "Channel4": ("Displayr Network", "Programmatic Display"),
}
ORGANIC_MAP = {"Organic_channel0": "Organic Social"}
CONTROL_RENAME = {
    "competitor_sales_control": "competitor_sales",
    "sentiment_score_control": "sentiment_score",
    "Promo": "promo",
}


def slug(name: str) -> str:
    return name.lower().replace(" ", "_")


PAID_CHANNELS = [name for name, _ in CHANNEL_MAP.values()]
CHANNEL_FAMILY = dict(CHANNEL_MAP.values())
IMPRESSION_COLS = [f"{slug(c)}_impressions" for c in PAID_CHANNELS]
SPEND_COLS = [f"{slug(c)}_spend" for c in PAID_CHANNELS]
ORGANIC_COLS = [slug(c) for c in ORGANIC_MAP.values()]
CONTROL_COLS = ["competitor_sales", "sentiment_score"]
NON_MEDIA_COLS = ["promo"]

SAMPLING = SAMPLING_PRESETS[SAMPLING_PRESET]
if SAMPLING_PRESET == "smoke":
    SENSITIVITY_PRESET = SAMPLING_PRESETS["smoke"]
