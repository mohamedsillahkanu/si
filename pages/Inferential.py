import streamlit as st
import pandas as pd
import numpy as np
from scipy import stats
from statsmodels.formula.api import ols
import statsmodels.api as sm

# Functions for different tests
def run_ttest(df, col1, col2, paired=False):
    if paired:
        stat, p_value = stats.ttest_rel(df[col1], df[col2])
    else:
        stat, p_value = stats.ttest_ind(df[col1], df[col2])
    return stat, p_value

def run_anova(df, col, group_col):
    model = ols(f'{col} ~ C({group_col})', data=df).fit()
    anova_table = sm.stats.anova_lm(model, typ=2)
    return anova_table

def run_chisquare(df, col1, col2):
    contingency_table = pd.crosstab(df[col1], df[col2])
    stat, p_value, _, _ = stats.chi2_contingency(contingency_table)
    return stat, p_value

def run_correlation(df, col1, col2, method='pearson'):
    if method == 'pearson':
        corr, p_value = stats.pearsonr(df[col1], df[col2])
    elif method == 'spearman':
        corr, p_value = stats.spearmanr(df[col1], df[col2])
    else:
        corr, p_value = stats.kendalltau(df[col1], df[col2])
    return corr, p_value

# Streamlit UI
st.title("Inferential Statistics App")

# File upload
file = st.file_uploader("Upload your CSV or XLSX file", type=["csv", "xlsx"])

if file:
    # Load file
    if file.name.endswith('.csv'):
        df = pd.read_csv(file)
    else:
        df = pd.read_excel(file)
    
    st.write("Data Preview", df.head())

    # Select Test
    test = st.selectbox("Select an inferential test", 
                        ["t-test", "ANOVA", "Chi-Square", "Correlation"])
    
    if test:
        # t-test options
        if test == "t-test":
            col1 = st.selectbox("Select first numeric column", df.select_dtypes(include=[np.number]).columns)
            col2 = st.selectbox("Select second numeric column", df.select_dtypes(include=[np.number]).columns)
            paired = st.checkbox("Paired t-test", False)
            
            # Run t-test
            if st.button("Run t-test"):
                stat, p_value = run_ttest(df, col1, col2, paired)
                st.write(f"t-statistic: {stat}, p-value: {p_value}")
                if p_value < 0.05:
                    st.write("Result is statistically significant")
                else:
                    st.write("Result is not statistically significant")

        # ANOVA options
        elif test == "ANOVA":
            col = st.selectbox("Select a numeric column for ANOVA", df.select_dtypes(include=[np.number]).columns)
            group_col = st.selectbox("Select a categorical grouping column", df.select_dtypes(exclude=[np.number]).columns)
            
            # Run ANOVA
            if st.button("Run ANOVA"):
                anova_table = run_anova(df, col, group_col)
                st.write(anova_table)

        # Chi-square options
        elif test == "Chi-Square":
            col1 = st.selectbox("Select first categorical column", df.select_dtypes(exclude=[np.number]).columns)
            col2 = st.selectbox("Select second categorical column", df.select_dtypes(exclude=[np.number]).columns)
            
            # Run Chi-Square
            if st.button("Run Chi-Square"):
                try:
                    stat, p_value = run_chisquare(df, col1, col2)
                    st.write(f"Chi-square statistic: {stat}, p-value: {p_value}")
                    if p_value < 0.05:
                        st.write("Result is statistically significant")
                    else:
                        st.write("Result is not statistically significant")
                except ValueError as e:
                    st.write(f"Error: {e}")

        # Correlation options
        elif test == "Correlation":
            col1 = st.selectbox("Select first numeric column", df.select_dtypes(include=[np.number]).columns)
            col2 = st.selectbox("Select second numeric column", df.select_dtypes(include=[np.number]).columns)
            method = st.radio("Choose correlation method", ["pearson", "spearman", "kendall"])
            
            # Run correlation
            if st.button("Run Correlation"):
                corr, p_value = run_correlation(df, col1, col2, method)
                st.write(f"Correlation coefficient: {corr}, p-value: {p_value}")
                if p_value < 0.05:
                    st.write("Result is statistically significant")
                else:
                    st.write("Result is not statistically significant")

        else:
            st.write("Please select a valid test.")

