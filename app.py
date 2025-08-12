import streamlit as st
st.set_option('deprecation.showPyplotGlobalUse', False)
st.title('E-commerce Company Insights')
st.write('Here is our LLM generated dashboard')
import matplotlib.pyplot as plt
import pandas as pd

# Data
data = {
    'year': [2020]*12 + [2021]*12 + [2022]*12 + [2023]*12,
    'month': list(range(1, 13))*4,
    'number_of_orders': [
        150, 120, 180, 160, 200, 190, 210, 220, 230, 240, 250, 260,
        270, 280, 290, 300, 310, 320, 330, 340, 350, 360, 370, 380,
        390, 400, 410, 420, 430, 440, 450, 460, 470, 480, 490, 500,
        510, 520, 530, 540, 550, 560, 570, 580, 590, 600, 610, 620
    ]
}

# Creating DataFrame
df = pd.DataFrame(data)

# Creating a 'date' column for plotting
df['date'] = pd.to_datetime(df[['year', 'month']].assign(DAY=1))

# Plotting
plt.figure(figsize=(15, 7))
plt.plot(df['date'], df['number_of_orders'], marker='o', linestyle='-', color='b')
plt.title('Number of Orders Per Month (Jan 2020 - Dec 2023)')
plt.xlabel('Date')
plt.ylabel('Number of Orders')
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()

st.pyplot()
