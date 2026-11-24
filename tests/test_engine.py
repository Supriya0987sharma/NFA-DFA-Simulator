
import pytest

from engine import subset_construction


def test_basic_nfa_to_dfa():
    states = {"q0", "q1", "q2"}
    alphabet = {"0", "1"}

    transitions = {
        ("q0", "0"): {"q0", "q1"},
        ("q0", "1"): {"q0"},
        ("q1", "1"): {"q2"}
    }

    result = subset_construction(
        states,
        alphabet,
        transitions,
        "q0",
        {"q2"}
    )

    A = frozenset({"q0"})
    B = frozenset({"q0", "q1"})
    C = frozenset({"q0", "q2"})

    assert result["start_state"] == A
    assert result["transitions"][(A, "0")] == B
    assert result["transitions"][(A, "1")] == A
    assert result["transitions"][(B, "0")] == B
    assert result["transitions"][(B, "1")] == C
    assert result["final_states"] == {C}


def test_epsilon_transition():
    states = {"q0", "q1", "q2"}
    alphabet = {"0"}

    transitions = {
        ("q0", "ε"): {"q1"},
        ("q1", "0"): {"q2"}
    }

    result = subset_construction(
        states,
        alphabet,
        transitions,
        "q0",
        {"q2"}
    )

    start = frozenset({"q0", "q1"})
    final = frozenset({"q2"})

    assert result["start_state"] == start
    assert result["transitions"][(start, "0")] == final
    assert final in result["final_states"]


def test_dead_state():
    states = {"q0", "q1"}
    alphabet = {"0", "1"}

    transitions = {
        ("q0", "0"): {"q1"}
    }

    result = subset_construction(
        states,
        alphabet,
        transitions,
        "q0",
        {"q1"}
    )

    dead = frozenset()
    
    assert dead in result["states"]
    assert result["transitions"][(dead, "0")] == dead
    assert result["transitions"][(dead, "1")] == dead


def test_invalid_start_state():
    with pytest.raises(ValueError):
        subset_construction(
            {"q0", "q1"},
            {"0", "1"},
            {},
            "q5",
            {"q1"}
        )


def test_invalid_final_state():
    with pytest.raises(ValueError):
        subset_construction(
            {"q0", "q1"},
            {"0", "1"},
            {},
            "q0",
            {"q5"}
        )
