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
| Split | reproducible random 80/20 train/test split |
| Baseline | `DummyRegressor` using the training mean |
| Candidate | `LinearRegression` |

The source dataset contains several possible predictors:

- `species`
- `island`
- `bill_length_mm`
- `bill_depth_mm`
- `flipper_length_mm`
- `sex`

This experiment intentionally selects only `flipper_length_mm`.

That makes the experiment easy to interpret: it asks whether one physical
measurement carries enough information to predict body mass substantially
better than simply predicting the training-set mean for every penguin.

## Feature Selection

Flipper length is a direct morphological measurement associated with penguin
body size.

The selected feature is:

```text
flipper_length_mm
```

The target is:

```text
body_mass_g
```

Using one feature also makes the first experiment deliberately constrained.
The goal is not to find the strongest possible penguin body-mass model.
The goal is to establish a clear, reproducible experiment and determine
whether this single feature provides meaningful predictive information.

## Data Resolution

The source dataset contains 344 observations.

The model requires both:

- `flipper_length_mm`
- `body_mass_g`

for every observation used in the experiment.

Two observations are missing one of these required values and are therefore
excluded according to the declared data-resolution policy.

The resulting modeling dataset contains:

```text
342 complete observations
```

No values are imputed for this experiment.

## Train/Test Experiment

The 342 modeling observations are divided into:

- 273 training observations
- 69 held-out test observations

The training observations are used to fit both models.

The 69 test observations remain held out until evaluation.

Both the baseline and candidate are therefore evaluated on exactly the same
unseen observations. This gives the comparison a common experimental basis.

## Models

### Mean-Value Baseline

The baseline uses scikit-learn's `DummyRegressor` with the mean strategy.

It learns only the mean body mass from the training observations and predicts
that same value for every test observation.

The baseline answers an important question:

> Does the candidate model actually learn useful predictive information from
> flipper length?

A useful candidate should outperform this simple reference model.

### Linear Regression Candidate

The candidate uses scikit-learn's `LinearRegression`.

It estimates a linear relationship between:

```text
flipper length → body mass
```

The candidate therefore tests whether changes in flipper length provide useful
information for estimating body mass.

## Held-Out Results

The experiment produced the following test-set metrics:

| Model | R² | MAE | RMSE |
| --- | ---: | ---: | ---: |
| Mean baseline | -0.010 | 693.15 g | 819.59 g |
| Linear regression | 0.782 | 315.86 g | 380.69 g |

The candidate improves substantially on the baseline.

### R²

The linear regression achieved:

```text
R² = 0.782
```

For this held-out test set, the model explains a substantial portion of the
variation in penguin body mass using only flipper length.

The baseline R² is slightly below zero:

```text
R² = -0.010
```

A negative held-out R² indicates that the baseline performed slightly worse
than simply using the test-set mean as a reference.

### Mean Absolute Error

The candidate model has:

```text
MAE = 315.86 g
```

This means the candidate's predictions differ from the observed body masses
by about 316 grams on average, measured as absolute error.

The baseline MAE is much larger:

```text
MAE = 693.15 g
```

### Root Mean Squared Error

The candidate model has:

```text
RMSE = 380.69 g
```

The baseline RMSE is:

```text
RMSE = 819.59 g
```

RMSE gives greater influence to larger errors than MAE, so examining both
metrics helps characterize prediction error.

## Actual vs. Predicted

A standard regression diagnostic compares the observed target values with the
values predicted by the candidate model.

![Actual versus predicted penguin body mass](images/actual-vs-predicted.png)

Points closer to the reference relationship indicate predictions that are
closer to the observed body mass.

This chart provides information that a single metric cannot: it shows how the
model behaves across smaller and larger penguins and makes unusually large
prediction errors easier to identify.

The overall pattern is consistent with the held-out R² result: flipper length
contains substantial predictive information about body mass, although the
predictions are not perfect.

## Residuals

A residual is:

```text
observed value - predicted value
```

The residual plot shows the candidate model's prediction errors across the
held-out observations.

![Penguin body-mass regression residuals](images/residuals.png)

For a useful linear model, residuals should generally remain centered around
zero without a strong systematic pattern.

This plot should be examined for:

- unusually large errors
- curvature or other non-linear structure
- changing error magnitude
- groups of observations behaving differently

Residual analysis is important because a reasonably strong R² can coexist
with systematic modeling problems that are easier to see visually.

## Baseline vs. Candidate

The baseline comparison asks whether using the selected feature produces a
meaningful improvement over a model that uses no predictor information.

![Baseline and candidate model comparison](images/model-comparison.png)

The candidate linear regression model has a substantially higher held-out R²
than the mean-value baseline.

This is the central experimental comparison:

```text
Mean baseline
    ↓
Does flipper length add useful predictive information?
    ↓
Linear regression
```

For this split, the answer is yes.

## Assessment

The experiment supports the conclusion that flipper length provides substantial
predictive information about penguin body mass.

The candidate linear regression model:

- substantially improves R² over the baseline
- reduces mean absolute error
- reduces root mean squared error
- produces predictions that track the observed body masses reasonably well

The conclusion is deliberately limited to the evidence produced by this
experiment.

It does not establish that:

- linear regression is the best possible model
- flipper length is the best possible feature
- one feature is sufficient for every analytical purpose
- the same performance will occur on every possible train/test split
- the relationship is identical across penguin species or other subgroups

## Next Experiments

This experiment establishes a simple reference point that can be extended.

Possible next experiments include:

- adding `bill_length_mm`
- adding `bill_depth_mm`
- using several morphological features together
- comparing alternative regression models
- testing different train/test splits
- examining performance by species
- comparing species-specific models
- investigating whether additional features reduce residual error

Each new experiment can retain the same basic analytical structure while
changing the declared target, selected features, split, or candidate model.

## Experiment Workflow

The project separates planning from execution.

```text
QUESTION
    ↓
EXPERIMENT SPECIFICATION
    ↓
LOAD AND VALIDATE DATA
    ↓
PREPARE MODELING VIEW
    ↓
TRAIN/TEST SPLIT
    ↓
BASELINE + CANDIDATE
    ↓
HELD-OUT EVALUATION
    ↓
VISUAL EVIDENCE
    ↓
ASSESSMENT
```

`plan_experiment.py` contains the analyst's pre-run experiment specification.

`run_experiment.py` performs the ordinary pandas and scikit-learn operations
that execute the declared experiment.

The specification does not train models or calculate results.

The execution does not silently redefine the analyst's decisions.

## Project Structure

```text
src/
└── penguins_body_mass/
    ├── __init__.py
    ├── app.py
    ├── plan_experiment.py
    └── run_experiment/
        ├── __init__.py
        ├── run_experiment.py
        └── run_experiment_utils.py
```

The major responsibilities are:

- `app.py` - stable entry point for the complete project
- `plan_experiment.py` - declares the experiment specification
- `run_experiment.py` - executes the experiment and records the evidence
- `run_experiment_utils.py` - contains small reusable execution helpers

## Run

From the repository root:

```shell
uv run python -m penguins_body_mass.app
```

The run:

1. loads the Palmer Penguins dataset
2. validates the declared experiment against the observed data
3. resolves missing required values
4. creates the declared train/test split
5. trains the baseline model
6. trains the candidate model
7. evaluates both models on the same held-out observations
8. generates and saves the regression charts
9. records the experiment assessment
10. displays the generated charts

Generated figures are written to:

```text
docs/images/
├── actual-vs-predicted.png
├── residuals.png
└── model-comparison.png
```

## See Also

- [API](./api.md)
