"""app.py - Run the penguin body-mass experiment.

Run from the repository root:

uv run python -m penguins_body_mass.app
"""

from penguins_body_mass.run_experiment import run_experiment


def main() -> None:
    """Run the complete experiment."""
    run_experiment()


if __name__ == "__main__":
    main()
