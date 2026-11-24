
from collections import deque
import string


EPSILON = "ε"


def epsilon_closure(state_set, transitions):
    """
    Find all states reachable using only epsilon transitions.
    """
    closure = set(state_set)
    stack = list(state_set)

    while stack:
        current = stack.pop()

        next_states = transitions.get(
            (current, EPSILON), set()
        )

        for state in next_states:
            if state not in closure:
                closure.add(state)
                stack.append(state)

    return frozenset(closure)


def move(state_set, symbol, transitions):
    """
    Find all states reachable from a subset
    using the given input symbol.
    """
    result = set()

    for state in state_set:
        next_states = transitions.get(
            (state, symbol), set()
        )
        result.update(next_states)

    return result


def subset_construction(
    states,
    alphabet,
    transitions,
    start_state,
    final_states
):
    """
    Convert an NFA into an equivalent DFA
    using the Subset Construction algorithm.
    """

    # Validate input
    states = set(states)
    alphabet = list(alphabet)
    final_states = set(final_states)

    if not states:
        raise ValueError("NFA must contain at least one state.")

    if start_state not in states:
        raise ValueError("Start state must belong to NFA states.")

    if not final_states.issubset(states):
        raise ValueError("All final states must belong to NFA states.")

    if EPSILON in alphabet:
        raise ValueError("Epsilon must not be included in the alphabet.")

    for (source, symbol), destinations in transitions.items():
        if source not in states:
            raise ValueError(f"Unknown source state: {source}")

        if symbol != EPSILON and symbol not in alphabet:
            raise ValueError(f"Unknown input symbol: {symbol}")

        if not set(destinations).issubset(states):
            raise ValueError("Transition contains an unknown destination state.")

    # Step 1: Find initial DFA state
    start_subset = epsilon_closure(
        {start_state}, transitions
    )

    dfa_states = {start_subset}
    dfa_transitions = {}
    steps = []

    queue = deque([start_subset])

    # Step 2: Process every discovered subset
    while queue:
        current_subset = queue.popleft()

        for symbol in alphabet:

            # Find reachable NFA states
            reached_states = move(
                current_subset,
                symbol,
                transitions
            )

            # Include epsilon-reachable states
            next_subset = epsilon_closure(
                reached_states,
                transitions
            )

            dfa_transitions[
                (current_subset, symbol)
            ] = next_subset

            is_new = next_subset not in dfa_states

            steps.append({
                "current_state": current_subset,
                "symbol": symbol,
                "reached_states": frozenset(reached_states),
                "next_state": next_subset,
                "is_new": is_new
            })

            if is_new:
                dfa_states.add(next_subset)
                queue.append(next_subset)

    # Step 3: Identify DFA final states
    dfa_final_states = {
        subset
        for subset in dfa_states
        if subset.intersection(final_states)
    }

    # Step 4: Assign readable DFA labels
    labels = {}

    for index, subset in enumerate(
        sorted(dfa_states, key=lambda s: sorted(s))
    ):
        if index < len(string.ascii_uppercase):
            label = string.ascii_uppercase[index]
        else:
            label = f"S{index}"

        labels[subset] = label

    # Return complete DFA
    return {
        "states": dfa_states,
        "alphabet": alphabet,
        "transitions": dfa_transitions,
        "start_state": start_subset,
        "final_states": dfa_final_states,
        "labels": labels,
        "steps": steps
    }
