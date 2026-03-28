# ui/components/charts.py
import streamlit as st
import altair as alt
import pandas as pd

def probability_bar_chart(predictions: pd.DataFrame):
    """
    Display probability distribution for a batch of predictions.
    Expects a DataFrame with columns: ['url', 'prediction', 'probability']
    """
    if predictions.empty:
        st.warning("No predictions to display")
        return

    chart = alt.Chart(predictions).mark_bar().encode(
        x=alt.X('url:N', title='URL', axis=alt.Axis(labelAngle=-45)),
        y=alt.Y('probability:Q', title='Probability'),
        color=alt.Color('prediction:N', scale=alt.Scale(domain=['Legit', 'Phishing'], range=['green', 'red']))
    ).properties(
        width=700,
        height=400,
        title="Prediction Probabilities"
    )

    st.altair_chart(chart, use_container_width=True)