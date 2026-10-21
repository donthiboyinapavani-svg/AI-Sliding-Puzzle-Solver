
import streamlit as st
import pandas as pd
import random
import time

st.set_page_config(
    page_title="AI Sliding-Puzzle Solver",
    page_icon="🧩",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------- COLORFUL ACADEMIC THEME ----------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #f0f7ff, #f7f2ff, #fff7ed);
    color: #172033;
}
[data-testid="stHeader"] {
    background: transparent;
}
.block-container {
    max-width: 1300px;
    padding-top: 1.5rem;
    padding-bottom: 3rem;
}
.hero {
    background: linear-gradient(120deg, #312e81, #2563eb, #0891b2);
    color: white;
    padding: 35px;
    border-radius: 22px;
    margin-bottom: 25px;
    box-shadow: 0 10px 30px #312e8130;
}
.hero h1 {
    color: white;
    font-size: 36px;
}
.hero p {
    color: #e0f2fe;
    font-size: 16px;
}
.section-card {
    background: rgba(255,255,255,0.95);
    padding: 22px;
    border: 1px solid #dbeafe;
    border-radius: 17px;
    margin-bottom: 16px;
    box-shadow: 0 5px 18px #33415510;
}
.tile {
    background: linear-gradient(145deg, #ffffff, #dbeafe);
    border: 2px solid #93c5fd;
    border-radius: 13px;
    padding: 16px 4px;
    text-align: center;
    font-size: 25px;
    font-weight: 800;
    color: #1d4ed8;
    margin-bottom: 5px;
}
.blank-tile {
    background: #e2e8f0;
    border: 2px dashed #94a3b8;
    border-radius: 13px;
    padding: 16px 4px;
    text-align: center;
    font-size: 25px;
    color: #64748b;
    margin-bottom: 5px;
}
.small-note {
    color: #64748b;
    font-size: 13px;
}
h1, h2, h3 {
    color: #1e3a8a;
}
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #eef2ff, #ecfeff);
}
.stButton > button {
    border-radius: 11px;
    border: 1px solid #c7d2fe;
    font-weight: 600;
    transition: 0.2s;
}
.stButton > button:hover {
    border-color: #6366f1;
    color: #4338ca;
}
div[data-testid="stMetric"] {
    background: white;
    border: 1px solid #dbeafe;
    border-radius: 14px;
    padding: 15px;
}
div[data-testid="stAlert"] {
    border-radius: 12px;
}
</style>
""", unsafe_allow_html=True)


# ---------- INTERACTIVE PUZZLE FUNCTIONS ----------
def goal_state(size):
    return list(range(1, size * size)) + [0]


def move_tile(index, size):
    board = st.session_state.board
    blank = board.index(0)

    row, col = divmod(index, size)
    blank_row, blank_col = divmod(blank, size)

    if abs(row - blank_row) + abs(col - blank_col) == 1:
        board[index], board[blank] = board[blank], board[index]
        st.session_state.move_count += 1


def shuffle_puzzle(size):
    board = goal_state(size)
    blank = board.index(0)
    previous_blank = -1

    # Shuffle using valid moves, so the puzzle remains solvable.
    for _ in range(100 if size == 3 else 180):
        row, col = divmod(blank, size)
        neighbours = []

        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = row + dr, col + dc

            if 0 <= nr < size and 0 <= nc < size:
                new_blank = nr * size + nc
                if new_blank != previous_blank:
                    neighbours.append(new_blank)

        if not neighbours:
            continue

        next_blank = random.choice(neighbours)
        board[blank], board[next_blank] = (
            board[next_blank], board[blank]
        )

        previous_blank = blank
        blank = next_blank

    st.session_state.board = board
    st.session_state.move_count = 0


def reset_puzzle(size):
    st.session_state.board = goal_state(size)
    st.session_state.move_count = 0


# ---------- SIDEBAR ----------
with st.sidebar:
    st.title("🧩 Project Controls")
    st.caption("AI Mini-Capstone | Searching Techniques")
    st.divider()

    puzzle_type = st.selectbox(
        "Puzzle Configuration",
        ["8-Puzzle (3 × 3)", "15-Puzzle (4 × 4)"]
    )

    algorithm = st.selectbox(
        "Search Algorithm",
        ["Breadth-First Search (BFS)", "A* Search"]
    )

    heuristic = st.selectbox(
        "A* Heuristic",
        ["Manhattan Distance", "Misplaced Tiles"]
    )

    st.info(
        "The puzzle controls work in the frontend. "
        "AI search execution will be connected by the backend."
    )

    st.divider()
    st.caption("Project team: Add all four team members' names here.")


# ---------- INITIALIZE BOARD ----------
size = 3 if puzzle_type.startswith("8") else 4

if (
    "board" not in st.session_state
    or st.session_state.get("board_size") != size
):
    st.session_state.board = goal_state(size)
    st.session_state.board_size = size
    st.session_state.move_count = 0

board = st.session_state.board
is_solved = board == goal_state(size)


# ---------- HEADER ----------
st.markdown("""
<div class="hero">
    <h1>🧩 AI Sliding-Puzzle Solver</h1>
    <p><b>Uninformed vs Informed Search with Heuristic Analysis</b></p>
    <p>
        An interactive academic demonstration of state-space search,
        heuristic functions, and AI problem-solving.
    </p>
</div>
""", unsafe_allow_html=True)


# ---------- PROJECT OVERVIEW ----------
st.subheader("📘 Project Overview")

a, b, c = st.columns(3)

with a:
    st.markdown("""
    <div class="section-card">
        <h4>🎯 Problem Statement</h4>
        <p>Find a sequence of valid tile moves that transforms
        a sliding puzzle into its goal configuration.</p>
    </div>
    """, unsafe_allow_html=True)

with b:
    st.markdown("""
    <div class="section-card">
        <h4>🧠 AI Concepts</h4>
        <p>State-space search, uninformed search, informed search,
        and heuristic evaluation.</p>
    </div>
    """, unsafe_allow_html=True)

with c:
    st.markdown("""
    <div class="section-card">
        <h4>📊 Evaluation</h4>
        <p>Compare solution length, states explored, execution time,
        and heuristic effectiveness.</p>
    </div>
    """, unsafe_allow_html=True)


# ---------- PUZZLE PLAYGROUND ----------
st.subheader("🎮 Interactive Puzzle Playground")

left, right = st.columns([1.1, 1])

with left:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown("#### 🧩 Puzzle Board")

    st.caption(
        "Click a tile next to the empty space to move it."
    )

    for r in range(size):
        cells = st.columns(size)

        for col in range(size):
            index = r * size + col
            value = st.session_state.board[index]

            with cells[col]:
                if value == 0:
                    st.markdown(
                        '<div class="blank-tile">□</div>',
                        unsafe_allow_html=True
                    )
                else:
                    st.button(
                        str(value),
                        key=f"tile_{size}_{index}",
                        use_container_width=True,
                        on_click=move_tile,
                        args=(index, size)
                    )

    if is_solved:
        st.success("🎉 Puzzle is in its goal configuration!")

    st.markdown(f"**Moves made:** {st.session_state.move_count}")

    btn1, btn2 = st.columns(2)

    with btn1:
        st.button(
            "🔀 Shuffle Puzzle",
            use_container_width=True,
            on_click=shuffle_puzzle,
            args=(size,),
            key="shuffle"
        )

    with btn2:
        st.button(
            "↻ Reset Puzzle",
            use_container_width=True,
            on_click=reset_puzzle,
            args=(size,),
            key="reset"
        )

    st.caption(
        "Shuffle generates a solvable board using legal tile moves."
    )
    st.markdown('</div>', unsafe_allow_html=True)


with right:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown("#### 🤖 AI Solver")

    st.write("**Selected algorithm**")
    st.info(algorithm)

    st.write("**Selected puzzle**")
    st.info(puzzle_type)

    if algorithm == "A* Search":
        st.write("**Selected heuristic**")
        st.info(heuristic)
    else:
        st.caption("BFS does not require a heuristic function.")

    st.button(
        "▶ Solve Puzzle",
        disabled=True,
        use_container_width=True,
        key="solve"
    )

    st.caption(
        "AI solving and solution animation will be enabled "
        "after backend integration."
    )
    st.markdown('</div>', unsafe_allow_html=True)


# ---------- ALGORITHM EXPLANATION ----------
st.subheader("📚 AI Algorithms")

tab1, tab2 = st.tabs([
    "🔎 BFS — Uninformed Search",
    "⭐ A* — Informed Search"
])

with tab1:
    st.markdown("""
    <div class="section-card">
        <h4>Breadth-First Search (BFS)</h4>
        <p><b>Approach:</b> Explores states level by level,
        expanding states in order of depth.</p>
        <p><b>Evaluation:</b> Uses the path depth, without a heuristic
        estimate of the distance to the goal.</p>
        <p><b>Completeness:</b> Complete for a finite branching factor.</p>
        <p><b>Optimality:</b> Finds a shortest solution when all moves
        have equal cost.</p>
        <p><b>Consideration:</b> Can require substantial memory because
        it stores many states.</p>
    </div>
    """, unsafe_allow_html=True)

with tab2:
    st.markdown("""
    <div class="section-card">
        <h4>A* Search</h4>
        <p><b>Evaluation function:</b> f(n) = g(n) + h(n)</p>
        <p><b>g(n):</b> Cost of the path from the start state.</p>
        <p><b>h(n):</b> Estimated remaining cost to the goal.</p>
        <p><b>Manhattan Distance:</b> Sum of each numbered tile's
        horizontal and vertical distance from its goal position.</p>
        <p><b>Misplaced Tiles:</b> Number of numbered tiles that
        are not in their goal positions.</p>
        <p><b>Consideration:</b> Performance depends on the heuristic
        and the states explored.</p>
    </div>
    """, unsafe_allow_html=True)


# ---------- METHODOLOGY ----------
st.subheader("🛠️ Proposed Methodology")

steps = [
    ("1. Initial State", "Represent the puzzle as a state."),
    ("2. Generate Successors", "Move a neighboring tile into the blank."),
    ("3. Search", "Explore states using BFS or A*."),
    ("4. Goal Test", "Check whether the target configuration is reached."),
    ("5. Evaluate", "Record solution length, states explored, and runtime.")
]

for title, description in steps:
    st.markdown(f"**{title}**  \n{description}")


# ---------- RESULTS ----------
st.subheader("📈 Experimental Results")

st.caption(
    "No AI algorithm has been executed by this frontend. "
    "The table below is a template for backend experiments."
)

results = pd.DataFrame({
    "Metric": [
        "Solution length (moves)",
        "States explored",
        "Execution time",
        "Solution found"
    ],
    "BFS": ["Pending", "Pending", "Pending", "Pending"],
    "A*": ["Pending", "Pending", "Pending", "Pending"]
})

st.dataframe(
    results,
    use_container_width=True,
    hide_index=True
)

st.warning(
    "Populate this table with actual experimental results after "
    "running and testing both algorithms."
)


# ---------- APPLICATIONS & LIMITATIONS ----------
st.subheader("🌍 Applications and Limitations")

x, y = st.columns(2)

with x:
    st.markdown("""
    <div class="section-card">
        <h4>🌍 Applications</h4>
        <ul>
            <li>AI search and planning demonstrations</li>
            <li>State-space problem solving</li>
            <li>Heuristic algorithm education</li>
            <li>Decision-making and path-search concepts</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with y:
    st.markdown("""
    <div class="section-card">
        <h4>⚠️ Limitations</h4>
        <ul>
            <li>Search can become expensive for large state spaces.</li>
            <li>BFS can use substantial memory.</li>
            <li>A* performance depends on its heuristic.</li>
            <li>Results depend on the initial puzzle state.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)


# ---------- CONCLUSION ----------
st.subheader("🎓 Conclusion and Future Scope")

st.write(
    "This project demonstrates how uninformed and informed search "
    "techniques can solve sliding puzzles. Future improvements include "
    "solution animation, additional heuristics, and automated "
    "performance comparison."
)

st.divider()
st.caption(
    "AI Mini-Capstone | Sliding-Puzzle Solver | Frontend Prototype"
)
