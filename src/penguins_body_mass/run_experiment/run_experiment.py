"""run_experiment.py - Run the penguin body-mass regression experiment.

The analyst's decisions live in plan_experiment.py as a single SPEC.
This file executes that SPEC and keeps the run aligned with it.

Run from the repository root:

uv run python -m penguins_body_mass.app
"""

import logging
from pathlib import Path

from composable_data_core import (
    Evaluation,
    ExperimentAssessment,
    ResolutionAction,
    SplitMethod,
)
from datafun_toolkit.logger import get_logger, log_header
import matplotlib.pyplot as plt
from ml_vizkit import compare_models, show_actual_vs_predicted, show_residuals
import pandas as pd
import seaborn as sns
from sklearn.dummy import DummyRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score, root_mean_squared_error
from sklearn.model_selection import train_test_split

from penguins_body_mass.plan_experiment import EXPERIMENT_SPEC
from penguins_body_mass.run_experiment.run_experiment_utils import save_figure

__all__ = ["run_experiment"]

LOG: logging.Logger = get_logger("PENGUINS-BODY-MASS", level="DEBUG")
IMAGES_DIR = Path("docs/images")


def _evaluate(model_id: str, y_true, y_pred) -> Evaluation:
    """Evaluate one regression model on held-out observations."""
    return Evaluation(
        model_id=model_id,
        metrics={
            "r2": float(r2_score(y_true, y_pred)),
            "mae": float(mean_absolute_error(y_true, y_pred)),
            "rmse": float(root_mean_squared_error(y_true, y_pred)),
        },
    )


def _save(ax, name: str) -> None:
    """Save and log one visualization."""
    path = IMAGES_DIR / name
    save_figure(ax, path)
    LOG.info("Saved figure: %s", path)


def run_experiment() -> ExperimentAssessment:
    """Run the penguin body-mass regression experiment declared in SPEC."""
    log_header(LOG, "PENGUINS BODY MASS")

    LOG.info(
        "%s | %s | %s",
        EXPERIMENT_SPEC.grain.observation,
        EXPERIMENT_SPEC.learning_mode,
        EXPERIMENT_SPEC.problem_type,
    )

    # ========================================================
    # === RUN 1. Load and Validate Data ===
    # ========================================================

    df: pd.DataFrame = sns.load_dataset(EXPERIMENT_SPEC.dataset)

    LOG.info(
        "Loaded %d rows and %d columns",
        df.shape[0],
        df.shape[1],
    )

    if EXPERIMENT_SPEC.target not in df.columns:
        raise ValueError(f"Target {EXPERIMENT_SPEC.target!r} not found in dataset.")

    available_features: tuple[str, ...] = tuple(
        column for column in df.columns if column != EXPERIMENT_SPEC.target
    )

    unknown_features = set(EXPERIMENT_SPEC.selected_features) - set(available_features)

    if unknown_features:
        raise ValueError(
            f"Selected features not found in dataset: {sorted(unknown_features)}"
        )

    LOG.info("Target: %s", EXPERIMENT_SPEC.target)
    LOG.info("Available features: %s", available_features)
    LOG.info("Selected features: %s", EXPERIMENT_SPEC.selected_features)

    # ========================================================
    # === RUN 2. Prepare Modeling Data ===
    # ========================================================

    if EXPERIMENT_SPEC.resolution.action is not ResolutionAction.DROP:
        raise ValueError(
            f"Unsupported resolution action: {EXPERIMENT_SPEC.resolution.action}"
        )

    required_columns = [
        *EXPERIMENT_SPEC.selected_features,
        EXPERIMENT_SPEC.target,
    ]

    df_model: pd.DataFrame = df.loc[:, required_columns].dropna().copy()

    LOG.info(
        "Modeling on %d of %d rows (%s)",
        len(df_model),
        len(df),
        EXPERIMENT_SPEC.resolution.action,
    )

    X = df_model.loc[
        :,
        list(EXPERIMENT_SPEC.selected_features),
    ]

    y = df_model.loc[
        :,
        EXPERIMENT_SPEC.target,
    ]

    # ========================================================
    # === RUN 3. Split Data ===
    # ========================================================

    if EXPERIMENT_SPEC.split.method is not SplitMethod.RANDOM:
        raise ValueError(f"Unsupported split method: {EXPERIMENT_SPEC.split.method}")

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=EXPERIMENT_SPEC.split.test_size,
        random_state=EXPERIMENT_SPEC.split.seed,
    )

    LOG.info(
        "Train: %d | Test: %d",
        len(X_train),
        len(X_test),
    )

    # ========================================================
    # === RUN 4. Train and Predict ===
    # ========================================================

    baseline = DummyRegressor(
        strategy=EXPERIMENT_SPEC.baseline.parameters["strategy"],
    )

    baseline.fit(
        X_train,
        y_train,
    )

    baseline_predictions = baseline.predict(
        X_test,
    )

    candidate = LinearRegression()

    candidate.fit(
        X_train,
        y_train,
    )

    candidate_predictions = candidate.predict(
        X_test,
    )

    # ========================================================
    # === RUN 5. Evaluate ===
    # ========================================================

    baseline_evaluation = _evaluate(
        EXPERIMENT_SPEC.baseline_id,
        y_test,
        baseline_predictions,
    )

    candidate_evaluation = _evaluate(
        EXPERIMENT_SPEC.candidate_id,
        y_test,
        candidate_predictions,
    )

    LOG.info(
        "Baseline: %s",
        dict(baseline_evaluation.metrics),
    )

    LOG.info(
        "Candidate: %s",
        dict(candidate_evaluation.metrics),
    )

    # ========================================================
    # === RUN 6. Visualize and Save ===
    # ========================================================

    actual_vs_predicted_ax = show_actual_vs_predicted(
        y_test,
        candidate_predictions,
    )

    actual_vs_predicted_ax.set_title("Penguin Body Mass: Actual vs Predicted")

    _save(
        actual_vs_predicted_ax,
        "actual-vs-predicted.png",
    )

    residual_ax = show_residuals(
        y_test,
        candidate_predictions,
    )

    residual_ax.set_title("Penguin Body Mass: Residuals")

    _save(
        residual_ax,
        "residuals.png",
    )

    comparison_ax = compare_models(
        {
            "Mean baseline": baseline_evaluation.metrics["r2"],
            "Linear regression": candidate_evaluation.metrics["r2"],
        },
        metric_name="R²",
        title="Held-Out Model Comparison",
    )

    comparison_ax.set_ylabel("R²")

    _save(
        comparison_ax,
        "model-comparison.png",
    )

    # ========================================================
    # === RUN 7. Assess ===
    # ========================================================

    baseline_r2 = baseline_evaluation.metrics["r2"]
    candidate_r2 = candidate_evaluation.metrics["r2"]

    baseline_beaten = candidate_r2 > baseline_r2

    conclusion = (
        "Linear regression outperformed the mean baseline "
        "on the held-out test observations."
        if baseline_beaten
        else "Linear regression did not outperform the mean baseline "
        "on the held-out test observations."
    )

    assessment = ExperimentAssessment(
        comparison=(
            "Mean-value baseline versus linear regression "
            "on the same held-out test observations."
        ),
        conclusion=conclusion,
        rationale=(
            "Both models used the same target, selected feature, training data, "
            "test data, and evaluation metrics, so the comparison uses a common "
            "experimental basis."
        ),
        winner_model_id=(
            EXPERIMENT_SPEC.candidate_id
            if baseline_beaten
            else EXPERIMENT_SPEC.baseline_id
        ),
        baseline_beaten=baseline_beaten,
    )

    LOG.info(
        "Assessment: %s",
        assessment.conclusion,
    )

    # ========================================================
    # === RUN 8. Display ===
    # ========================================================

    LOG.info("Close chart windows to continue.")
    plt.show()

    return assessment
