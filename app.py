import streamlit as st 
import pandas as pd 

name = st.text_input("Enter Your Name : ")
f_name = st.text_input("Enter Your Father Name : ")
adr = st.text_area("Enter Your Address ")
userClass = st.selectbox("Enter Your Class :",(1,2,3,4,5,6))