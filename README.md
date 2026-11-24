# SwiftRoute AI — Intelligent Parcel Prioritization, Packing Optimization and Delivery Route Planning System

**Design and Analysis of Algorithms (ETCCDA302) — Capstone Project**  
**Department of Computer Science & Engineering, K.R. Mangalam University**  
**Submitted by:** Arth Rana | **Roll No.:** 2501350005 | **Section:** B.Tech CSE (FSD-A)

---

## 1. Project Introduction

In modern logistics and e-commerce supply chains, courier distribution centers receive thousands of packages daily with distinct delivery deadlines, client priority levels, physical parcel weights, and destination coordinates. Logistics firms face four compounding algorithmic challenges before dispatching delivery vehicles:

1. **Prioritization**: Which parcels must be serviced first based on urgency and deadline?
2. **Packing Optimization**: Given a delivery vehicle with a rigid payload capacity, which subset of prioritized parcels yields maximum profit without exceeding weight limits?
3. **Shortest Path Routing**: What is the shortest road network distance from the central logistics depot to every designated customer drop-off node?
4. **Tour Scheduling (TSP)**: In what sequence should the delivery van visit customer drop-offs and return to the depot while minimizing cumulative driving distance and fuel consumption?

The **SwiftRoute AI** is an integrated software system that bridges foundational Computer Science algorithms into an operational, automated decision-support pipeline.

---

## 2. Problem Statement

Given:
- A set of $n$ parcels, where each parcel $p_i$ is defined by $\langle \text{ID}, \text{Customer}, \text{Location}, \text{Weight } w_i, \text{Priority } r_i, \text{Deadline } d_i, \text{Value } v_i \rangle$.
- A delivery vehicle with maximum gross payload capacity $W$.
- A city road network represented as a weighted undirected graph $G = (V, E)$, where $V$ represents geographic junctions / delivery locations and $E$ represents bidirectional roads weighted by driving distance in kilometers.
- A designated warehouse depot $s \in V$.

The objective is to:
1. Sort and rank all parcels deterministically by urgency.
2. Select an optimal subset of parcels $S \subseteq \{1, \dots, n\}$ maximizing total revenue $\sum_{i \in S} v_i$ subject to $\sum_{i \in S} w_i \le W$.
3. Compute the shortest driving routes from depot $s$ to all unique destinations $V_{\text{dest}} = \{ \text{Location}(p_i) \mid i \in S \}$.
4. Construct a closed-loop delivery tour $T = \langle s, v_{\pi(1)}, v_{\pi(2)}, \dots, v_{\pi(k)}, s \rangle$ visiting all locations in $V_{\text{dest}}$ with minimum total driving distance.

---

## 3. Objectives

- **Algorithmic Rigor**: Manually implement all foundational algorithms from first principles (no built-in sorting, no NetworkX shortest path functions, no third-party TSP solvers).
- **End-to-End Pipeline Integration**: Connect Merge Sort, 0/1 Knapsack Dynamic Programming, Dijkstra's Algorithm, and Nearest Neighbor TSP into a unified workflow.
- **Empirical Complexity Analysis**: Benchmark and record actual execution times using `time.perf_counter()` across Small ($n=10$), Medium ($n=100$), and Large ($n=500$) datasets to validate theoretical asymptotic bounds.
- **Accessible User Interfaces**: Deliver an interactive Streamlit Web UI alongside a full-featured Command-Line Interface (CLI).
- **Academic Readiness**: Provide complete unit tests, architecture documentation, and viva defense preparation materials.

---

## 4. Technologies Used

- **Language**: Python 3.10+ (Standard Python libraries: `heapq`, `json`, `dataclasses`, `time`, `typing`, `unittest`).
- **Data Visualization & Plotting**: Matplotlib (`matplotlib.pyplot`) for route maps and empirical runtime curves.
- **Graph Layout Rendering**: NetworkX (used strictly for layout rendering and node plotting; **never** for Dijkstra or TSP calculation).
- **Interactive Web UI**: Streamlit.
- **Data Handling**: Pandas (used only for tabular UI presentation and CSV export).

---

## 5. Project Architecture

```
CAPSTONE/
├── app.py                     # Interactive Streamlit Web Application
├── main.py                    # CLI application, interactive menu & automated demo runner
├── requirements.txt           # Python dependency specifications
├── README.md                  # Comprehensive project documentation
├── CAPSTONE_REPORT.md         # Detailed 5-phase capstone project report
├── VIVA_QUESTIONS.md          # 30+ Viva questions and beginner-friendly answers
├── .gitignore                 # Standard Python gitignore
│
├── algorithms/                # Algorithmic core (all manually implemented)
│   ├── __init__.py
│   ├── sorting.py             # Manual Merge Sort (Priority desc, Deadline asc, ID asc)
│   ├── knapsack.py            # Manual 0/1 Knapsack DP with full 2D matrix backtracking
│   ├── dijkstra.py            # Manual Dijkstra Shortest Path with heapq (min-heap)
│   ├── tsp.py                 # Manual Nearest Neighbor TSP Approximation
│   └── performance.py         # Empirical benchmarking suite (time.perf_counter)
│
├── models/                    # Domain data models
│   ├── __init__.py
│   ├── parcel.py              # Parcel dataclass, validation & serialization
│   └── delivery_graph.py      # Adjacency list DeliveryGraph data structure
│
├── data/                      # Persistent JSON sample datasets
│   ├── parcels.json           # 15 realistic parcels with varied weights & values
│   └── graph.json             # 11-node Gurugram NCR delivery network graph
│
├── visualization/             # Plotting and rendering engines
│   ├── __init__.py
│   ├── graph_visualizer.py    # Matplotlib delivery tour and graph visualizer
│   └── performance_charts.py  # Runtime bar charts, line plots & knapsack scaling
│
├── tests/                     # Automated unit and integration tests
│   ├── __init__.py
│   ├── test_sorting.py        # Merge sort edge cases, stability & tiebreakers
│   ├── test_knapsack.py       # 0/1 Knapsack DP capacity limits & edge cases
│   ├── test_dijkstra.py       # Shortest path verification & disconnected nodes
│   ├── test_tsp.py            # Nearest Neighbor routing & loop closure
│   └── test_integration.py     # End-to-end multi-algorithm pipeline tests
│
├── reports/                   # Benchmarks, CSV outputs & generated charts
│   ├── performance_results.csv
│   ├── performance_runtime_comparison.png
│   ├── performance_scaling_curves.png
│   ├── knapsack_capacity_impact.png
│   └── delivery_route_visualization.png
│
└── screenshots/               # Stored visualization artifacts for report submission
    ├── delivery_route_visualization.png
    ├── knapsack_capacity_impact.png
    ├── performance_runtime_comparison.png
    └── performance_scaling_curves.png
```

---

## 6. Algorithm Explanations

### A. Sorting Algorithm: Manual Merge Sort
- **File**: `algorithms/sorting.py`
- **Paradigm**: Divide-and-Conquer.
- **Logic**:
  1. Recursively divide the parcel list into two equal halves until sublists of size $\le 1$ are reached.
  2. Merge the sorted sublists using a multi-criteria comparator `comes_before(a, b)`:
     - **Criterion 1**: Higher Priority First ($a.\text{priority} > b.\text{priority}$).
     - **Criterion 2**: Earlier Deadline First ($a.\text{deadline} < b.\text{deadline}$).
     - **Criterion 3**: Lexicographical Parcel ID tie-breaker ($a.\text{id} < b.\text{id}$).
- **Time Complexity**: $O(n \log n)$ in Best, Average, and Worst cases.
- **Space Complexity**: $O(n)$ auxiliary memory for merging.
- **Stability**: Preserved; guarantees deterministic ordering.

### B. Dynamic Programming: 0/1 Knapsack
- **File**: `algorithms/knapsack.py`
- **Paradigm**: Dynamic Programming (Bottom-Up Tabulation).
- **Logic**:
  1. Construct a 2D DP matrix `dp` of size $(n + 1) \times (W + 1)$ where `dp[i][w]` represents the maximum revenue achievable from the first $i$ prioritized parcels subject to vehicle capacity $w$.
  2. Base cases: `dp[0][w] = 0` and `dp[i][0] = 0`.
  3. Recurrence relation:
     $$\text{dp}[i][w] = \begin{cases} \text{dp}[i-1][w] & \text{if } w_i > w \\ \max(\text{dp}[i-1][w], \text{dp}[i-1][w - w_i] + v_i) & \text{if } w_i \le w \end{cases}$$
  4. Backtracking: Trace back from cell `dp[n][W]` to cell `dp[0][0]` to extract the exact subset of parcels packed.
- **Time Complexity**: $O(n \cdot W)$ (Pseudo-polynomial).
- **Space Complexity**: $O(n \cdot W)$ for table storage.

### C. Graph Representation: Adjacency List
- **File**: `models/delivery_graph.py`
- **Structure**: Dictionary mapping node names to lists of tuples `(neighbor, distance_km)`.
- **Properties**: Undirected, weighted by realistic road distances.
- **Space Complexity**: $O(V + E)$, strictly more space-efficient than an adjacency matrix $O(V^2)$ for sparse road networks ($E \ll V^2$).

### D. Shortest Path Algorithm: Manual Dijkstra
- **File**: `algorithms/dijkstra.py`
- **Paradigm**: Greedy Algorithm with Min-Heap.
- **Logic**:
  1. Initialize distance to source as $0$ and all other nodes as $\infty$.
  2. Push `(0.0, source)` into a Python `heapq` priority queue.
  3. Pop node $u$ with minimum tentative distance.
  4. Relax all neighbors $v$ of $u$: if $\text{dist}[u] + \text{weight}(u, v) < \text{dist}[v]$, update $\text{dist}[v]$ and record $u$ as predecessor of $v$.
  5. Backtrack predecessor pointers to reconstruct the exact road path.
- **Time Complexity**: $O((V + E) \log V)$ using binary min-heap.
- **Space Complexity**: $O(V + E)$ for distance table, predecessors, and heap.

### E. Tour Optimization: Nearest Neighbor TSP Approximation
- **File**: `algorithms/tsp.py`
- **Paradigm**: Greedy Heuristic.
- **Logic**:
  1. Start delivery vehicle at `Central Warehouse`.
  2. At current node $u$, find the unvisited destination $v$ that minimizes the Dijkstra shortest-path distance $\text{dist}(u, v)$.
  3. Traverse to $v$, append to itinerary, mark $v$ as visited.
  4. Repeat until all selected delivery locations are visited.
  5. Close the tour by calculating the shortest path from the final delivery stop back to `Central Warehouse`.
- **Heuristic Disclaimer**: TSP is NP-Hard. Nearest Neighbor executes in $O(k^2)$ time where $k$ is the number of stops. While it yields fast, practical delivery tours, it does not guarantee the global optimal tour because early greedy choices can force a long final return leg.

---

## 7. Time and Space Complexity Summary

| Module | Algorithm | Technique | Time Complexity | Auxiliary Space | Key Invariant / Property |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Parcel Prioritization** | Merge Sort | Divide & Conquer | $O(n \log n)$ | $O(n)$ | Stable; strictly deterministic tie-breaking |
| **Vehicle Packing** | 0/1 Knapsack | Dynamic Programming | $O(n \cdot W)$ | $O(n \cdot W)$ | Optimal substructure; full table backtracking |
| **Road Network** | Adjacency List | Graph Structure | $O(V + E)$ | $O(V + E)$ | Memory-efficient representation of sparse road maps |
| **Shortest Road Paths** | Dijkstra | Greedy (Binary Heap) | $O((V + E) \log V)$ | $O(V + E)$ | Non-negative edge weights; triangular relaxation |
| **Delivery Tour** | Nearest Neighbor | Greedy TSP Heuristic | $O(k^2 + k(V+E)\log V)$ | $O(V + E)$ | Fast polynomial approximation for NP-Hard routing |

---

## 8. Empirical Performance Analysis

Performance was evaluated using Python's high-resolution `time.perf_counter()` on actual machine hardware.

### A. Genuine Execution Measurements Table

| Dataset Size | Algorithm | Elements Processed | Execution Time (ms) | Theoretical Complexity |
| :--- | :--- | :--- | :--- | :--- |
| **Small (10)** | Merge Sort | $n=10$ | **0.0149 ms** | $O(n \log n)$ |
| **Small (10)** | 0/1 Knapsack DP | $n=10, W=50$ | **0.1316 ms** | $O(n \cdot W)$ |
| **Small (10)** | Dijkstra (Heap) | $V=10, E=20$ | **0.0186 ms** | $O((V + E) \log V)$ |
| **Small (10)** | Nearest Neighbor TSP | Stops $k=5$ | **0.1767 ms** | $O(k^2)$ |
| **Medium (100)** | Merge Sort | $n=100$ | **0.2113 ms** | $O(n \log n)$ |
| **Medium (100)** | 0/1 Knapsack DP | $n=100, W=200$ | **7.4802 ms** | $O(n \cdot W)$ |
| **Medium (100)** | Dijkstra (Heap) | $V=30, E=91$ | **0.1442 ms** | $O((V + E) \log V)$ |
| **Medium (100)** | Nearest Neighbor TSP | Stops $k=15$ | **1.5944 ms** | $O(k^2)$ |
| **Large (500)** | Merge Sort | $n=500$ | **2.1197 ms** | $O(n \log n)$ |
| **Large (500)** | 0/1 Knapsack DP | $n=500, W=500$ | **70.1319 ms** | $O(n \cdot W)$ |
| **Large (500)** | Dijkstra (Heap) | $V=100, E=336$ | **0.3044 ms** | $O((V + E) \log V)$ |
| **Large (500)** | Nearest Neighbor TSP | Stops $k=30$ | **8.8744 ms** | $O(k^2)$ |

### B. Observations and Insights
1. **Merge Sort Growth**: Scaled smoothly from $0.015 \text{ ms}$ for $n=10$ to $2.120 \text{ ms}$ for $n=500$, aligning with predictable $O(n \log n)$ sub-quadratic scaling.
2. **0/1 Knapsack Pseudo-Polynomial Growth**: The execution time is directly proportional to both item count $n$ and capacity $W$. At $n=500, W=500$, the algorithm computes a matrix with $250,501$ entries, taking $70.13 \text{ ms}$. Sensitivity testing confirmed linear scaling with respect to $W$.
3. **Dijkstra Heap Efficiency**: Even on a 100-node graph with 336 road segments, Dijkstra executed in only $0.304 \text{ ms}$ thanks to $O((V+E)\log V)$ binary min-heap operations.
4. **TSP Practicality**: Nearest Neighbor solved a 30-stop delivery tour across a 100-node road network in $8.87 \text{ ms}$, validating its suitability for real-time dispatch systems.

---

## 9. Sample Input & Output Walkthrough

### Sample Run with Vehicle Capacity $W = 35 \text{ kg}$:

1. **Intake**: 15 parcels loaded from `data/parcels.json`.
2. **Prioritization (Merge Sort)**:
   - Rank 1: `P104` (Sneha Patel, Priority 10, Deadline 1 hr, Wt 4 kg, Value ₹1900)
   - Rank 2: `P111` (Manish Kumar, Priority 10, Deadline 1 hr, Wt 2 kg, Value ₹1750)
   - Rank 3: `P101` (Aarav Sharma, Priority 9, Deadline 2 hrs, Wt 5 kg, Value ₹1200)
   - Rank 4: `P107` (Kabir Singh, Priority 9, Deadline 2 hrs, Wt 3 kg, Value ₹1400)
   - Rank 5: `P115` (Karan Johar, Priority 9, Deadline 2 hrs, Wt 4 kg, Value ₹1350)
   - Rank 6: `P103` (Rohan Gupta, Priority 8, Deadline 2 hrs, Wt 12 kg, Value ₹1500)
   - Rank 7: `P113` (Suresh Menon, Priority 8, Deadline 3 hrs, Wt 5 kg, Value ₹1250)
3. **Packing (0/1 Knapsack DP)**:
   - Selected Parcels: `P104`, `P111`, `P101`, `P107`, `P115`, `P103`, `P113`
   - Total Weight: **$35 \text{ kg} / 35 \text{ kg}$ (100% vehicle utilization)**
   - Total Monetary Value: **₹10,350.00**
   - Remaining Capacity: **$0 \text{ kg}$**
4. **Shortest Paths (Dijkstra)**:
   - Central Warehouse $\to$ Rajiv Chowk: **$2.80 \text{ km}$** (`Central Warehouse -> Rajiv Chowk`)
   - Central Warehouse $\to$ MG Road: **$5.60 \text{ km}$** (`Central Warehouse -> MG Road`)
   - Central Warehouse $\to$ Cyber City: **$8.70 \text{ km}$** (`Central Warehouse -> Sector 14 -> Cyber City`)
   - Central Warehouse $\to$ Golf Course Road: **$10.10 \text{ km}$** (`Central Warehouse -> MG Road -> Golf Course Road`)
5. **Route Planning (Nearest Neighbor TSP)**:
   - Leg 1: Central Warehouse $\to$ Rajiv Chowk ($2.80 \text{ km}$)
   - Leg 2: Rajiv Chowk $\to$ MG Road ($8.40 \text{ km}$)
   - Leg 3: MG Road $\to$ Cyber City ($3.80 \text{ km}$)
   - Leg 4: Cyber City $\to$ Golf Course Road ($8.30 \text{ km}$)
   - Leg 5: Golf Course Road $\to$ Central Warehouse ($10.10 \text{ km}$)
   - **Ordered Route**: `Central Warehouse ➔ Rajiv Chowk ➔ MG Road ➔ Cyber City ➔ Golf Course Road ➔ Central Warehouse`
   - **Total Driving Distance**: **$33.40 \text{ km}$**

---

## 10. Generated Artifacts & Screenshots

All visual charts and test records are persistently stored:
- `reports/performance_results.csv`: Complete empirical benchmark data table.
- `reports/performance_runtime_comparison.png`: Grouped logarithmic bar chart comparing all algorithms.
- `reports/performance_scaling_curves.png`: Input size $N$ vs execution time curves.
- `reports/knapsack_capacity_impact.png`: Capacity $W$ scaling curve showing $O(n \cdot W)$ linearity.
- `reports/delivery_route_visualization.png`: Full delivery network map with directional TSP route overlay.

### How to Capture Live UI Screenshots for Submission:
1. Start the Streamlit application using `./venv/bin/streamlit run app.py`.
2. Open your browser at `http://localhost:8501`.
3. Navigate through the sidebar pages (Dashboard, Parcel Prioritization, Packing Optimization, Delivery Graph, Shortest Path Finder, Route Optimization, Performance Analysis).
4. On macOS, press `Cmd + Shift + 4` to capture screenshots of each page and save them into the `screenshots/` folder.

---

## 11. Installation and Execution Instructions

### Prerequisites
- Python 3.10, 3.11, 3.12, 3.13, or 3.14.
- Git.

### Step 1: Clone Repository
```bash
git clone https://github.com/<your-username>/mini-courier-planner.git
cd mini-courier-planner
```

### Step 2: Set Up Virtual Environment & Dependencies
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Step 3: Run Automated End-to-End Demo (CLI)
```bash
python main.py --demo
```

### Step 4: Run Interactive Terminal Application
```bash
python main.py
```

### Step 5: Run Empirical Benchmarks
```bash
python main.py --benchmark
```

### Step 6: Launch Streamlit Web Application
```bash
streamlit run app.py
```
Open `http://localhost:8501` in your browser.

### Step 7: Run Automated Unit Tests
```bash
python -m unittest discover tests
```

---

## 12. Limitations

1. **Heuristic TSP Bound**: Nearest Neighbor does not guarantee the minimum possible traveling distance; poor initial choices can result in suboptimal tours.
2. **Knapsack Integer Capacity**: The standard 0/1 DP table relies on integer weight units. Fractional weights require scaling (e.g., converting kg to grams), which increases memory.
3. **Static Traffic Representation**: Edge weights represent fixed distance rather than real-time dynamic traffic delays.

---

## 13. Future Scope

1. **Metaheuristic Routing**: Integrate 2-Opt or Simulated Annealing local search to refine the Nearest Neighbor TSP tour towards true optimality.
2. **Multi-Vehicle Capacitated VRP (CVRP)**: Expand from a single courier van to a fleet of heterogeneous vehicles servicing disjoint customer clusters.
3. **Time-Window Constraints (VRPTW)**: Incorporate hard customer availability time-windows alongside road network transit times.
4. **Live GIS Integration**: Connect OpenStreetMap API or Google Maps Distance Matrix API for real-world live traffic routing.

---

## 14. Conclusion

The **Mini-Courier Planner** successfully models and solves the modern courier dispatch problem. By combining Merge Sort for deterministic prioritization, 0/1 Knapsack Dynamic Programming for vehicle packing, Dijkstra's algorithm for accurate shortest road paths, and Nearest Neighbor TSP for tour scheduling, the system optimizes both logistics revenue and delivery efficiency. Empirical benchmarking across small, medium, and large datasets demonstrates strong adherence to theoretical complexity models, providing an exemplary foundation for academic study and practical logistics software engineering.



CODE TO RUN
source venv/bin/activate
python main.py --demo
python main.py
streamlit run app.py
python -m unittest discover tests -v
python -m algorithms.performance



Mini-Courier Planner: Algorithmic Logistics Optimization Engine

Design and Analysis of Algorithms (ETCCDA302) — Capstone Project
Department of Computer Science & Engineering, K.R. Mangalam University

Executive Overview & Verification Status

The Mini-Courier Planner has been developed, verified, benchmarked, and committed. All four core algorithms were implemented manually from mathematical first principles in Python 3 without high-level library shortcuts (no built-in sort() for prioritization, no NetworkX shortest-path routines, no external TSP solvers).

Reports & Visualizations: Charts (.png) and tabular CSV data (.csv) generated and saved into reports/ and screenshots/.
User Interfaces: Both an Interactive Streamlit Web Dashboard (app.py) and a Full-Featured Terminal CLI / Demo Runner (main.py) are included.
1. Project Directory Structure
CAPSTONE/
├── app.py                             # Interactive Streamlit Web UI (9 modules)
├── main.py                            # Interactive CLI menu & automated demo runner
├── requirements.txt                   # Dependency specifications (Streamlit, Matplotlib, Pandas, NetworkX)
├── README.md                          # Comprehensive project documentation
├── CAPSTONE_REPORT.md                 # 5-Phase academic capstone project report
├── VIVA_QUESTIONS.md                  # 35 Viva Voce questions & beginner-friendly answers
├── .gitignore                         # Git ignore rules for venv, caches, and OS files
│
├── algorithms/                        # Manual algorithmic implementations
│   ├── __init__.py
│   ├── sorting.py                     # Manual Merge Sort (Priority desc, Deadline asc, ID tie-breaker)
│   ├── knapsack.py                    # Manual 0/1 Knapsack DP with full 2D table backtracking
│   ├── dijkstra.py                    # Manual Dijkstra Shortest Path with binary min-heap (heapq)
│   ├── tsp.py                         # Manual Nearest Neighbor TSP tour planner
│   └── performance.py                 # Empirical benchmarking suite (time.perf_counter)
│
├── models/                            # Domain data models
│   ├── __init__.py
│   ├── parcel.py                      # Parcel dataclass, validation & serialization
│   └── delivery_graph.py              # Adjacency-list DeliveryGraph data structure
│
├── data/                              # Persistent JSON sample datasets
│   ├── parcels.json                   # 15 realistic parcels with varied weights, deadlines & values
│   └── graph.json                     # 11-node Gurugram NCR delivery network graph
│
├── visualization/                     # Plotting and rendering engines
│   ├── __init__.py
│   ├── graph_visualizer.py            # Matplotlib delivery tour and graph visualizer
│   └── performance_charts.py          # Grouped bar chart, scaling curves & knapsack sensitivity
│
├── tests/                             # Automated test suite (28 test cases)
│   ├── __init__.py
│   ├── test_sorting.py                # Empty, single, multi, tie-breakers, large dataset
│   ├── test_knapsack.py               # Zero capacity, oversized parcels, optimal DP verification
│   ├── test_dijkstra.py               # Shortest paths, multiple routes, disconnected nodes
│   ├── test_tsp.py                    # Closed-loop tour, duplicate locations, unreachable nodes
│   └── test_integration.py            # End-to-end multi-algorithm pipeline tests
│
├── reports/                           # Empirical benchmarks & generated plots
│   ├── performance_results.csv        # Actual CPU execution measurements
│   ├── performance_runtime_comparison.png  # Logarithmic grouped bar chart
│   ├── performance_scaling_curves.png      # Input size vs execution time curves
│   ├── knapsack_capacity_impact.png        # Pseudo-polynomial O(n·W) linear growth curve
│   └── delivery_route_visualization.png    # Route map with directional arrows
│
└── screenshots/                       # Exported visualization figures ready for report submission
    ├── delivery_route_visualization.png
    ├── knapsack_capacity_impact.png
    ├── performance_runtime_comparison.png
    └── performance_scaling_curves.png

3. How to Run the Project
Step 1: Activate Virtual Environment
bash
cd /Users/krishnakumar/Documents/CAPSTONE
source venv/bin/activate

(Dependencies are already installed in venv/: streamlit, matplotlib, pandas, networkx)

Step 2: Run Automated End-to-End Demo (CLI)

Executes all 4 algorithms sequentially on Gurugram NCR delivery data and prints step-by-step results:

bash
python main.py --demo
Step 3: Run Interactive Terminal Application

Provides an interactive menu for adding parcels, setting custom vehicle capacities, and calculating custom routes:

bash
python main.py
Step 4: Launch the Streamlit Web Application

Launches a responsive browser interface featuring all 9 required pages:

bash
streamlit run app.py

Open http://localhost:8501 in your browser.

Step 5: Run Automated Unit Tests
bash
python -m unittest discover tests -v

(Executes all 28 unit and edge-case tests)

Step 6: Re-run Benchmarking Suite

Regenerates CSV tables and PNG charts:

bash
python -m algorithms.performance
4. Capturing Evidence & Screenshots for Submission
The script has already saved high-resolution Matplotlib charts directly into reports/ and screenshots/:
delivery_route_visualization.png: Visual road network with numbered delivery stops and red directional tour arrows.
performance_runtime_comparison.png: Grouped logarithmic bar chart comparing all algorithms.
performance_scaling_curves.png: Input size vs runtime growth curves.
knapsack_capacity_impact.png: Proof of pseudo-polynomial growth.
To capture live web UI screenshots:
Run streamlit run app.py
Use Cmd + Shift + 4 (on macOS) to capture each tab: Dashboard, Parcel Prioritization, Packing Optimization, Delivery Graph, Shortest Paths, Route Optimization, and Performance Analysis.
5. How to Upload the Project to GitHub

A clean Git repository has already been initialized and committed locally. To push it to your GitHub profile:

bash
# 1. Create a new empty repository on github.com (e.g. named 'mini-courier-planner')
# 2. Add your GitHub remote URL
git remote add origin https://github.com/<YOUR_GITHUB_USERNAME>/mini-courier-planner.git
# 3. Rename branch to main (if preferred) and push
git branch -M main
git push -u origin main
