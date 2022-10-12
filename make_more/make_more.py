import streamlit as st
st.set_page_config(layout="wide")
import pandas as pd
import torch

st.title('Make More')


with st.sidebar.expander('Import data'):
    uploaded_file_1 = st.file_uploader('names')
    
if uploaded_file_1 is not None:
    #read txt file
    words = uploaded_file_1.read().decode('utf-8').splitlines()
    # transform in a dataframe
    df = pd.DataFrame(words, columns=['words'])
    st.write(df)
    '''
    Create a 27x27 matrix of zeros,
    append the count value for every couple of letters,
    representing the real distribution of the next letter, as probabilities.
    '''
    # 1. Create a 27x27 matrix of zeros
    import torch
    N = torch.zeros((27,27), dtype=torch.int32)

    list_of_letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '.']
    string_to_integer = {letter: i for i, letter in enumerate(list_of_letters)}
    integer_to_string = {i: letter for i, letter in enumerate(list_of_letters)}

    for w in words:
        w = '.' + w + '.' # add . to the end of the name
        for i in range(len(w)-1):
            ch_1 = w[i] # current letter as string
            ch_2 = w[i+1] # next letter as string
            row = string_to_integer[ch_1] # current letter as integer
            col = string_to_integer[ch_2] # next letter as integer
            N[row, col] += 1

    # 2. Plot N as matrix
    import plotly.express as px
    fig = px.imshow(N, color_continuous_scale='Blues')
    # add labels
    fig.update_xaxes(title_text='Next letter')
    fig.update_yaxes(title_text='Current letter')
    # add text to each cell
    for i in range(27):
        for j in range(27):
            xh1 = integer_to_string[i]
            xh2 = integer_to_string[j]
            fig.add_annotation(text=xh1 + xh2, x=i, y=j, showarrow=False)
    # set size
    fig.update_layout(width=800, height=800)
     
    st.plotly_chart(fig, use_container_width=True)

    # 3. Create function to generate a name
    import random
    def generate_name():
        name = ''
        ch = integer_to_string[random.randint(0, 26)] # start with a random letter
        name += ch
        while ch != '.':
            # then sample the next letter from the distribution of the next letter
            ch = integer_to_string[torch.multinomial(N[string_to_integer[ch]].float(), 1).item()]
            name += ch
        return name

    # test the code generating 10 names
    for i in range(10):
        print(generate_name())