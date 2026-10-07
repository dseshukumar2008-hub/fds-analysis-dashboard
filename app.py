import os
import textwrap
import math

import streamlit as st
import pandas as pd
import plotly.express as px


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Game Sales Analytics",
    page_icon="🎮",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# =========================================================
# HELPER
# IMPORTANT: st.html() is used so HTML is rendered as HTML,
# not displayed as a code block.
# =========================================================

def render_html(html):
    st.html(textwrap.dedent(html).strip())


# =========================================================
# CUSTOM CSS
# =========================================================

render_html("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

.stApp {
    background-color: #f8fafc;
    font-family: 'Inter', sans-serif;
}

#MainMenu, footer, header {
    visibility: hidden;
}

.block-container {
    max-width: 1400px;
    padding-top: 2rem;
    padding-bottom: 5rem;
}

/* HERO */
.hero {
    background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%);
    border-radius: 16px;
    padding: 48px 56px;
    position: relative;
    overflow: hidden;
    margin-bottom: 40px;
    box-shadow: 0 10px 25px -5px rgba(15, 23, 42, 0.2);
}

.hero::before {
    content: "";
    position: absolute;
    top: -50%;
    right: -10%;
    width: 600px;
    height: 600px;
    background: radial-gradient(circle, rgba(99,102,241,0.15) 0%, transparent 70%);
    border-radius: 50%;
}

.hero-content {
    position: relative;
    z-index: 2;
}

.hero-badge {
    display: inline-flex;
    align-items: center;
    background: rgba(255, 255, 255, 0.1);
    border: 1px solid rgba(255, 255, 255, 0.2);
    color: #e0e7ff;
    padding: 6px 14px;
    border-radius: 99px;
    font-size: 12px;
    font-weight: 600;
    letter-spacing: 0.05em;
    text-transform: uppercase;
    margin-bottom: 20px;
}

.hero-title {
    color: #ffffff;
    font-size: 48px;
    font-weight: 800;
    letter-spacing: -0.02em;
    margin: 0 0 12px 0;
    line-height: 1.1;
}

.hero-subtitle {
    color: #818cf8;
    font-size: 20px;
    font-weight: 500;
    margin: 0 0 20px 0;
}

.hero-description {
    color: #cbd5e1;
    font-size: 15px;
    line-height: 1.6;
    max-width: 700px;
    margin: 0;
}

/* SECTION HEADERS */
.section-wrapper {
    margin-top: 56px;
    margin-bottom: 24px;
    border-bottom: 1px solid #e2e8f0;
    padding-bottom: 16px;
}

.section-label {
    color: #4f46e5;
    font-size: 13px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-bottom: 8px;
}

.section-header {
    display: flex;
    align-items: center;
    gap: 12px;
}

.section-icon {
    font-size: 24px;
}

.section-title {
    font-size: 28px;
    font-weight: 700;
    color: #0f172a;
    letter-spacing: -0.01em;
    margin: 0;
}

.section-description {
    color: #64748b;
    font-size: 15px;
    margin-top: 8px;
    max-width: 800px;
}

/* KPI CARDS */
.kpi-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 20px;
    margin-bottom: 20px;
}

.kpi-card {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    padding: 24px;
    box-shadow: 0 1px 3px rgba(15, 23, 42, 0.05);
    transition: all 0.2s ease;
    display: flex;
    flex-direction: column;
    position: relative;
    overflow: hidden;
}

.kpi-card:hover {
    box-shadow: 0 10px 15px -3px rgba(15, 23, 42, 0.08);
    border-color: #cbd5e1;
    transform: translateY(-2px);
}

.kpi-card::after {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    width: 4px;
    height: 100%;
    background: #4f46e5;
    opacity: 0;
    transition: opacity 0.2s ease;
}

.kpi-card:hover::after {
    opacity: 1;
}

.kpi-top {
    display: flex;
    align-items: center;
    gap: 12px;
    color: #64748b;
    font-size: 13px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.03em;
    margin-bottom: 16px;
}

.kpi-icon {
    font-size: 20px;
}

.kpi-value {
    font-size: 36px;
    font-weight: 700;
    color: #0f172a;
    line-height: 1.1;
    margin-bottom: 8px;
    letter-spacing: -0.01em;
}

.kpi-footer {
    color: #94a3b8;
    font-size: 13px;
    font-weight: 500;
    margin-top: auto;
}

/* CHART CARDS */
.chart-card {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    padding: 24px;
    box-shadow: 0 1px 3px rgba(15, 23, 42, 0.05);
    margin-bottom: 24px;
    transition: box-shadow 0.2s ease;
}

.chart-card:hover {
    box-shadow: 0 4px 6px -1px rgba(15, 23, 42, 0.08);
}

/* ML RESULT CARDS */
.ml-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 24px;
}

.result-card {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    padding: 32px;
    box-shadow: 0 1px 3px rgba(15, 23, 42, 0.05);
    position: relative;
    overflow: hidden;
}

.result-card::before {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 4px;
    background: linear-gradient(90deg, #3b82f6, #4f46e5);
}

.result-label {
    display: inline-block;
    background: #eff6ff;
    color: #2563eb;
    padding: 4px 12px;
    border-radius: 99px;
    font-size: 12px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-bottom: 16px;
}

.result-title {
    font-size: 24px;
    font-weight: 700;
    color: #0f172a;
    margin: 0 0 12px 0;
}

.result-value {
    font-size: 42px;
    font-weight: 800;
    color: #4f46e5;
    margin: 0 0 16px 0;
    letter-spacing: -0.02em;
}

.result-note {
    color: #64748b;
    font-size: 14px;
    line-height: 1.6;
    margin: 0;
}

/* RQ CARDS */
.rq-card {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    padding: 24px;
    box-shadow: 0 1px 3px rgba(15, 23, 42, 0.05);
    margin-bottom: 24px;
    height: 100%;
    display: flex;
    flex-direction: column;
}

.rq-number {
    display: inline-block;
    background: #f1f5f9;
    color: #0f172a;
    font-size: 13px;
    font-weight: 700;
    padding: 6px 12px;
    border-radius: 6px;
    letter-spacing: 0.02em;
    margin-bottom: 16px;
    width: max-content;
}

.rq-title {
    font-size: 18px;
    font-weight: 600;
    color: #0f172a;
    margin: 0 0 12px 0;
}

.rq-text {
    color: #475569;
    font-size: 15px;
    line-height: 1.6;
    margin: 0;
}

/* INSIGHT CARDS */
.insight-card {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    padding: 24px;
    box-shadow: 0 1px 3px rgba(15, 23, 42, 0.05);
    margin-bottom: 24px;
    border-left: 4px solid #3b82f6;
}

.insight-card.recommendation {
    border-left: 4px solid #8b5cf6;
    background: #faf5ff;
}

.insight-number {
    color: #3b82f6;
    font-size: 12px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-bottom: 8px;
}

.insight-card.recommendation .insight-number {
    color: #8b5cf6;
}

.insight-title {
    font-size: 18px;
    font-weight: 600;
    color: #0f172a;
    margin: 0 0 12px 0;
}

.insight-text {
    color: #475569;
    font-size: 15px;
    line-height: 1.6;
    margin: 0;
}

/* FOOTER */
.dashboard-footer {
    margin-top: 64px;
    padding-top: 32px;
    border-top: 1px solid #e2e8f0;
    text-align: center;
    color: #64748b;
    font-size: 14px;
}
</style>
""")


# =========================================================
# FIND DATASET
# =========================================================

def find_dataset():
    candidates = [
        "vgsales.csv",
        "./data/vgsales.csv",
        "/kaggle/working/vgsales.csv",
        "/content/vgsales.csv",
    ]

    for path in candidates:
        if os.path.exists(path):
            return path

    if os.path.exists("/kaggle/input"):
        for root, _, files in os.walk("/kaggle/input"):
            for file in files:
                if file.lower() == "vgsales.csv":
                    return os.path.join(root, file)

    return None


dataset_path = find_dataset()

if dataset_path is None:
    st.error(
        "vgsales.csv was not found. "
        "Add the dataset to the project root or Streamlit deployment files."
    )
    st.stop()


# =========================================================
# LOAD DATA
# =========================================================

@st.cache_data
def load_data(path):
    data = pd.read_csv(path)

    data["Year"] = pd.to_numeric(
        data["Year"],
        errors="coerce",
    )

    data["Global_Sales"] = pd.to_numeric(
        data["Global_Sales"],
        errors="coerce",
    )

    return data


df = load_data(dataset_path)


# =========================================================
# VALIDATE DATA
# =========================================================

required = [
    "Platform",
    "Year",
    "Genre",
    "Publisher",
    "Global_Sales",
]

missing = [
    column
    for column in required
    if column not in df.columns
]

if missing:
    st.error(f"Missing required columns: {missing}")
    st.stop()


analysis_data = df.dropna(
    subset=required
).copy()


# =========================================================
# HERO
# =========================================================

render_html("""
<div class="hero">
    <div class="hero-content">

        <div class="hero-badge">
            🎮 FOUNDATIONS OF DATA SCIENCE
        </div>

        <div class="hero-title">
            Game Sales Analytics
        </div>

        <div class="hero-subtitle">
            Interactive Analysis & Data Storytelling
        </div>

        <div class="hero-description">
            Explore how platform, genre, publisher and release year
            are associated with variations in global video game sales.
        </div>

    </div>
</div>
""")


# =========================================================
# SECTION 1 — PROJECT OVERVIEW
# =========================================================

render_html("""
<div class="section-wrapper">
    <div class="section-label">Section 01</div>
    <div class="section-header">
        <span class="section-icon">📌</span>
        <h2 class="section-title">Project Overview</h2>
    </div>
    <div class="section-description">
        A high-level snapshot of the complete video game sales dataset.
    </div>
</div>
""")


total_games = len(df)
total_sales = df["Global_Sales"].sum()
average_sales = df["Global_Sales"].mean()
platform_count = df["Platform"].nunique()
genre_count = df["Genre"].nunique()
publisher_count = df["Publisher"].nunique()

valid_years = df["Year"].dropna()
year_min = int(valid_years.min())
year_max = int(valid_years.max())


render_html(f"""
<div class="kpi-grid">
    <div class="kpi-card">
        <div class="kpi-top"><span class="kpi-icon">🎮</span> Dataset Size</div>
        <div class="kpi-value">{total_games:,}</div>
        <div class="kpi-footer">Video game records</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-top"><span class="kpi-icon">🌍</span> Total Global Sales</div>
        <div class="kpi-value">{total_sales:,.1f} M</div>
        <div class="kpi-footer">Worldwide sales</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-top"><span class="kpi-icon">📊</span> Average Sales</div>
        <div class="kpi-value">{average_sales:.3f} M</div>
        <div class="kpi-footer">Average per game</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-top"><span class="kpi-icon">🕹️</span> Platforms</div>
        <div class="kpi-value">{platform_count}</div>
        <div class="kpi-footer">Gaming platforms</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-top"><span class="kpi-icon">🎯</span> Genres</div>
        <div class="kpi-value">{genre_count}</div>
        <div class="kpi-footer">Game categories</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-top"><span class="kpi-icon">🏢</span> Publishers</div>
        <div class="kpi-value">{publisher_count}</div>
        <div class="kpi-footer">Unique publishers</div>
    </div>
</div>
<div style="margin-top:14px; color:#64748b; font-size:14px; font-weight:500;">
    📅 Release-year coverage: <b>{year_min}</b> – <b>{year_max}</b>
</div>
""")


# =========================================================
# SECTION 2 — EXPLORATORY ANALYSIS
# NO FILTER PANEL
# =========================================================

render_html("""
<div class="section-wrapper">
    <div class="section-label">Section 02</div>
    <div class="section-header">
        <span class="section-icon">🔍</span>
        <h2 class="section-title">Exploratory Analysis</h2>
    </div>
    <div class="section-description">
        Analysis of sales distribution, publisher patterns
    and historical release-year trends.
    </div>
</div>
""")


# Full dataset — no filters
filtered = analysis_data.copy()


# =========================================================
# GLOBAL SALES DISTRIBUTION
# =========================================================

render_html('<div class="chart-card">')

st.subheader("📈 Global Sales Distribution")

fig_distribution = px.histogram(
    filtered,
    x="Global_Sales",
    nbins=60,
    labels={"Global_Sales": "Global Sales (millions)"},
)

fig_distribution.update_layout(
    template="plotly_white",
    height=430,
    margin=dict(l=35, r=25, t=20, b=45),
    font=dict(
        family="Inter, Arial",
        color="#344054",
    ),
)

fig_distribution.update_traces(
    hovertemplate="Sales: %{x:.2f} M<br>Games: %{y}<extra></extra>"
)

st.plotly_chart(
    fig_distribution,
    use_container_width=True,
)

render_html('</div>')


# =========================================================
# PUBLISHER + RELEASE YEAR
# =========================================================

publisher_sales = (
    filtered
    .groupby("Publisher")["Global_Sales"]
    .sum()
    .sort_values(ascending=False)
    .head(15)
    .sort_values()
)

year_sales = (
    filtered
    .groupby("Year")["Global_Sales"]
    .sum()
    .sort_index()
)


c1, c2 = st.columns(2, gap="large")


# =========================================================
# PUBLISHER ANALYSIS
# =========================================================

with c1:
    render_html('<div class="chart-card">')

    st.subheader("🏢 Publisher Analysis")

    fig_pub = px.bar(
        publisher_sales.reset_index(),
        x="Global_Sales",
        y="Publisher",
        orientation="h",
        labels={"Global_Sales": "Global Sales (M)"},
    )

    fig_pub.update_layout(
        template="plotly_white",
        height=520,
        margin=dict(l=20, r=20, t=20, b=35),
        font=dict(
            family="Inter, Arial",
            color="#344054",
        ),
    )

    fig_pub.update_traces(
        hovertemplate="<b>%{y}</b><br>"
                      "Global Sales: %{x:.2f} M"
                      "<extra></extra>"
    )

    st.plotly_chart(
        fig_pub,
        use_container_width=True,
    )

    render_html('</div>')


# =========================================================
# RELEASE YEAR
# =========================================================

with c2:
    render_html('<div class="chart-card">')

    st.subheader("📅 Release-Year Trend")

    fig_year = px.line(
        year_sales.reset_index(),
        x="Year",
        y="Global_Sales",
        markers=True,
        labels={
            "Year": "Release Year",
            "Global_Sales": "Global Sales (M)",
        },
    )

    fig_year.update_layout(
        template="plotly_white",
        height=520,
        margin=dict(l=20, r=20, t=20, b=35),
        font=dict(
            family="Inter, Arial",
            color="#344054",
        ),
    )

    fig_year.update_traces(
        line=dict(width=3),
        marker=dict(size=6),
        hovertemplate="<b>Year:</b> %{x}<br>"
                      "<b>Global Sales:</b> %{y:.2f} M"
                      "<extra></extra>",
    )

    st.plotly_chart(
        fig_year,
        use_container_width=True,
    )

    render_html('</div>')


# =========================================================
# SECTION 3 — ADVANCED VISUALIZATIONS
# =========================================================

render_html("""
<div class="section-wrapper">
    <div class="section-label">Section 03</div>
    <div class="section-header">
        <span class="section-icon">✨</span>
        <h2 class="section-title">Advanced Visualizations</h2>
    </div>
    <div class="section-description">
        Additional visual stories from the project's analysis,
    using interactive Plotly visualizations.
    </div>
</div>
""")


# =========================================================
# PLATFORM COMPETITION — RADIAL VIEW
# =========================================================

platform_sales = (
    filtered
    .groupby("Platform")["Global_Sales"]
    .sum()
    .sort_values(ascending=False)
    .head(12)
    .sort_values()
)


render_html('<div class="chart-card">')

st.subheader("🏆 Platform Competition — Radial View")

fig_polar = px.bar_polar(
    platform_sales.reset_index(),
    r="Global_Sales",
    theta="Platform",
    color="Global_Sales",
    color_continuous_scale="Blues",
    labels={
        "Global_Sales": "Global Sales (M)",
        "Platform": "Platform",
    },
)

fig_polar.update_layout(
    template="plotly_white",
    height=560,
    margin=dict(l=25, r=25, t=25, b=25),
    font=dict(
        family="Inter, Arial",
        color="#344054",
    ),
    polar=dict(
        bgcolor="rgba(248,250,252,.65)",
        radialaxis=dict(
            showgrid=True,
            gridcolor="#e4e7ec",
            tickfont=dict(size=10),
        ),
        angularaxis=dict(
            tickfont=dict(size=11),
        ),
    ),
    coloraxis_showscale=False,
    showlegend=False,
)

fig_polar.update_traces(
    hovertemplate="<b>%{theta}</b><br>"
                  "Global Sales: %{r:.2f} M"
                  "<extra></extra>",
    marker_line_width=1,
)

st.plotly_chart(
    fig_polar,
    use_container_width=True,
)

render_html('</div>')


# =========================================================
# GENRE + PLATFORM × GENRE
# =========================================================

advanced_c1, advanced_c2 = st.columns(2, gap="large")


# =========================================================
# GENRE SALES COMPOSITION
# =========================================================

with advanced_c1:

    genre_sales = (
        filtered
        .groupby("Genre")["Global_Sales"]
        .sum()
        .sort_values(ascending=False)
    )

    render_html('<div class="chart-card">')

    st.subheader("🎯 Genre Sales Composition")

    fig_genre = px.pie(
        genre_sales.reset_index(),
        names="Genre",
        values="Global_Sales",
        hole=0.52,
        labels={"Global_Sales": "Global Sales (M)"},
    )

    fig_genre.update_layout(
        template="plotly_white",
        height=500,
        margin=dict(l=20, r=20, t=20, b=20),
        font=dict(
            family="Inter, Arial",
            color="#344054",
        ),
        legend=dict(
            orientation="h",
            y=-0.05,
        ),
    )

    fig_genre.update_traces(
        hovertemplate="<b>%{label}</b><br>"
                      "Global Sales: %{value:.2f} M<br>"
                      "Share: %{percent}"
                      "<extra></extra>"
    )

    st.plotly_chart(
        fig_genre,
        use_container_width=True,
    )

    render_html('</div>')


# =========================================================
# PLATFORM × GENRE HEATMAP
# =========================================================

with advanced_c2:

    render_html('<div class="chart-card">')

    st.subheader("🔥 Platform × Genre Sales Heatmap")

    top_platforms = (
        filtered
        .groupby("Platform")["Global_Sales"]
        .sum()
        .nlargest(15)
        .index
    )

    heat = (
        filtered[
            filtered["Platform"].isin(top_platforms)
        ]
        .pivot_table(
            index="Platform",
            columns="Genre",
            values="Global_Sales",
            aggfunc="sum",
            fill_value=0,
        )
    )

    heat = heat.reindex(top_platforms)

    # Log transform improves visual readability because
    # a few platform-genre combinations dominate.
    heat_log = heat.map(
        lambda x: math.log1p(x)
    )

    fig_heat = px.imshow(
        heat_log,
        aspect="auto",
        color_continuous_scale="Blues",
        labels=dict(
            x="Genre",
            y="Platform",
            color="log(1 + sales)",
        ),
    )

    fig_heat.update_layout(
        template="plotly_white",
        height=500,
        margin=dict(l=20, r=20, t=20, b=35),
        font=dict(
            family="Inter, Arial",
            color="#344054",
        ),
    )

    fig_heat.update_traces(
        customdata=heat.values,
        hovertemplate="<b>Platform:</b> %{y}<br>"
                      "<b>Genre:</b> %{x}<br>"
                      "<b>Global Sales:</b> %{customdata:.2f} M"
                      "<extra></extra>",
    )

    st.plotly_chart(
        fig_heat,
        use_container_width=True,
    )

    render_html('</div>')


# =========================================================
# SECTION 4 — MACHINE LEARNING SUMMARY
# =========================================================

render_html("""
<div class="section-wrapper">
    <div class="section-label">Section 04</div>
    <div class="section-header">
        <span class="section-icon">🤖</span>
        <h2 class="section-title">Machine Learning Summary</h2>
    </div>
    <div class="section-description">
        A concise summary of the machine-learning results obtained in Part 3.
    </div>
</div>
""")


ml1, ml2 = st.columns(2, gap="large")


with ml1:
    render_html("""
    <div class="result-card">
        <div class="result-label">Regression Model</div>
        <div class="result-title">Gradient Boosting</div>
        <div class="result-value">9.29% R²</div>
        <div class="result-note">
            Best testing R² among the evaluated regression models.<br>
            Continuous sales prediction remains limited.
        </div>
    </div>
    """)


with ml2:
    render_html("""
    <div class="result-card">
        <div class="result-label">Classification Model</div>
        <div class="result-title">Support Vector Machine (SVM)</div>
        <div class="result-value">88.51% ACC</div>
        <div class="result-note">
            Highest testing accuracy among the evaluated classification models.
        </div>
    </div>
    """)


# =========================================================
# MODEL COMPARISON
# =========================================================

with st.expander("View complete model comparisons"):

    t1, t2 = st.columns(2)

    with t1:
        st.markdown("#### Regression")

        st.dataframe(
            pd.DataFrame({
                "Model": [
                    "Gradient Boosting",
                    "Linear Regression",
                    "Random Forest",
                ],
                "Training R² (%)": [
                    23.22,
                    16.08,
                    64.72,
                ],
                "Testing R² (%)": [
                    9.29,
                    9.00,
                    4.29,
                ],
            }),
            use_container_width=True,
            hide_index=True,
        )

    with t2:
        st.markdown("#### Classification")

        st.dataframe(
            pd.DataFrame({
                "Model": [
                    "SVM",
                    "Logistic Regression",
                    "Random Forest",
                ],
                "Training Accuracy (%)": [
                    88.09,
                    87.64,
                    94.49,
                ],
                "Testing Accuracy (%)": [
                    88.51,
                    88.36,
                    86.19,
                ],
            }),
            use_container_width=True,
            hide_index=True,
        )


# =========================================================
# SECTION 5 — RESEARCH QUESTION FINDINGS
# =========================================================

render_html("""
<div class="section-wrapper">
    <div class="section-label">Section 05</div>
    <div class="section-header">
        <span class="section-icon">🎯</span>
        <h2 class="section-title">Research Question Findings</h2>
    </div>
    <div class="section-description">
        The main conclusions drawn from the complete analytical workflow.
    </div>
</div>
""")


rq_cards = [
    (
        "RQ1",
        "Platform Differences",
        "Global video game sales differ substantially across "
        "platforms, indicating clear variation in overall "
        "platform-level sales performance.",
    ),
    (
        "RQ2",
        "Game Characteristics",
        "Sales vary across genres, publishers, release years "
        "and platform–genre combinations.",
    ),
    (
        "RQ3",
        "Machine-Learning Performance",
        "Gradient Boosting achieved the highest regression "
        "testing R² of 9.29%, while SVM achieved the highest "
        "classification testing accuracy of 88.51%.",
    ),
    (
        "RQ4",
        "Platform Competition & Historical Trends",
        "Platform and release-year patterns vary across "
        "different periods of the video game industry.",
    ),
]


for start in [0, 2]:
    a, b = st.columns(2, gap="large")

    for col, item in zip(
        [a, b],
        rq_cards[start:start + 2],
    ):
        with col:
            render_html(f"""
            <div class="rq-card">
                <div class="rq-number">{item[0]}</div>
                <div class="rq-title">{item[1]}</div>
                <div class="rq-text">{item[2]}</div>
            </div>
            """)


# =========================================================
# SECTION 6 — KEY INSIGHTS & RECOMMENDATIONS
# =========================================================

render_html("""
<div class="section-wrapper">
    <div class="section-label">Section 06</div>
    <div class="section-header">
        <span class="section-icon">💡</span>
        <h2 class="section-title">Key Insights & Recommendations</h2>
    </div>
    <div class="section-description">
        The final visual story derived from the project's analysis.
    </div>
</div>
""")


insights = [
    (
        "Insight 01",
        "Sales are highly uneven",
        "A relatively small number of games achieve very high "
        "sales, while most titles have comparatively low sales.",
    ),
    (
        "Insight 02",
        "Platform differences are substantial",
        "Gaming platforms show noticeably different overall "
        "sales performance.",
    ),
    (
        "Insight 03",
        "Game characteristics matter",
        "Genre, publisher, release year and platform–genre "
        "combinations are associated with different sales patterns.",
    ),
    (
        "Insight 04",
        "Historical trends are important",
        "Release-year analysis shows changing sales patterns "
        "across different periods of the gaming industry.",
    ),
    (
        "Insight 05",
        "Classification performs better",
        "SVM achieved 88.51% testing accuracy, while the best "
        "regression model achieved only 9.29% testing R².",
    ),
    (
        "Recommendation",
        "Improve future prediction",
        "Future models could include additional non-leaking "
        "game characteristics and contextual variables.",
    ),
]


for start in [0, 2, 4]:
    a, b = st.columns(2, gap="large")

    for col, item in zip(
        [a, b],
        insights[start:start + 2],
    ):
        with col:
            render_html(f"""
            <div class="insight-card {'recommendation' if 'Recommendation' in item[0] else ''}">
                <div class="insight-number">{item[0]}</div>
                <div class="insight-title">{item[1]}</div>
                <div class="insight-text">{item[2]}</div>
            </div>
            """)


# =========================================================
# FOOTER
# =========================================================

render_html("""
<div class="dashboard-footer">
    🎮 <b>Game Sales Analytics</b>
    &nbsp;•&nbsp;
    Foundations of Data Science Project
    <br>
    Interactive visualization, analysis and data storytelling
</div>
""")
