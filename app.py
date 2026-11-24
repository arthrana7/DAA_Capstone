"""
app.py
SwiftRoute AI — Enterprise Courier Logistics & Fleet Route Optimization Engine
Design & Analysis of Algorithms (ETCCDA302) — Capstone Project
Interactive Streamlit Application
"""

import os
import json
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

from models.parcel import Parcel
from models.delivery_graph import DeliveryGraph
from algorithms.sorting import sort_parcels_with_metrics
from algorithms.knapsack import knapsack_01
from algorithms.dijkstra import dijkstra_shortest_paths
from algorithms.tsp import solve_tsp_nearest_neighbor
from visualization.graph_visualizer import plot_delivery_network
from algorithms.performance import run_benchmarks


# Page Configuration
st.set_page_config(
    page_title="SwiftRoute AI | Logistics Optimization Engine",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom High-End Styling (Modern Tech / Glassmorphism Aesthetic)
st.markdown("""
<style>
    /* Global Container Enhancements */
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    /* Modern Gradient Header */
    .brand-banner {
        background: linear-gradient(135deg, #1E1B4B 0%, #312E81 50%, #4338CA 100%);
        border: 1px solid rgba(129, 140, 248, 0.25);
        border-radius: 16px;
        padding: 24px 30px;
        margin-bottom: 24px;
        box-shadow: 0 10px 25px -5px rgba(49, 46, 129, 0.25);
    }
    
    .brand-title {
        color: #F8FAFC !important;
        font-size: 2.1rem;
        font-weight: 800;
        letter-spacing: -0.02em;
        margin: 0;
        display: flex;
        align-items: center;
        gap: 12px;
    }
    
    .brand-subtitle {
        color: #C7D2FE !important;
        font-size: 1.0rem;
        font-weight: 500;
        margin-top: 6px;
        margin-bottom: 0;
    }

    .status-pill {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: rgba(16, 185, 129, 0.15);
        border: 1px solid rgba(16, 185, 129, 0.35);
        color: #10B981;
        padding: 4px 12px;
        border-radius: 9999px;
        font-size: 0.78rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    /* KPI Cards */
    .kpi-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 14px;
        padding: 18px 20px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.04), 0 2px 4px -2px rgba(0, 0, 0, 0.03);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .kpi-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.07);
    }
    .kpi-label {
        font-size: 0.82rem;
        font-weight: 600;
        color: #64748B;
        text-transform: uppercase;
        letter-spacing: 0.04em;
    }
    .kpi-val {
        font-size: 1.7rem;
        font-weight: 800;
        color: #0F172A;
        margin-top: 4px;
    }

    /* Algorithm Badges */
    .badge-purple {
        background-color: #EDE9FE;
        color: #5B21B6;
        padding: 4px 10px;
        border-radius: 8px;
        font-size: 0.82rem;
        font-weight: 700;
        display: inline-block;
    }
    .badge-emerald {
        background-color: #D1FAE5;
        color: #065F46;
        padding: 4px 10px;
        border-radius: 8px;
        font-size: 0.82rem;
        font-weight: 700;
        display: inline-block;
    }
    .badge-amber {
        background-color: #FEF3C7;
        color: #92400E;
        padding: 4px 10px;
        border-radius: 8px;
        font-size: 0.82rem;
        font-weight: 700;
        display: inline-block;
    }

    /* Callout Box */
    .custom-callout {
        background: #F8FAFC;
        border-left: 4px solid #4F46E5;
        border-radius: 8px;
        padding: 14px 18px;
        margin: 14px 0;
        color: #334155;
        font-size: 0.93rem;
    }

    /* Step Sequence */
    .route-step {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 10px 14px;
        background: #F1F5F9;
        border-radius: 10px;
        margin-bottom: 8px;
        font-size: 0.92rem;
        font-weight: 600;
        color: #1E293B;
    }
    .route-num {
        background: #4F46E5;
        color: white;
        border-radius: 50%;
        width: 26px;
        height: 26px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 0.78rem;
        font-weight: 800;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_data
def load_base_data():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(base_dir, "data", "parcels.json"), "r", encoding="utf-8") as f:
        p_data = json.load(f)
    with open(os.path.join(base_dir, "data", "graph.json"), "r", encoding="utf-8") as f:
        g_data = json.load(f)
    return p_data, g_data


p_raw, g_raw = load_base_data()

# Session State Initialization
if "parcels" not in st.session_state:
    st.session_state.parcels = [Parcel.from_dict(p) for p in p_raw]

if "graph" not in st.session_state:
    st.session_state.graph = DeliveryGraph.from_dict(g_raw)
    st.session_state.warehouse = g_raw.get("warehouse", "Okhla Central Hub")


# Sidebar Styling & Navigation
with st.sidebar:
    st.markdown("""
    <div style="padding: 12px 0 18px 0; text-align: left;">
        <div style="display: flex; align-items: center; gap: 10px;">
            <div style="background: linear-gradient(135deg, #4F46E5, #06B6D4); padding: 8px 11px; border-radius: 12px; font-size: 1.4rem;">⚡</div>
            <div>
                <div style="font-size: 1.25rem; font-weight: 800; color: #1E293B; letter-spacing: -0.02em;">SwiftRoute AI</div>
                <div style="font-size: 0.75rem; color: #64748B; font-weight: 600;">ENTERPRISE LOGISTICS SUITE</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="status-pill">● System Online • v3.2</div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    menu_choice = st.radio(
        "Navigation Hub",
        [
            "⚡ Mission Control (Dashboard)",
            "📦 Consignment Inventory",
            "🎯 Urgency Prioritization (Merge Sort)",
            "⚖️ Payload Capacity Optimizer (0/1 Knapsack)",
            "🌐 Road Network Topology",
            "🧭 Shortest Path Navigation (Dijkstra)",
            "🚚 Multi-Stop Tour Dispatcher (TSP)",
            "📈 Algorithmic Benchmark Suite",
            "📚 Capstone Architecture & Viva Guide"
        ]
    )

    st.markdown("---")
    st.caption("⚙️ **Core Algorithmic Complexity Matrix**")
    st.markdown("""
    - **Merge Sort**: $O(n \\log n)$
    - **0/1 Knapsack DP**: $O(n \\cdot W)$
    - **Dijkstra Heap**: $O((V+E) \\log V)$
    - **Nearest Neighbor TSP**: $O(k^2)$
    """)
    st.markdown("---")
    st.caption("📍 **Active Depot**: `" + str(st.session_state.warehouse) + "`")


# -------------------------------------------------------------
# 1. MISSION CONTROL (DASHBOARD)
# -------------------------------------------------------------
if menu_choice == "⚡ Mission Control (Dashboard)":
    st.markdown(f"""
    <div class="brand-banner">
        <div class="brand-title">⚡ SwiftRoute AI: Mission Control</div>
        <div class="brand-subtitle">Automated Multi-Stage Algorithmic Pipeline for Intelligent Logistics & Fleet Scheduling</div>
    </div>
    """, unsafe_allow_html=True)

    # High-impact KPI row
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">Active Consignments</div>
            <div class="kpi-val">{len(st.session_state.parcels)} <span style="font-size:0.9rem; color:#64748B; font-weight:500;">pkgs</span></div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        total_wt = sum(p.weight for p in st.session_state.parcels)
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">Cumulative Cargo</div>
            <div class="kpi-val">{total_wt} <span style="font-size:0.9rem; color:#64748B; font-weight:500;">kg</span></div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        total_val = sum(p.value for p in st.session_state.parcels)
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">Gross Value</div>
            <div class="kpi-val">₹{total_val:,.0f}</div>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">Delivery Hubs</div>
            <div class="kpi-val">{len(st.session_state.graph.get_nodes())} <span style="font-size:0.9rem; color:#64748B; font-weight:500;">nodes</span></div>
        </div>
        """, unsafe_allow_html=True)
    with col5:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">Dispatch Center</div>
            <div class="kpi-val" style="font-size:1.05rem; padding-top:6px; color:#4F46E5;">{st.session_state.warehouse}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Pipeline Workflow Section
    c_pipe, c_summary = st.columns([1.6, 1.0])
    with c_pipe:
        st.subheader("🔄 Multi-Stage Computational Pipeline")
        st.markdown("""
        ```mermaid
        flowchart LR
            subgraph S1["Phase 1: Prioritize"]
                A[Raw Inflow] --> B[Merge Sort\nO(n log n)]
            end
            subgraph S2["Phase 2: Cargo Packing"]
                B --> C[0/1 Knapsack DP\nO(n·W)]
            end
            subgraph S3["Phase 3: Road Routing"]
                C --> D[Dijkstra Heap\nO(V+E log V)]
                D --> E[Nearest Neighbor TSP\nO(k²)]
            end
            E --> F([Dispatched Fleet])
            style S1 fill:#EEF2FF,stroke:#4F46E5,stroke-width:2px
            style S2 fill:#ECFDF5,stroke:#10B981,stroke-width:2px
            style S3 fill:#FFFBEB,stroke:#F59E0B,stroke-width:2px
        ```
        """)

    with c_summary:
        st.subheader("📋 Quick Dispatch Insights")
        avg_weight = total_wt / len(st.session_state.parcels) if st.session_state.parcels else 0
        critical_count = sum(1 for p in st.session_state.parcels if p.priority >= 9)

        st.markdown(f"""
        <div class="custom-callout">
            <b>⚡ Dispatch Readiness:</b> Ready for optimization.<br>
            <b>🚨 Critical Urgency Packages:</b> {critical_count} parcels<br>
            <b>⚖️ Mean Parcel Weight:</b> {avg_weight:.1f} kg<br>
            <b>📍 Primary Logistics Depot:</b> {st.session_state.warehouse}
        </div>
        """, unsafe_allow_html=True)

        st.info("Navigate through the sidebar modules to run each algorithm independently or simulate fleet routing.")

    st.markdown("---")
    st.subheader("📦 Live Consignment Pool")
    df_preview = pd.DataFrame([p.to_dict() for p in st.session_state.parcels])
    st.dataframe(df_preview, use_container_width=True)


# -------------------------------------------------------------
# 2. CONSIGNMENT INVENTORY
# -------------------------------------------------------------
elif menu_choice == "📦 Consignment Inventory":
    st.markdown("""
    <div class="brand-banner">
        <div class="brand-title">📦 Consignment Inventory & Intake</div>
        <div class="brand-subtitle">Real-time package registry, destination filtering, and dynamic parcel ingestion</div>
    </div>
    """, unsafe_allow_html=True)

    tab_view, tab_add = st.tabs(["📋 Consignment Directory", "➕ Ingest New Consignment"])

    with tab_view:
        df_p = pd.DataFrame([p.to_dict() for p in st.session_state.parcels])

        col_f1, col_f2 = st.columns([2, 1])
        with col_f1:
            loc_filter = st.multiselect("Filter by Drop-Off Location", options=sorted(df_p["delivery_location"].unique()))
        with col_f2:
            min_priority = st.slider("Minimum Priority Rating", 1, 10, 1)

        filtered_df = df_p.copy()
        if loc_filter:
            filtered_df = filtered_df[filtered_df["delivery_location"].isin(loc_filter)]
        filtered_df = filtered_df[filtered_df["priority"] >= min_priority]

        st.dataframe(filtered_df, use_container_width=True)
        st.caption(f"Displaying {len(filtered_df)} of {len(df_p)} recorded consignments.")

    with tab_add:
        st.markdown("#### Register a New Parcel Consignment")
        with st.form("add_consignment_form"):
            c1, c2 = st.columns(2)
            with c1:
                new_id = st.text_input("Consignment ID", f"SR-{len(st.session_state.parcels) + 101}")
                cust_name = st.text_input("Recipient / Customer Name", "Aditi Rao")
                deliv_loc = st.selectbox("Designated Destination Hub", options=st.session_state.graph.get_nodes())
            with c2:
                wt = st.number_input("Gross Weight (kg)", min_value=1, max_value=60, value=5)
                prio = st.slider("Urgency Priority (1 = Routine, 10 = Emergency)", 1, 10, 8)
                dline = st.number_input("Service Deadline (hours)", min_value=1, max_value=24, value=2)
                val = st.number_input("Consignment Invoice Value (₹)", min_value=100.0, max_value=25000.0, value=1500.0, step=50.0)

            submitted = st.form_submit_button("Ingest Consignment into Pipeline", type="primary")
            if submitted:
                new_parcel = Parcel(new_id, cust_name, deliv_loc, int(wt), int(prio), int(dline), float(val))
                st.session_state.parcels.append(new_parcel)
                st.success(f"✓ Consignment {new_id} ingested successfully!")
                st.rerun()


# -------------------------------------------------------------
# 3. URGENCY PRIORITIZATION (MERGE SORT)
# -------------------------------------------------------------
elif menu_choice == "🎯 Urgency Prioritization (Merge Sort)":
    st.markdown("""
    <div class="brand-banner">
        <div class="brand-title">🎯 Urgency Prioritization Engine</div>
        <div class="brand-subtitle">Deterministic Divide-and-Conquer Sorting via Manual Merge Sort — O(n log n)</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="custom-callout">
        <b>Hierarchical Comparator Criteria:</b><br>
        1. <b>Priority Rank (Descending)</b>: High-priority parcels must be loaded and dispatched first.<br>
        2. <b>Delivery Deadline (Ascending)</b>: Earlier deadlines take precedence when priority scores tie.<br>
        3. <b>Consignment ID (Ascending)</b>: Strict lexicographical tie-breaker for deterministic repeatability.
    </div>
    """, unsafe_allow_html=True)

    btn_run = st.button("🚀 Execute Merge Sort Algorithm", type="primary")

    sorted_list, sort_time = sort_parcels_with_metrics(st.session_state.parcels)

    m1, m2, m3 = st.columns(3)
    with m1:
        st.metric("Consignments Sorted", len(sorted_list))
    with m2:
        st.metric("Sorting Execution Time", f"{sort_time * 1000:.4f} ms")
    with m3:
        st.metric("Theoretical Bound", "O(n log n)")

    c_left, c_right = st.columns(2)
    with c_left:
        st.subheader("📥 Raw Unsorted Inflow")
        st.dataframe(pd.DataFrame([p.to_dict() for p in st.session_state.parcels]), use_container_width=True)

    with c_right:
        st.subheader("🏆 Prioritized Dispatch Queue")
        st.dataframe(pd.DataFrame([p.to_dict() for p in sorted_list]), use_container_width=True)


# -------------------------------------------------------------
# 4. PAYLOAD CAPACITY OPTIMIZER (0/1 KNAPSACK)
# -------------------------------------------------------------
elif menu_choice == "⚖️ Payload Capacity Optimizer (0/1 Knapsack)":
    st.markdown("""
    <div class="brand-banner">
        <div class="brand-title">⚖️ Vehicle Payload Packing Optimization</div>
        <div class="brand-subtitle">Exact 0/1 Knapsack Dynamic Programming with 2D Tabulation & Backtracking — O(n · W)</div>
    </div>
    """, unsafe_allow_html=True)

    sorted_parcels, _ = sort_parcels_with_metrics(st.session_state.parcels)

    capacity = st.slider("Set Vehicle Maximum Payload Capacity Limit (kg)", min_value=10, max_value=120, value=35, step=5)

    knap_result = knapsack_01(sorted_parcels, capacity=capacity)

    # Metrics
    utilization = (knap_result.total_weight / capacity) * 100 if capacity > 0 else 0
    k1, k2, k3, k4 = st.columns(4)
    with k1:
        st.metric("Loaded Payload", f"{knap_result.total_weight} / {capacity} kg", f"{utilization:.1f}% Utilized")
    with k2:
        st.metric("Total Revenue Yield", f"₹{knap_result.total_value:,.2f}")
    with k3:
        st.metric("Spare Payload Margin", f"{knap_result.remaining_capacity} kg")
    with k4:
        st.metric("DP Computation Time", f"{knap_result.execution_time * 1000:.3f} ms")

    # Progress bar for payload utilization
    st.progress(min(1.0, utilization / 100.0), text=f"Vehicle Payload Utilization: {utilization:.1f}%")

    st.subheader(f"🚚 Optimally Packed Consignments ({len(knap_result.selected_parcels)} items selected)")
    if knap_result.selected_parcels:
        st.dataframe(pd.DataFrame([p.to_dict() for p in knap_result.selected_parcels]), use_container_width=True)
    else:
        st.warning("No consignments fit within the specified payload constraint.")

    with st.expander("🔍 Inspect Dynamic Programming Tabulation Matrix"):
        st.caption("Matrix cell dp[i][w] defines the optimal monetary yield using a subset of first i prioritized parcels with weight limit w.")
        slice_rows = min(15, len(knap_result.dp_table))
        slice_cols = min(22, len(knap_result.dp_table[0]))
        dp_subset = [row[:slice_cols] for row in knap_result.dp_table[:slice_rows]]
        df_dp = pd.DataFrame(dp_subset)
        df_dp.index = [f"Item {i} ({sorted_parcels[i-1].parcel_id if i>0 else 'Init'})" for i in range(slice_rows)]
        df_dp.columns = [f"{w}kg" for w in range(slice_cols)]
        st.dataframe(df_dp)


# -------------------------------------------------------------
# 5. ROAD NETWORK TOPOLOGY
# -------------------------------------------------------------
elif menu_choice == "🌐 Road Network Topology":
    st.markdown("""
    <div class="brand-banner">
        <div class="brand-title">🌐 Road Network Topology & Graph Model</div>
        <div class="brand-subtitle">Weighted Undirected Adjacency List Representation — O(V + E) Space Complexity</div>
    </div>
    """, unsafe_allow_html=True)

    g = st.session_state.graph
    nodes = g.get_nodes()

    col_map, col_adj = st.columns([1.2, 1.0])

    with col_map:
        st.subheader("🗺️ Road Infrastructure Network Map")
        fig = plot_delivery_network(g)
        st.pyplot(fig)

    with col_adj:
        st.subheader("🔗 Network Adjacency Registry")
        adj_data = []
        for u in nodes:
            neighbors = g.get_neighbors(u)
            connections = ", ".join([f"{v} ({dist} km)" for v, dist in neighbors])
            adj_data.append({
                "Hub / Node": u,
                "Connectivity (Degree)": len(neighbors),
                "Direct Roads": connections
            })
        st.dataframe(pd.DataFrame(adj_data), use_container_width=True)


# -------------------------------------------------------------
# 6. SHORTEST PATH NAVIGATION (DIJKSTRA)
# -------------------------------------------------------------
elif menu_choice == "🧭 Shortest Path Navigation (Dijkstra)":
    st.markdown("""
    <div class="brand-banner">
        <div class="brand-title">🧭 Shortest Path Navigation Engine</div>
        <div class="brand-subtitle">Single-Source Shortest Paths via Manual Dijkstra with Binary Min-Heap — O((V + E) log V)</div>
    </div>
    """, unsafe_allow_html=True)

    g = st.session_state.graph
    warehouse = st.session_state.warehouse

    c_src, c_dst = st.columns(2)
    with c_src:
        src = st.selectbox("Dispatch Origin (Source Hub)", options=g.get_nodes(), index=g.get_nodes().index(warehouse))
    with c_dst:
        dst = st.selectbox("Destination Hub (Target)", options=g.get_nodes(), index=1)

    d_res = dijkstra_shortest_paths(g, src)
    dist = d_res.get_distance_to(dst)
    path = d_res.get_path_to(dst)

    d1, d2, d3 = st.columns(3)
    with d1:
        st.metric("Shortest Distance", f"{dist:.2f} km" if dist != float("inf") else "Unreachable")
    with d2:
        st.metric("Turn-by-Turn Waypoints", len(path) if path else 0)
    with d3:
        st.metric("Heap Compute Runtime", f"{d_res.execution_time * 1000:.4f} ms")

    if path:
        st.markdown(f"""
        <div class="custom-callout" style="border-left-color: #10B981;">
            <b>📍 Optimized Driving Route:</b> {' ➔ '.join(path)}
        </div>
        """, unsafe_allow_html=True)
    else:
        st.error(f"No valid driving connection between {src} and {dst}.")

    st.subheader(f"📊 All Shortest Reachable Distances from '{src}'")
    all_details = d_res.get_route_details(g.get_nodes())
    st.dataframe(pd.DataFrame(all_details), use_container_width=True)


# -------------------------------------------------------------
# 7. MULTI-STOP TOUR DISPATCHER (TSP)
# -------------------------------------------------------------
elif menu_choice == "🚚 Multi-Stop Tour Dispatcher (TSP)":
    st.markdown("""
    <div class="brand-banner">
        <div class="brand-title">🚚 Multi-Stop Tour Dispatcher (TSP)</div>
        <div class="brand-subtitle">Closed-Loop Itinerary Scheduling via Nearest Neighbor Heuristic Approximation — O(k²)</div>
    </div>
    """, unsafe_allow_html=True)

    g = st.session_state.graph
    warehouse = st.session_state.warehouse

    # Pre-select packed parcel locations by default
    sorted_parcels, _ = sort_parcels_with_metrics(st.session_state.parcels)
    packed_parcels = knapsack_01(sorted_parcels, capacity=35).selected_parcels
    default_stops = list(dict.fromkeys(p.delivery_location for p in packed_parcels if p.delivery_location != warehouse))

    available_stops = [n for n in g.get_nodes() if n != warehouse]
    selected_stops = st.multiselect("Select Customer Drop-Off Destinations", options=available_stops, default=default_stops)

    if st.button("⚡ Generate Closed-Loop Dispatch Tour", type="primary"):
        if not selected_stops:
            st.warning("Please choose at least one drop-off stop.")
        else:
            tsp_res = solve_tsp_nearest_neighbor(g, warehouse, selected_stops)

            t1, t2, t3, t4 = st.columns(4)
            with t1:
                st.metric("Total Circuit Distance", f"{tsp_res.total_distance_km:.2f} km")
            with t2:
                st.metric("Customer Stops Serviced", len(selected_stops))
            with t3:
                fuel_est = tsp_res.total_distance_km / 8.5
                st.metric("Est. Fuel Burn", f"{fuel_est:.2f} L", "Avg 8.5 km/L")
            with t4:
                st.metric("Tour Solver Latency", f"{tsp_res.execution_time * 1000:.3f} ms")

            st.markdown(f"""
            <div class="custom-callout" style="border-left-color: #4F46E5;">
                <b>🏁 Continuous Delivery Tour:</b> {' ➔ '.join(tsp_res.route_sequence)}
            </div>
            """, unsafe_allow_html=True)

            c_itin, c_map = st.columns([1, 1.2])
            with c_itin:
                st.subheader("📋 Step-by-Step Dispatch Legs")
                for idx, leg in enumerate(tsp_res.detailed_legs, start=1):
                    st.markdown(f"""
                    <div class="route-step">
                        <div class="route-num">{idx}</div>
                        <div>
                            <div>{leg.from_node} ➔ {leg.to_node}</div>
                            <div style="font-size:0.8rem; color:#64748B;">Leg Distance: {leg.distance_km:.2f} km | Via: {' -> '.join(leg.path)}</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

            with c_map:
                st.subheader("🗺️ Active Tour Map Overlay")
                fig = plot_delivery_network(g, tsp_res)
                st.pyplot(fig)


# -------------------------------------------------------------
# 8. ALGORITHMIC BENCHMARK SUITE
# -------------------------------------------------------------
elif menu_choice == "📈 Algorithmic Benchmark Suite":
    st.markdown("""
    <div class="brand-banner">
        <div class="brand-title">📈 Empirical Algorithmic Benchmark Suite</div>
        <div class="brand-subtitle">Rigorous High-Resolution time.perf_counter() Profiling Across Input Scales</div>
    </div>
    """, unsafe_allow_html=True)

    reports_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "reports")
    csv_file = os.path.join(reports_dir, "performance_results.csv")

    if st.button("🔄 Execute Fresh Benchmark Harness", type="primary"):
        with st.spinner("Benchmarking Merge Sort, Knapsack DP, Dijkstra, and TSP across N=10, 100, 500..."):
            run_benchmarks(reports_dir)
            st.success("Empirical benchmarks completed and charts updated!")

    if os.path.exists(csv_file):
        df_bench = pd.read_csv(csv_file)
        st.subheader("📊 Empirical Execution Measurements")
        st.dataframe(df_bench, use_container_width=True)

        col_b1, col_b2 = st.columns(2)
        with col_b1:
            st.subheader("Grouped Logarithmic Runtime Comparison")
            bar_img = os.path.join(reports_dir, "performance_runtime_comparison.png")
            if os.path.exists(bar_img):
                st.image(bar_img, use_container_width=True)
        with col_b2:
            st.subheader("Empirical Scaling Growth Curves")
            line_img = os.path.join(reports_dir, "performance_scaling_curves.png")
            if os.path.exists(line_img):
                st.image(line_img, use_container_width=True)

        st.subheader("0/1 Knapsack Capacity Sensitivity (Pseudo-Polynomial Linearity)")
        knap_img = os.path.join(reports_dir, "knapsack_capacity_impact.png")
        if os.path.exists(knap_img):
            st.image(knap_img, use_container_width=True)
    else:
        st.info("No benchmark dataset recorded yet. Click the button above to run benchmarks.")


# -------------------------------------------------------------
# 9. CAPSTONE ARCHITECTURE & VIVA GUIDE
# -------------------------------------------------------------
elif menu_choice == "📚 Capstone Architecture & Viva Guide":
    st.markdown("""
    <div class="brand-banner">
        <div class="brand-title">📚 Capstone Architecture & Viva Defense Manual</div>
        <div class="brand-subtitle">Mathematical First Principles, Complexity Derivations & Viva Voce Preparation</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    ### 🏛️ Architectural Framework
    SwiftRoute AI addresses four foundational algorithmic challenges in physical distribution logistics:
    1. **Parcel Prioritization (Divide & Conquer)**: Stable Merge Sort guarantees $O(n \\log n)$ deterministic urgency ordering.
    2. **Payload Optimization (Dynamic Programming)**: 0/1 Knapsack DP solves cargo value maximization subject to gross vehicle weight constraints in $O(n \\cdot W)$.
    3. **Road Distance Minimization (Greedy Graphs)**: Dijkstra's algorithm with min-heap priority queue computes true shortest road paths in $O((V+E)\\log V)$.
    4. **Fleet Tour Scheduling (Heuristic Approximation)**: Nearest Neighbor TSP constructs closed-loop vehicle itineraries in $O(k^2)$.
    """)

    st.markdown("---")
    st.subheader("⏱️ Asymptotic Complexity Matrix")
    st.markdown("""
    | Operational Stage | Core Algorithm | Design Paradigm | Time Complexity | Auxiliary Space | Key Invariant |
    | :--- | :--- | :--- | :--- | :--- | :--- |
    | **Prioritization** | Merge Sort | Divide & Conquer | $O(n \\log n)$ | $O(n)$ | Strictly stable; multi-criteria deterministic tie-breakers |
    | **Payload Packing** | 0/1 Knapsack | Dynamic Programming | $O(n \\cdot W)$ | $O(n \\cdot W)$ | Bellman principle of optimality; 2D matrix backtracking |
    | **Network Routing** | Dijkstra | Greedy (Min-Heap) | $O((V+E) \\log V)$ | $O(V + E)$ | Non-negative edge weights; triangular relaxation |
    | **Tour Dispatch** | Nearest Neighbor | Greedy TSP Heuristic | $O(k^2)$ | $O(V + E)$ | Fast polynomial approximation for NP-Hard routing |
    """)

    st.markdown("---")
    st.subheader("🎓 High-Yield Viva Voce Questions & Technical Answers")

    with st.expander("Q1: Why choose Merge Sort over Quick Sort for parcel prioritization?"):
        st.write("""
        **Answer:** Merge Sort guarantees a strict worst-case time complexity of $O(n \\log n)$, unlike Quick Sort which degenerates to $O(n^2)$ on unfavorable pivot selections. Crucially, Merge Sort is naturally **stable**, meaning parcels with identical priority and deadline retain their original relative order without unnecessary reshuffling.
        """)

    with st.expander("Q2: Why is the 0/1 Knapsack DP algorithm considered pseudo-polynomial rather than purely polynomial?"):
        st.write("""
        **Answer:** The time complexity is $O(n \\cdot W)$, where $W$ is the numeric capacity of the vehicle. However, the input size of $W$ in binary representation is $b = \\lceil \\log_2 W \\rceil$ bits. Expressed in terms of input length $b$, the complexity is $O(n \\cdot 2^b)$, which is exponential with respect to input bits. Hence, it is pseudo-polynomial.
        """)

    with st.expander("Q3: Can Dijkstra's algorithm handle negative road segment weights?"):
        st.write("""
        **Answer:** No. Dijkstra relies on a greedy premise: once a vertex is extracted from the min-heap, its tentative distance is finalized and will never decrease. Negative edges violate this triangular relaxation invariant, requiring the Bellman-Ford algorithm ($O(V \\cdot E)$) instead. In real-world physical road networks, distances are strictly non-negative ($w(u, v) > 0$).
        """)

    with st.expander("Q4: Why use an Adjacency List rather than an Adjacency Matrix for the road network?"):
        st.write("""
        **Answer:** Physical city road networks are sparse graphs where each junction typically connects to only 2 to 5 roads ($E \\ll V^2$). An Adjacency List occupies $O(V + E)$ memory, whereas an Adjacency Matrix consumes $O(V^2)$ memory regardless of sparsity, leading to excessive space waste.
        """)

    with st.expander("Q5: Does Nearest Neighbor guarantee the optimal Traveling Salesperson tour?"):
        st.write("""
        **Answer:** No. Nearest Neighbor is a greedy heuristic. While it operates efficiently in $O(k^2)$ time, early greedy choices can leave the vehicle stranded far from the depot, forcing an expensive return trip. TSP is NP-Hard, so exact solutions require exponential time ($O(n^2 2^n)$ via Bellman-Held-Karp).
        """)
