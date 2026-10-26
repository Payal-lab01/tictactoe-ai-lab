# TicTacToe AI Lab

An interactive Tic-Tac-Toe game built with Python and Streamlit that demonstrates adversarial search, Minimax decision-making, Alpha-Beta Pruning, and algorithm performance analysis.

## 🚀 Live Demo

**Play Tic-Tac-Toe AI Lab here:** [Launch the App](https://tictactoe-ai-lab-mwke7xnmgdnebaipguanjp.streamlit.app/)

Try different difficulty levels and explore how Minimax and Alpha-Beta Pruning power the AI.

## Features

- **Three difficulty levels:** Easy, Medium, and Unbeatable.
- **Minimax:** Searches possible future game states to select optimal moves.
- **Alpha-Beta Pruning:** Reduces unnecessary search by pruning branches that cannot affect the final decision.
- **AI explanations:** Displays a strategic explanation for the selected move.
- **Performance dashboard:** Compares nodes explored, execution time, and search efficiency.
- **Automated tests:** Validates game logic, AI decisions, and algorithm performance.

## Tech Stack

- Python
- Streamlit
- Pandas
- Minimax
- Alpha-Beta Pruning

## Project Structure

```text
tic-tac-toe/
├── ai/
│   ├── __init__.py
│   ├── engine.py
│   └── benchmark.py
├── app.py
├── test_engine.py
├── test_minimax.py
├── test_benchmark.py
├── test_benchmark_dashboard.py
├── requirements.txt
└── README.md
```

## Algorithms

### 1. Minimax

Minimax explores possible game states and chooses moves that maximize the AI's outcome while assuming the human opponent also plays optimally.

### 2. Alpha-Beta Pruning

Alpha-Beta Pruning improves Minimax by skipping branches that cannot change the final decision. It produces the same optimal score while potentially evaluating far fewer nodes.

### 3. Difficulty Levels

- **Easy:** Chooses a random legal move.
- **Medium:** Uses depth-limited Minimax with a heuristic evaluation.
- **Unbeatable:** Uses Minimax with Alpha-Beta Pruning.

## Performance Results

Measured on the empty starting board in one benchmark run:

| Metric | Minimax | Alpha-Beta |
|---|---:|---:|
| Nodes explored | 549,946 | 20,866 |
| Execution time | 2,973.170 ms | 121.400 ms |
| Final score | 0 | 0 |

**Observed node reduction: 96.21%**

Alpha-Beta Pruning explored approximately 26.4 times fewer nodes and was approximately 24.5 times faster in this run. Actual execution times vary by machine and run.

Both algorithms returned a score of `0`, representing a draw under optimal play.

## Installation and Setup

### Prerequisites

- Python 3.9 or a compatible newer version
- pip

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd tic-tac-toe
```

Replace `YOUR_GITHUB_REPOSITORY_URL` with your actual repository URL.

### 2. Create a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

Ensure `requirements.txt` includes the dependencies used by the project, including Streamlit and Pandas.

### 4. Run the application

```bash
streamlit run app.py
```

Open the local URL shown in the terminal.

## Testing

Run the available test scripts:

```bash
python test_engine.py
python test_minimax.py
python test_benchmark.py
python test_benchmark_dashboard.py
```

## Learning Outcomes

This project demonstrates:

- Adversarial search in two-player games.
- Game-state evaluation and terminal-state scoring.
- Optimization using Alpha-Beta Pruning.
- Heuristic evaluation for depth-limited search.
- Empirical algorithm comparison using node counts and runtime.
- Interactive application development using Streamlit.

## Future Improvements

- Add a visual search-tree explorer.
- Display the winning line on the board.
- Improve the explanation system to identify forced wins and defensive moves.
- Add difficulty and performance comparisons across different board states.
- Deploy the application online.

## Author

Developed as an Artificial Intelligence and Soft Computing project.
