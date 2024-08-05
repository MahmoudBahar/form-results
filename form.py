import pandas as pd
import streamlit as st
import numpy as np
import psycopg2
from streamlit_extras.stylable_container import stylable_container
from functools import reduce
from time import sleep

if 'server' not in globals():
    server = 'mtnatega.postgres.database.azure.com'
    database = 'postgres'
    username = 'natega'
    password = 'Mt100323'
    port = '5432'
    sslmode = 'require'

@st.cache_data()
def data():
    conn = psycopg2.connect(
    host=server,
    database=database,
    user=username,
    password=password,
    port=port,
    sslmode=sslmode
    )
    cur = conn.cursor()
    select_query = '''
        SELECT * FROM form
        '''
    cur.execute(select_query)
    df = pd.DataFrame(cur.fetchall(), columns= [i[0]for i in cur.description])
    return df['id_image'].apply(lambda x: x.tobytes()), df['pay_image'].apply(lambda x: x.tobytes()), df.drop(['id_image', 'pay_image', 'no'], axis = 1)
id_images, pay_images, df = data()
col1, col2 = st.columns([1, 1])
with col1:
    st.text_input('الاسم بالعربي رباعي', key='name', label_visibility='collapsed', placeholder="الاسم بالعربي رباعي")
with col2:
    st.selectbox('القسم', key='dep', options=[None, 'ميكانيكا صناعية', 'ميكاترونيكس', 'اتصالات', 'كهرباء', 'حاسبات', 'ميكانيكا انتاج', 'اتصالات credit', 'باور credit', 'طبية'], label_visibility='collapsed', placeholder="القسم")
col1, col2, col3 = st.columns([1, 1, 1])
with col1:
    st.text_input('الرقم القومي', key='ID', label_visibility='collapsed', placeholder="الرقم القومي", max_chars = 14)
with col2:
    st.text_input('رقم الهاتف', key='phone', label_visibility='collapsed', placeholder="رقم الهاتف")
with col3:
    st.selectbox('عدد المرافقين', key='add_no', options=[None, 'مرافق واحد (100 ج)', 'اتنين مرافقين (200 ج)', 'ثلاث مرافقين (300 ج)'], label_visibility='collapsed', placeholder="عدد المرافقين")
with stylable_container(
        key="Upload_Data",
        css_styles="""
        h2{
        display: flex;
            justify-content: flex-end;
        }
        """
    ):
    st.header(f'عدد المرافقين المسجلين: {sum(i*j for i, j in enumerate(df['add_number'].value_counts(), start = 1))}', divider='rainbow')
temp = df
if st.session_state['name'] != None and st.session_state['name'] != '':
    temp = temp[temp['name'].str.startswith(st.session_state['name'])]
if st.session_state['dep'] != None and st.session_state['dep'] != '':
    temp = temp[temp['dep'] == st.session_state['dep']]
if st.session_state['ID'] != None and st.session_state['ID'] != '':
    temp = temp[temp['id'] == st.session_state['ID']]
if st.session_state['phone'] != None and st.session_state['phone'] != '':
    temp = temp[temp['phone'].str.contains(st.session_state['phone'])]
if st.session_state['add_no'] != None and st.session_state['add_no'] != '':
    temp = temp[temp['add_number'] == st.session_state['add_no']]

with stylable_container(
    key="Upload_Data",
    css_styles="""
    h2{
    display: flex;
        justify-content: flex-end;
    }
    """
):
    st.header(f'عدد الطلاب المسجلين: {temp.shape[0]}', divider='rainbow')

with st.container(border=True):
    for i, j in temp.iterrows():
        with stylable_container(
            key="Upload_Data",
            css_styles="""
            span{
            display: flex;
                justify-content: flex-end;
            }
            """
        ):
            with st.expander(f'بيانات الطالب -{i+1}', icon='🎓'):
                col1, col2 = st.columns([1,1],vertical_alignment='center')
                with col1:
                    with stylable_container(
                        key="Upload_Data",
                        css_styles="""
                        h2{
                        display: flex;
                            justify-content: flex-end;
                        }
                        """
                    ):
                        st.image(id_images[i], caption='صورة البطاقة')
                with col2:
                    with stylable_container(
                        key="Upload_Data",
                        css_styles="""
                        h2{
                        display: flex;
                            justify-content: flex-end;
                        }
                        """
                    ):
                        st.image(pay_images[i], caption='صورة عملية الدفع')
                with stylable_container(
                    key="Upload_Data",
                    css_styles="""
                    p{
                        display: flex;
                        justify-content: flex-end;
                    }
                    """
                ):
                    st.write(f'الاسم: {j['name']}')
                    st.write(f'القسم: {j['dep']}')
                    st.write(f'الرقم القومي: {j['id']}')
                    st.write(f'رقم الهاتف: {j['phone']}')
                    st.write(f'رقم العملية: {j['pay_no']}')
                    st.write(f'عدد المرافقين : {j['add_number']}')
        sleep(0.5)
