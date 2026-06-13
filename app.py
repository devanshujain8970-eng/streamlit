import streamlit as st
import pandas as pd
import os

FILE_NAME = "hidden_gems.csv"

# Create file if it doesn't exist
if not os.path.exists(FILE_NAME):
    df = pd.DataFrame(columns=[
        "Place Name",
        "City",
        "Category",
        "Description"
    ])
    df.to_csv(FILE_NAME, index=False)

st.set_page_config(
    page_title="LocalLens",
    page_icon="🌍",
    layout="wide"
)

st.title("🌍 LocalLens")
st.subheader("Discover Hidden Gems Recommended by Locals")

# Sidebar Filters
st.sidebar.header("Search Hidden Gems")

df = pd.read_csv(FILE_NAME)

cities = ["All"] + sorted(df["City"].dropna().unique().tolist())
categories = ["All"] + sorted(df["Category"].dropna().unique().tolist())

selected_city = st.sidebar.selectbox(
    "Choose City",
    cities
)

selected_category = st.sidebar.selectbox(
    "Choose Category",
    categories
)

# Filter Data
filtered_df = df.copy()

if selected_city != "All":
    filtered_df = filtered_df[
        filtered_df["City"] == selected_city
    ]

if selected_category != "All":
    filtered_df = filtered_df[
        filtered_df["Category"] == selected_category
    ]

# Display Posts
st.header("📍 Explore Hidden Gems")

if len(filtered_df) == 0:
    st.info("No hidden gems found.")
else:
    for index, row in filtered_df.iterrows():
        with st.container():
            st.markdown(f"## {row['Place Name']}")
            st.markdown(f"**City:** {row['City']}")
            st.markdown(f"**Category:** {row['Category']}")
            st.write(row['Description'])
            st.divider()

# Add New Place
st.header("➕ Add a Hidden Gem")

with st.form("add_place"):

    place_name = st.text_input("Place Name")

    city = st.text_input("City")

    category = st.selectbox(
        "Category",
        [
            "Restaurant",
            "Cafe",
            "View Point",
            "Nature",
            "Park",
            "Shopping",
            "Photography",
            "Cultural Spot"
        ]
    )

    description = st.text_area(
        "Description"
    )

    submit = st.form_submit_button(
        "Submit"
    )

    if submit:

        if place_name and city and description:

            new_entry = pd.DataFrame({
                "Place Name": [place_name],
                "City": [city],
                "Category": [category],
                "Description": [description]
            })

            new_entry.to_csv(
                FILE_NAME,
                mode="a",
                header=False,
                index=False
            )

            st.success(
                "Hidden Gem Added Successfully!"
            )

        else:
            st.error(
                "Please fill all fields."
            )