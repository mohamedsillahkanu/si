import streamlit as st
import pandas as pd
import altair as alt

# Set title
st.title('TEAM 6: DEEP LEARNING FOR WILDFIRE DETECTION AND PREDICTION')

# Header
st.sidebar.markdown("---")
st.sidebar.markdown("Team 6 - Wildfire Dectection")

# Sidebar navigation
page = st.sidebar.selectbox("Select a Page", ["Topic", "Why", "Wildfire Definition", "Video of wildfire", "Fire Image", "No Fire Image", "Problem Statement","Objective", "Dataset Overview", "Workflow Diagram",'Models','Prediction', "Conclusion", "Project Summary", "Thank you"])

if page == "Topic":
    # Modelling Images
    st.header('TOPIC')
    topic_url = 'https://raw.githubusercontent.com/Archonz-crazy/DL_final_project/main/code/resources/Slide1.JPG'
    # Display image
    st.image(topic_url)

elif page == "Why":
    # Modelling Images
    st.header('WHY?')
    agenda_url = 'https://raw.githubusercontent.com/Archonz-crazy/DL_final_project/main/code/resources/Slide2.JPG'
    # Display image
    st.image(agenda_url)

elif page == "Wildfire Definition":
    # Modelling Images
    st.header('WILDFIRE DEFINITION')
    agenda_url = 'https://raw.githubusercontent.com/Archonz-crazy/DL_final_project/main/code/resources/Slide3.JPG'
    # Display image
    st.image(agenda_url)

elif page == "Video of wildfire":
    # URL to MOV file
    video_url = 'https://raw.githubusercontent.com/Archonz-crazy/DL_final_project/main/code/resources/fire1.mov'
    # Display video
    st.video(video_url)
    st.write('This is a vidoe of a wildfire which shows how deadly it can be and how fast it spreads over an area')

elif page == "Fire Image":
    # Modelling Images
    st.header('FIRE IMAGE')
    fire_url = 'https://raw.githubusercontent.com/Archonz-crazy/DL_final_project/main/code/resources/Slide4.JPG'
    # Display image
    st.image(fire_url)

elif page == "No Fire Image":
    # Modelling Images
    st.header('NO FIRE IMAGE')
    nofire_url = 'https://raw.githubusercontent.com/Archonz-crazy/DL_final_project/main/code/resources/Slide5.JPG'
    # Display image
    st.image(nofire_url)

elif page == "Problem Statement":
    # Modelling Images
    st.header('PROBLEM STATEMENT')
    prob_url = 'https://raw.githubusercontent.com/Archonz-crazy/DL_final_project/main/code/resources/Slide6.JPG'
    # Display image
    st.image(prob_url)

elif page == 'Objective':
    # Modelling Images
    st.header('OBJECTIVE')
    prob_url = 'https://github.com/Archonz-crazy/DL_final_project/blob/main/code/resources/Slide7.JPG?raw=true'
    # Display image
    st.image(prob_url)

elif page == "Dataset Overview":
    st.header("DATASET OVERVIEW")
    prob_url = 'https://github.com/Archonz-crazy/DL_final_project/blob/main/code/resources/Slide8.JPG?raw=true'
    # Display image
    st.image(prob_url)
    # Visualization graphs
    st.header('Visualization Graphs')

    # Dummy data for visualization
    data = {'Class': ['Fire', 'NoFire'], 'Count': [6000, 5000]}
    df = pd.DataFrame(data)

    # Bar graph for Fire
    st.subheader('Bar Graph for Fire and NoFire Images')
    fig_fire = alt.Chart(df).mark_bar().encode(
        x='Class',
        y='Count',
        tooltip=['Class', 'Count']
    ).interactive()
    st.altair_chart(fig_fire, use_container_width=True)

    # Fire images
    data1 = {'Class': ['Train', 'Test', 'Valid'], 'Count': [9000, 1000, 1000]}
    df1 = pd.DataFrame(data1)

    # Bar graph for Fire
    st.subheader('Bar Graph for Fire Images')
    fig_fire1 = alt.Chart(df1).mark_bar().encode(
        x='Class',
        y='Count',
        tooltip=['Class', 'Count']
    ).interactive()
    st.altair_chart(fig_fire1, use_container_width=True)

    # NoFire images
    data2 = {'Class': ['Train', 'Test', 'Valid'], 'Count': [5400, 800, 800]}
    df2 = pd.DataFrame(data2)
    # Bar graph for NoFire
    st.subheader('Bar Graph for NoFire Images')
    fig_fire2 = alt.Chart(df2).mark_bar().encode(
        x='Class',
        y='Count',
        tooltip=['Class', 'Count']
    ).interactive()
    st.altair_chart(fig_fire2, use_container_width=True)

elif page == "Workflow Diagram":
    # Modelling Images
    st.header('WORKFLOW DIAGRAM')
    work_url = 'https://github.com/Archonz-crazy/DL_final_project/blob/main/code/resources/slide9.jpeg?raw=true'
    # Display image
    st.image(work_url)
    
elif page == "Project Summary":

    st.title("Team 6 AI - Wildfire Detection Project")

    st.write(
        """
        A wildfire, also known as a forest fire, bushfire, or vegetation fire, is an uncontrolled fire that spreads rapidly through vegetation, such as forests, grasslands, or shrublands.
        Wildfires can be ignited by various sources, including lightning, human activities, or volcanic eruptions. Our objective is to develop a deep learning-based system for early wildfire detection and prediction.
        We utilize over 10,000 images from various types of wildfires such as forest fires, grass fires, and bushfires.
        """
    )

    st.title("Implementation Plan")

    st.write(
        """
        1. Data Preparation:
           - Load and preprocess the FlameVision Dataset.
           - Augment training data for model robustness.

        2. Model Selection:
           - Choose Convolutional Neural Network as the deep learning architecture.
           - Explore pre-trained models and transfer learning techniques.

        3. Model Training:
           - Adjust hyperparameters.
           - Implement early stopping and learning rate scheduling.
           - Evaluate performance on the validation set.

        4. Model Evaluation:
           - Assess the model's performance on the test set.
           - Analyze strengths and weaknesses.

        5. Fine-tuning and Optimization:
           - Adjust the model based on performance analysis.
           - Experiment with optimization techniques (learning rates, regularization, dropout).

        6. Real-time Detection and Prediction:
           - Develop a pipeline for real-time wildfire images or video streams.
           - Apply the trained model for detection and prediction.
           - Implement post-processing to filter false positives.

        Finally, we trained a robust model that can accurately detect and classify different types of wildfires.
        The system utilizes deep learning algorithms and image processing techniques to analyze real-time wildfire images, enabling timely response and mitigation efforts.
        Thank you all for your attention!
        """
    )