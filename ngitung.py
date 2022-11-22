import streamlit as st
from nltk.tokenize import sent_tokenize

data1 = st.text_area("Data1", height=250)


data2 = st.text_input("da")

l1 = [sentence for sentence in sent_tokenize(data1)]
l3  = [sentence for sentence in sent_tokenize(data2)]

st.caption("different")
res = [x for x in l1 + l3 if x not in l1 or x not in l3]
col1,col2 = st.columns(2)
with col1:
     st.table(l1)
     
with col2:
     st.table(l3)
     
st.table(res)
     