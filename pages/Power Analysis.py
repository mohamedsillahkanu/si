import streamlit as st
import pandas as pd
import numpy as np
from statsmodels.stats.power import TTestIndPower
import matplotlib.pyplot as plt

# App title
st.title("Power Analysis for Sample Size Determination")

# Sidebar for navigation
st.sidebar.title("Navigation")
section = st.sidebar.radio("Go to", ["Power Analysis Overview", "Power Analysis Illustration"])

# 1. Power Analysis Overview Section
if section == "Power Analysis Overview":
    st.header("Power Analysis for Sample Size Determination")
    
    st.subheader("When to Use It")
    st.write("""
        Power analysis is used to determine the sample size required to detect an effect of a given size with a certain level of confidence.
        It is often used in medical research to plan experiments and ensure that the study is adequately powered.
    """)
    
    st.subheader("Data Requirements")
    st.write("You need the following parameters for performing power analysis:")
    st.write("1. **Effect Size**: The expected difference between the means of two groups, expressed in standard deviation units.")
    st.write("2. **Alpha (Significance Level)**: The probability of rejecting the null hypothesis when it is true (commonly set at 0.05).")
    st.write("3. **Power**: The probability of correctly rejecting the null hypothesis (commonly set at 0.8 or 80%).")
    
    st.subheader("Purpose of Power Analysis")
    st.write("""
        The purpose of power analysis is to determine the minimum sample size needed for a study to detect an effect of a given size.
        It ensures that the study is neither underpowered nor unnecessarily large.
    """)
    
    st.subheader("Real-Life Medical Examples (Malaria)")
    st.write("Here is a practical example of how power analysis can be used in malaria research:")
    
    st.write("""
    **Determining Sample Size for Drug Efficacy Study**: 
       Researchers can use power analysis to determine the sample size needed to detect a significant difference in parasite clearance rates between two treatment groups.
    """)
    
    st.write("For more information, visit the [Wikipedia page on Power Analysis](https://en.wikipedia.org/wiki/Power_analysis).")

# 2. Power Analysis Illustration Section
elif section == "Power Analysis Illustration":
    st.header("Power Analysis Illustration")
    
    # Input fields for power analysis
    st.subheader("Enter Parameters for Power Analysis")
    effect_size = st.number_input("Effect Size (Cohen's d)", value=0.5)
    alpha = st.number_input("Significance Level (Alpha)", value=0.05)
    power = st.number_input("Power (1 - Beta)", value=0.8)
    
    # Button to perform power analysis
    if st.button("Calculate Required Sample Size"):
        try:
            # Perform power analysis using TTestIndPower
            analysis = TTestIndPower()
            sample_size = analysis.solve_power(effect_size=effect_size, alpha=alpha, power=power, alternative='two-sided')
            
            # Display the required sample size
            st.write(f"**Required Sample Size:** {int(np.ceil(sample_size))}")
            
            # Display a tip for interpretation
            st.write("""
            **Tip for Interpretation**: 
            - The calculated sample size is the minimum number of observations needed per group to achieve the desired power for detecting the specified effect size.
            """)
            
            # Plot power curve
            st.write("**Power Curve**:")
            effect_sizes = np.linspace(0.1, 1.5, 100)
            powers = analysis.power(effect_size=effect_sizes, nobs1=sample_size, alpha=alpha)
            plt.figure(figsize=(10, 6))
            plt.plot(effect_sizes, powers, label='Power Curve')
            plt.axhline(y=power, color='r', linestyle='--', label='Desired Power')
            plt.xlabel("Effect Size (Cohen's d)")
            plt.ylabel("Power")
            plt.title("Power Curve for Varying Effect Sizes")
            plt.legend()
            st.pyplot(plt)
        
        except Exception as e:
            st.error(f"Error during Power Analysis: {e}")

