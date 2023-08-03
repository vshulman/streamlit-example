from collections import namedtuple
import altair as alt
import math
import numpy as np
import pandas as pd
import streamlit as st
from datetime import datetime
# from langchain.llms import OpenAI, Anthropic
from langchain.chat_models import ChatOpenAI
from langchain.chat_models import ChatAnthropic
from langchain.schema import AIMessage, HumanMessage, SystemMessage
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    AIMessagePromptTemplate,
    HumanMessagePromptTemplate,
)



import json

openai_api_key = st.secrets["openai_api_key"]


@st.cache_data(ttl=60)
def load_data(sheets_url):
    csv_url = sheets_url.replace("/edit#gid=", "/export?format=csv")
    return pd.read_csv(csv_url, on_bad_lines='skip')


def full_prompt(prompt, function, additional_info, input_text = "<ARTICLE>"):
    return f"{prompt}\n\nHere is information about me: {additional_info}\n\n.  Here is the article: {input_text}"

@st.cache_data()
def summarize_article(prompt, function, additional_info, input_text, model = "GPT 3.5"):
    print(f"Summarizing article: {input_text} with {prompt} and {additional_info}")
    fp = full_prompt(prompt, function, additional_info, input_text)
    if model == "GPT 3.5":
        # llm = OpenAI(temperature=0.7, openai_api_key=openai_api_key, model="gpt-3.5-turbo")
        chat = ChatOpenAI(temperature=0, openai_api_key=openai_api_key, model="gpt-3.5-turbo")
    elif model == "GPT 4":
        chat = ChatOpenAI(temperature=0, openai_api_key=openai_api_key, model="gpt-4")
    elif model == "Claude 2":
        chat = ChatAnthropic(model = "claude-2")

    # summary = llm(fp) only works for davinci
    messages = [
        # SystemMessage(
        #     content=prompt
        # ), 
        HumanMessage(
            content = fp
        )
    ]

    summary = chat(messages)

    return summary.content


FUNCTIONS = ["HR", "Sales", "Marketing", "Finance", "Operations", "IT", "Legal", "Other"]
BASE_PROMPT = """You are my friend and mentor. You are sending me an article you think is relevant for me.
You believe this article will help me and my goals. Write 1-2 informal sentences telling me specifically why this article is relevant and beneficial for me to read. Only say things that are true. Only say things that will truly help me. Finish the sentence: “You should read this because”.
Do not mention my role in your reasoning. Do not make assumptions about me beyond what I tell you."""

BASE_MORE = "I am a senior engineer in at JPMorgan, a financial services company. I would like to be a stronger team leader and manager. I am responsible for end user authentication for our retail operations."

st.title('TLDR4ME')
content = ''
st.markdown("[Edit Articles / Function Fit](https://docs.google.com/spreadsheets/d/1GnAgAxrPD1KK_5m9pjnEXX7l4m5p1owHTSdRU96jvlQ/edit#gid=698226199)")
articles = []
# open all_articles_v2.json

# with open('all_articles_v2.json') as f:
#     data = json.load(f)

# convert data, which is a list of dictionaries, to a dataframe
# but, exclude the 'content' column

# df = pd.DataFrame(data).drop(columns=['content', 'link'])
df = load_data(st.secrets["public_gsheets_url"])

function = st.sidebar.selectbox("Your Function", FUNCTIONS)
additional_info = st.sidebar.text_area("More About You", key="more_details", value=BASE_MORE, height=200)
st.sidebar.divider()
model = st.sidebar.selectbox("Model", ["GPT 3.5", " GPT 4", "Claude 2"])
prompt = st.sidebar.text_area("Summary Prompt", key="summary_prompt", value=BASE_PROMPT, height=275)
clicked = st.sidebar.button("Generate Email")
summaries = []


# if function is not none, filter the dataframe to only show rows with that function
if function:
    df2 = df[df[function.lower()] == 'x']
st.dataframe(df2)

if clicked:
    st.sidebar.caption(full_prompt(prompt, function, additional_info))
    st.echo("You clicked the button")
    # read all the relevant articles, pass each one into the summarize function, then add result to array and render it
    for index, row in df2.iterrows():
        st.echo(row['content'])
        summary = summarize_article(prompt, function, additional_info, row['content'])
        summaries.append({"summary": summary, "title": row['title']})
        # content += "\n\n" + f"##{row['title']}\n {summary}"

st.header('Email Preview')
if summaries:
    st.markdown(f"""
                ### {datetime.now().strftime("%B %d, %Y")}
                ### Developments in {function}
                """)
    for summary in summaries:

        st.markdown("#### " + summary['title'])
        st.markdown(summary['summary'])



                      



# when a user selects a function, filter the dataframe to only show rows with that function

# when the user clicks "submit", grab all rows with the column matching the user's function
# run each article through the OpenAI API to summarize using the summary prompt
# then render as an email in a new field




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
