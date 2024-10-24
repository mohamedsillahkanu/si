import streamlit as st
import pandas as pd
import numpy as np
import arviz as az
import matplotlib.pyplot as plt
import pymc as pm  # Use PyMC 4 for compatibility

# App title
st.title("Bayesian Inference for Survival Analysis")

# Sidebar for navigation
st.sidebar.title("Navigation")
section = st.sidebar.radio("Go to", ["Bayesian Inference Overview", "Bayesian Inference Illustration"])

# 1. Bayesian Inference Overview Section
if section == "Bayesian Inference Overview":
    st.header("Bayesian Inference for Survival Analysis")
    
    st.subheader("When to Use It")
    st.write("""
        Bayesian Inference is used when we want to incorporate prior knowledge along with observed data to estimate the distribution of parameters. 
        It is commonly used in medical research for survival analysis to estimate the effect of covariates on survival time, incorporating prior beliefs or historical data.
    """)
    
    st.subheader("Data Requirements")
    st.write("You need the following variables for Bayesian Inference in survival analysis:")
    st.write("1. **Time to Event**: The time duration until the event occurs (e.g., death, relapse).")
    st.write("2. **Event Occurrence**: A binary variable indicating whether the event occurred (1 for event, 0 for censored).")
    st.write("3. **Covariates**: Variables that may affect the survival outcome (e.g., age, treatment, comorbidities).")
    
    st.subheader("Purpose of Bayesian Inference")
    st.write("""
        The purpose of Bayesian Inference is to estimate the distribution of model parameters by combining observed data with prior information. 
        In survival analysis, it allows us to estimate the effect of covariates while taking into account uncertainty and prior knowledge.
    """)
    
    st.subheader("Real-Life Medical Examples (Malaria)")
    st.write("Here are two practical examples of how Bayesian Inference can be used in malaria research:")
    
    st.write("""
    1. **Assessing the Effect of Treatment on Survival**: 
       Bayesian Inference can be used to assess the effect of different antimalarial treatments on patient survival time, incorporating prior knowledge from past studies.
    """)
    
    st.write("""
    2. **Evaluating the Impact of Age and Comorbidities**: 
       The approach can be used to evaluate the impact of patient age and comorbidities on the likelihood of relapse or death, while incorporating prior distributions based on historical data.
    """)
    
    st.write("For more information, visit the [Wikipedia page on Bayesian Inference](https://en.wikipedia.org/wiki/Bayesian_inference).")

# 2. Bayesian Inference Illustration Section
elif section == "Bayesian Inference Illustration":
    st.header("Bayesian Inference Illustration")
    
    st.subheader("Upload your dataset (CSV or XLSX)")
    uploaded_file = st.file_uploader("Choose a CSV or XLSX file", type=["csv", "xlsx"], key="bayesian_file")
    
    if uploaded_file is not None:
        # Load the dataset based on file type
        try:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            elif uploaded_file.name.endswith('.xlsx'):
                df = pd.read_excel(uploaded_file)
                
            st.write("Here is a preview of your data:")
            st.write(df.head())
            
            # Ask the user to select the required columns
            time_column = st.selectbox("Select the time to event variable", df.columns)
            event_column = st.selectbox("Select the event occurrence variable", df.columns)
            covariate_columns = st.multiselect("Select the covariate variables", [col for col in df.columns if col not in [time_column, event_column]])
            
            st.write(f"You selected: {time_column}, {event_column}, and covariates: {covariate_columns} for Bayesian Inference.")
            
            # Button to perform Bayesian inference
            if st.button("Perform Bayesian Inference"):
                try:
                    with pm.Model() as model:
                        # Priors for unknown model parameters
                        alpha = pm.Normal('alpha', mu=0, sigma=10)
                        betas = pm.Normal('betas', mu=0, sigma=10, shape=len(covariate_columns))
                        
                        # Linear combination of covariates
                        X = df[covariate_columns].values
                        linear_combination = alpha + pm.math.dot(X, betas)
                        
                        # Likelihood (observed survival times)
                        lambda_ = pm.math.exp(linear_combination)
                        T = df[time_column].values
                        event = df[event_column].values
                        survival = pm.Exponential('survival', lam=lambda_, observed=T)
                        censoring = pm.Bernoulli('censoring', p=0.5, observed=event)
                        
                        # Posterior distribution
                        trace = pm.sample(1000, return_inferencedata=True)
                        
                        # Display results
                        st.write("**Posterior Summary:**")
                        st.text(az.summary(trace))
                        
                        # Plot the trace
                        st.write("Trace Plot:")
                        az.plot_trace(trace)
                        st.pyplot(plt)
                        
                        # Display a tip for interpretation
                        st.write("""
                        **Tip for Interpretation**: 
                        - The posterior distributions of the parameters represent the uncertainty about the effect of each covariate.
                        - The credible intervals can be used to determine the likely range of parameter values.
                        """)
                except Exception as e:
                    st.error(f"Error during Bayesian Inference: {e}")
                
        except Exception as e:
            st.error(f"Error loading file: {e}")


