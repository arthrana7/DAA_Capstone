# SwiftRoute AI: Algorithmic Logistics Optimization Engine
## Capstone Project Report — Design & Analysis of Algorithms (ETCCDA302)
**Department of Computer Science & Engineering, K.R. Mangalam University**  
**Programme:** B.Tech Computer Science & Engineering (FSD-A)  
**Submitted By:** Arth Rana  
**Roll No.:** 2501350005  

---

## 1. Executive Summary & Problem Formulation

In modern parcel delivery and urban supply chain logistics, distribution hubs face four interrelated algorithmic challenges daily:
1. **Urgency-Driven Prioritization**: Determining which packages must receive immediate processing based on emergency priority levels and strict customer delivery deadlines.
2. **Payload-Constrained Cargo Packing**: Selecting an optimal combination of parcels that maximizes cumulative invoice revenue while strictly adhering to a delivery vehicle's maximum gross payload capacity ($W$).
3. **Shortest Network Pathfinding**: Computing the exact minimum road driving distances from the central logistics depot to every designated customer drop-off location across an urban road grid.
4. **Closed-Loop Tour Scheduling (TSP)**: Determining the optimal sequence of stops for the delivery vehicle to visit all designated drop-off points and return safely to the depot while minimizing cumulative driving distance and fuel burn.

**SwiftRoute AI** is an integrated algorithmic dispatch engine built from mathematical first principles in Python 3. The system integrates four foundational computer science algorithmic paradigms into a cohesive, sequential pipeline:
- **Divide-and-Conquer**: Manual 3-tier Merge Sort for stable $O(n \log n)$ prioritization.
- **Dynamic Programming**: Manual 0/1 Knapsack Tabulation with 2D matrix backtracking in $O(n \cdot W)$ time.
- **Greedy Graph Traversal**: Manual Dijkstra Shortest Path algorithm using a binary min-heap (`heapq`) in $O((V+E)\log V)$ time.
- **Heuristic Tour Approximation**: Manual Nearest Neighbor heuristic for Traveling Salesperson Problem (TSP) in $O(k^2)$ time.

No high-level black-box sorting libraries, third-party shortest-path functions, or external TSP solvers were used in core algorithmic routines.

---

## 2. Phase 1 — Problem Design, Network Topology & Data Modeling

### 2.1 Domain Data Architecture
Each consignment is encapsulated by a dedicated data record containing seven primary attributes:
- **Consignment ID** (`parcel_id`): Unique alphanumeric tracking code (`SR-101` to `SR-116`).
- **Recipient** (`customer_name`): Name of customer/client.
- **Destination Node** (`delivery_location`): Target node in the urban road network.
- **Payload Weight** (`weight`): Integer mass in kilograms ($w_i \in [1, 20]$ kg).
- **Urgency Rating** (`priority`): Integer priority on a 1-to-10 scale ($10 = \text{Emergency}$, $1 = \text{Routine}$).
- **Service Deadline** (`delivery_deadline`): Maximum allowable turnaround time in hours.
- **Invoice Value** (`value`): Monetary worth of consignment in Indian Rupees (₹).

The active operational dataset consists of **16 real-world parcels** across **12 urban road hubs** centered at `Okhla Central Hub`.

### 2.2 Complete Parcel Inventory Dataset

| ID | Recipient / Customer | Destination Location | Weight (kg) | Priority (1-10) | Deadline (hrs) | Invoice Value (₹) |
| :---: | :--- | :--- | :---: | :---: | :---: | :---: |
| **SR-101** | Aryan Malhotra | Connaught Place | 4 | 10 | 1 | ₹2,100.00 |
| **SR-102** | Ishita Sengupta | Nehru Place | 3 | 10 | 2 | ₹1,850.00 |
| **SR-103** | Devansh Mehra | Hauz Khas | 5 | 9 | 2 | ₹1,400.00 |
| **SR-104** | Kavya Singhania | Noida Sector 18 | 6 | 9 | 3 | ₹1,650.00 |
| **SR-105** | Tanya Chawla | Saket District Centre | 4 | 8 | 2 | ₹1,300.00 |
| **SR-106** | Rishi Kapoor | Lajpat Nagar | 7 | 8 | 4 | ₹1,200.00 |
| **SR-107** | Ananya Deshmukh | Aerocity Hub | 2 | 9 | 1 | ₹1,950.00 |
| **SR-108** | Siddharth Joshi | Greater Kailash | 5 | 8 | 3 | ₹1,250.00 |
| **SR-109** | Rhea Batra | Jasola Vihar | 8 | 7 | 4 | ₹950.00 |
| **SR-110** | Harshvardhan Rao | Lodhi Colony | 3 | 9 | 2 | ₹1,500.00 |
| **SR-111** | Meenakshi Sundaram | Vasant Kunj | 6 | 7 | 5 | ₹1,100.00 |
| **SR-112** | Zoya Akhtar | Connaught Place | 2 | 10 | 1 | ₹2,250.00 |
| **SR-113** | Nikhil Aggarwal | Nehru Place | 12 | 6 | 6 | ₹850.00 |
| **SR-114** | Simran Kaur | Hauz Khas | 4 | 8 | 3 | ₹1,350.00 |
| **SR-115** | Abhinav Saxena | Saket District Centre | 9 | 5 | 7 | ₹700.00 |
| **SR-116** | Pooja Hegde | Noida Sector 18 | 5 | 9 | 2 | ₹1,600.00 |

### 2.3 Road Network Graph Modeling
The metropolitan delivery territory is modeled as a weighted undirected graph $G = (V, E)$:
- **Vertices ($V$, $|V| = 12$)**: `Okhla Central Hub` (Primary Depot), `Nehru Place`, `Lajpat Nagar`, `Lodhi Colony`, `Connaught Place`, `Hauz Khas`, `Saket District Centre`, `Greater Kailash`, `Jasola Vihar`, `Noida Sector 18`, `Aerocity Hub`, `Vasant Kunj`.
- **Edges ($E$, $|E| = 17$)**: Bidirectional roadway segments weighted by actual driving distance in kilometers.
- **Storage Paradigm**: Adjacency list (`Dict[str, List[Tuple[str, float]]]`). Because metropolitan road grids are sparse ($E \ll V^2$), an adjacency list consumes strictly $O(V + E)$ auxiliary memory, drastically outperforming an $O(V^2)$ adjacency matrix.

---

## 3. Phase 2 — Consignment Prioritization and Payload Packing

### 3.1 Consignment Prioritization via Manual Merge Sort
- **Algorithmic Paradigm**: Divide-and-Conquer.
- **Multi-Level Comparator Logic**:
  1. **Primary Key**: Urgency Priority (`priority`) in **descending** order.
  2. **Secondary Key**: Service Deadline (`delivery_deadline`) in **ascending** order.
  3. **Tie-Breaker Key**: Consignment ID (`parcel_id`) in **ascending** lexicographical order.
- **Theoretical Complexity**: Time $O(n \log n)$ across all cases; Auxiliary Space $O(n)$ for merging. Stable sorting preserves natural arrival order.

### 3.2 Vehicle Payload Optimization via 0/1 Knapsack Dynamic Programming
Given vehicle payload capacity $W = 35\text{ kg}$:
$$\text{dp}[i][w] = \begin{cases} \text{dp}[i-1][w] & \text{if } w_i > w \\ \max(\text{dp}[i-1][w], \, \text{dp}[i-1][w - w_i] + v_i) & \text{if } w_i \le w \end{cases}$$

#### Knapsack Optimization Results ($W = 35\text{ kg}$):
- **Parcels Selected (9 items)**: `SR-101`, `SR-112`, `SR-102`, `SR-107`, `SR-103`, `SR-110`, `SR-116`, `SR-104`, `SR-114`
- **Total Payload Weight Loaded**: **$34\text{ kg} / 35\text{ kg}$** ($97.14\%$ payload capacity utilization)
- **Cumulative Consignment Revenue**: **₹15,650.00**
- **Remaining Payload Margin**: **$1\text{ kg}$**
- **Excluded Parcels**: Lower-priority/heavy packages (e.g., `SR-106`, `SR-109`, `SR-113`, `SR-115`) were deferred to prevent payload breaches.

---

## 4. Phase 3 — Shortest Road Pathfinding and Closed-Loop Tour Dispatch

### 4.1 Shortest Path Navigation via Dijkstra's Algorithm
The 9 selected parcels map to **6 unique destination hubs**:
1. `Nehru Place`: $3.20\text{ km}$ (`Okhla Central Hub ➔ Nehru Place`)
2. `Noida Sector 18`: $7.00\text{ km}$ (`Okhla Central Hub ➔ Jasola Vihar ➔ Noida Sector 18`)
3. `Lodhi Colony`: $8.80\text{ km}$ (`Okhla Central Hub ➔ Nehru Place ➔ Lajpat Nagar ➔ Lodhi Colony`)
4. `Hauz Khas`: $8.90\text{ km}$ (`Okhla Central Hub ➔ Saket District Centre ➔ Hauz Khas`)
5. `Connaught Place`: $13.60\text{ km}$ (`Okhla Central Hub ➔ Nehru Place ➔ Lajpat Nagar ➔ Lodhi Colony ➔ Connaught Place`)
6. `Aerocity Hub`: $15.00\text{ km}$ (`Okhla Central Hub ➔ Saket District Centre ➔ Vasant Kunj ➔ Aerocity Hub`)

Complexity: Time $O((V + E) \log V)$, Space $O(V + E)$.

---

### 4.2 Closed-Loop Delivery Tour via Nearest Neighbor TSP Heuristic
- **Ordered Tour Sequence**:  
  `Okhla Central Hub ➔ Nehru Place ➔ Lodhi Colony ➔ Hauz Khas ➔ Aerocity Hub ➔ Connaught Place ➔ Noida Sector 18 ➔ Okhla Central Hub`
- **Total Circuit Driving Distance**: **$53.60\text{ km}$**  
  ($3.20 + 5.60 + 4.20 + 8.20 + 11.50 + 13.90 + 7.00 = 53.60\text{ km}$)
- **Estimated Fuel Burn**: $\approx 6.31\text{ Litres}$ (at an average van economy of $8.5\text{ km/L}$)
- **Loop Closed**: Yes (Vehicle safely returns to base depot).

---

## 5. Phase 4 — Testing and Verification

- **Automated Unit Tests**: 28 tests passing in 0.003s across sorting, knapsack, dijkstra, tsp, and end-to-end integration.
- **Empirical Benchmarking**: Verified $O(n \log n)$ sub-quadratic scaling for Merge Sort and $O(n \cdot W)$ pseudo-polynomial linearity for 0/1 Knapsack.

---

## 6. How to Run

```bash
cd CAPSTONE-DAA
source venv/bin/activate
pip install -r requirements.txt

# Run Web Dashboard
streamlit run app.py

# Run Automated CLI Demo
python main.py --demo

# Run Unit Tests
python -m unittest discover tests -v
```

---
**Report Submitted By:** **Arth Rana** (Roll No.: **2501350005**)  
B.Tech CSE FSD-A, K.R. Mangalam University
