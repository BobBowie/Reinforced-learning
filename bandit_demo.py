# bandit_demo.py
import streamlit as st
import numpy as np
import pandas as pd
import altair as alt

# ---------------------------------------
# App config
# ---------------------------------------
st.set_page_config(page_title="Bandit Time Machine", layout="wide")
st.caption("App loaded ✅")

# ---------------------------------------
# Design tokens
# ---------------------------------------
COLORS = {
    "INK_900": "#0B0F14",
    "INK_700": "#1F2933",
    "INK_500": "#3E4C59",
    "FOG_050": "#FAFBFD",
    "FOG_100": "#F5F7FA",
    "FOG_200": "#E4E7EB",
    "ACCENT_1": "#2F6FED",   # blue
    "ACCENT_2": "#16A085",   # teal/green
    "ACCENT_3": "#7B61FF",
    "ACCENT_4": "#F2C94C",
    "ACCENT_BAD": "#D64545",
}

AXIS_FONT = 'Courier New, ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", monospace'
BODY_FONT = 'Inter, "IBM Plex Sans", system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif'

# Chart heights
H_TRAFFIC = 560
H_SCATTER = 460
H_RL_LINE = 400

# Spacer to mirror RL controls so the tables align
CONTROLS_ROW_PX = 72  # ~height of epsilon slider + button row

# ---------------------------------------
# Global CSS (body text)
# ---------------------------------------
st.markdown(f"""
<style>
  html, body, [class*="css"] {{
    font-family: {BODY_FONT};
    color: {COLORS["INK_700"]};
    background-color: {COLORS["FOG_100"]};
  }}
  .stMetric {{ background:#fff; border:1px solid {COLORS["FOG_200"]}; border-radius:10px; padding:12px; }}
  .dataframe {{ font-variant-numeric: tabular-nums; }}
  .dataframe th {{ background-color:{COLORS["FOG_050"]} !important; font-weight:600; }}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------
# Altair theme — high-contrast “MatLab-ish”
# ---------------------------------------
def lab_theme():
    return {
        "config": {
            "font": AXIS_FONT,
            "view": {"stroke": "black", "strokeWidth": 1},
            "axis": {
                "grid": True,
                "gridColor": "#efefef",     # very light grid
                "gridOpacity": 0.6,
                "domainColor": "black",
                "tickColor": "black",
                "labelFont": AXIS_FONT,
                "titleFont": AXIS_FONT,
                "labelFontSize": 13,        # bigger labels
                "titleFontSize": 16,        # bigger titles
                "labelColor": "#000",       # dark
                "titleColor": "#000",
            },
            "legend": {
                "labelFont": AXIS_FONT,
                "titleFont": AXIS_FONT,
                "labelFontSize": 13,
                "titleFontSize": 14,
                "labelColor": "#000",
                "titleColor": "#000",
                "symbolType": "circle",     # default symbol shape
                "orient": "top",
            },
            "title": {
                "font": AXIS_FONT,
                "fontSize": 22,
                "fontWeight": "bold",
                "color": "#000",
            },
            "range": {"category": {"scheme": "tableau10"}},
            "point": {
                "filled": True,             # filled points = clearer
                "size": 110,
                "stroke": "black",
                "strokeWidth": 1.2,
                "opacity": 1.0,
            },
            "line": {"strokeWidth": 2.6},
        }
    }

alt.themes.register("lab", lab_theme)
alt.themes.enable("lab")

# Category color scale with your domain
subject_palette = alt.Scale(
    domain=[
        "Limited Time Offer!",
        "You Won't Believe This...",
        "Exclusive Deal Inside",
        "Last Chance to Save",
        "Free Gift Waiting",
    ],
    scheme="tableau10",
)

# ---------------------------------------
# Helpers
# ---------------------------------------
def render_kpis(total_emails, total_conversions):
    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("Total Emails Sent", f"{total_emails:,}" if total_emails is not None else "—")
    with c2:
        st.metric("Total Conversions", f"{total_conversions:,}" if total_conversions is not None else "—")
    with c3:
        if (total_emails or 0) > 0 and (total_conversions is not None):
            st.metric("Conversion Rate", f"{(total_conversions/total_emails)*100:.2f}%")
        else:
            st.metric("Conversion Rate", "—")

def stacked_traffic_chart(df, conv_color, remainder_color, *, label_color="white", label_side=False):
    """
    Stacked column chart: Conversions vs remainder (Traffic - Conversions).
    label_side=False -> white labels centered inside the conversion segment.
    label_side=True  -> colored labels placed to the right of the column (callouts).
    """
    if df is None or df.empty:
        return alt.Chart(pd.DataFrame({"x":[0]})).mark_text(text="No data", font=AXIS_FONT).properties(height=H_TRAFFIC)

    plot_df = df.copy()
    plot_df["ConvRate"] = (plot_df["Conversions"] / plot_df["Traffic"]).fillna(0)
    plot_df["HalfConv"] = plot_df["Conversions"] / 2.0
    plot_df["LabelY"] = np.maximum(plot_df["Conversions"], 40)

    x_enc = alt.X("Subject:N", sort=None, title="Subject")
    y_abs = alt.Y("Traffic:Q", axis=alt.Axis(title="Emails Sent"))

    conv_bar = (
        alt.Chart(plot_df)
        .mark_bar(size=34, color=conv_color)
        .encode(
            x=x_enc,
            y=alt.Y("Conversions:Q", axis=alt.Axis(title="Emails Sent")),
            y2=alt.Y2(value=0),
            tooltip=[
                alt.Tooltip("Subject:N"),
                alt.Tooltip("Traffic:Q", title="Total Sent"),
                alt.Tooltip("Conversions:Q", title="Conversions"),
                alt.Tooltip("ConvRate:Q", title="Conversion Rate", format=".1%"),
            ],
        )
    )

    remainder_bar = (
        alt.Chart(plot_df)
        .mark_bar(size=34, color=remainder_color)
        .encode(x=x_enc, y=y_abs, y2="Conversions:Q")
    )

    if label_side:
        labels = (
            alt.Chart(plot_df)
            .mark_text(align="left", baseline="middle", dx=4, color=label_color,
                       font=AXIS_FONT, fontWeight="bold", fontSize=13)
            .encode(
                x=alt.X("Subject:N", sort=None, title="Subject", bandPosition=0.65),
                y=alt.Y("LabelY:Q"),
                text=alt.Text("ConvRate:Q", format=".0%"),
            )
        )
    else:
        labels = (
            alt.Chart(plot_df)
            .mark_text(color=label_color, font=AXIS_FONT, fontWeight="bold", fontSize=12, dy=8)
            .encode(
                x=x_enc,
                y=alt.Y("HalfConv:Q"),
                text=alt.Text("ConvRate:Q", format=".0%"),
            )
        )

    bars = (conv_bar + remainder_bar).properties(height=H_TRAFFIC)
    return bars + labels

def build_reward_scatter(df, title_suffix):
    agg = df.groupby("Subject").agg(Chosen=("Reward","count"), Conversions=("Reward","sum")).reset_index()
    total_chosen = max(int(agg["Chosen"].sum()), 1)
    agg["Traffic_Share"] = agg["Chosen"] / total_chosen
    agg["Conv_Rate"] = np.where(agg["Chosen"] > 0, agg["Conversions"] / agg["Chosen"], 0.0)

    pts = (
        alt.Chart(agg, title=title_suffix)
        .mark_point(filled=True, size=110, stroke='black', strokeWidth=1.2, opacity=1.0)
        .encode(
            x=alt.X("Traffic_Share:Q", axis=alt.Axis(format="%"), title="Traffic Share"),
            y=alt.Y("Conv_Rate:Q", axis=alt.Axis(format="%"), title="Empirical Conversion Rate"),
            color=alt.Color(
                "Subject:N",
                title="Subject Line",
                scale=subject_palette,
                # Legend symbols that match the plotted points
                legend=alt.Legend(
                    symbolType="circle",
                    symbolStrokeColor="black",
                    symbolStrokeWidth=1.2,
                    symbolSize=200,
                ),
            ),
            tooltip=[
                alt.Tooltip("Subject:N"),
                alt.Tooltip("Chosen:Q", title="Emails Sent"),
                alt.Tooltip("Conversions:Q", title="Conversions"),
                alt.Tooltip("Traffic_Share:Q", title="Traffic Share", format=".1%"),
                alt.Tooltip("Conv_Rate:Q", title="Empirical Rate", format=".1%"),
            ]
        )
        .properties(height=H_SCATTER)
    )

    # Stronger dashed reference line
    guide = (
        alt.Chart(pd.DataFrame({"x":[0,1], "y":[0,1]}))
        .mark_line(strokeDash=[5,5], color="#333", strokeWidth=1.6)
        .encode(x="x:Q", y="y:Q")
    )
    return pts + guide

# ---------------------------------------
# App body
# ---------------------------------------
st.title("Email Marketing: Random Reality vs Intelligent Optimization")
st.caption("Scenario: 10,000 emails, 5 subject lines. Compare random sending vs ε-greedy RL.")

n_subjects = 5
n_iterations = 10000
subject_names = [
    "Limited Time Offer!",
    "You Won't Believe This...",
    "Exclusive Deal Inside",
    "Last Chance to Save",
    "Free Gift Waiting",
]

_truth_rng = np.random.default_rng(42)
true_conversion_rates = _truth_rng.uniform(0.1, 0.6, size=n_subjects)

# State
if "monte_carlo_results" not in st.session_state:
    st.session_state.monte_carlo_results = None
    st.session_state.rl_results = None

# Two aligned columns
left, right = st.columns(2, gap="large")

# ---------------- LEFT (Random) ----------------
with left:
    st.subheader("What Actually Happened (Random Sends)")
    st.caption("Reality: emails were sent uniformly at random.")

    kpi_left = st.empty()
    with kpi_left.container():
        mc_df0 = st.session_state.monte_carlo_results
        render_kpis(
            len(mc_df0) if mc_df0 is not None else None,
            int(mc_df0["Reward"].sum()) if mc_df0 is not None else None
        )

    # spacer to mirror RL controls height (keeps tables aligned)
    st.markdown(f"<div style='height:{CONTROLS_ROW_PX}px'></div>", unsafe_allow_html=True)

    mc_run = st.button("Simulate Random Reality", type="primary", key="run_mc")

    st.markdown("**Final Results After 1 Month (Random Strategy)**")
    table_left = st.empty()

    if mc_run:
        per_subject = n_iterations // n_subjects
        rows = []
        rng = np.random.default_rng(123)
        for sid in range(n_subjects):
            p = float(true_conversion_rates[sid])
            for n in range(per_subject):
                rows.append({
                    "Email_Number": sid * per_subject + n + 1,
                    "Subject": subject_names[sid],
                    "Subject_ID": sid,
                    "Reward": int(rng.random() < p),
                    "SuccessProb": p,
                })
        st.session_state.monte_carlo_results = pd.DataFrame(rows)
        with kpi_left.container():
            df = st.session_state.monte_carlo_results
            render_kpis(len(df), int(df["Reward"].sum()))

    if st.session_state.monte_carlo_results is not None:
        mc_df = st.session_state.monte_carlo_results
        total_conv = int(mc_df["Reward"].sum())
        final = mc_df.groupby("Subject")["Reward"].agg(["sum","count"])
        final.columns = ["Conversions","Emails Sent"]
        final["Conversion Rate"] = (final["Conversions"]/final["Emails Sent"]*100).round(2)
        with table_left.container():
            st.dataframe(final, use_container_width=True)
            st.success(f"Random reality simulation completed. Total conversions: {total_conv:,}")

# ---------------- RIGHT (RL) ----------------
with right:
    st.subheader("What Could Have Happened (Intelligent Learning)")
    st.caption("Optimization: ε-greedy policy exploits the best subject lines.")

    kpi_right = st.empty()
    with kpi_right.container():
        rl_df0 = st.session_state.rl_results
        render_kpis(
            len(rl_df0) if rl_df0 is not None else None,
            int(rl_df0["Reward"].sum()) if rl_df0 is not None else None
        )

    # Epsilon control (kept)
    eps = st.slider("Exploration Rate (ε)", 0.0, 1.0, 0.10, step=0.05,
                    help="Higher ε = more exploration, lower ε = more exploitation")

    rl_run = st.button("Simulate Intelligent Learning", type="secondary", key="run_rl")

    st.markdown("**Final Results After 1 Month (Intelligent Strategy)**")

    if rl_run:
        counts = np.zeros(n_subjects)
        rewards = np.zeros(n_subjects)
        rl_rows = []
        rng = np.random.default_rng(456)
        for i in range(n_iterations):
            if rng.random() < eps:
                sid = rng.integers(0, n_subjects)
            else:
                sid = int(np.argmax(rewards / (counts + 1e-6)))
            p = float(true_conversion_rates[sid])
            r = rng.random() < p
            counts[sid] += 1
            rewards[sid] += r
            rl_rows.append({
                "Email_Number": i + 1,
                "Subject": subject_names[sid],
                "Subject_ID": sid,
                "Reward": int(r),
                "SuccessProb": p,
            })
        st.session_state.rl_results = pd.DataFrame(rl_rows)
        with kpi_right.container():
            df = st.session_state.rl_results
            render_kpis(len(df), int(df["Reward"].sum()))

    if st.session_state.rl_results is not None:
        rl_df = st.session_state.rl_results
        rl_final = rl_df.groupby("Subject")["Reward"].agg(["sum","count"])
        rl_final.columns = ["Conversions","Emails Sent"]
        rl_final["Conversion Rate"] = (rl_final["Conversions"]/rl_final["Emails Sent"]*100).round(2)
        st.dataframe(rl_final, use_container_width=True)

        mc_conv = int(st.session_state.monte_carlo_results["Reward"].sum()) if st.session_state.monte_carlo_results is not None else 0
        rl_conv = int(rl_df["Reward"].sum()); imp = rl_conv - mc_conv
        imp_pct = (imp/mc_conv*100) if mc_conv>0 else 0.0
        st.success(f"Intelligent learning simulation completed. Improvement: +{imp:,} (+{imp_pct:+.1f}%).")

# ---------------------------------------
# Traffic Distribution
# ---------------------------------------
st.markdown("---")
st.subheader("Traffic Distribution")

mc_df = st.session_state.monte_carlo_results
rl_df = st.session_state.rl_results

def traffic_df(df):
    if df is None: return None
    t = df.groupby("Subject")["Reward"].agg(["count","sum"]).reset_index()
    t.columns = ["Subject","Traffic","Conversions"]
    return t

if (mc_df is not None) and (rl_df is not None):
    t1, t2 = st.columns(2, gap="large")
    with t1:
        st.caption("Random Strategy")
        st.altair_chart(
            stacked_traffic_chart(
                traffic_df(mc_df),
                COLORS["ACCENT_1"],
                COLORS["INK_500"],
                label_color="white",
                label_side=False
            ),
            use_container_width=True,
        )
    with t2:
        st.caption("Intelligent Learning")
        st.altair_chart(
            stacked_traffic_chart(
                traffic_df(rl_df),
                COLORS["ACCENT_2"],
                COLORS["INK_500"],
                label_color=COLORS["ACCENT_2"],
                label_side=True
            ),
            use_container_width=True,
        )
elif mc_df is not None:
    st.caption("Random Strategy")
    st.altair_chart(
        stacked_traffic_chart(
            traffic_df(mc_df),
            COLORS["ACCENT_1"], COLORS["INK_500"],
            label_color="white", label_side=False
        ),
        use_container_width=True,
    )
elif rl_df is not None:
    st.caption("Intelligent Learning")
    st.altair_chart(
        stacked_traffic_chart(
            traffic_df(rl_df),
            COLORS["ACCENT_2"], COLORS["INK_500"],
            label_color=COLORS["ACCENT_2"], label_side=True
        ),
        use_container_width=True,
    )

# ---------------------------------------
# Reward Dynamics (high contrast) + replay slider
# ---------------------------------------
st.markdown("---")
st.subheader("Reward Dynamics: A/B vs Reinforcement Learning")

cL, cR = st.columns(2, gap="large")
with cL:
    st.caption("A/B Baseline")
    if mc_df is None:
        st.info("Run the Random Reality simulation to populate A/B scatter.")
    else:
        st.altair_chart(build_reward_scatter(mc_df, ""), use_container_width=True)

with cR:
    st.caption("Reinforcement Learning")
    if rl_df is None:
        st.info("Run the Intelligent Learning simulation to populate RL scatter.")
    else:
        st.altair_chart(build_reward_scatter(rl_df, ""), use_container_width=True)

        st.markdown("**Cumulative Reward Over Time (RL)**")

        # Build history
        rl_hist = rl_df.sort_values("Email_Number").copy()
        rl_hist["CumReward"] = rl_hist.groupby("Subject")["Reward"].cumsum()
        rl_hist["CumChosen"] = rl_hist.groupby("Subject").cumcount() + 1
        rl_hist["Step"] = rl_hist["Email_Number"]

        # Replay slider
        max_step = int(rl_hist["Step"].max()) if not rl_hist.empty else 100
        step_view = st.slider("Show progression up to step", 100, max_step, max_step, step=100, key="replay_slider")
        rl_view = rl_hist[rl_hist["Step"] <= step_view]

        total_reward = int(rl_view["Reward"].sum())
        counts_now = rl_view.groupby("Subject").size() if not rl_view.empty else pd.Series(dtype=int)
        top_share = float(counts_now.max() / counts_now.sum()) if counts_now.sum() > 0 else 0.0
        best_true = float(np.max(true_conversion_rates))
        regret = best_true * len(rl_view) - total_reward

        m1, m2, m3 = st.columns(3)
        m1.metric("Total Reward", f"{total_reward:,}")
        m2.metric("Top Arm Share", f"{top_share*100:.1f}%")
        m3.metric("Regret (theoretical)", f"{regret:,.0f}")

        line = (
            alt.Chart(rl_view)
            .mark_line()  # theme gives thicker stroke
            .encode(
                x=alt.X("Step:Q", title="Step"),
                y=alt.Y("CumReward:Q", title="Cumulative Reward"),
                color=alt.Color(
                    "Subject:N",
                    title="Subject Line",
                    scale=subject_palette,
                    # Legend symbols matching points
                    legend=alt.Legend(
                        symbolType="circle",
                        symbolStrokeColor="black",
                        symbolStrokeWidth=1.2,
                        symbolSize=200,
                    ),
                ),
            )
            .properties(height=H_RL_LINE)
        )
        st.altair_chart(line, use_container_width=True)

# ---------------------------------------
# Reset
# ---------------------------------------
if st.button("Reset All Simulations"):
    st.session_state.monte_carlo_results = None
    st.session_state.rl_results = None
    st.rerun()
