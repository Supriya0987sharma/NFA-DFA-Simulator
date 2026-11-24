
def make_nfa_diagram(states, alphabet, transitions, start_state, final_states):
    """
    Generate a Graphviz DOT diagram for the original NFA.
    """

    states = sorted(states)
    final_states = set(final_states)

    # Assign safe internal IDs to states
    state_ids = {
        state: f"n{index}"
        for index, state in enumerate(states)
    }

    dot = """
    digraph NFA {
        rankdir=LR;
        bgcolor="white";
        graph [pad="0.4", nodesep="0.7", ranksep="1.0"];
        node [
            shape=circle,
            style=filled,
            fillcolor="#B7DDE8",
            color="#263238",
            penwidth=2,
            fontname="Arial",
            fontsize=14
        ];
        edge [
            color="#263238",
            penwidth=1.8,
            fontname="Arial",
            fontsize=12
        ];

        start [shape=point, label="", width=0.15];
    """

    # Add start arrow
    dot += f'\nstart -> {state_ids[start_state]};\n'

    # Add all states
    for state in states:

        state_id = state_ids[state]

        if state in final_states:
            shape = "doublecircle"
        else:
            shape = "circle"

        # Escape special characters in labels
        safe_label = (
            state.replace("\\", "\\\\")
            .replace('"', '\\"')
        )

        dot += (
            f'{state_id} [label="{safe_label}", '
            f'shape={shape}];\n'
        )

    # Group transitions with the same source and destination
    grouped_transitions = {}

    for (source, symbol), destinations in transitions.items():

        for destination in destinations:

            key = (source, destination)

            if key not in grouped_transitions:
                grouped_transitions[key] = set()

            grouped_transitions[key].add(symbol)

    # Add transition arrows
    for (source, destination), symbols in grouped_transitions.items():

        labels = ", ".join(
            sorted(symbols, key=lambda x: (x == "ε", x))
        )

        safe_label = (
            labels.replace("\\", "\\\\")
            .replace('"', '\\"')
        )

        dot += (
            f'{state_ids[source]} -> {state_ids[destination]} '
            f'[label="{safe_label}"];\n'
        )

    dot += "}"

    return dot


def make_dfa_diagram(result):
    """
    Generate a Graphviz DOT diagram for the generated DFA.
    """

    dot = """
    digraph DFA {
        rankdir=LR;
        bgcolor="white";
        graph [pad="0.4", nodesep="0.7", ranksep="1.0"];
        node [
            style=filled,
            fillcolor="#B7DDE8",
            color="#263238",
            penwidth=2,
            fontname="Arial",
            fontsize=13
        ];
        edge [
            color="#263238",
            penwidth=1.8,
            fontname="Arial",
            fontsize=12
        ];

        start [shape=point, label="", width=0.15];
    """

    start_label = result["labels"][result["start_state"]]

    dot += f'\nstart -> "{start_label}";\n'

    # Add DFA states
    for subset, label in result["labels"].items():

        shape = (
            "doublecircle"
            if subset in result["final_states"]
            else "circle"
        )

        subset_text = (
            ", ".join(sorted(subset)) if subset else "∅"
        )

        safe_label = (
            f"{label}\\n{{{subset_text}}}"
            .replace("\\", "\\\\")
            .replace('"', '\\"')
        )

        dot += (
            f'"{label}" [shape={shape}, '
            f'label="{safe_label}"];\n'
        )

    # Add DFA transitions
    for (subset, symbol), destination in result["transitions"].items():

        source_label = result["labels"][subset]
        destination_label = result["labels"][destination]

        safe_symbol = (
            symbol.replace("\\", "\\\\")
            .replace('"', '\\"')
        )

        dot += (
            f'"{source_label}" -> "{destination_label}" '
            f'[label="{safe_symbol}"];\n'
        )

    dot += "}"

    return dot
