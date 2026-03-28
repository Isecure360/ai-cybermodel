# ui/components/tables.py
import streamlit as st
import pandas as pd

def display_predictions_table(df: pd.DataFrame):
    """
    Display a table of predictions with colors for phishing/legit.
    Expects columns: ['url', 'prediction', 'probability']
    """
    if df.empty:
        st.warning("No predictions to display")
        return

    # Add a styled column for prediction
    df_display = df.copy()
    df_display["prediction_label"] = df_display["prediction"].apply(
        lambda x: f"✅ Legit" if x == 0 else f"❌ Phishing"
    )
    df_display["probability"] = df_display["probability"].apply(lambda x: f"{x:.2f}")

    st.table(df_display[["url", "prediction_label", "probability"]])


def display_model_info_table(model_metadata: dict, metrics: dict = None):
    """
    Display active model info and optionally its metrics
    model_metadata: {"active_model":..., "feature_version":..., "model_type":..., "version":...}
    metrics: {"accuracy":..., "f1":..., "precision":..., "recall":...}
    """
    st.subheader("Active Model Info")
    info_df = pd.DataFrame.from_dict(model_metadata, orient="index", columns=["Value"])
    st.table(info_df)

    if metrics:
        st.subheader("Model Metrics")
        metrics_df = pd.DataFrame.from_dict(metrics, orient="index", columns=["Value"])
        st.table(metrics_df)


def display_history_table(history_df: pd.DataFrame):
    """
    Display historical predictions or training runs
    Expects columns: ['timestamp', 'url', 'prediction', 'probability']
    """
    if history_df.empty:
        st.info("No history available")
        return

    history_df = history_df.copy()
    history_df["prediction_label"] = history_df["prediction"].apply(
        lambda x: "Legit" if x == 0 else "Phishing"
    )
    history_df["probability"] = history_df["probability"].apply(lambda x: f"{x:.2f}")
    st.dataframe(history_df[["timestamp", "url", "prediction_label", "probability"]], height=400)