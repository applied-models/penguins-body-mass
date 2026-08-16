"""plan_experiment.py - Plan the penguin body-mass regression experiment.

Purpose:
    Declare the complete pre-run experiment specification for predicting
    penguin body mass from flipper length.

Analytical question:
    How well can flipper length predict penguin body mass?

The experiment compares:
    - a mean-value baseline
    - linear regression

This file contains the analyst-facing decisions.
It does not load data, train models, calculate metrics, or create charts.

Run the full project from the repository root:

uv run python -m penguins_body_mass.app
"""

from typing import Final

from composable_data_core import (
    ExperimentSpec,
    Grain,
    LearningMode,
    ModelPlan,
    ModelRole,
    ProblemType,
    Resolution,
    ResolutionAction,
    SplitMethod,
    SplitPlan,
)

# ============================================================
# === Experiment Specification ===
# ============================================================

EXPERIMENT_SPEC: Final[ExperimentSpec[str]] = ExperimentSpec(
    # ========================================================
    # === Analytical Meaning ===
    # ========================================================
    # CUSTOM: Dataset used for this experiment.
    dataset="penguins",
    # OBS: One row in the Palmer Penguins dataset represents one penguin.
    grain=Grain("one penguin"),
    # OBS: This experiment has a target, so it is supervised learning.
    learning_mode=LearningMode.SUPERVISED,
    # OBS: The target is continuous numeric, so this is a regression problem.
    problem_type=ProblemType.REGRESSION,
    # ========================================================
    # === Target and Selected Features ===
    # ========================================================
    # CUSTOM: Numeric target to predict.
    target="body_mass_g",
    # CUSTOM: Features selected for this experiment.
    selected_features=("flipper_length_mm",),
    # CUSTOM: Explain why these features were selected.
    feature_rationale=r"""
        Flipper length was selected because it is a direct morphological
        measurement associated with penguin body size.

        This experiment asks whether one simple, interpretable feature can
        predict body mass better than a no-feature mean-value baseline.
        """,
    # ========================================================
    # === Data Resolution ===
    # ========================================================
    # WHY: Rows missing either required value cannot participate
    # in this experiment.
    resolution=Resolution(
        problem=(
            "Rows missing the selected feature or target cannot be used "
            "in this regression experiment."
        ),
        action=ResolutionAction.DROP,
        rationale=r"""
            The model requires both the selected feature and target for every
            observation used in the experiment.

            Rows missing either required value are excluded from the
            modeling view.
            """,
    ),
    # ========================================================
    # === Train/Test Split ===
    # ========================================================
    # CUSTOM: Declare how observations are divided into train and test sets.
    split=SplitPlan(
        method=SplitMethod.RANDOM,
        test_size=0.20,
        seed=42,
        rationale=r"""
            Individual penguins are independent observations for this example,
            so a reproducible random holdout is appropriate.

            Both models use the same training observations and are evaluated
            on the same held-out test observations.
            """,
    ),
    # ========================================================
    # === Baseline Model ===
    # ========================================================
    baseline_id="mean-baseline",
    # WHY: A baseline provides the minimum performance a useful model
    # should beat.
    baseline=ModelPlan(
        estimator="DummyRegressor",
        role=ModelRole.BASELINE,
        parameters={"strategy": "mean"},
        rationale=r"""
            The baseline predicts the mean body mass observed in the
            training data.

            A useful candidate model should improve on this simple prediction
            that does not use flipper length.
            """,
    ),
    # ========================================================
    # === Candidate Model ===
    # ========================================================
    candidate_id="linear-regression",
    # CUSTOM: Declare the model to investigate and explain why it was selected.
    candidate=ModelPlan(
        estimator="LinearRegression",
        role=ModelRole.CANDIDATE,
        rationale=r"""
            Linear regression provides a simple and interpretable test of
            whether body mass changes approximately linearly with
            flipper length.
            """,
    ),
)
