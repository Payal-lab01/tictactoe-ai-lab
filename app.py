import random
from pathlib import Path

import pandas as pd
import streamlit as st

from ai.benchmark import run_benchmark
from ai.engine import (
    EMPTY,
    HUMAN,
    AI,
    new_board,
    available_moves,
    make_move,
    winner,
    is_draw,
    best_move,
    best_move_alphabeta,
    medium_move,
    explain_move,
)


# =========================================================
# PAGE CONFIGURATION & STYLING
# =========================================================

st.set_page_config(
    page_title="TicTacToe AI Lab",
    page_icon="🎮",
    layout="wide",
    initial_sidebar_state="expanded",
)

css_path = Path(__file__).parent / "style.css"
if css_path.exists():
    st.markdown(
        f"<style>{css_path.read_text(encoding='utf-8')}</style>",
        unsafe_allow_html=True,
    )


# =========================================================
# SESSION STATE
# =========================================================

defaults = {
    "board": new_board(),
    "game_over": False,
    "message": "Your move. Place X on the board.",
    "difficulty": "Unbeatable",
    "algorithm": "Alpha-Beta Pruning",
    "ai_explanation": "",
    "benchmark_results": None,
    "human_wins": 0,
    "ai_wins": 0,
    "draws": 0,
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# =========================================================
# GAME LOGIC
# =========================================================

def reset_game():
    st.session_state.board = new_board()
    st.session_state.game_over = False
    st.session_state.message = "Your move. Place X on the board."
    st.session_state.ai_explanation = ""


def check_game_over():
    result = winner(st.session_state.board)

    if result == HUMAN:
        st.session_state.message = "You won! Excellent play."
        st.session_state.game_over = True
        st.session_state.human_wins += 1
    elif result == AI:
        st.session_state.message = "The AI wins this round."
        st.session_state.game_over = True
        st.session_state.ai_wins += 1
    elif is_draw(st.session_state.board):
        st.session_state.message = "Draw! Neither side could win."
        st.session_state.game_over = True
        st.session_state.draws += 1


def ai_turn():
    board = st.session_state.board
    moves = available_moves(board)

    if not moves:
        return

    difficulty = st.session_state.difficulty
    algorithm = st.session_state.algorithm

    if difficulty == "Easy":
        move = random.choice(moves)
    elif difficulty == "Medium":
        move = medium_move(board)
    elif algorithm == "Minimax":
        move = best_move(board)
    else:
        move = best_move_alphabeta(board)

    if move is not None:
        # Explain the choice against the board before the AI moves.
        st.session_state.ai_explanation = explain_move(board, move)
        st.session_state.board = make_move(board, move, AI)


def play_human_move(index):
    if st.session_state.game_over:
        return

    board = st.session_state.board
    if board[index] != EMPTY:
        return

    st.session_state.board = make_move(board, index, HUMAN)
    check_game_over()

    if not st.session_state.game_over:
        ai_turn()
        check_game_over()


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:
    st.markdown(
        """
        <div style="padding:10px 0 20px;">
            <div style="font-size:12px;letter-spacing:3px;
                        color:#00e5ff;font-weight:700;">
                AI LAB / 001
            </div>
            <div style="font-size:26px;font-weight:800;
                        color:#f3f0ff;margin-top:5px;">
                CONTROL PANEL
            </div>
            <div style="color:#8592ad;font-size:13px;">
                Configure your opponent
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.selectbox(
        "AI DIFFICULTY",
        ["Easy", "Medium", "Unbeatable"],
        key="difficulty",
    )

    difficulty_descriptions = {
        "Easy": "Random legal moves. A relaxed opponent.",
        "Medium": "Depth-limited Minimax with heuristic evaluation.",
        "Unbeatable": "Minimax with Alpha-Beta Pruning.",
    }
    st.caption(difficulty_descriptions[st.session_state.difficulty])

    st.selectbox(
        "SEARCH ALGORITHM",
        ["Minimax", "Alpha-Beta Pruning"],
        key="algorithm",
        help="Choose the search algorithm used in Unbeatable difficulty. Easy remains random and Medium uses depth-limited Minimax.",
    )
    st.caption(
        "Minimax explores all relevant states; Alpha-Beta Pruning skips branches that cannot improve the decision. Both are optimal in Unbeatable mode."
    )

    st.markdown("---")
    st.markdown("**PLAYER CONFIGURATION**")
    st.markdown("🔹 You — `X`")
    st.markdown("🟣 AI — `O`")

    st.button(
        "↻  NEW GAME",
        on_click=reset_game,
        use_container_width=True,
    )

    st.markdown("---")
    st.caption("Built with Python · Streamlit · Adversarial Search")


# =========================================================
# HEADER
# =========================================================

st.markdown(
    """
    <div style="
        padding:10px 0 24px;
        border-bottom:1px solid rgba(142,117,255,0.2);
        margin-bottom:25px;
    ">
        <div style="
            color:#00e5ff;font-size:12px;letter-spacing:4px;
            font-weight:700;margin-bottom:10px;
        ">STRATEGY ENGINE / LIVE SESSION</div>
        <div style="
            font-size:clamp(32px,5vw,52px);font-weight:900;
            line-height:1.1;letter-spacing:-2px;color:#f5f3ff;
        ">TIC TAC TOE<span style="color:#a678ff;">.</span></div>
        <div style="font-size:15px;color:#9caac5;margin-top:12px;">
            Think ahead. Outsmart the algorithm. Control the board.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

games_played = (
    st.session_state.human_wins
    + st.session_state.ai_wins
    + st.session_state.draws
)

overview1, overview2, overview3 = st.columns(3)
overview1.metric("YOUR WINS", st.session_state.human_wins)
overview2.metric("AI WINS", st.session_state.ai_wins)
overview3.metric("GAMES PLAYED", games_played)


# =========================================================
# GAME BOARD & AI INSIGHTS
# =========================================================

game_col, insight_col = st.columns([1.15, 0.85], gap="large")

with game_col:
    st.markdown("### 🎮 The Arena")
    st.caption(f"CURRENT MODE / {st.session_state.difficulty.upper()}")

    if st.session_state.game_over:
        result = winner(st.session_state.board)
        if result == HUMAN:
            st.success("🏆 VICTORY — You won!")
        elif result == AI:
            st.error("🤖 DEFEAT — The AI won.")
        else:
            st.info("🤝 DRAW — Perfectly matched.")
    else:
        st.info(st.session_state.message)

    board = st.session_state.board

    for row in range(3):
        cells = st.columns(3, gap="small")
        for col in range(3):
            index = row * 3 + col
            value = board[index]

            if value == HUMAN:
                label = "✕"
            elif value == AI:
                label = "○"
            else:
                label = "+"

            clicked = cells[col].button(
                label,
                key=f"cell_{index}",
                use_container_width=True,
                disabled=st.session_state.game_over or value != EMPTY,
            )

            if clicked:
                play_human_move(index)
                st.rerun()

    st.markdown(
        """
        <div style="
            text-align:center;padding:12px 0;color:#8794b0;
            font-size:12px;letter-spacing:1px;
        ">
            YOUR MOVE <span style="color:#00e5ff;">●</span>
            &nbsp; / &nbsp; X = CYAN &nbsp; · &nbsp; O = PURPLE
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.session_state.game_over:
        st.button("↻ PLAY AGAIN", on_click=reset_game, use_container_width=True)


with insight_col:
    st.markdown("### 🧠 AI Intelligence")
    st.caption("DECISION SUPPORT / MOVE ANALYSIS")

    active_algorithm = (
        st.session_state.algorithm
        if st.session_state.difficulty == "Unbeatable"
        else ("Random Moves" if st.session_state.difficulty == "Easy" else "Depth-Limited Minimax")
    )
    st.markdown(
        f"""
        <div style="
            border:1px solid rgba(0,229,255,0.25);
            background:linear-gradient(
                145deg,rgba(13,34,49,0.85),rgba(22,17,43,0.85)
            );
            border-radius:16px;padding:18px;margin:10px 0 16px;
        ">
            <div style="
                color:#00e5ff;font-size:11px;font-weight:700;
                letter-spacing:2px;
            ">ACTIVE ALGORITHM</div>
            <div style="
                font-size:20px;color:#f4f2ff;font-weight:800;
                margin:8px 0;
            ">{active_algorithm}</div>
            <div style="color:#9ba9c5;font-size:13px;">
                Evaluating moves, anticipating your response,
                and choosing a strategy.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("**LAST MOVE EXPLANATION**")
    if st.session_state.ai_explanation:
        st.info(st.session_state.ai_explanation)
    else:
        st.caption("The AI's reasoning will appear here after it makes a move.")

    st.markdown("**HOW IT THINKS**")
    st.markdown(
        """
        - **Easy:** Random legal move.
        - **Medium:** Limited-depth Minimax with a heuristic.
        - **Unbeatable + Minimax:** Full Minimax search.
        - **Unbeatable + Alpha-Beta Pruning:** Full search with branch pruning.
        """
    )


# =========================================================
# PERFORMANCE ANALYTICS DASHBOARD
# =========================================================

st.markdown("---")
st.caption("A N A L Y T I C S  C E N T E R  /  0 0 2")
st.title("Algorithm Performance.")
st.markdown(
    "Explore search efficiency, computational cost, "
    "and the impact of Alpha-Beta Pruning."
)

control_left, control_right = st.columns([2, 1])

with control_left:
    st.caption(
        "Test configuration: empty board · same scoring rules · "
        "runtime varies between runs"
    )

with control_right:
    if st.button(
        "▶ RUN BENCHMARK",
        key="run_analytics_benchmark",
        use_container_width=True,
    ):
        with st.spinner("Measuring algorithm performance..."):
            st.session_state.benchmark_results = run_benchmark()

results = st.session_state.benchmark_results

if results is None:
    st.markdown(
        """
        <div style="
            background:linear-gradient(
                135deg,rgba(30,20,55,.8),rgba(10,27,42,.8)
            );
            border:1px dashed rgba(0,229,255,.35);
            border-radius:18px;padding:35px 20px;text-align:center;
        ">
            <div style="font-size:34px;color:#a678ff;">⌁</div>
            <div style="font-size:20px;font-weight:800;color:#f4f2ff;margin-top:8px;">
                No benchmark data yet
            </div>
            <div style="color:#9caac5;font-size:13px;margin-top:8px;">
                Run a benchmark to populate the analytics dashboard.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
else:
    minimax_data = results["Minimax"]
    alphabeta_data = results["Alpha-Beta"]

    m_nodes = minimax_data["nodes"]
    a_nodes = alphabeta_data["nodes"]
    m_time = minimax_data["time_ms"]
    a_time = alphabeta_data["time_ms"]

    nodes_saved = m_nodes - a_nodes
    node_reduction = (nodes_saved / m_nodes) * 100 if m_nodes > 0 else 0
    speedup = m_time / a_time if a_time > 0 else 0
    time_saved = m_time - a_time

    st.markdown("### Performance at a glance")
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)

    kpi1.metric(
        "NODE REDUCTION",
        f"{node_reduction:.2f}%",
        help="Percentage of Minimax nodes not explored by Alpha-Beta.",
    )
    kpi2.metric(
        "SEARCH SPEEDUP",
        f"{speedup:.2f}×",
        help="Minimax runtime divided by Alpha-Beta runtime.",
    )
    kpi3.metric(
        "NODES SAVED",
        f"{nodes_saved:,}",
        help="Difference in node counts for this benchmark.",
    )
    kpi4.metric(
        "TIME SAVED",
        f"{time_saved:.1f} ms",
        help="Difference between the measured runtimes.",
    )

    st.markdown("")
    efficiency_col, summary_col = st.columns(2, gap="large")

    with efficiency_col:
        st.markdown("#### Search efficiency")
        st.metric("Search nodes eliminated", f"{node_reduction:.2f}%")
        st.progress(
            min(max(node_reduction / 100, 0.0), 1.0),
            text="Percentage of nodes eliminated",
        )

    with summary_col:
        st.markdown("#### Benchmark validation")
        same_score = minimax_data["score"] == alphabeta_data["score"]

        if same_score:
            st.success(
                f"Both algorithms returned score {minimax_data['score']}."
            )
        else:
            st.warning(
                "The returned scores differ. Investigate the implementations."
            )

        st.caption(
            "Matching scores on this board support consistency for this test, "
            "but do not prove correctness for every possible position."
        )

    st.markdown("---")
    st.markdown("### Algorithm comparison")
    chart_nodes, chart_time = st.columns(2, gap="large")

    with chart_nodes:
        st.markdown("#### Nodes explored")
        node_df = pd.DataFrame(
            {"Nodes": [m_nodes, a_nodes]},
            index=["Minimax", "Alpha-Beta"],
        )
        st.bar_chart(node_df, height=250)
        st.caption("Fewer explored nodes indicate less search work in this run.")

    with chart_time:
        st.markdown("#### Execution time")
        time_df = pd.DataFrame(
            {"Time (ms)": [m_time, a_time]},
            index=["Minimax", "Alpha-Beta"],
        )
        st.bar_chart(time_df, height=250)
        st.caption("Wall-clock runtime can fluctuate between runs.")

    st.markdown("---")
    st.markdown("### Detailed results")

    detailed_df = pd.DataFrame(
        {
            "Algorithm": ["Minimax", "Alpha-Beta"],
            "Score": [minimax_data["score"], alphabeta_data["score"]],
            "Nodes explored": [m_nodes, a_nodes],
            "Execution time (ms)": [round(m_time, 3), round(a_time, 3)],
        }
    )

    st.dataframe(
        detailed_df,
        hide_index=True,
        use_container_width=True,
    )

    with st.expander("How to interpret these results"):
        st.markdown(
            """
            **Minimax** searches possible game states while assuming both
            players choose moves optimally.

            **Alpha-Beta Pruning** uses alpha and beta bounds to skip branches
            that cannot change the final Minimax decision.

            **Node reduction**

            `(Minimax nodes - Alpha-Beta nodes) / Minimax nodes × 100`

            **Speedup**

            `Minimax runtime / Alpha-Beta runtime`

            These results describe this benchmark implementation on the empty
            board. They are empirical measurements, not universal guarantees.
            """
        )

    st.caption(
        "Results persist during reruns in the current Streamlit session. "
        "Running a new benchmark replaces the previous measurements."
    )


# =========================================================
# FOOTER
# =========================================================

st.markdown("---")
st.markdown(
    """
    <div style="
        text-align:center;padding:10px 0;color:#77839f;font-size:12px;
    ">
        TIC TAC TOE AI LAB &nbsp;·&nbsp;
        MINIMAX + ALPHA-BETA PRUNING &nbsp;·&nbsp;
        BUILT WITH PYTHON
    </div>
    """,
    unsafe_allow_html=True,
)
