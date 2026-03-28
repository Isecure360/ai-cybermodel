# 📍 ui/app.py
import streamlit as st
import pandas as pd
import requests
from datetime import datetime
from utils import get_prediction, get_model_info
from components.cards import prediction_card
from components.charts import probability_bar_chart
# --------------------------
# CONFIG
# --------------------------
st.set_page_config(
    page_title="Phishing Detection Dashboard",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

API_BASE_URL = "http://localhost:8000/api/v1"

# --------------------------
# SIDEBAR NAVIGATION
# --------------------------
st.sidebar.title("🛡️ Phishing Detection")
menu = st.sidebar.radio("Navigate", ["Prediction", "Batch Upload", "Model Info", "History"])

# --------------------------
# PREDICTION PAGE
# --------------------------
if menu == "Prediction":
    st.title("🔗 Single URL Prediction")
    url_input = st.text_input("Enter URL to check:", placeholder="https://example.com/login")

    if st.button("Predict"):
        if not url_input:
            st.warning("Please enter a URL to proceed!")
        else:
            with st.spinner("Checking URL..."):
                try:
                    result = get_prediction(url_input, API_BASE_URL)
                    st.success("Prediction Complete!")
                    col1, col2, col3 = st.columns([2, 1, 1])
                    col1.write(f"**URL:** {result['url']}")
                    col2.metric("Prediction", "Phishing" if result['prediction'] else "Legit",
                                delta=f"{result['probability']*100:.2f}%")
                    col3.write(f"**Probability:** {result['probability']:.2f}")
                except Exception as e:
                    st.error(f"Prediction failed: {str(e)}")

# --------------------------
# BATCH UPLOAD PAGE
# --------------------------
elif menu == "Batch Upload":
    st.title("📁 Batch URL Prediction")
    uploaded_file = st.file_uploader("Upload CSV/Excel file with URLs", type=["csv", "xlsx"])

    if uploaded_file:
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        if "url" not in df.columns:
            st.warning("Your file must contain a column named `url`")
        else:
            st.info("Processing batch predictions...")
            df["prediction"] = None
            df["probability"] = None

            for idx, row in df.iterrows():
                try:
                    pred = get_prediction(row["url"], API_BASE_URL)
                    df.at[idx, "prediction"] = "Phishing" if pred["prediction"] else "Legit"
                    df.at[idx, "probability"] = pred["probability"]
                except:
                    df.at[idx, "prediction"] = "Error"
                    df.at[idx, "probability"] = None

            st.success("Batch Prediction Complete!")
            st.dataframe(df)
            st.download_button(
                "📥 Download Results",
                df.to_csv(index=False).encode('utf-8'),
                file_name=f"batch_predictions_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )

# --------------------------
# MODEL INFO PAGE
# --------------------------
elif menu == "Model Info":
    st.title("🤖 Active Model Metadata")
    try:
        model_info = get_model_info(API_BASE_URL)
        st.write("**Active Model:**", model_info.get("active_model"))
        st.write("**Feature Version:**", model_info.get("feature_version"))
        st.write("**Model Type:**", model_info.get("model_type"))
        st.write("**Version:**", model_info.get("version"))
    except Exception as e:
        st.error(f"Failed to fetch model info: {str(e)}")

# --------------------------
# HISTORY PAGE
# --------------------------
elif menu == "History":
    st.title("📜 Past Predictions")
    try:
        history_df = pd.read_csv("data/predictions_cache.csv")
        st.dataframe(history_df)
        st.download_button(
            "📥 Download History",
            history_df.to_csv(index=False).encode("utf-8"),
            file_name=f"prediction_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )
    except FileNotFoundError:
        st.warning("No historical predictions found.")