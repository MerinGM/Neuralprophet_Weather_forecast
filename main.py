import streamlit as st
from datetime import datetime
from calculate import prepare
from calculate import predictor


date = datetime.today().strftime('%Y-%m-%d')
st.write("DATE : ",date)
st.write('Today\'s log:')

# td_precip = st.text_input('Rainfall', '',key=td_precip)
# td_max = st.text_input('Max-Temp', '',key=td_max)
# td_min = st.text_input('Min-Temp', '',key=td_min)

if 'stage' not in st.session_state:
    st.session_state.stage = 0
if 'td_precip' not in st.session_state:   
    st.session_state.td_precip = 0
if 'td_max' not in st.session_state:    
    st.session_state.td_max = 0
if 'td_min' not in st.session_state:    
    st.session_state.td_min = 0
    
ip_precip = st.number_input('Rainfall',min_value=None, max_value=None,value = st.session_state.td_precip)
ip_max = st.number_input('Max-Temp',min_value=None, max_value=None, value = st.session_state.td_max)
ip_min = st.number_input('Min-Temp',min_value=None, max_value=None, value = st.session_state.td_min)
# td_precip
# td_max
# td_min
def callback():
    st.session_state.td_precip = ip_precip 
    st.session_state.td_max = ip_max
    st.session_state.td_min = ip_min
    df = prepare(st.session_state.td_precip,st.session_state.td_max,st.session_state.td_min)
   # df = prepare(td_precip,td_max,td_min)
    prediction = predictor(df)
    st.write('Temperature for tomorrow:', prediction)
    set_state(1)




    
def set_state(i):
    st.session_state.stage = i

if st.session_state.stage == 0:
    st.button('Begin', on_click=callback)

if st.session_state.stage >= 1:
    st.button ('New prediction', on_click=set_state, args=[0])
    st.session_state.td_precip = 0
    st.session_state.td_max = 0
    st.session_state.td_min = 0



# '''
# def form_callback():
#     st.write(st.session_state.my_slider)
#     st.write(st.session_state.my_checkbox)

# with st.form(key='my_form'):
#     slider_input = st.slider('My slider', 0, 10, 5, key='my_slider')
#     checkbox_input = st.checkbox('Yes or No', key='my_checkbox')
#     submit_button = st.form_submit_button(label='Submit', on_click=form_callback)
# '''