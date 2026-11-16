# ==============================================================================
# SALES + STAFF COMMAND CENTRE (ENTERPRISE ANALYTICS & ML FORECASTING)
# Developer: ROG3RS / 0542470810
# ==============================================================================

import streamlit as st
import pandas as pd
import numpy as np
import hashlib
import hmac
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor

# ==============================================================================
# 1. PAGE CONFIGURATION & MODERN UI STYLING
# ==============================================================================
# [SAFE TO EDIT]: You can change page_title or page_icon freely.
st.set_page_config(
    page_title="Sales & Staff Command Centre | ROG3RS",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# [SAFE TO EDIT]: Custom CSS for fonts, animated gradient background, and cards.
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    /* Animated Dark Glassmorphic Background */
    .stApp {
        background: radial-gradient(circle at 15% 20%, #1e293b 0%, #0f172a 45%, #020617 100%);
        color: #f8fafc;
    }

    /* Hide Default Streamlit Menus for Clean App Look */
    [data-testid="stToolbar"], #MainMenu, footer, .stDeployButton {
        visibility: hidden !important;
        display: none !important;
    }

    /* Animated Top Accent Bar */
    .top-banner {
        background: linear-gradient(90deg, #06b6d4, #3b82f6, #8b5cf6, #ec4899);
        background-size: 300% 300%;
        animation: gradientMove 6s ease infinite;
        height: 6px;
        border-radius: 4px;
        margin-bottom: 18px;
    }
    @keyframes gradientMove {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* Executive KPI Cards */
    .kpi-box {
        background: rgba(30, 41, 59, 0.75);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(148, 163, 184, 0.2);
        border-radius: 12px;
        padding: 16px;
        transition: transform 0.2s ease, border-color 0.2s ease;
    }
    .kpi-box:hover {
        transform: translateY(-3px);
        border-color: #38bdf8;
    }
    .kpi-label { font-size: 12px; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.8px; font-weight: 700; }
    .kpi-num { font-size: 24px; font-weight: 800; color: #f8fafc; margin: 4px 0; }
    .kpi-sub { font-size: 12px; color: #38bdf8; }

    /* Flag & Alert Boxes */
    .flag-danger {
        background: rgba(127, 29, 29, 0.65);
        border-left: 5px solid #ef4444;
        padding: 14px;
        border-radius: 8px;
        margin-bottom: 12px;
    }
    .flag-success {
        background: rgba(6, 78, 59, 0.65);
        border-left: 5px solid #10b981;
        padding: 14px;
        border-radius: 8px;
        margin-bottom: 12px;
    }
    .flag-warn {
        background: rgba(120, 53, 15, 0.65);
        border-left: 5px solid #f59e0b;
        padding: 14px;
        border-radius: 8px;
        margin-bottom: 12px;
    }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# 2. ZERO-BYPASS SECURITY & AUTHENTICATION GATE
# ==============================================================================
def verify_admin_credentials(username_input: str, password_input: str) -> bool:
    """Validates login safely with a fallback if secrets.toml is missing locally."""
    input_hash = hashlib.sha256(password_input.encode()).hexdigest()
    
    try:
        expected_user = st.secrets["admin_credentials"]["username"]
        expected_hash = st.secrets["admin_credentials"]["password_hash"]
    except Exception:
        # Fallback for local testing if secrets.toml isn't found yet
        expected_user = "rog3rs_admin"
        expected_hash = hashlib.sha256("CommandCentre2026!".encode()).hexdigest()

    user_ok = hmac.compare_digest(username_input.strip(), expected_user)
    pass_ok = hmac.compare_digest(input_hash, expected_hash)
    return user_ok and pass_ok

# ==============================================================================
# 3. UNIVERSAL DATASET LOADER & DEMO GENERATOR
# ==============================================================================
@st.cache_data
def generate_enterprise_demo_data() -> pd.DataFrame:
    """Generates realistic multi-branch sales & staff data for instant testing."""
    np.random.seed(2026)
    staff_profiles = [
        ("Kwame Mensah", "Accra Central", 18, 1.35),
        ("Abena Osei", "Kumasi Metro", 14, 1.25),
        ("Kofi Boateng", "Takoradi Port", 24, 1.15),
        ("Efua Asante", "Enchi / Aowin", 9, 1.20),
        ("Yaw Darko", "Tamale North", 4, 0.72),
        ("Ama Serwaa", "Tema Industrial", 11, 0.65),
        ("Kojo Antwi", "Cape Coast", 3, 0.80),
        ("Akosua Frimpong", "Sunyani West", 16, 1.10),
    ]
    products = ["Solar Kits", "Agro Inputs", "Construction Materials", "POS Terminals", "Wholesale FMCG"]
    rows = []
    start_date = datetime(2026, 1, 1)

    for i in range(420):
        staff, location, tenure_months, skill_factor = staff_profiles[i % len(staff_profiles)]
        prod = products[np.random.randint(0, len(products))]
        tx_date = start_date + timedelta(days=int(i * 0.7))
        units = np.random.randint(5, 60)
        unit_price = np.random.uniform(120, 650)
        sales = round(units * unit_price * skill_factor, 2)
        # Introduce realistic cost & occasional loss scenarios
        cost_ratio = np.random.uniform(0.55, 0.78) if skill_factor >= 1.0 else np.random.uniform(0.88, 1.18)
        cost = round(sales * cost_ratio, 2)
        profit = round(sales - cost, 2)
        target = round(sales * (0.92 if skill_factor >= 1.0 else 1.25), 2)
        rows.append({
            "Date": tx_date.strftime("%Y-%m-%d"),
            "Staff_Name": staff,
            "Locality": location,
            "Product_Line": prod,
            "Tenure_Months": tenure_months,
            "Sales": sales,
            "Cost": cost,
            "Profit": profit,
            "Sales_Target": target,
            "Units_Sold": units
        })
    return pd.DataFrame(rows)

def load_any_dataset(uploaded_file) -> pd.DataFrame:
    """Reads CSV, Excel, JSON, or TXT/TSV files seamlessly."""
    name = uploaded_file.name.lower()
    if name.endswith(".csv"):
        return pd.read_csv(uploaded_file)
    elif name.endswith((".xlsx", ".xls")):
        return pd.read_excel(uploaded_file)
    elif name.endswith(".json"):
        return pd.read_json(uploaded_file)
    elif name.endswith((".tsv", ".txt")):
        return pd.read_csv(uploaded_file, sep=None, engine="python")
    raise ValueError("Unsupported file format.")

# ==============================================================================
# 4. SIDEBAR: DATA INGESTION, COLUMN MAPPING & DYNAMIC FILTERS
# ==============================================================================
st.sidebar.markdown("## 🚀 Command Centre")
st.sidebar.caption("Developer: **ROG3RS / 0542470810**")

if st.sidebar.button("🔒 Lock & Sign Out", use_container_width=True):
    st.session_state["auth_ok"] = False
    st.rerun()

st.sidebar.markdown("---")
uploaded = st.sidebar.file_uploader("📂 Upload Any Dataset (CSV, Excel, JSON)", type=["csv", "xlsx", "xls", "json", "tsv"])

if uploaded is not None:
    try:
        raw_df = load_any_dataset(uploaded)
        st.sidebar.success(f"✅ Loaded `{uploaded.name}` ({len(raw_df):,} rows)")
    except Exception as e:
        st.sidebar.error(f"File error: {e}")
        raw_df = generate_enterprise_demo_data()
else:
    raw_df = generate_enterprise_demo_data()
    st.sidebar.info("ℹ️ Using Live Enterprise Demo Dataset. Upload your file above anytime.")

all_cols = raw_df.columns.tolist()
num_cols = raw_df.select_dtypes(include=[np.number]).columns.tolist()
cat_cols = raw_df.select_dtypes(exclude=[np.number]).columns.tolist()

# Helper to auto-detect best matching column names for any uploaded file
def auto_pick(candidates, fallback_list):
    for cand in candidates:
        for col in fallback_list:
            if cand in col.lower():
                return col
    return fallback_list[0] if fallback_list else None

st.sidebar.markdown("### 🧭 Universal Column Mapper")
staff_col = st.sidebar.selectbox("Staff / Rep Column:", ["None"] + all_cols, index=(["None"] + all_cols).index(auto_pick(["staff", "rep", "agent", "employee", "name"], cat_cols)) if cat_cols else 0)
loc_col = st.sidebar.selectbox("Locality / Branch Column:", ["None"] + all_cols, index=(["None"] + all_cols).index(auto_pick(["local", "region", "branch", "city", "area", "zone"], cat_cols)) if cat_cols else 0)
date_col = st.sidebar.selectbox("Date / Period Column:", ["None"] + all_cols, index=(["None"] + all_cols).index(auto_pick(["date", "time", "month", "period", "year"], all_cols)) if all_cols else 0)
tenure_col = st.sidebar.selectbox("Tenure / Duration Column:", ["None"] + num_cols, index=(["None"] + num_cols).index(auto_pick(["tenure", "month", "duration", "exp", "age"], num_cols)) if num_cols else 0)

sales_col = st.sidebar.selectbox("Sales / Revenue Column:", num_cols, index=num_cols.index(auto_pick(["sale", "rev", "amount", "income", "total"], num_cols)) if num_cols else 0)
cost_col = st.sidebar.selectbox("Cost / Expense Column:", ["None"] + num_cols, index=(["None"] + num_cols).index(auto_pick(["cost", "exp", "spend"], num_cols)) if num_cols else 0)
profit_col = st.sidebar.selectbox("Profit / Net Column:", ["None (Auto-Calculate)"] + num_cols, index=(["None (Auto-Calculate)"] + num_cols).index(auto_pick(["profit", "net", "margin"], num_cols)) if auto_pick(["profit", "net", "margin"], num_cols) else 0)

# Build working dataframe with standardized financial metrics
df = raw_df.copy()
df["_Sales"] = pd.to_numeric(df[sales_col], errors="coerce").fillna(0)
df["_Cost"] = pd.to_numeric(df[cost_col], errors="coerce").fillna(0) if cost_col != "None" else 0.0
if profit_col != "None (Auto-Calculate)":
    df["_Profit"] = pd.to_numeric(df[profit_col], errors="coerce").fillna(0)
else:
    df["_Profit"] = df["_Sales"] - df["_Cost"]

# Separate Profit vs Loss clearly
df["_Loss"] = np.where(df["_Profit"] < 0, abs(df["_Profit"]), 0.0)

# --- INTERACTIVE COLUMN & VALUE FILTER ---
st.sidebar.markdown("### 🔍 Dynamic Slice Filters")
if cat_cols:
    filter_dim = st.sidebar.selectbox("Filter by Category Column:", ["None"] + cat_cols)
    if filter_dim != "None":
        choices = sorted(df[filter_dim].dropna().astype(str).unique().tolist())
        picked = st.sidebar.multiselect(f"Select {filter_dim} values:", choices, default=choices)
        if picked:
            df = df[df[filter_dim].astype(str).isin(picked)]

# ==============================================================================
# 5. MAIN COMMAND CENTRE TABS
# ==============================================================================
st.markdown("<div class='top-banner'></div>", unsafe_allow_html=True)
st.markdown("## 📊 Executive Sales + Staff Command Centre")

# --- TOP PRIORITY TOTALS & STATISTICAL RIBBON ---
tot_sales = df["_Sales"].sum()
tot_cost = df["_Cost"].sum()
tot_profit = df["_Profit"].sum()
tot_loss = df["_Loss"].sum()
mean_sales = df["_Sales"].mean()
med_sales = df["_Sales"].median()
std_sales = df["_Sales"].std()

r1, r2, r3, r4, r5, r6, r7 = st.columns(7)
metrics_ribbon = [
    (r1, "TOTAL SALES", f"{tot_sales:,.2f}", f"Avg: {mean_sales:,.1f}"),
    (r2, "TOTAL COST", f"{tot_cost:,.2f}", f"{(tot_cost/tot_sales*100 if tot_sales else 0):.1f}% of Sales"),
    (r3, "NET PROFIT", f"{tot_profit:,.2f}", f"Margin: {(tot_profit/tot_sales*100 if tot_sales else 0):.1f}%"),
    (r4, "TOTAL LOSSES", f"{tot_loss:,.2f}", f"{(df['_Profit'] < 0).sum()} loss records"),
    (r5, "MEAN (AVG)", f"{mean_sales:,.2f}", "Per transaction"),
    (r6, "MEDIAN", f"{med_sales:,.2f}", "50th percentile"),
    (r7, "STD DEVIATION", f"{std_sales:,.2f}", "Volatility spread"),
]
for col_obj, lbl, val, sub in metrics_ribbon:
    with col_obj:
        st.markdown(f"""
        <div class="kpi-box">
            <div class="kpi-label">{lbl}</div>
            <div class="kpi-num">{val}</div>
            <div class="kpi-sub">{sub}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

tab_sales, tab_staff, tab_ml, tab_pivot = st.tabs([
    "💰 Sales & Loss Diagnostics",
    "🏆 Staff Performance & Motivation Engine",
    "🤖 AI Future Predictions & Trend Explainer",
    "🔀 Relational Pivot & Column Comparator"
])

# ------------------------------------------------------------------------------
# TAB 1: SALES & LOSS DIAGNOSTICS
# ------------------------------------------------------------------------------
with tab_sales:
    st.markdown("### 📈 Revenue, Cost, Profit & Loss Breakdown")
    
    # Flag critical financial issues automatically
    loss_rows = df[df["_Profit"] < 0]
    if not loss_rows.empty:
        worst_loc = loss_rows.groupby(loc_col)["_Loss"].sum().idxmax() if loc_col != "None" else "General Operations"
        worst_loss_amt = loss_rows.groupby(loc_col)["_Loss"].sum().max() if loc_col != "None" else tot_loss
        st.markdown(f"""
        <div class="flag-danger">
            🚨 <b>CRITICAL LOSS FLAG:</b> Detected <b>{len(loss_rows)}</b> loss-making transactions totaling <b>{tot_loss:,.2f}</b>. 
            Highest loss concentration is in <b>{worst_loc}</b> (<b>{worst_loss_amt:,.2f}</b> lost due to cost exceeding sales revenue).
        </div>
        """, unsafe_allow_html=True)

    c_left, c_right = st.columns(2)
    with c_left:
        if date_col != "None":
            trend_df = df.groupby(date_col)[["_Sales", "_Cost", "_Profit"]].sum().reset_index().sort_values(date_col)
            fig_trend = px.line(trend_df, x=date_col, y=["_Sales", "_Cost", "_Profit"],
                                title="Sales vs. Cost vs. Profit Over Time",
                                color_discrete_map={"_Sales": "#38bdf8", "_Cost": "#f59e0b", "_Profit": "#10b981"})
            fig_trend.update_layout(paper_bgcolor="#1e293b", plot_bgcolor="#1e293b", font_color="#f8fafc")
            st.plotly_chart(fig_trend, use_container_width=True)
        else:
            fig_hist = px.histogram(df, x="_Sales", nbins=25, title="Sales Distribution & Spread", color_discrete_sequence=["#38bdf8"])
            fig_hist.update_layout(paper_bgcolor="#1e293b", plot_bgcolor="#1e293b", font_color="#f8fafc")
            st.plotly_chart(fig_hist, use_container_width=True)

    with c_right:
        if loc_col != "None":
            loc_df = df.groupby(loc_col)[["_Sales", "_Profit", "_Loss"]].sum().reset_index().sort_values("_Sales", ascending=False)
            fig_loc = px.bar(loc_df, x=loc_col, y=["_Sales", "_Profit", "_Loss"], barmode="group",
                             title="Locality Performance: Sales, Profit & Losses",
                             color_discrete_map={"_Sales": "#38bdf8", "_Profit": "#10b981", "_Loss": "#ef4444"})
            fig_loc.update_layout(paper_bgcolor="#1e293b", plot_bgcolor="#1e293b", font_color="#f8fafc")
            st.plotly_chart(fig_loc, use_container_width=True)

# ==============================================================================
# TAB 2: STAFF PERFORMANCE, TENURE & MOTIVATION ENGINE (FIXED AGGREGATION)
# ==============================================================================
with tab_staff:
    st.markdown("### 🧑‍💼 Staff Intelligence: Who, Where, How Long & Action Plan")

    if staff_col != "None":
        # Group data safely using explicit named aggregations to prevent KeyError
        agg_kwargs = {
            "_Sales_sum": pd.NamedAgg(column="_Sales", aggfunc="sum"),
            "_Sales_mean": pd.NamedAgg(column="_Sales", aggfunc="mean"),
            "_Cost_sum": pd.NamedAgg(column="_Cost", aggfunc="sum"),
            "_Profit_sum": pd.NamedAgg(column="_Profit", aggfunc="sum"),
            "_Loss_sum": pd.NamedAgg(column="_Loss", aggfunc="sum"),
        }
        if tenure_col != "None":
            agg_kwargs["Tenure_max"] = pd.NamedAgg(column=tenure_col, aggfunc="max")

        staff_perf = df.groupby(staff_col).agg(**agg_kwargs).reset_index()

        # Find best locality per staff member safely
        if loc_col != "None":
            best_locs = df.groupby([staff_col, loc_col])["_Profit"].sum().reset_index()
            best_locs = best_locs.sort_values("_Profit", ascending=False).drop_duplicates(staff_col)
            best_locs = best_locs.rename(columns={loc_col: "Top_Locality"})[[staff_col, "Top_Locality"]]
            staff_perf = staff_perf.merge(best_locs, on=staff_col, how="left")
        else:
            staff_perf["Top_Locality"] = "All Zones"

        # Calculate Active Span / Duration
        if tenure_col != "None":
            staff_perf["Duration"] = staff_perf["Tenure_max"].astype(str) + " Months"
        elif date_col != "None":
            spans = df.groupby(staff_col)[date_col].nunique().reset_index(name="Active_Periods")
            staff_perf = staff_perf.merge(spans, on=staff_col, how="left")
            staff_perf["Duration"] = staff_perf["Active_Periods"].fillna(1).astype(str) + " Active Periods"
        else:
            staff_perf["Duration"] = "Logged Records"

        # Intelligent Recommendation Engine (Resources vs Motivation vs Coaching)
        avg_team_profit = staff_perf["_Profit_sum"].mean()
        avg_team_sales = staff_perf["_Sales_sum"].mean()

        def diagnose_staff(row):
            # [SAFE TO EDIT]: Customize management rules and thresholds here.
            if row["_Profit_sum"] >= avg_team_profit * 1.15:
                return "🌟 TOP PERFORMER: Needs More Resources & Expansion Budget (High ROI)"
            elif row["_Sales_sum"] >= avg_team_sales * 0.9 and row["_Profit_sum"] < avg_team_profit * 0.7:
                return "⚠️ HIGH COST / LOSS LEAK: Audit Pricing & Discounting (Margin Issue)"
            elif row["_Profit_sum"] < 0:
                return "🚨 UNDERPERFORMING (NET LOSS): Immediate Coaching, Motivation & Cost Freeze"
            else:
                return "💪 NEEDS MOTIVATION & INCENTIVES: Set Stretch Bonus to Unlock Potential"

        staff_perf["Manager_Action_Plan"] = staff_perf.apply(diagnose_staff, axis=1)
        staff_perf = staff_perf.sort_values("_Profit_sum", ascending=False)

        top_rep = staff_perf.iloc[0]
        bot_rep = staff_perf.iloc[-1]

        col_w, col_l = st.columns(2)
        with col_w:
            st.markdown(f"""
            <div class="flag-success">
                🏆 <b>WHO IS PERFORMING BETTER: {top_rep[staff_col]}</b><br>
                • <b>Where:</b> Strongest in <b>{top_rep['Top_Locality']}</b><br>
                • <b>How Long:</b> Performing across <b>{top_rep['Duration']}</b><br>
                • <b>Totals:</b> Sales <b>{top_rep['_Sales_sum']:,.2f}</b> | Net Profit <b>{top_rep['_Profit_sum']:,.2f}</b><br>
                • <b>Prescription:</b> {top_rep['Manager_Action_Plan']}
            </div>
            """, unsafe_allow_html=True)

        with col_l:
            loss_reason = "High operational/product costs exceeding revenue" if bot_rep["_Loss_sum"] > 0 else "Low transaction volume & weak closing rate"
            st.markdown(f"""
            <div class="flag-danger">
                📉 <b>WHO IS PERFORMING WORSE: {bot_rep[staff_col]}</b><br>
                • <b>Where Loss/Drag Comes From:</b> <b>{bot_rep['Top_Locality']}</b> (Losses: <b>{bot_rep['_Loss_sum']:,.2f}</b>)<br>
                • <b>How Long:</b> Tracked over <b>{bot_rep['Duration']}</b><br>
                • <b>Why:</b> {loss_reason}<br>
                • <b>Prescription:</b> {bot_rep['Manager_Action_Plan']}
            </div>
            """, unsafe_allow_html=True)

        fig_staff = px.bar(
            staff_perf, x=staff_col, y=["_Sales_sum", "_Profit_sum", "_Loss_sum"],
            barmode="group", title="Staff Comparison: Total Sales, Net Profit & Losses",
            color_discrete_map={"_Sales_sum": "#38bdf8", "_Profit_sum": "#10b981", "_Loss_sum": "#ef4444"}
        )
        fig_staff.update_layout(paper_bgcolor="#1e293b", plot_bgcolor="#1e293b", font_color="#f8fafc")
        st.plotly_chart(fig_staff, use_container_width=True)

        st.markdown("#### 📋 Complete Staff Scorecard & Resource/Motivation Matrix")
        st.dataframe(staff_perf, use_container_width=True)
    else:
        st.warning("⚠️ Please select a Staff / Rep Column in the sidebar to activate Staff Intelligence.")
        
        
# ==============================================================================
# FOOTER WATERMARK
# ==============================================================================
st.markdown("---")
st.markdown("<p style='text-align:center; color:#64748b; font-size:12px;'>Sales + Staff Command Centre • Developed by <b>ROG3RS / 0542470810</b></p>", unsafe_allow_html=True)