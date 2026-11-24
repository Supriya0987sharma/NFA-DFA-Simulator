# NFA to DFA Conversion Simulator

An interactive web-based simulator that converts a Non-Deterministic Finite Automaton (NFA) into an equivalent Deterministic Finite Automaton (DFA) using the **Subset Construction Algorithm**.

## Overview

This project demonstrates how an NFA can be converted into a DFA through an interactive Streamlit application. Users can define automata, enter transitions, perform conversion, and visualize the resulting state diagrams.

## Features

- Define NFA states, alphabet, initial state, and final states.
- Enter transitions, including epsilon transitions.
- Convert NFA into an equivalent DFA using subset construction.
- Calculate epsilon closures.
- Generate DFA states and transition tables.
- Handle dead states during conversion.
- Visualize original NFA and converted DFA diagrams.
- Display step-by-step subset construction.
- Download the DFA transition table as a CSV file.
- Validate invalid inputs and automata definitions.

## Technologies Used

- Python
- Streamlit
- Pandas
- Graphviz
- Pytest

## Project Structure

```text
NFA-DFA-Simulator/
│
├── app.py
├── engine.py
├── visualizer.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── docs/
├── screenshots/
└── tests/
    └── test_engine.py
```

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/Supriya0987sharma/NFA-DFA-Simulator.git
```

### 2. Navigate to the project directory

```bash
cd NFA-DFA-Simulator
```

### 3. Create a virtual environment

```bash
python -m venv .venv
```

### 4. Activate the virtual environment

**Windows PowerShell:**

```powershell
.venv\Scripts\Activate.ps1
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

## Run the Application

Start the Streamlit application using:

```bash
python -m streamlit run app.py
```

The application will open in your default web browser.

## Run Tests

Execute the automated test suite using:

```bash
python -m pytest tests/test_engine.py -v
```

## Algorithm

The project implements the **Subset Construction Algorithm**, which converts an NFA into an equivalent DFA.

The conversion involves:

1. Finding the epsilon closure of the initial NFA state.
2. Creating DFA states from sets of NFA states.
3. Calculating transitions for each input symbol.
4. Identifying accepting DFA states.
5. Handling missing transitions using a dead state when required.

## Testing

The project includes automated test cases covering:

- Basic NFA to DFA conversion
- Epsilon transitions
- Dead-state handling
- Invalid start-state validation
- Invalid final-state validation

## Learning Outcomes

- Understanding NFA and DFA concepts.
- Implementing the subset construction algorithm.
- Working with epsilon transitions and epsilon closures.
- Understanding automata visualization.
- Applying Python testing practices.

## License

This project is developed for academic and educational purposes as part of Automata Theory coursework.