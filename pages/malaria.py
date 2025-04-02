import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation
import time
import altair as alt
from collections import deque
import math

# Set page configuration
st.set_page_config(
    page_title="Malaria Agent-Based Simulation",
    layout="wide"
)

# Constants
SUSCEPTIBLE = 'susceptible'
INFECTED = 'infected'
RECOVERED = 'recovered'
DEAD = 'dead'

# Function to initialize agents
def initialize_agents(params):
    agents = []
    population = params['population']
    initial_infected = params['initial_infected']
    canvas_width = 50
    canvas_height = 30
    
    for i in range(population):
        has_bednet = params['use_bednets'] and np.random.random() < params['bednet_coverage']
        
        agents.append({
            'id': i,
            'x': np.random.random() * canvas_width,
            'y': np.random.random() * canvas_height,
            'dx': (np.random.random() - 0.5) * 0.4,  # Reduced speed
            'dy': (np.random.random() - 0.5) * 0.4,  # Reduced speed
            'state': INFECTED if i < initial_infected else SUSCEPTIBLE,
            'days_infected': 1 if i < initial_infected else 0,
            'days_immune': 0,
            'has_bednet': has_bednet
        })
    
    return agents, canvas_width, canvas_height

# Function to update agent positions and states
def update_agents(agents, params, canvas_width, canvas_height):
    # Update positions
    for agent in agents:
        # Skip movement for dead agents
        if agent['state'] == DEAD:
            continue
        
        # Move agent
        x = agent['x'] + agent['dx']
        y = agent['y'] + agent['dy']
        
        # Bounce off walls
        if x < 0 or x > canvas_width:
            x = max(0, min(x, canvas_width))
            agent['dx'] *= -1
            
        if y < 0 or y > canvas_height:
            y = max(0, min(y, canvas_height))
            agent['dy'] *= -1
            
        # Update position
        agent['x'] = x
        agent['y'] = y
    
    # Process infections
    infected_agents = [a for a in agents if a['state'] == INFECTED]
    
    for agent in agents:
        if agent['state'] == SUSCEPTIBLE:
            # Check for infections from nearby infected agents
            for infected_agent in infected_agents:
                distance = math.sqrt(
                    (agent['x'] - infected_agent['x']) ** 2 + 
                    (agent['y'] - infected_agent['y']) ** 2
                )
                
                # Infection occurs within proximity with reduced chance if bednet is used
                if distance < 2:  # Reduced proximity
                    infection_chance = params['transmission_rate']
                    
                    # Reduce transmission if using bednets
                    if agent['has_bednet']:
                        infection_chance *= (1 - params['bednet_efficacy'])
                    
                    if np.random.random() < infection_chance:
                        agent['state'] = INFECTED
                        agent['days_infected'] = 1
                        break  # Once infected, no need to check other infected agents
    
    # Process infected agents (recovery or death)
    for agent in agents:
        if agent['state'] == INFECTED:
            agent['days_infected'] += 1
            
            # Recovery or death check
            if np.random.random() < params['recovery_rate']:
                agent['state'] = RECOVERED
                agent['days_infected'] = 0
                agent['days_immune'] = 1
            elif np.random.random() < params['mortality_rate']:
                agent['state'] = DEAD
                agent['days_infected'] = 0
                
        elif agent['state'] == RECOVERED:
            agent['days_immune'] += 1
            
            # End of immunity period
            if agent['days_immune'] > params['immunity_period']:
                agent['state'] = SUSCEPTIBLE
                agent['days_immune'] = 0
    
    return agents

# Calculate statistics from agents
def calculate_statistics(agents):
    statistics = {
        'susceptible': len([a for a in agents if a['state'] == SUSCEPTIBLE]),
        'infected': len([a for a in agents if a['state'] == INFECTED]),
        'recovered': len([a for a in agents if a['state'] == RECOVERED]),
        'dead': len([a for a in agents if a['state'] == DEAD])
    }
    return statistics

# Plot the current state of the simulation
def plot_simulation(agents, canvas_width, canvas_height):
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Define colors for each state
    colors = {
        SUSCEPTIBLE: '#3498db',  # Blue
        INFECTED: '#e74c3c',     # Red
        RECOVERED: '#2ecc71',    # Green
        DEAD: '#7f8c8d'          # Gray
    }
    
    # Plot agents
    for agent in agents:
        color = colors[agent['state']]
        
        # Draw agent
        circle = plt.Circle((agent['x'], agent['y']), 0.3, color=color)
        ax.add_patch(circle)
        
        # Draw bednet indicator
        if agent['has_bednet'] and agent['state'] != DEAD:
            bednet_circle = plt.Circle(
                (agent['x'], agent['y']), 0.5, 
                fill=False, color='#9b59b6'  # Purple for bednets
            )
            ax.add_patch(bednet_circle)
    
    # Set plot properties
    ax.set_xlim(0, canvas_width)
    ax.set_ylim(0, canvas_height)
    ax.set_aspect('equal')
    ax.set_xticks([])
    ax.set_yticks([])
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)
    
    return fig

# Create a line chart for the disease progression
def plot_disease_progression(history):
    # Create a DataFrame from the history
    df = pd.DataFrame(history)
    
    # Melt the DataFrame to create a format suitable for Altair
    melted_df = df.melt(
        id_vars=['day'],
        value_vars=['susceptible', 'infected', 'recovered', 'dead'],
        var_name='state',
        value_name='count'
    )
    
    # Create the Altair chart
    chart = alt.Chart(melted_df).mark_line().encode(
        x=alt.X('day:Q', title='Day'),
        y=alt.Y('count:Q', title='Population'),
        color=alt.Color('state:N', scale=alt.Scale(
            domain=['susceptible', 'infected', 'recovered', 'dead'],
            range=['#3498db', '#e74c3c', '#2ecc71', '#7f8c8d']
        ))
    ).properties(
        width=600,
        height=300
    ).interactive()
    
    return chart

# Main app
def main():
    st.title("Malaria Agent-Based Simulation")
    
    # Create sidebar for simulation parameters
    st.sidebar.header("Simulation Parameters")
    
    # Population
    population = st.sidebar.slider(
        "Population", 
        min_value=10, 
        max_value=500, 
        value=200, 
        step=10
    )
    
    # Initial infected
    initial_infected = st.sidebar.slider(
        "Initial Infected", 
        min_value=1, 
        max_value=min(50, population), 
        value=5, 
        step=1
    )
    
    # Transmission rate
    transmission_rate = st.sidebar.slider(
        "Transmission Rate", 
        min_value=0.1, 
        max_value=0.9, 
        value=0.4, 
        step=0.05,
        format="%.2f"
    )
    
    # Recovery rate
    recovery_rate = st.sidebar.slider(
        "Recovery Rate", 
        min_value=0.01, 
        max_value=0.3, 
        value=0.1, 
        step=0.01,
        format="%.2f"
    )
    
    # Mortality rate
    mortality_rate = st.sidebar.slider(
        "Mortality Rate", 
        min_value=0.0, 
        max_value=0.2, 
        value=0.03, 
        step=0.01,
        format="%.2f"
    )
    
    # Immunity period
    immunity_period = st.sidebar.slider(
        "Immunity Period (days)", 
        min_value=0, 
        max_value=100, 
        value=30, 
        step=5
    )
    
    # Bed nets
    use_bednets = st.sidebar.checkbox("Use Bed Nets", value=False)
    
    bednet_coverage = 0.5
    bednet_efficacy = 0.7
    
    if use_bednets:
        bednet_coverage = st.sidebar.slider(
            "Bed Net Coverage", 
            min_value=0, 
            max_value=100, 
            value=50, 
            step=5,
            format="%d%%"
        ) / 100.0  # Convert percentage to decimal
        
        bednet_efficacy = st.sidebar.slider(
            "Bed Net Efficacy", 
            min_value=0, 
            max_value=100, 
            value=70, 
            step=5,
            format="%d%%"
        ) / 100.0  # Convert percentage to decimal
    
    # Collect parameters
    params = {
        'population': population,
        'initial_infected': initial_infected,
        'transmission_rate': transmission_rate,
        'recovery_rate': recovery_rate,
        'mortality_rate': mortality_rate,
        'immunity_period': immunity_period,
        'use_bednets': use_bednets,
        'bednet_coverage': bednet_coverage,
        'bednet_efficacy': bednet_efficacy
    }
    
    # Initialize session state for simulation
    if 'agents' not in st.session_state:
        st.session_state.agents, st.session_state.canvas_width, st.session_state.canvas_height = initialize_agents(params)
        st.session_state.day = 0
        st.session_state.running = False
        st.session_state.history = []
        st.session_state.statistics = calculate_statistics(st.session_state.agents)
        st.session_state.history.append({
            'day': st.session_state.day,
            **st.session_state.statistics
        })
    
    # Create two columns for the simulation view and controls
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Display the simulation
        st.subheader("Simulation View")
        simulation_plot = st.empty()
        
        # Plot initial state
        fig = plot_simulation(
            st.session_state.agents,
            st.session_state.canvas_width,
            st.session_state.canvas_height
        )
        simulation_plot.pyplot(fig)
        plt.close(fig)
        
        # Display disease progression chart
        st.subheader("Disease Progression")
        chart_container = st.empty()
        
        if len(st.session_state.history) > 1:
            chart = plot_disease_progression(st.session_state.history)
            chart_container.altair_chart(chart, use_container_width=True)
    
    with col2:
        # Display statistics
        st.subheader("Current Statistics")
        
        stats_container = st.container()
        
        # Create colored metrics for each statistic
        stats_container.markdown(f"**Day:** {st.session_state.day}")
        
        susceptible_col, infected_col = stats_container.columns(2)
        recovered_col, dead_col = stats_container.columns(2)
        
        susceptible_col.markdown(
            f"<div style='color:#3498db;font-weight:bold;'>Susceptible: {st.session_state.statistics['susceptible']}</div>", 
            unsafe_allow_html=True
        )
        
        infected_col.markdown(
            f"<div style='color:#e74c3c;font-weight:bold;'>Infected: {st.session_state.statistics['infected']}</div>", 
            unsafe_allow_html=True
        )
        
        recovered_col.markdown(
            f"<div style='color:#2ecc71;font-weight:bold;'>Recovered: {st.session_state.statistics['recovered']}</div>", 
            unsafe_allow_html=True
        )
        
        dead_col.markdown(
            f"<div style='color:#7f8c8d;font-weight:bold;'>Dead: {st.session_state.statistics['dead']}</div>", 
            unsafe_allow_html=True
        )
        
        # Control buttons
        st.subheader("Controls")
        
        button_col1, button_col2 = st.columns(2)
        
        with button_col1:
            if st.button("Start/Stop"):
                st.session_state.running = not st.session_state.running
        
        with button_col2:
            if st.button("Reset"):
                st.session_state.agents, st.session_state.canvas_width, st.session_state.canvas_height = initialize_agents(params)
                st.session_state.day = 0
                st.session_state.running = False
                st.session_state.history = []
                st.session_state.statistics = calculate_statistics(st.session_state.agents)
                st.session_state.history.append({
                    'day': st.session_state.day,
                    **st.session_state.statistics
                })
                
                # Update the plots
                fig = plot_simulation(
                    st.session_state.agents,
                    st.session_state.canvas_width,
                    st.session_state.canvas_height
                )
                simulation_plot.pyplot(fig)
                plt.close(fig)
    
    # About this simulation section
    with st.expander("About This Simulation"):
        st.markdown("""
        ### Goal and Utility
        
        This interactive simulation aims to demonstrate how infectious diseases like malaria spread through populations and how public health interventions (like bed nets) can impact disease dynamics. It serves as an educational tool for understanding:
        
        - Basic epidemiological concepts (transmission, recovery, immunity)
        - The impact of different parameters on disease spread
        - How preventive measures like bed nets can reduce transmission
        - Population-level effects of individual interventions
        
        ### Simulation Details
        
        This is a simplified agent-based model of malaria transmission in a population. Each dot represents a person who can be in one of four states:
        
        - **Susceptible (Blue)**: Can become infected when near infected individuals
        - **Infected (Red)**: Has malaria and can spread it to susceptible individuals
        - **Recovered (Green)**: Temporarily immune to malaria
        - **Dead (Gray)**: Deceased due to malaria complications
        
        The purple circles around some individuals represent bed nets, which reduce the chance of malaria transmission.
        
        Adjust the parameters to see how different factors affect the spread of malaria in the population. Try scenarios with different intervention strategies by changing the bed net coverage and efficacy.
        """)
    
    # Run simulation if active
    if st.session_state.running and st.session_state.statistics['infected'] > 0:
        st.session_state.agents = update_agents(
            st.session_state.agents,
            params,
            st.session_state.canvas_width,
            st.session_state.canvas_height
        )
        
        st.session_state.day += 1
        st.session_state.statistics = calculate_statistics(st.session_state.agents)
        
        st.session_state.history.append({
            'day': st.session_state.day,
            **st.session_state.statistics
        })
        
        # Update the simulation plot
        fig = plot_simulation(
            st.session_state.agents,
            st.session_state.canvas_width,
            st.session_state.canvas_height
        )
        simulation_plot.pyplot(fig)
        plt.close(fig)
        
        # Update the disease progression chart
        if len(st.session_state.history) > 1:
            chart = plot_disease_progression(st.session_state.history)
            chart_container.altair_chart(chart, use_container_width=True)
        
        # Rerun the app to continue the simulation
        time.sleep(0.1)  # Small delay to control simulation speed
        st.experimental_rerun()
    elif st.session_state.running and st.session_state.statistics['infected'] == 0:
        st.session_state.running = False
        st.info("Simulation complete - no more infected individuals remaining.")

if __name__ == "__main__":
    main()
