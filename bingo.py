import streamlit as st
import random
from config import BINGO_COLUMNS, get_initial_numbers
from state import load_state, save_state, load_previous_state, save_current_as_previous
from audio import play_number_sound

def sound_setting_changed():
    save_state(st.session_state)

# Carregar estado atual
initial_state = load_state()
if 'drawn_numbers' not in st.session_state:
    st.session_state.drawn_numbers = initial_state['drawn_numbers']
if 'remaining_numbers' not in st.session_state:
    st.session_state.remaining_numbers = initial_state['remaining_numbers']
if 'sound_enabled' not in st.session_state:
    st.session_state.sound_enabled = initial_state['sound_enabled']

st.set_page_config(layout="wide")

st.title('Bingo App')

# Sidebar
with st.sidebar:
    st.header("Controles")
    st.subheader(f"Números restantes: {len(st.session_state.remaining_numbers)}")
    
    st.checkbox('Habilitar som', key='sound_enabled', on_change=sound_setting_changed)

    if st.button('Sortear Número'):
        if st.session_state.remaining_numbers:
            drawn_number = random.choice(st.session_state.remaining_numbers)
            st.session_state.drawn_numbers.append(drawn_number)
            st.session_state.remaining_numbers.remove(drawn_number)
            save_state(st.session_state)
            play_number_sound(drawn_number)
    
    if st.button('Resetar Jogo'):
        if st.session_state.get('confirm_reset', False):
            save_current_as_previous(st.session_state)
            st.session_state.drawn_numbers = []
            st.session_state.remaining_numbers = get_initial_numbers()
            st.session_state.confirm_reset = False
            save_state(st.session_state)
        else:
            st.session_state.confirm_reset = True
            st.warning("Tem certeza que deseja resetar o jogo? Clique novamente para confirmar.")

    if st.button('Carregar Jogo Anterior'):
        if st.session_state.get('confirm_load_previous', False):
            previous_state = load_previous_state()
            st.session_state.drawn_numbers = previous_state['drawn_numbers']
            st.session_state.remaining_numbers = previous_state['remaining_numbers']
            st.session_state.sound_enabled = previous_state['sound_enabled']
            save_state(st.session_state)
            st.session_state.confirm_load_previous = False
        else:
            st.session_state.confirm_load_previous = True
            st.warning("Tem certeza que deseja carregar o jogo anterior? Clique novamente para confirmar.")

    if st.session_state.drawn_numbers:
        last_number = st.session_state.drawn_numbers[-1]
        st.header(f'Último número: **{last_number}**')

# Tabela de Números
st.header('Tabela de Números')
st.subheader('Tabela completa de números:')

# Estilos
cell_width = '60px'
unsorted_style = f'background-color: #f0f0f0; color: #333; font-size: 20px; width: {cell_width}; height: {cell_width}; padding: 10px; text-align: center; border-radius: 10px; margin: 5px; display: inline-block;'
sorted_style = f'background-color: #00ff00; color: #333; font-size: 20px; width: {cell_width}; height: {cell_width}; padding: 10px; text-align: center; border-radius: 10px; margin: 5px; display: inline-block;'
label_style = f'font-size: 20px; width: {cell_width}; height: {cell_width}; padding: 10px; text-align: center; margin: 5px; display: inline-block;'

for label, (start, end) in BINGO_COLUMNS.items():
    row_html = f'<div style="display: flex; flex-direction: row; align-items: center;"><div style="{label_style}">{label}</div>'
    for number in range(start, end + 1):
        style = sorted_style if number in st.session_state.drawn_numbers else unsorted_style
        row_html += f'<div style="{style}">{number}</div>'
    row_html += '</div>'
    st.markdown(row_html, unsafe_allow_html=True)

if st.session_state.drawn_numbers:
    st.subheader('Números sorteados (em ordem):')
    st.write(', '.join(map(str, sorted(st.session_state.drawn_numbers))))