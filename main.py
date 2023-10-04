import streamlit as st
from datetime import datetime
from calculate import retrain
from calculate import make_prediction


date = datetime.today().strftime('%Y-%m-%d')
st.write("DATE : ",date)
st.write('Today\'s log:')

# td_precip = st.text_input('Rainfall', '',key=td_precip)
# td_max = st.text_input('Max-Temp', '',key=td_max)
# td_min = st.text_input('Min-Temp', '',key=td_min)

if 'stage' not in st.session_state:
    st.session_state.retrain = 0
if 'td_precip' not in st.session_state:   
    st.session_state.td_precip = 0
if 'td_max' not in st.session_state:    
    st.session_state.td_max = 0
if 'td_min' not in st.session_state:    
    st.session_state.td_min = 0
if 'period' not in st.session_state:    
    st.session_state.period = 1
    
def callback():
    st.session_state.td_precip = ip_precip 
    st.session_state.td_max = ip_max
    st.session_state.td_min = ip_min
    str=retrain(st.session_state.td_precip, st.session_state.td_max, st.session_state.td_min)
    st.write(str)
    #retrain(ip_precip,ip_max,ip_min)
    
    
def call_fun():
    st.session_state.period = period
    fcst = make_prediction(st.session_state.period)
    display = fcst[["ds","yhat1"]].copy()
    display.columns = [["date","predicted temperature"]]
    st.dataframe(display, hide_index=True)


    # if fcst.all:
    #     st.write(fcst[['ds','yhat1']])
    # else:
    #     st.write("oops")
    # st.button("New prediction",on_click=call_fun())    
         
# def check_state():
    
#     if st.session_state.retrain == 0:
#         callback
#         st.session_state.retrain = 2
#     else :
#         st.write("Model can't be retrained")    

ip_precip = st.number_input('Rainfall',min_value=None, max_value=None,value = st.session_state.td_precip)
ip_max = st.number_input('Max-Temp',min_value=None, max_value=None, value = st.session_state.td_max)
ip_min = st.number_input('Min-Temp',min_value=None, max_value=None, value = st.session_state.td_min)
st.button("Retrain", on_click=callback)
period = st.number_input("Prediction period", min_value=1,max_value=None,value = st.session_state.period)
st.button("Predict",on_click=call_fun)
   

# '''
# def form_callback():
#     st.write(st.session_state.my_slider)
#     st.write(st.session_state.my_checkbox)

# with st.form(key='my_form'):
#     slider_input = st.slider('My slider', 0, 10, 5, key='my_slider')
#     checkbox_input = st.checkbox('Yes or No', key='my_checkbox')
#     submit_button = st.form_submit_button(label='Submit', on_click=form_callback)
# '''