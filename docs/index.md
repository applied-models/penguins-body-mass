# Penguins Body Mass

This project asks:

> How well can flipper length predict penguin body mass?

It provides a reproducible supervised regression experiment using the
Palmer Penguins dataset.

The experiment compares:

- a mean-value baseline
- linear regression using `flipper_length_mm`

The analytical decisions are declared with
[`composable-data-core`](https://pypi.org/project/composable-data-core/).

Standard model visualizations are created with
[`ml-vizkit`](https://pypi.org/project/ml-vizkit/).

## Analytical Plan

The experiment uses:

| Item | Declaration |
| --- | --- |
| Dataset | Palmer Penguins |
| Grain | one penguin |
| Learning mode | supervised |
| Problem type | regression |
| Target | `body_mass_g` |
| Selected feature | `flipper_length_mm` |
| Split | reproducible random train/test split |
| Baseline | `DummyRegressor` using the training mean |
| Candidate | `LinearRegression` |

The dataset contains additional available features, but this experiment
intentionally selects only flipper length.

## Feature Selection

Flipper length is a direct morphological measurement associated with penguin
body size.

This experiment asks whether one simple, interpretable feature can predict
body mass better than a no-feature mean-value baseline.

## Data Resolution

The source dataset contains 344 observations.

Two observations are missing either the selected feature or target and are
excluded from the modeling view.

The resulting experiment uses 342 complete observations.

## Train/Test Experiment

The modeling observations are divided into:

- 273 training observations
- 69 held-out test observations

Both models are trained using the same training observations and evaluated
using the same held-out test observations.

This provides a comparable basis for evaluating the baseline and candidate.

## Results

The held-out evaluation produced:

| Model | R² | MAE | RMSE |
| --- | ---: | ---: | ---: |
| Mean baseline | -0.010 | 693.15 | 819.59 |
| Linear regression | 0.782 | 315.86 | 380.69 |

The linear regression substantially outperformed the mean-value baseline on
all three evaluation measures.

## Actual vs. Predicted

![Actual versus predicted body mass](images/actual-vs-predicted.png)

This view compares the observed penguin body mass values with the predictions
produced by the trained linear regression model.

## Residuals

![Regression residuals](images/residuals.png)

Residuals show the difference between the observed and predicted body mass.

Residual structure should be examined for patterns that may indicate where the
linear model does not adequately describe the data.

## Model Comparison

![Baseline and candidate model comparison](images/model-comparison.png)

The candidate linear regression model clearly improves on the mean-value
baseline for this held-out test set.

## Assessment

The experiment supports the conclusion that flipper length provides substantial
predictive information about penguin body mass.

The candidate linear regression model outperformed the baseline on the same
held-out observations while using only one selected feature.

This does not establish that linear regression is the best possible model or
that flipper length is the best possible feature set.

Possible next experiments include:

- adding additional morphological features
- comparing other regression models
- testing alternative feature combinations
- examining whether species-specific models behave differently

## Project Structure

```text
src/
└── penguins_body_mass/
    ├── __init__.py
    ├── app.py
    ├── plan_experiment.py
    └── run_experiment.py
```

`plan_experiment.py` declares what will be tested and why.

`run_experiment.py` performs the experiment and records the resulting evidence.

`app.py` provides the stable project entry point.

## Run

From the repository root:

```shell
uv run python -m penguins_body_mass.app
```

## See Also

- [API](./api.md)
