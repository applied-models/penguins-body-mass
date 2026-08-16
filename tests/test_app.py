"""Tests for the app entry point."""

from penguins_body_mass.app import main


def test_main_calls_run_experiment(monkeypatch) -> None:
    """The app entry point should invoke the experiment runner once."""
    calls: list[str] = []

    def fake_run_experiment() -> None:
        calls.append("called")

    monkeypatch.setattr(
        "penguins_body_mass.app.run_experiment",
        fake_run_experiment,
    )

    main()

    assert calls == ["called"]
