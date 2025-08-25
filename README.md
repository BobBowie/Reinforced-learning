# Bandit Time Machine — Reinforcement Learning for Marketing, Made Intuitive

A hands-on Streamlit simulator to teach how reinforcement learning (RL) can optimize marketing performance. It contrasts a "random reality" A/B baseline with an intelligent multi-armed bandit policy (ε-greedy) that learns while sending. The app simulates 10,000 emails across five subject lines and visualizes how traffic reallocation boosts total conversions.

## Executive summary 
- **What it is**: An interactive simulator showing how RL reallocates email traffic in-flight to maximize conversions.
- **Why it matters**: Unlike static A/B tests that split traffic evenly, bandits learn continuously—lifting conversions while still learning.
- **How it works (at a glance)**: Each subject line is an arm; ε-greedy balances exploration (ε) with exploitation (1−ε).
- **What you’ll take away**: Practical intuition for exploration–exploitation, regret, and when to use bandits vs. A/B in marketing.

## Problem framing
- **Marketing reality**: You have multiple creative options (subject lines). Every send is an opportunity to learn which one converts best.
- **Optimization goal**: Maximize total conversions while you learn — not just estimate which is best at the end.
- **Bandit formulation**: Each creative is an "arm" with an unknown conversion probability. Each email sent is a trial that returns a binary reward (convert vs not).

## Methods and reasoning
- **A/B baseline (uniform allocation)**
  - Sends traffic evenly to all subject lines.
  - Great for estimation; leaves performance on the table during the test.
- **Multi-armed bandit (ε-greedy policy)**
  - With probability ε, explore a random arm (keep learning).
  - Otherwise, exploit the empirically best arm (boost performance).
  - Simple, transparent, and effective for stationary problems.
- **Key ideas**
  - **Exploration vs exploitation**: Continuous testing vs scaling winners now.
  - **Regret**: The gap between actual conversions and what you’d get if you always chose the best arm (unknown upfront). Lower regret = better policy.
  - **Stationarity assumption**: True conversion rates are stable over the run. This makes ε-greedy a sensible baseline.

## What the simulator does
- Creates a fixed, reproducible "world" by drawing true conversion rates for 5 subject lines (seeded for consistency).
- Simulates 10,000 sends under:
  - **Random Reality**: A/B-like uniform allocation
  - **Intelligent Learning**: ε-greedy allocation
- Surfaces KPIs, allocation charts, reward dynamics, and a replayable learning trajectory to make the algorithm’s behavior easy to grasp.

## How to read the visuals
- **KPIs**: Total emails, total conversions, and achieved conversion rate.
- **Traffic distribution (stacked bars)**: Shows how much traffic goes to each subject and how much of that traffic converted.
- **Reward dynamics (scatter)**: Each subject’s traffic share vs empirical conversion rate — ideal points drift up-right as the policy learns.
- **Cumulative reward (lines + slider)**: Watch the policy concentrate traffic and separate winners from the rest; see total reward and theoretical regret over time.

## Libraries and why they were chosen
- **Streamlit**: Rapid, interactive UI for data apps; ideal for explaining ML to non-technical audiences.
- **NumPy**: Fast, vectorized numeric simulation (sampling, counters).
- **Pandas**: Compact tabular transformations and aggregations for KPIs.
- **Altair**: Declarative, publication-quality charts with a consistent, high-contrast theme for clarity.

## Mathematical intuition (brief)
- Each arm i has unknown probability p_i of success. Observing binary outcomes, we estimate p_i via empirical mean.
- ε-greedy picks a random arm with probability ε (explore), else picks argmax of estimated p_i (exploit).
- Over time, estimates improve and traffic concentrates on better arms; cumulative regret grows more slowly than uniform allocation.

## Practical guidance for marketers
- Use bandits when you care about **performance during learning** (campaigns with meaningful volume and time)
- Keep some exploration (ε > 0) so you don’t miss late-emerging winners
- Monitor stability: if audience or seasonality shifts, consider adaptive or Bayesian policies (see extensions)
- Combine with business constraints: fairness caps, minimum exposure guarantees, and holdout groups for measurement

## Theory notes and method comparisons
- **ε-greedy**: Baseline policy, transparent and easy to communicate; fixed-ε favors simplicity. Decaying-ε variants reduce exploration over time.
- **UCB (Upper Confidence Bound)**: Optimism in the face of uncertainty; balances mean and uncertainty, with strong logarithmic regret guarantees under standard assumptions.
- **Thompson Sampling**: Bayesian posterior sampling; typically strong empirical performance and theoretical guarantees comparable to UCB.
- **Contextual Bandits**: Incorporate features (e.g., audience, time of day) to tailor allocation; lifts performance when heterogeneous effects exist.
- In practice, start with ε-greedy to align teams, then graduate to UCB/Thompson or contextual approaches for scale and robustness.

## Real-world deployment checklist
- Define objective and constraints (e.g., conversions, revenue, fairness caps).
- Choose exploration schedule (fixed ε vs decaying) and safety rails (min traffic per variant).
- Handle delayed rewards/attribution windows; consider credit assignment strategies.
- Monitor drift and non-stationarity (seasonality, fatigue); adapt via sliding windows or change-point detection.
- Instrument logs for decisions, context, outcomes; build auditability and dashboards.
- A/B vs bandit governance: when to use each, and how to report uplift with guardrails.

## Stakeholder FAQ (non-technical)
- **Will this "turn off" learning too early?** With ε > 0 or decaying ε, the policy retains exploration so late winners can still be discovered.
- **Is this fair to creatives that start slow?** Minimum exposure rules and controlled exploration protect against early false negatives.
- **What about seasonality or list fatigue?** Use adaptive policies (windowed estimates, change detection) to stay responsive.
- **Can we still do clean measurement?** Keep a small holdout or run a wrap-up AB once the bandit stabilizes to validate effects.

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

## Limitations and extensions (roadmap)
- **Assumptions**: Binary rewards, stationarity, immediate feedback, independent arms.
- **Extensions**:
  - Thompson Sampling (Bayesian), UCB (optimism), or softmax policies
  - Non-stationarity: drifting rates, change-point detection, sliding windows
  - Delayed rewards and attribution windows (e.g., conversions after email open)
  - Contextual bandits (use features: audience, device, time of day)
  - Constraints: brand safety, frequency caps, fairness across segments

## Productionization notes
- Start with offline simulation/AB to calibrate priors and safety rails.
- Add monitoring for drift, guardrails on minimum exploration, and interpretable dashboards.
- Log policy decisions and outcomes for auditability and iterative improvement.

## References and further reading
- Sutton & Barto, "Reinforcement Learning: An Introduction" (2nd ed.)
- Lattimore & Szepesvári, "Bandit Algorithms" (2020)
- Bubeck & Cesa-Bianchi, "Regret Analysis of Stochastic and Nonstochastic Multi-armed Bandit Problems" (Foundations and Trends in ML)
- Scott, "A modern Bayesian look at the multi-armed bandit" (with applications in marketing experimentation)

## Repository structure
```
.
├─ bandit_demo.py      # Streamlit app: UI, simulation, and visualizations
└─ README.md           # You are here
```

## License
MIT. See `LICENSE` if included in this repository.

## Author
Designed to clearly explain and demonstrate applied reinforcement learning for growth experimentation — bridging ML rigor and marketing impact.
