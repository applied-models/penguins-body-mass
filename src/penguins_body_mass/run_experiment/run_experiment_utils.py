"""run_experiment_utils.py - utility functions for running experiments."""

from pathlib import Path

from matplotlib.axes import Axes
from matplotlib.figure import Figure


def save_figure(ax: Axes, path: Path) -> None:
    """Save the Matplotlib figure associated with an Axes object."""
    figure = ax.figure

    if not isinstance(figure, Figure):
        raise TypeError("Expected a Matplotlib Figure.")

    path.parent.mkdir(parents=True, exist_ok=True)

    figure.savefig(
        path,
        bbox_inches="tight",
    )
