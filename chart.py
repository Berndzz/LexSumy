import pandas as pd
import altair as alt
import streamlit as st


def chart(raw_text,summ):
    temp = {"Original" : len(raw_text),
            "Summary" : len(summ)}
    df = pd.DataFrame([temp])
    df = df.T
    df.reset_index(inplace=True)
    df.columns = ['Kalimat','Kata']
    c = alt.Chart(df).mark_bar().encode(x = 'Kalimat' , y='Kata')
    st.altair_chart(c)
