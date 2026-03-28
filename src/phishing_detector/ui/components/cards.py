# ui/components/cards.py
import streamlit as st

def prediction_card(url: str, prediction: str, probability: float):
    """
    Display a prediction as a colored card.
    """
    color = "red" if prediction.lower() == "phishing" else "green"
    st.markdown(f"""
    <div style="
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
        background-color: #f5f5f5;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    ">
        <h4 style="margin: 0;">URL:</h4>
        <p style="margin: 0; word-break: break-all;">{url}</p>
        <h4 style="margin-top: 10px; margin-bottom: 5px;">Prediction:</h4>
        <span style="
            color: white;
            background-color: {color};
            padding: 5px 10px;
            border-radius: 5px;
            font-weight: bold;
        ">{prediction}</span>
        <p style="margin-top: 5px;">Probability: {probability:.2f}</p>
    </div>
    """, unsafe_allow_html=True)