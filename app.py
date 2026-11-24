

import streamlit as st
import pandas as pd

from engine import subset_construction
from visualizer import make_nfa_diagram, make_dfa_diagram


# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="NFA to DFA Simulator",
    page_icon="🔄",
    layout="wide"
)

st.title("NFA to DFA Conversion Simulator")
st.caption("Subset Construction Algorithm | CSET302 Automata Theory")

st.markdown(
    "Convert a Non-Deterministic Finite Automaton (NFA) "
    "into an equivalent Deterministic Finite Automaton (DFA)."
)

st.divider()


# ==========================================
# NFA INPUT SECTION
# ==========================================

st.header("1. Define your NFA")

col1, col2 = st.columns(2)

with col1:
    states_input = st.text_input(
        "Enter NFA states (comma separated)",
        value="q0,q1,q2"
    )

    alphabet_input = st.text_input(
        "Enter input alphabet (comma separated)",
        value="0,1"
    )

    start_state = st.text_input(
        "Initial state",
        value="q0"
    )

with col2:
    final_input = st.text_input(
        "Final states (comma separated)",
        value="q2"
    )


# ==========================================
# TRANSITION INPUT SECTION
# ==========================================

st.header("2. Enter NFA transitions")

st.info(
    "Enter one transition per line in this format: "
    "source,input,destination. Use ε for epsilon transitions."
)

transitions_input = st.text_area(
    "Transition definitions",
    value="""q0,0,q0
q0,0,q1
q0,1,q0
q1,1,q2""",
    height=160
)

st.caption(
    "Example: q0,0,q1 means state q0 moves to q1 on input 0."
)


# ==========================================
# NFA TO DFA CONVERSION
# ==========================================

if st.button(
    "Convert NFA to DFA",
    type="primary",
    use_container_width=True
):

    try:
        # Parse states
        states = {
            item.strip()
            for item in states_input.split(",")
            if item.strip()
        }

        # Parse alphabet
        alphabet = [
            item.strip()
            for item in alphabet_input.split(",")
            if item.strip()
        ]

        # Parse final states
        final_states = {
            item.strip()
            for item in final_input.split(",")
            if item.strip()
        }

        # Parse transitions
        transitions = {}

        for line_number, line in enumerate(
            transitions_input.splitlines(),
            start=1
        ):

            if not line.strip():
                continue

            parts = [
                part.strip()
                for part in line.split(",")
            ]

            if len(parts) != 3 or not all(parts):
                raise ValueError(
                    f"Invalid transition at line {line_number}. "
                    "Use source,input,destination."
                )

            source, symbol, destination = parts

            key = (source, symbol)

            if key not in transitions:
                transitions[key] = set()

            transitions[key].add(destination)

        # Validate input
        if not states:
            raise ValueError(
                "Please enter at least one NFA state."
            )

        if not alphabet:
            raise ValueError(
                "Please enter at least one input symbol."
            )

        if len(alphabet) != len(set(alphabet)):
            raise ValueError(
                "Duplicate input symbols are not allowed."
            )

        if not start_state.strip():
            raise ValueError(
                "Please enter an initial state."
            )

        if not final_states.issubset(states):
            raise ValueError(
                "Final states must belong to the NFA states."
            )

        # Perform conversion
        result = subset_construction(
            states,
            alphabet,
            transitions,
            start_state.strip(),
            final_states
        )

        # Store both NFA and DFA results together
        st.session_state["dfa_result"] = result

        st.session_state["nfa_data"] = {
            "states": states,
            "alphabet": alphabet,
            "transitions": transitions,
            "start_state": start_state.strip(),
            "final_states": final_states
        }

        st.success(
            "NFA successfully converted into DFA!"
        )

    except Exception as error:

        st.session_state.pop("dfa_result", None)
        st.session_state.pop("nfa_data", None)

        st.error(f"Conversion failed: {error}")


# ==========================================
# DISPLAY RESULTS
# ==========================================

result = st.session_state.get("dfa_result")
nfa_data = st.session_state.get("nfa_data")


if result is not None and nfa_data is not None:

    st.divider()

    st.header("3. DFA Conversion Results")

    # Summary metrics
    col1, col2, col3 = st.columns(3)

    col1.metric(
        "DFA States",
        len(result["states"])
    )

    col2.metric(
        "DFA Final States",
        len(result["final_states"])
    )

    col3.metric(
        "Input Symbols",
        len(result["alphabet"])
    )

    # Generated states
    st.subheader("Generated DFA States")

    for subset, label in result["labels"].items():

        subset_text = (
            ", ".join(sorted(subset))
            if subset else "∅"
        )

        
    if subset == result["start_state"]:
        status = "Initial State"

    elif subset in result["final_states"]:
        status = "Final State"

    elif not subset:
        status = "Dead State"

    else:
        status = "Normal State"


        st.write(
            f"**{label} = {{{subset_text}}}** — {status}"
        )

    # --------------------------------------
    # DFA TRANSITION TABLE
    # --------------------------------------

    st.subheader("DFA Transition Table")

    table_data = []

    for subset, label in result["labels"].items():

        row = {
            "DFA State": label,
            "NFA Subset": (
                "{" + ", ".join(sorted(subset)) + "}"
                if subset else "∅"
            )
        }

        for symbol in result["alphabet"]:

            destination = result["transitions"][
                (subset, symbol)
            ]

            row[symbol] = result["labels"][destination]

        table_data.append(row)

    df = pd.DataFrame(table_data)

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

    # CSV download
    csv_data = df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="Download DFA Transition Table (CSV)",
        data=csv_data,
        file_name="dfa_transition_table.csv",
        mime="text/csv",
        use_container_width=True
    )

    # --------------------------------------
    # STEP-BY-STEP CONVERSION
    # --------------------------------------

    st.subheader("Step-by-Step Subset Construction")

    for index, step in enumerate(
        result["steps"],
        start=1
    ):

        current = result["labels"][
            step["current_state"]
        ]

        destination = result["labels"][
            step["next_state"]
        ]

        reached = (
            ", ".join(sorted(step["reached_states"]))
            if step["reached_states"]
            else "Empty set"
        )

        with st.expander(
            f"Step {index}: {current} on input {step['symbol']}"
        ):

            st.write(
                f"Current DFA state: {current}"
            )

            st.write(
                f"Input symbol: {step['symbol']}"
            )

            st.write(
                f"NFA destination states: {reached}"
            )

            st.write(
                f"Resulting DFA state: {destination}"
            )

            if step["is_new"]:
                st.success(
                    "A new DFA state was discovered."
                )
            else:
                st.info(
                    "This DFA state was already discovered."
                )

    # --------------------------------------
    # NFA AND DFA DIAGRAMS
    # --------------------------------------

    st.divider()

    st.header("4. Automata State Diagrams")

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("Original NFA")

        nfa_dot = make_nfa_diagram(
            nfa_data["states"],
            nfa_data["alphabet"],
            nfa_data["transitions"],
            nfa_data["start_state"],
            nfa_data["final_states"]
        )

        st.graphviz_chart(
            nfa_dot,
            use_container_width=True
        )

    with col2:

        st.subheader("Converted DFA")

        dfa_dot = make_dfa_diagram(result)

        st.graphviz_chart(
            dfa_dot,
            use_container_width=True
        )

    st.success(
        "NFA to DFA conversion and visualization completed."
    )


else:

    st.info(
        "Enter your NFA details and click "
        "'Convert NFA to DFA' to see the results."
    )


# ==========================================
# FOOTER
# ==========================================

st.divider()

st.caption(
    "NFA to DFA Conversion Simulator | "
    "CSET302 - Automata Theory and Computability"
)
