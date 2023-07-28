from collections import namedtuple
import altair as alt
import math
import numpy as np
import pandas as pd
import streamlit as st

import json

@st.cache_data(ttl=60)
def load_data(sheets_url):
    csv_url = sheets_url.replace("/edit#gid=", "/export?format=csv")
    return pd.read_csv(csv_url, on_bad_lines='skip')


FUNCTIONS = ["HR", "Sales", "Marketing", "Finance", "Operations", "IT", "Legal", "Other"]

st.title('TechCrunch Articles')
# open all_articles_v2.json

# with open('all_articles_v2.json') as f:
#     data = json.load(f)

# convert data, which is a list of dictionaries, to a dataframe
# but, exclude the 'content' column

# df = pd.DataFrame(data).drop(columns=['content', 'link'])
df = load_data(st.secrets["public_gsheets_url"])

option = st.sidebar.selectbox("Your Function", FUNCTIONS)
additiona_info = st.sidebar.text_input("More About You", key="more_details")
st.table(df)



"""
# "database - articles"
# https://docs.google.com/spreadsheets/d/1GnAgAxrPD1KK_5m9pjnEXX7l4m5p1owHTSdRU96jvlQ/edit?usp=sharing

# If not already done, store the value of all_articles_v2.json in a database (with ids)
# Create a table called persona-article-match with the following columns:
# - id (primary key)
# - persona_id (int)
# - article_id (int)
# - article_score (float)

# Create a table called persona with the following columns:
# - id (primary key)
# - function (string)

# create a function that takes in N articles at a time and a persona id
# and returns each article with a score using OpenAI (use json as the tool, or just do this in colab)

# create a function that takes in a detailed person description + persona and a list of article IDs
# and rewrites each article for the user
# ensure all data is cached
"""