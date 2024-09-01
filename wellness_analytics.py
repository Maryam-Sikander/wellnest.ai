import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime

class WellnessAnalytics:
    def __init__(self):
        # Initialize session state data 
        if 'data' not in st.session_state:
            st.session_state.data = pd.DataFrame(columns=[
                'Date', 'Work Hours', 'Mood', 'Energy', 'Hydration',
                'Walking', 'Meditation', 'Sleep Hours', 'Stress Level',
                'Social Time', 'Balance Score'
            ])
    
    def calculate_balance_score(self, work_hours, mood, energy, hydration, walking, meditation, sleep_hours, stress_level, social_time):
        work_life_balance = max(0, 10 - (work_hours / 2.4))
        mood_score = mood
        energy_score = energy
        hydration_score = min(10, hydration / 0.8)
        exercise_score = min(10, walking / 6)
        mindfulness_score = min(10, meditation / 3)
        sleep_score = min(10, sleep_hours / 0.8)
        stress_management_score = max(0, 10 - stress_level)
        social_score = min(10, social_time * 5)
        
        total_score = (
            work_life_balance +
            mood_score +
            energy_score +
            hydration_score +
            exercise_score +
            mindfulness_score +
            sleep_score +
            stress_management_score +
            social_score
        ) / 9
        
        balance_score = round(total_score * 10, 2)
        
        return balance_score
    
    def get_suggestion(self, score):
        if score >= 75:
            return "🎉 Great job! You're maintaining a good balance."
        elif score >= 50:
            return "👍 You're on the right track, but there's room for improvement."
        else:
            return "🌱 It looks like there's room for improvement. Let's make some positive adjustments to bring more harmony into your routine. You've got this!"
    
    def display_wellness_tracking(self):
        st.subheader("YOUR WELLNESS SCORE & PROGRESS")
        col1, col2, col3 = st.columns(3)

        with col1:
            work_hours = st.number_input("Work Hours", min_value=0, max_value=24, value=8)
            sleep_hours = st.number_input("Sleep Hours", min_value=0, max_value=24, value=7)
            social_time = st.number_input("Social Time (hours)", min_value=0, max_value=24, value=1)

        with col2:
            hydration = st.number_input("Glasses of Water", min_value=0, max_value=20, value=4)
            walking = st.number_input("Walking (minutes)", min_value=0, max_value=300, value=30)
            meditation = st.number_input("Meditation (minutes)", min_value=0, max_value=120, value=10)

        with col3:
            stress_level = st.slider("Stress Level", min_value=1, max_value=10, value=5)
            mood = st.slider("Your Mood", min_value=1, max_value=10, value=5)
            energy = st.slider("Energy Level", min_value=1, max_value=10, value=5)

        if st.button("Get Wellbeing Score"):
            balance_score = self.calculate_balance_score(work_hours, mood, energy, hydration, walking, meditation, sleep_hours, stress_level, social_time)
            new_data = pd.DataFrame({
                'Date': [datetime.now().date()],
                'Work Hours': [work_hours],
                'Mood': [mood],
                'Energy': [energy],
                'Hydration': [hydration],
                'Walking': [walking],
                'Meditation': [meditation],
                'Sleep Hours': [sleep_hours],
                'Stress Level': [stress_level],
                'Social Time': [social_time],
                'Balance Score': [balance_score]
            })
            st.session_state.data = pd.concat([st.session_state.data, new_data], ignore_index=True)
            st.success("Data saved successfully!")

        # Display latest balance score and suggestion
        if not st.session_state.data.empty:
            latest_score = st.session_state.data['Balance Score'].iloc[-1]
            st.subheader(f"YOUR WELLBEING SCORE: {latest_score}%")
            st.write(self.get_suggestion(latest_score))

            # gauge chart
            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=latest_score,
                domain={'x': [0, 1], 'y': [0, 1]},
                title={'text': "WELLBEING SCORE"},
                gauge={
                    'axis': {'range': [0, 100]},
                    'bar': {'color': "darkblue"},
                    'steps': [
                        {'range': [0, 50], 'color': "lightcoral"},
                        {'range': [50, 75], 'color': "lightyellow"},
                        {'range': [75, 100], 'color': "lightgreen"}
                    ],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': 90
                    }
                }
            ))
            st.plotly_chart(fig)

            st.markdown("---")
            st.write("Your Progress Analytics")

            # Heatmap for daily activities
            activities = ['Work Hours', 'Sleep Hours', 'Walking', 'Meditation', 'Social Time']
            heatmap_data = st.session_state.data[['Date'] + activities].set_index('Date')
            color_scale = px.colors.sequential.Teal

            fig = px.imshow(
                heatmap_data.T,
                labels=dict(x="Date", y="Activity", color="Hours"),
                aspect="auto",
                title="Daily Activities Heatmap",
                color_continuous_scale=color_scale  # Apply the color scale
            )

            st.plotly_chart(fig)

            # Radar chart 
            latest_day = st.session_state.data.iloc[-1]
            categories = ['Work-Life Balance', 'Mood', 'Energy', 'Hydration', 'Exercise', 'Mindfulness', 'Sleep', 'Stress Management', 'Social']
            values = [
                10 - (latest_day['Work Hours'] / 2.4), latest_day['Mood'], latest_day['Energy'],
                latest_day['Hydration'] / 0.8, latest_day['Walking'] / 6, latest_day['Meditation'] / 3,
                latest_day['Sleep Hours'] / 0.8, 10 - latest_day['Stress Level'], latest_day['Social Time'] * 5
            ]

            fig = go.Figure(data=go.Scatterpolar(
                r=values,
                theta=categories,
                fill='toself'
            ))
            fig.update_layout(
                polar=dict(
                    radialaxis=dict(visible=True, range=[0, 10])
                ),
                showlegend=False,
                title="Today's well-being Radar"
            )
            st.plotly_chart(fig)

        # Display PAST data
        st.subheader("Your Wellness Data")
        st.dataframe(st.session_state.data)
