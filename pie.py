import random
import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd

st.header("Pie Dash by Brandon Salazar")
# Initialize session state to store the counts
if "responses" not in st.session_state:
    st.session_state.responses = {"Yes": 0, "No": 0}

# Title and question input
chart_title = st.text_input("Enter a title for your pie chart:")
question = st.text_input("Ask a Yes/No question:")

# Number of responses input
num_responses = st.number_input("How many responses do you want?", min_value=1, step=1, value=1)

# Button to generate the responses
if st.button("Generate Responses"):
    if chart_title and question:
        for _ in range(num_responses):
            response = random.choice(["Yes", "No"])
            st.session_state.responses[response] += 1
        st.write(f"Question: **{question}**")
        st.write(f"Generated {num_responses} responses.")
    elif not chart_title:
        st.warning("Please enter a title for the pie chart.")
    else:
        st.warning("Please enter a question.")


# Pie chart function
def create_pie_chart():
    fig, ax = plt.subplots()
    labels = st.session_state.responses.keys()
    sizes = st.session_state.responses.values()

    # Check if all values are zero
    if sum(sizes) == 0:
        ax.text(0.5, 0.5, "No data yet", horizontalalignment='center', verticalalignment='center',
                transform=ax.transAxes, fontsize=12)
        ax.set_xticks([])
        ax.set_yticks([])
    else:
        colors = ['#66b3ff', '#ff9999']
        explode = (0.1, 0)  # "explode" the Yes slice
        ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors, explode=explode)
        ax.set_title(chart_title if chart_title else "Yes vs No Responses")

    return fig


# Display the pie chart
st.pyplot(create_pie_chart())

# Show counts
st.write("### Response Counts:")
st.write(st.session_state.responses)

# Export to CSV
if st.button("Export to CSV"):
    # Prepare the data for export
    data = pd.DataFrame.from_dict(st.session_state.responses, orient="index", columns=["Count"])
    data.index.name = "Response"

    # Save to CSV
    csv_file = f"{chart_title.replace(' ', '_')}_responses.csv" if chart_title else "responses.csv"
    data.to_csv(csv_file)

    st.success(f"Data exported successfully to {csv_file}")
    st.download_button(
        label="Download CSV File",
        data=open(csv_file, "rb").read(),
        file_name=csv_file,
        mime="text/csv",
    )
