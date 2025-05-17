import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression

# Set page configuration
st.set_page_config(
    page_title="Malaria Intervention Planning Tool",
    page_icon="🦟",
    layout="wide"
)

# Add custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #2c3e50;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #34495e;
        margin-top: 2rem;
    }
    .metric-container {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
    }
    .info-box {
        background-color: #e3f2fd;
        border-left: 5px solid #2196f3;
        padding: 10px;
        border-radius: 5px;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("<h1 class='main-header'>Malaria Intervention Planning Tool</h1>", unsafe_allow_html=True)
st.markdown("<div class='info-box'>This tool uses fictional data to model the relationship between malaria intervention coverage and disease prevalence. Set your target reduction goal to get recommended intervention levels.</div>", unsafe_allow_html=True)

# Generate fictional dataset
@st.cache_data
def generate_data():
    # List of fictional regions
    regions = ["North Province", "Central District", "Eastern Zone", "Western Area", 
               "Southern Region", "Coastal Strip", "Mountain Region", "Lake Basin"]
    
    # Base data
    np.random.seed(42)
    num_years = 10
    current_year = 2024
    years = list(range(current_year - num_years + 1, current_year + 1))
    
    data = []
    
    # Create baseline parameters for each region
    region_params = {}
    for region in regions:
        # Random baseline parameters for each region
        pop_base = np.random.randint(50000, 500000)
        malaria_rate_base = np.random.uniform(0.05, 0.30)  # 5-30% baseline
        itn_effect = np.random.uniform(0.5, 0.7)  # ITN effectiveness
        irs_effect = np.random.uniform(0.4, 0.6)  # IRS effectiveness
        act_effect = np.random.uniform(0.3, 0.5)  # ACT effectiveness
        
        # Store parameters
        region_params[region] = {
            'pop_base': pop_base,
            'malaria_rate_base': malaria_rate_base,
            'itn_effect': itn_effect,
            'irs_effect': irs_effect,
            'act_effect': act_effect
        }
    
    # Generate data for each region and year
    for region in regions:
        params = region_params[region]
        for year in years:
            # Calculate population with small yearly growth
            population = int(params['pop_base'] * (1 + np.random.uniform(0.01, 0.03) * (year - (current_year - num_years + 1))))
            
            # Intervention coverage increases over time with some randomness
            year_factor = (year - (current_year - num_years + 1)) / num_years
            
            itn_coverage = min(0.1 + 0.6 * year_factor + np.random.uniform(-0.1, 0.1), 0.95)
            irs_coverage = min(0.05 + 0.4 * year_factor + np.random.uniform(-0.1, 0.1), 0.8)
            act_coverage = min(0.2 + 0.5 * year_factor + np.random.uniform(-0.1, 0.1), 0.9)
            
            # Calculate malaria prevalence based on intervention coverage
            malaria_reduction = (itn_coverage * params['itn_effect'] + 
                                irs_coverage * params['irs_effect'] + 
                                act_coverage * params['act_effect']) * 0.8  # 0.8 is an interaction factor
            
            # Ensure reduction doesn't exceed 90%
            malaria_reduction = min(malaria_reduction, 0.9)
            
            malaria_rate = params['malaria_rate_base'] * (1 - malaria_reduction)
            malaria_cases = int(population * malaria_rate)
            
            # Calculate costs
            itn_cost_per_unit = np.random.uniform(6, 10)
            irs_cost_per_unit = np.random.uniform(3, 7)
            act_cost_per_unit = np.random.uniform(1, 3)
            
            # ITNs are distributed to households (assume average household size of 5)
            households = population / 5
            itn_units_needed = households * itn_coverage
            itn_cost = itn_units_needed * itn_cost_per_unit
            
            # IRS is applied to households
            irs_units_needed = households * irs_coverage
            irs_cost = irs_units_needed * irs_cost_per_unit
            
            # ACT is given to malaria cases
            act_units_needed = malaria_cases * act_coverage
            act_cost = act_units_needed * act_cost_per_unit
            
            # Total intervention cost
            total_cost = itn_cost + irs_cost + act_cost
            
            data.append({
                'Region': region,
                'Year': year,
                'Population': population,
                'ITN_Coverage': itn_coverage,
                'IRS_Coverage': irs_coverage,
                'ACT_Coverage': act_coverage,
                'Malaria_Rate': malaria_rate,
                'Malaria_Cases': malaria_cases,
                'ITN_Units': int(itn_units_needed),
                'IRS_Units': int(irs_units_needed),
                'ACT_Units': int(act_units_needed),
                'ITN_Cost': itn_cost,
                'IRS_Cost': irs_cost,
                'ACT_Cost': act_cost,
                'Total_Cost': total_cost
            })
    
    return pd.DataFrame(data), region_params

# Generate the data
df, region_params = generate_data()

# Sidebar for interaction
st.sidebar.markdown("## Control Panel")
st.sidebar.markdown("Use the sliders below to set your target reduction and adjust intervention parameters.")

# Target reduction slider
target_reduction = st.sidebar.slider(
    "Target Malaria Reduction (%)",
    min_value=10,
    max_value=90,
    value=40,
    step=5
)

# Advanced settings expander
with st.sidebar.expander("Advanced Settings"):
    itn_cost_modifier = st.slider("ITN Cost Modifier", 0.5, 2.0, 1.0, 0.1)
    irs_cost_modifier = st.slider("IRS Cost Modifier", 0.5, 2.0, 1.0, 0.1)
    act_cost_modifier = st.slider("ACT Cost Modifier", 0.5, 2.0, 1.0, 0.1)
    
    intervention_effectiveness = st.slider(
        "Overall Intervention Effectiveness Modifier", 
        0.5, 1.5, 1.0, 0.1,
        help="Adjust the overall effectiveness of all interventions"
    )

# Filter to the most recent year for current status
current_year = df['Year'].max()
current_data = df[df['Year'] == current_year]

# Dashboard Layout
tab1, tab2, tab3, tab4 = st.tabs(["Current Status", "Historical Trends", "Intervention Planning", "Cost Analysis"])

# Tab 1: Current Status
with tab1:
    st.markdown("<h2 class='sub-header'>Current Malaria Situation Overview</h2>", unsafe_allow_html=True)
    
    # Summary metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("<div class='metric-container'>", unsafe_allow_html=True)
        st.metric("Total Population", f"{current_data['Population'].sum():,}")
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("<div class='metric-container'>", unsafe_allow_html=True)
        st.metric("Total Malaria Cases", f"{current_data['Malaria_Cases'].sum():,}")
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col3:
        st.markdown("<div class='metric-container'>", unsafe_allow_html=True)
        avg_rate = (current_data['Malaria_Cases'].sum() / current_data['Population'].sum()) * 100
        st.metric("Average Prevalence Rate", f"{avg_rate:.2f}%")
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col4:
        st.markdown("<div class='metric-container'>", unsafe_allow_html=True)
        st.metric("Total Annual Cost", f"${current_data['Total_Cost'].sum():,.2f}")
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Current status by region
    st.markdown("### Current Status by Region")
    col1, col2 = st.columns([3, 2])
    
    with col1:
        # Map-like visualization of malaria prevalence by region
        fig = px.bar(current_data, x='Region', y='Malaria_Rate', 
                     color='Malaria_Rate', color_continuous_scale='Reds',
                     labels={'Malaria_Rate': 'Prevalence Rate', 'Region': 'Region'},
                     title='Malaria Prevalence by Region')
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Current intervention coverage
        intervention_data = pd.melt(
            current_data, 
            id_vars=['Region'], 
            value_vars=['ITN_Coverage', 'IRS_Coverage', 'ACT_Coverage'],
            var_name='Intervention', 
            value_name='Coverage'
        )
        
        intervention_data['Intervention'] = intervention_data['Intervention'].str.replace('_Coverage', '')
        
        fig = px.bar(
            intervention_data, 
            x='Coverage', 
            y='Region', 
            color='Intervention',
            orientation='h',
            labels={'Coverage': 'Coverage Rate', 'Region': 'Region'},
            title='Current Intervention Coverage by Region'
        )
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)
    
    # Data table
    with st.expander("View Detailed Current Data"):
        display_cols = ['Region', 'Population', 'Malaria_Rate', 'Malaria_Cases', 
                        'ITN_Coverage', 'IRS_Coverage', 'ACT_Coverage', 'Total_Cost']
        st.dataframe(current_data[display_cols], use_container_width=True)

# Tab 2: Historical Trends
with tab2:
    st.markdown("<h2 class='sub-header'>Historical Trends Analysis</h2>", unsafe_allow_html=True)
    
    # Time period selector
    years = sorted(df['Year'].unique())
    start_year, end_year = st.select_slider(
        "Select Time Period",
        options=years,
        value=(years[0], years[-1])
    )
    
    trends_data = df[(df['Year'] >= start_year) & (df['Year'] <= end_year)]
    
    # Region selector
    regions = sorted(df['Region'].unique())
    selected_regions = st.multiselect(
        "Select Regions to Display",
        options=regions,
        default=regions[:3]
    )
    
    if not selected_regions:
        selected_regions = regions  # If none selected, show all
    
    filtered_trends = trends_data[trends_data['Region'].isin(selected_regions)]
    
    # Aggregated trends
    agg_trends = filtered_trends.groupby('Year').agg({
        'Population': 'sum',
        'Malaria_Cases': 'sum',
        'Total_Cost': 'sum'
    }).reset_index()
    agg_trends['Malaria_Rate'] = agg_trends['Malaria_Cases'] / agg_trends['Population']
    
    # Historical prevalence trend
    st.markdown("### Historical Malaria Prevalence Trend")
    col1, col2 = st.columns([3, 2])
    
    with col1:
        fig = px.line(
            agg_trends, 
            x='Year', 
            y='Malaria_Rate',
            labels={'Malaria_Rate': 'Prevalence Rate', 'Year': 'Year'},
            title='Overall Malaria Prevalence Rate Over Time'
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Calculate correlation between interventions and malaria rates
        corr_data = filtered_trends.groupby('Year').agg({
            'ITN_Coverage': 'mean',
            'IRS_Coverage': 'mean',
            'ACT_Coverage': 'mean',
            'Malaria_Rate': 'mean'
        }).reset_index()
        
        corr_matrix = corr_data[['ITN_Coverage', 'IRS_Coverage', 'ACT_Coverage', 'Malaria_Rate']].corr()
        
        fig = px.imshow(
            corr_matrix,
            labels={'color': 'Correlation'},
            color_continuous_scale='RdBu_r',
            title='Correlation Between Interventions and Malaria Rate'
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    # Regional trends
    st.markdown("### Regional Trends")
    
    # Create a pivot for regional trends
    regional_pivot = filtered_trends.pivot_table(
        index='Year',
        columns='Region',
        values='Malaria_Rate'
    )
    
    fig = px.line(
        regional_pivot,
        labels={'value': 'Prevalence Rate', 'Year': 'Year'},
        title='Malaria Prevalence by Region Over Time'
    )
    fig.update_layout(height=500)
    st.plotly_chart(fig, use_container_width=True)
    
    # Intervention coverage over time
    st.markdown("### Intervention Coverage Trends")
    
    intervention_trends = filtered_trends.groupby('Year').agg({
        'ITN_Coverage': 'mean',
        'IRS_Coverage': 'mean',
        'ACT_Coverage': 'mean'
    }).reset_index()
    
    intervention_long = pd.melt(
        intervention_trends,
        id_vars=['Year'],
        value_vars=['ITN_Coverage', 'IRS_Coverage', 'ACT_Coverage'],
        var_name='Intervention',
        value_name='Coverage'
    )
    
    intervention_long['Intervention'] = intervention_long['Intervention'].str.replace('_Coverage', '')
    
    fig = px.line(
        intervention_long,
        x='Year',
        y='Coverage',
        color='Intervention',
        labels={'Coverage': 'Coverage Rate', 'Year': 'Year'},
        title='Intervention Coverage Over Time'
    )
    fig.update_layout(height=500)
    st.plotly_chart(fig, use_container_width=True)
    
    # Data table
    with st.expander("View Historical Data"):
        display_cols = ['Year', 'Region', 'Population', 'Malaria_Rate', 'Malaria_Cases', 
                        'ITN_Coverage', 'IRS_Coverage', 'ACT_Coverage', 'Total_Cost']
        st.dataframe(filtered_trends[display_cols], use_container_width=True)

# Tab 3: Intervention Planning
with tab3:
    st.markdown("<h2 class='sub-header'>Intervention Planning Tool</h2>", unsafe_allow_html=True)
    st.write(f"Planning for a **{target_reduction}%** reduction in malaria prevalence")
    
    # Function to build predictive model
    @st.cache_data
    def build_prediction_model(data):
        # Prepare data for model
        X = data[['ITN_Coverage', 'IRS_Coverage', 'ACT_Coverage']]
        y = data['Malaria_Rate']
        
        # Build a simple linear regression model
        model = LinearRegression()
        model.fit(X, y)
        
        return model
    
    # Build the model
    model = build_prediction_model(df)
    
    # Current status
    current_avg_rate = (current_data['Malaria_Cases'].sum() / current_data['Population'].sum())
    target_rate = current_avg_rate * (1 - target_reduction/100)
    
    st.markdown(f"""
    ### Current vs Target
    - Current Average Prevalence: **{current_avg_rate:.2%}**
    - Target Prevalence: **{target_rate:.2%}**
    """)
    
    # Function to calculate required interventions
    def calculate_interventions(region_data, target_reduction, cost_modifiers, effect_modifier):
        results = []
        
        for _, row in region_data.iterrows():
            region = row['Region']
            current_rate = row['Malaria_Rate']
            population = row['Population']
            
            # Target rate for this region
            target_rate = current_rate * (1 - target_reduction/100)
            
            # Current coverage
            current_itn = row['ITN_Coverage']
            current_irs = row['IRS_Coverage']
            current_act = row['ACT_Coverage']
            
            # Parameters for this region
            params = region_params[region]
            
            # A simple algorithm to determine new coverage levels
            # This is a simplified model - in real world, more complex optimization would be used
            
            # Calculate the maximum possible reduction with current effectiveness
            max_effect = (params['itn_effect'] + params['irs_effect'] + params['act_effect']) * 0.8 * effect_modifier
            
            if max_effect * 0.95 < target_reduction/100:
                # If target is not achievable even with maximum coverage
                new_itn = min(0.95, current_itn * 1.5)
                new_irs = min(0.8, current_irs * 1.5) 
                new_act = min(0.9, current_act * 1.5)
                achievable = False
            else:
                # Calculate new coverage levels based on effectiveness and current levels
                # This is a simplified approach - in reality, would use optimization
                factor = (target_reduction/100) / max_effect
                
                # Scale up each intervention proportionally
                new_itn = min(0.95, current_itn + (0.95 - current_itn) * factor * 1.2)  # ITN more effective
                new_irs = min(0.8, current_irs + (0.8 - current_irs) * factor)
                new_act = min(0.9, current_act + (0.9 - current_act) * factor * 0.8)   # ACT less effective for prevention
                achievable = True
            
            # Calculate expected new malaria rate
            malaria_reduction = (new_itn * params['itn_effect'] + 
                                new_irs * params['irs_effect'] + 
                                new_act * params['act_effect']) * 0.8 * effect_modifier
            
            expected_rate = current_rate * (1 - malaria_reduction)
            
            # Calculate units needed
            households = population / 5
            itn_units = int(households * new_itn)
            irs_units = int(households * new_irs)
            expected_cases = int(population * expected_rate)
            act_units = int(expected_cases * new_act)
            
            # Calculate costs with modifiers
            itn_cost = itn_units * np.random.uniform(6, 10) * cost_modifiers['itn']
            irs_cost = irs_units * np.random.uniform(3, 7) * cost_modifiers['irs']
            act_cost = act_units * np.random.uniform(1, 3) * cost_modifiers['act']
            total_cost = itn_cost + irs_cost + act_cost
            
            results.append({
                'Region': region,
                'Population': population,
                'Current_Rate': current_rate,
                'Target_Rate': target_rate,
                'Expected_Rate': expected_rate,
                'Current_ITN': current_itn,
                'New_ITN': new_itn,
                'Current_IRS': current_irs,
                'New_IRS': new_irs,
                'Current_ACT': current_act,
                'New_ACT': new_act,
                'ITN_Units': itn_units,
                'IRS_Units': irs_units,
                'ACT_Units': act_units,
                'ITN_Cost': itn_cost,
                'IRS_Cost': irs_cost,
                'ACT_Cost': act_cost,
                'Total_Cost': total_cost,
                'Achievable': achievable
            })
        
        return pd.DataFrame(results)
    
    # Calculate interventions
    cost_modifiers = {
        'itn': itn_cost_modifier,
        'irs': irs_cost_modifier,
        'act': act_cost_modifier
    }
    
    intervention_plan = calculate_interventions(
        current_data, 
        target_reduction, 
        cost_modifiers,
        intervention_effectiveness
    )
    
    # Visualize intervention plan
    col1, col2 = st.columns(2)
    
    with col1:
        # Current vs New coverage
        st.markdown("### Required Intervention Coverage")
        
        coverage_comparison = pd.DataFrame({
            'Region': intervention_plan['Region'],
            'Current ITN': intervention_plan['Current_ITN'],
            'New ITN': intervention_plan['New_ITN'],
            'Current IRS': intervention_plan['Current_IRS'],
            'New IRS': intervention_plan['New_IRS'],
            'Current ACT': intervention_plan['Current_ACT'],
            'New ACT': intervention_plan['New_ACT'],
        })
        
        coverage_long = pd.melt(
            coverage_comparison,
            id_vars=['Region'],
            var_name='Intervention',
            value_name='Coverage'
        )
        
        fig = px.bar(
            coverage_long,
            x='Region',
            y='Coverage',
            color='Intervention',
            barmode='group',
            labels={'Coverage': 'Coverage Rate', 'Region': 'Region'},
            title='Current vs. Required Intervention Coverage by Region'
        )
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Expected impact
        st.markdown("### Expected Impact on Malaria Prevalence")
        
        impact_data = pd.DataFrame({
            'Region': intervention_plan['Region'],
            'Current Rate': intervention_plan['Current_Rate'],
            'Target Rate': intervention_plan['Target_Rate'],
            'Expected Rate': intervention_plan['Expected_Rate']
        })
        
        impact_long = pd.melt(
            impact_data,
            id_vars=['Region'],
            var_name='Metric',
            value_name='Rate'
        )
        
        fig = px.bar(
            impact_long,
            x='Region',
            y='Rate',
            color='Metric',
            barmode='group',
            labels={'Rate': 'Prevalence Rate', 'Region': 'Region'},
            title='Current, Target, and Expected Malaria Rates by Region'
        )
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)
    
    # Units required
    st.markdown("### Intervention Units Required")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("<div class='metric-container'>", unsafe_allow_html=True)
        st.metric("Total ITNs Required", f"{intervention_plan['ITN_Units'].sum():,}")
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("<div class='metric-container'>", unsafe_allow_html=True)
        st.metric("Total IRS Units Required", f"{intervention_plan['IRS_Units'].sum():,}")
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col3:
        st.markdown("<div class='metric-container'>", unsafe_allow_html=True)
        st.metric("Total ACT Treatments Required", f"{intervention_plan['ACT_Units'].sum():,}")
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Detailed plan table
    st.markdown("### Detailed Intervention Plan")
    
    # Check if any regions cannot achieve the target
    unachievable = intervention_plan[~intervention_plan['Achievable']]
    if not unachievable.empty:
        st.warning(f"""
        ⚠️ The target reduction of {target_reduction}% may not be fully achievable in some regions 
        even with maximum intervention coverage. Consider adjusting the target or the intervention 
        effectiveness modifier.
        """)
    
    # Display the table
    display_cols = [
        'Region', 'Population', 
        'Current_Rate', 'Target_Rate', 'Expected_Rate',
        'New_ITN', 'ITN_Units',
        'New_IRS', 'IRS_Units',
        'New_ACT', 'ACT_Units',
        'Total_Cost'
    ]
    
    formatted_plan = intervention_plan[display_cols].copy()
    formatted_plan.columns = [
        'Region', 'Population', 
        'Current Rate', 'Target Rate', 'Expected Rate',
        'ITN Coverage', 'ITN Units',
        'IRS Coverage', 'IRS Units',
        'ACT Coverage', 'ACT Units',
        'Total Cost'
    ]
    
    # Format percentages and costs
    for col in ['Current Rate', 'Target Rate', 'Expected Rate', 'ITN Coverage', 'IRS Coverage', 'ACT Coverage']:
        formatted_plan[col] = formatted_plan[col].apply(lambda x: f"{x:.2%}")
    
    formatted_plan['Total Cost'] = formatted_plan['Total Cost'].apply(lambda x: f"${x:,.2f}")
    
    st.dataframe(formatted_plan, use_container_width=True)
    
    # Download plan as CSV
    csv = intervention_plan.to_csv(index=False)
    st.download_button(
        label="Download Intervention Plan as CSV",
        data=csv,
        file_name=f"malaria_intervention_plan_{target_reduction}pct.csv",
        mime="text/csv"
    )

# Tab 4: Cost Analysis
with tab4:
    st.markdown("<h2 class='sub-header'>Cost Analysis</h2>", unsafe_allow_html=True)
    
    # Calculate total costs
    total_itn_cost = intervention_plan['ITN_Cost'].sum()
    total_irs_cost = intervention_plan['IRS_Cost'].sum()
    total_act_cost = intervention_plan['ACT_Cost'].sum()
    total_intervention_cost = total_itn_cost + total_irs_cost + total_act_cost
    
    # Summary metrics
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("<div class='metric-container'>", unsafe_allow_html=True)
        st.metric("Total Estimated Cost", f"${total_intervention_cost:,.2f}")
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("<div class='metric-container'>", unsafe_allow_html=True)
        current_cases = current_data['Malaria_Cases'].sum()
        expected_cases = (intervention_plan['Population'] * intervention_plan['Expected_Rate']).sum()
        cases_averted = current_cases - expected_cases
        
        cost_per_case = total_intervention_cost / cases_averted if cases_averted > 0 else 0
        st.metric("Cost per Case Averted", f"${cost_per_case:.2f}")
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Cost breakdown pie chart
    st.markdown("### Cost Breakdown by Intervention Type")
    
    cost_data = pd.DataFrame({
        'Intervention': ['ITNs', 'IRS', 'ACT'],
        'Cost': [total_itn_cost, total_irs_cost, total_act_cost]
    })
    
    fig = px.pie(
        cost_data,
        values='Cost',
        names='Intervention',
        title='Proportion of Total Cost by Intervention Type'
    )
    fig.update_layout(height=500)
    st.plotly_chart(fig, use_container_width=True)
    
    # Cost by region
    st.markdown("### Cost Distribution by Region")
    
    region_costs = pd.DataFrame({
        'Region': intervention_plan['Region'],
        'ITN Cost': intervention_plan['ITN_Cost'],
        'IRS Cost': intervention_plan['IRS_Cost'],
        'ACT Cost': intervention_plan['ACT_Cost']
    })
    
    region_costs_long = pd.melt(
        region_costs,
        id_vars=['Region'],
        var_name='Intervention',
        value_name='Cost'
    )
    
    fig = px.bar(
        region_costs_long,
        x='Region',
        y='Cost',
        color='Intervention',
        barmode='stack',
        labels={'Cost': 'Cost ($)', 'Region': 'Region'},
        title='Total Cost by Region and Intervention Type'
    )
    fig.update_layout(height=500)
    st.plotly_chart(fig, use_container_width=True)
    
    # Cost-effectiveness analysis
    st.markdown("### Cost-Effectiveness Analysis")
    
    effectiveness_data = pd.DataFrame({
        'Region': intervention_plan['Region'],
        'Population': intervention_plan['Population'],
        'Current_Rate': intervention_plan['Current_Rate'],
        'Expected_Rate': intervention_plan['Expected_Rate'],
        'Total_Cost': intervention_plan['Total_Cost']
    })
    
    # Calculate cases averted
    effectiveness_data['Current_Cases'] = effectiveness_data['Population'] * effectiveness_data['Current_Rate']
    effectiveness_data['Expected_Cases'] = effectiveness_data['Population'] * effectiveness_data['Expected_Rate']
    effectiveness_data['Cases_Averted'] = effectiveness_data['Current_Cases'] - effectiveness_data['Expected_Cases']
    effectiveness_data['Cost_Per_Case'] = effectiveness_data['Total_Cost'] / effectiveness_data['Cases_Averted']
    
    fig = px.scatter(
        effectiveness_data,
        x='Cases_Averted',
        y='Cost_Per_Case',
        size='Population',
        color='Region',
        hover_name='Region',
        labels={
            'Cases_Averted': 'Malaria Cases Averted',
            'Cost_Per_Case': 'Cost per Case Averted ($)',
            'Population': 'Population'
        },
        title='Cost-Effectiveness by Region'
    )
    fig.update_layout(height=500)
    st.plotly_chart(fig, use_container_width=True)
    
    # Sensitivity analysis
    st.markdown("### Sensitivity Analysis")
    st.write("""
    Adjust the sliders in the sidebar to see how changes in costs and intervention effectiveness
    affect the overall cost and impact of the intervention plan.
    """)
    
    # Calculate scenarios
    scenarios = []
    
    # Base scenario (current settings)
    base = {
        'Scenario': 'Current Plan',
        'ITN Cost Modifier': itn_cost_modifier,
        'IRS Cost Modifier': irs_cost_modifier,
        'ACT Cost Modifier': act_cost_modifier,
        'Effectiveness': intervention_effectiveness,
        'Total Cost': total_intervention_cost,
        'Cases Averted': cases_averted
    }
    scenarios.append(base)
    
    # Higher costs scenario
    high_cost_modifiers = {
        'itn': itn_cost_modifier * 1.25,
        'irs': irs_cost_modifier * 1.25,
        'act': act_cost_modifier * 1.25
    }
    
    high_cost_plan = calculate_interventions(
        current_data, 
        target_reduction, 
        high_cost_modifiers,
        intervention_effectiveness
    )
    
    high_cost = {
        'Scenario': 'Higher Costs (+25%)',
        'ITN Cost Modifier': itn_cost_modifier * 1.25,
        'IRS Cost Modifier': irs_cost_modifier * 1.25,
        'ACT Cost Modifier': act_cost_modifier * 1.25,
        'Effectiveness': intervention_effectiveness,
        'Total Cost': high_cost_plan['Total_Cost'].sum(),
        'Cases Averted': current_cases - (high_cost_plan['Population'] * high_cost_plan['Expected_Rate']).sum()
    }
    scenarios.append(high_cost)
    
    # Lower effectiveness scenario
    low_eff_plan = calculate_interventions(
        current_data, 
        target_reduction, 
        cost_modifiers,
        intervention_effectiveness * 0.8
    )
    
    low_eff = {
        'Scenario': 'Lower Effectiveness (-20%)',
        'ITN Cost Modifier': itn_cost_modifier,
        'IRS Cost Modifier': irs_cost_modifier,
        'ACT Cost Modifier': act_cost_modifier,
        'Effectiveness': intervention_effectiveness * 0.8,
        'Total Cost': low_eff_plan['Total_Cost'].sum(),
        'Cases Averted': current_cases - (low_eff_plan['Population'] * low_eff_plan['Expected_Rate']).sum()
    }
    scenarios.append(low_eff)
    
    # Higher effectiveness scenario
    high_eff_plan = calculate_interventions(
        current_data, 
        target_reduction, 
        cost_modifiers,
        intervention_effectiveness * 1.2
    )
    
    high_eff = {
        'Scenario': 'Higher Effectiveness (+20%)',
        'ITN Cost Modifier': itn_cost_modifier,
        'IRS Cost Modifier': irs_cost_modifier,
        'ACT Cost Modifier': act_cost_modifier,
        'Effectiveness': intervention_effectiveness * 1.2,
        'Total Cost': high_eff_plan['Total_Cost'].sum(),
        'Cases Averted': current_cases - (high_eff_plan['Population'] * high_eff_plan['Expected_Rate']).sum()
    }
    scenarios.append(high_eff)
    
    scenarios_df = pd.DataFrame(scenarios)
    
    # Calculate cost per case averted
    scenarios_df['Cost per Case Averted'] = scenarios_df['Total Cost'] / scenarios_df['Cases Averted']
    
    # Display scenario comparison
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.bar(
            scenarios_df,
            x='Scenario',
            y='Total Cost',
            color='Scenario',
            labels={'Total Cost': 'Total Cost ($)', 'Scenario': 'Scenario'},
            title='Total Cost by Scenario'
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = px.bar(
            scenarios_df,
            x='Scenario',
            y='Cost per Case Averted',
            color='Scenario',
            labels={'Cost per Case Averted': 'Cost per Case Averted ($)', 'Scenario': 'Scenario'},
            title='Cost-Effectiveness by Scenario'
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    # Detailed scenario comparison table
    st.markdown("### Scenario Comparison")
    
    display_scenarios = scenarios_df.copy()
    display_scenarios['Total Cost'] = display_scenarios['Total Cost'].apply(lambda x: f"${x:,.2f}")
    display_scenarios['Cost per Case Averted'] = display_scenarios['Cost per Case Averted'].apply(lambda x: f"${x:.2f}")
    display_scenarios['Cases Averted'] = display_scenarios['Cases Averted'].apply(lambda x: f"{int(x):,}")
    
    st.dataframe(display_scenarios, use_container_width=True)

# Add a footer
st.markdown("""
---
### About this Tool

This tool uses fictional data to model malaria interventions and their impact. In a real-world scenario, this would integrate with:

1. Actual historical data on malaria prevalence and intervention coverage
2. More sophisticated epidemiological models
3. Regional-specific factors affecting malaria transmission
4. Detailed cost data from implementing organizations

For planning real interventions, please consult with public health experts and epidemiologists.
""")
