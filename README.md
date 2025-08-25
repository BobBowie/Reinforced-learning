# Bandit Time Machine — Email Marketing with Reinforcement Learning

An interactive Streamlit app that contrasts “random reality” A/B sending with an intelligent multi-armed bandit policy (ε-greedy). It simulates 10,000 emails across five subject lines and shows how reinforcement learning reallocates traffic in real time to maximize conversions.

## Why this exists
Traditional A/B tests split traffic uniformly and wait. Multi-armed bandits learn while they send, continuously shifting traffic toward better-performing options. This app makes that intuition visual, quantitative, and hands-on for product, growth, and data teams.

## What you’ll see
- **Two worlds side-by-side**:
  - Random Reality (uniform sends) vs Intelligent Learning (ε-greedy)
- **KPIs**: total emails, total conversions, conversion rate
- **Traffic distribution**: stacked bars showing conversions vs remainder
- **Reward dynamics**: scatter plots of traffic share vs empirical conversion rate
- **Replay**: cumulative reward lines with a step slider, plus regret and policy concentration

## Core concepts (at a glance)
- **A/B Baseline**: Sends traffic uniformly; good for estimation, slow to optimize
- **Multi-Armed Bandit**: Treats each subject line as an “arm”; balances exploration vs exploitation
- **ε-greedy policy**: With probability ε explore a random arm; otherwise exploit the empirically best arm
- **Regret**: Difference between the reward you got and the reward you could have gotten always pulling the best arm

## How it works (high level)
- Simulates a month of sending: `n_iterations = 10_000` emails across `n_subjects = 5` subjects
- Draws latent “true” conversion rates once (fixed seed) to create a repeatable world
- Random world sends uniformly; RL world updates counts/rewards and greedily exploits with ε exploration
- Results are visualized with Altair in a high-contrast, publication-style theme

## Run it locally
Requirements:
- Python 3.9+
- Packages: streamlit, numpy, pandas, altair

Install and launch:
```bash
pip install streamlit numpy pandas altair
streamlit run bandit_demo.py
```
Then open the local URL Streamlit prints (usually `http://localhost:8501`).

## One-click deploy (no local setup)
- Streamlit Community Cloud:
  1. Fork this repo
  2. Create a new Streamlit app from your fork
  3. Set the entry point to `bandit_demo.py`

## Using the app
- Click “Simulate Random Reality” to generate the baseline world
- Choose an exploration rate ε (default 0.10)
- Click “Simulate Intelligent Learning” to run the bandit policy
- Review:
  - Tables: per-subject emails, conversions, and conversion rates
  - Traffic charts: allocation differences and impact
  - Reward dynamics: scatter plots and cumulative reward by subject
  - Replay slider: step through the policy’s learning trajectory

## Design and implementation notes
- Deterministic seeds make the “truth” reproducible while each run’s sampling remains stochastic
- ε-greedy is intentionally simple and pedagogical; extensions are suggested below
- Visuals emphasize clarity for non-technical audiences while preserving analytical signal

## Extending the demo
- Add Bayesian/Thompson Sampling or UCB policies for comparison
- Introduce non-stationarity (drifting conversion rates) and adaptive policies
- Add cost/benefit modeling or multiple objectives (e.g., revenue, churn risk)
- Stream real or offline data to replace simulated rewards

## Repository structure
```
.
├─ bandit_demo.py      # Streamlit app: UI, simulation, and visualizations
└─ README.md           # You are here
```

## License
MIT. See `LICENSE` if included in this repository.

## Author
Crafted to communicate best practices and intuition behind applied reinforcement learning for growth experimentation, with production-quality visuals and explanations.
