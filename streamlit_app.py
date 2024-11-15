import pandas as pd
import plotly.graph_objects as go
import requests
import streamlit as st
import streamlit_pydantic as sp
from models.formModel import formModel
from streamlit_extras.stylable_container import stylable_container

# st.set_page_config(layout="wide")

sheet_id = st.secrets.gsheet.sheet_id
sheet_name = st.secrets.gsheet.sheet_name
form_url = st.secrets.gsheet.form_url
last_name = st.secrets.last_name
response_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?gid={sheet_name}&format=csv"
sideimg = "img/img_babyg.png"


def get_latest_votes():
    df_sheet = pd.read_csv(response_url)
    df_sheet.columns = ["ts", "bg", "words", "name", "names"]
    return df_sheet


with stylable_container(
    key="container_with_border",
    css_styles="""
            {
                border: 1px solid rgba(49, 51, 63, 0.2);
                border-radius: 0.5rem;
                padding: calc(1em - 1px)
            }
            """,
):

    st.markdown("# Welcome to babybet! 🍼")
    st.markdown(f"### Is Baby {last_name} a He or She? Vote now!")
    df_sheet = get_latest_votes()
    # dedupe df_sheet by same name, keep latest ts
    df_sheet = (
        df_sheet.sort_values(by="ts", ascending=False)
        .drop_duplicates(subset="name", keep="first")
        .reset_index(drop=True)
    )

    if not df_sheet.empty:
        # Get value counts
        bg_counts = df_sheet["bg"].value_counts()
        bg_last_5_votes = df_sheet["bg"].tail(5)
        # Create color-coded bar chart using plotly
        fig = go.Figure(
            data=[
                go.Pie(
                    labels=bg_counts.index,
                    values=bg_counts.values,
                    marker_colors=[
                        "#89CFF0" if x == "Boy" else "#FFB6C6" for x in bg_counts.index
                    ],
                    hole=0.3,  # Optional: makes it a donut chart, remove this line for a regular pie chart
                )
            ]
        )

        fig.update_layout(
            title="Current Votes Distribution",
            xaxis_title="Gender",
            yaxis_title="Count",
            showlegend=False,
        )

        col1, col2, col3 = st.columns(3)

        with col1:
            st.plotly_chart(fig)

        with col2:
            st.write("##")

        with col3:
            st.write("##")
            st.write("Last 5 votes:")
            st.dataframe(bg_last_5_votes)

        col01, col02, col03, col04 = st.columns(4)
        with col01:
            pass

        with col02:
            pass

        with col03:
            pass

        with col04:
            st.button("Refresh", on_click=get_latest_votes)

    else:
        st.write("No votes yet! Be the first to cast your vote!")


st.divider()

with st.expander("**And if you haven't voted yet, feel free to do that below:**"):

    with st.form(key="pydantic_form"):
        st.image("img/babybet.jpg", width=250)

        st.markdown(
            "_Or, if you already voted, please use the same name to update your vote!_"
        )

        data = sp.pydantic_input(key="my_custom_form_model", model=formModel)
        submit_button = st.form_submit_button(label="Submit")

        if submit_button:

            submit_url = f"https://docs.google.com/forms/d/e/{form_url}/formResponse"

            payload = {
                "entry.1933681190": data["boy_or_girl"],
                "entry.1628045289": data["sage_words_of_advice"],
                "entry.835637426": data["name_suggestions"],
                "entry.1388341965": data["your_name"],
            }

            try:
                requests.post(submit_url, data=payload)
                st.success("Vote submitted successfully!")
                st.balloons()
            except Exception as e:
                st.error(f"Error submitting form: {e}")
