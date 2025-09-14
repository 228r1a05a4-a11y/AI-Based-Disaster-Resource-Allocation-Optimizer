
import streamlit as st
import pandas as pd
import joblib
import plotly.express as px

# Load trained model
model = joblib.load("disaster_resource_model.pkl")

st.set_page_config(page_title="Disaster Resource Allocation Optimizer", layout="centered")

st.title("🌍 AI-Based Disaster Resource Allocation Optimizer")

st.write("Enter disaster details below to estimate affected population and required resources:")

# Input fields
year = st.number_input("Year", min_value=1970, max_value=2100, value=2025)
country = st.text_input("Country", "India")
region = st.text_input("Region", "South Asia")
continent = st.text_input("Continent", "Asia")
disaster_group = st.selectbox("Disaster Group", ["Natural", "Technological"])
disaster_subgroup = st.text_input("Disaster Subgroup", "Hydrological")
disaster_type = st.text_input("Disaster Type", "Flood")
disaster_subtype = st.text_input("Disaster Subtype", "Flash flood")
dis_mag_value = st.number_input("Disaster Magnitude Value", min_value=0.0, max_value=10.0, value=7.5)

# Predict button
if st.button("🔮 Predict Impact"):
    # Build DataFrame
    sample = pd.DataFrame([{
        "Year": year,
        "Country": country,
        "Region": region,
        "Continent": continent,
        "Disaster Group": disaster_group,
        "Disaster Subgroup": disaster_subgroup,
        "Disaster Type": disaster_type,
        "Disaster Subtype": disaster_subtype,
        "Dis Mag Value": dis_mag_value
    }])

    # Predict
    predicted = int(model.predict(sample)[0])
    st.success(f"Estimated Affected Population: {predicted:,}")

    # Resource calculation
    resources = {
        "Food (packets)": predicted * 14,
        "Water (liters)": predicted * 21,
        "Shelter (tents)": predicted * 0.25,
        "Medical Kits": predicted * 0.1
    }

    st.subheader("📦 Estimated Resource Requirements")
    for k, v in resources.items():
        st.write(f"**{k}**: {v:,.0f}")

    # Create DataFrame for chart
    df_resources = pd.DataFrame({
        "Resource": list(resources.keys()),
        "Quantity": list(resources.values())
    })

    # Plotly bar chart
    fig = px.bar(df_resources, x="Resource", y="Quantity",
                 text="Quantity", title="Resource Demand",
                 labels={"Quantity": "Required Quantity"},
                 color="Resource")
    fig.update_traces(texttemplate='%{text:,.0f}', textposition='outside')
    fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')

    st.plotly_chart(fig, use_container_width=True)
