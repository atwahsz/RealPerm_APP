# Install necessary libraries
# !pip install streamlit plotly pandas numpy scipy

import streamlit as st
import plotly.graph_objs as go
import numpy as np
import pandas as pd
from scipy.optimize import curve_fit

# Title of the App
st.title("Relative Permeability Curve App")

# Add Markdown text for description
st.markdown("""
This application visualizes the relative permeability curves for oil and water in porous media. 
It is particularly useful for reservoir engineering studies. Adjust the parameters below to see how they affect the curves.
""")

# Example Section
st.subheader("Example Parameters")
st.markdown("""
To get started, you can use the following example parameters:

- **Swc (Water Saturation)**: 0.2
- **Sor (Residual Oil Saturation)**: 0.2
- **Krw0 (Endpoint Water Relative Permeability)**: 0.3
- **Kro0 (Endpoint Oil Relative Permeability)**: 0.8
- **Nw (Water Corey Exponent)**: 2.0
- **No (Oil Corey Exponent)**: 2.0

These values can be adjusted using the sliders on the sidebar.
""")

# Sidebar for user input parameters with example values
st.sidebar.header("Input Parameters")
swc = st.sidebar.slider("Swc (Water Saturation)", 0.0, 1.0, 0.2)  # Example: 0.2
sor = st.sidebar.slider("Sor (Residual Oil Saturation)", 0.0, 1.0, 0.2)  # Example: 0.2
krw0 = st.sidebar.slider("Krw0 (End-point Water Relative Permeability)", 0.0, 1.0, 0.3)  # Example: 0.3
kro0 = st.sidebar.slider("Kro0 (End-point Oil Relative Permeability)", 0.0, 1.0, 0.8)  # Example: 0.8
nw = st.sidebar.slider("Nw (Water Corey Exponent)", 1.0, 10.0, 2.0)  # Example: 2.0
no = st.sidebar.slider("No (Oil Corey Exponent)", 1.0, 10.0, 2.0)  # Example: 2.0

# Corey model for relative permeability
def corey_model(Sw, Swc, Sor, krw0, kro0, nw, no):
    Se = (Sw - Swc) / (1 - Swc - Sor)
    krw = krw0 * Se**nw
    kro = kro0 * (1 - Se)**no
    return krw, kro

# Water saturation array
Sw = np.linspace(swc, 1 - sor, 100)

# Calculate krw and kro
krw, kro = corey_model(Sw, swc, sor, krw0, kro0, nw, no)

# Create a Plotly figure
fig = go.Figure()

# Add krw curve
fig.add_trace(go.Scatter(
    x=Sw, y=krw, mode='lines', name='Krw',
    line=dict(color='blue', width=2),
))

# Add kro curve
fig.add_trace(go.Scatter(
    x=Sw, y=kro, mode='lines', name='Kro',
    line=dict(color='red', width=2),
))

# Customize layout
fig.update_layout(
    title="Relative Permeability vs Water Saturation",
    xaxis_title="Water Saturation (Sw)",
    yaxis_title="Relative Permeability",
    legend_title="Permeability",
    template="plotly_white"
)

# Display the plot
st.plotly_chart(fig)

# Display data in a table
data = pd.DataFrame({
    "Water Saturation (Sw)": Sw,
    "Krw": krw,
    "Kro": kro
})

# Show the dataframe
st.subheader("Relative Permeability Data")
st.write(data)

# Option to download the data as CSV
csv = data.to_csv(index=False)
st.download_button(
    label="Download data as CSV",
    data=csv,
    file_name='relative_permeability_data.csv',
    mime='text/csv'
)
