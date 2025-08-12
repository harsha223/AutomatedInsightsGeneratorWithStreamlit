import streamlit as st
st.set_option('deprecation.showPyplotGlobalUse', False)
st.title('E-commerce Company Insights')
st.write('Here is our LLM generated dashboard')
import matplotlib.pyplot as plt

# Data
countries = ['Brasil', 'Japan', 'United States', 'Colombia', 'Spain', 'China', 'Australia', 'France', 'Germany', 'Belgium', 'South Korea', 'Poland', 'United Kingdom']
users = [6244, 1008, 9247, 7, 1694, 14000, 763, 2086, 1799, 448, 2240, 119, 1631]

# Plot
plt.figure(figsize=(10, 8))
plt.barh(countries, users, color='skyblue')
plt.xlabel('Number of Users')
plt.ylabel('Country')
plt.title('Number of Users Coming via Facebook by Country')
plt.tight_layout()

st.pyplot()
