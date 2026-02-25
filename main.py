import streamlit as st
import numpy as np
from scipy.stats import t

# -----------------------
# T-Test Function
# -----------------------
def ttest(data, mu0, alpha=0.05, alternative="two-sided"):
    data = np.array(data)
    n = len(data)

    xbar = np.mean(data)
    s = np.std(data, ddof=1)

    se = s / np.sqrt(n)
    t_cal = (xbar - mu0) / se
    df = n - 1

    if alternative == "two-sided":
        t_crit = t.ppf(1 - alpha/2, df)
        p_value = 2 * (1 - t.cdf(abs(t_cal), df))
        reject = abs(t_cal) > t_crit

    elif alternative == "greater":
        t_crit = t.ppf(1 - alpha, df)
        p_value = 1 - t.cdf(t_cal, df)
        reject = t_cal > t_crit

    elif alternative == "less":
        t_crit = t.ppf(alpha, df)
        p_value = t.cdf(t_cal, df)
        reject = t_cal < t_crit

    return {
        "Sample Mean": xbar,
        "Sample Std Dev": s,
        "t Statistic": t_cal,
        "Degrees of Freedom": df,
        "p-value": p_value,
        "Decision": "Reject H₀" if reject else "Fail to Reject H₀"
    }


# -----------------------
# Streamlit UI
# -----------------------

st.title("📊 One-Sample T-Test")

st.write("Enter your dataset as comma-separated values.")

# User inputs
data_input = st.text_area(
    "Dataset",
    placeholder="Example: 12, 15, 14, 10, 9, 11"
)

mu0 = st.number_input("Hypothesized Mean (μ₀)", value=0.0)

alpha = st.selectbox("Significance Level (α)", [0.01, 0.05, 0.10])

alternative = st.radio(
    "Alternative Hypothesis",
    ["two-sided", "greater", "less"]
)

if st.button("Run T-Test"):

    try:
        # Convert string input to list of floats
        data = [float(x.strip()) for x in data_input.split(",")]

        if len(data) < 2:
            st.error("Dataset must contain at least 2 values.")
        else:
            results = ttest(data, mu0, alpha, alternative)

            st.subheader("Results")
            for key, value in results.items():
                st.write(f"**{key}:** {value}")

    except:
        st.error("Invalid dataset format. Please enter numbers separated by commas.")