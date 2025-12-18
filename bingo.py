import streamlit as st
import random
from config import BINGO_COLUMNS, get_initial_numbers
from state import load_state, save_state, load_previous_state, save_current_as_previous
from audio import play_number_sound

st.set_page_config(layout="wide", page_title="Bingo Online 🎰", initial_sidebar_state="expanded")

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

# Obter o último número sorteado para destaque visual
last_number = None
if st.session_state.drawn_numbers:
    last_number = st.session_state.drawn_numbers[-1]

st.title('Bingo Online 🎰')

def get_stats(drawn_numbers, columns_config):
    stats = {label: 0 for label in columns_config.keys()}
    for number in drawn_numbers:
        for label, (start, end) in columns_config.items():
            if start <= number <= end:
                stats[label] += 1
                break
    return stats

# Sidebar
with st.sidebar:
    st.header("Controles")
    
    if last_number is not None:
        # HTML/CSS para o último número
        last_number_html = f"""
        <div style="
            background-color: #ffbf00;
            color: #000;
            padding: 10px;
            border-radius: 10px;
            text-align: center;
            margin-bottom: 20px;
        ">
            <h2 style="color: #000; margin: 0;">Último Número</h2>
            <p style="font-size: 80px; font-weight: bold; color: #000; margin: 0;">{last_number}</p>
        </div>
        """
        st.markdown(last_number_html, unsafe_allow_html=True)

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

    # Seção de Estatísticas
    st.write("---")
    st.header("Estatísticas")
    
    stats = get_stats(st.session_state.drawn_numbers, BINGO_COLUMNS)
    cols = st.columns(5)
    for i, (label, count) in enumerate(stats.items()):
        with cols[i]:
            label_color = "#ffbf00" if count == 15 else "inherit"
            html = f"""
            <div style="text-align: center;">
                <p style="font-size: 24px; font-weight: bold; color: {label_color};">{label}</p>
                <p style="font-size: 32px; font-weight: bold;">{count}</p>
            </div>
            """
            st.markdown(html, unsafe_allow_html=True)

# Tabela de Números
st.header('Tabela de Números')
st.subheader('Tabela completa de números:')

# Estilos CSS aprimorados
cell_width = '60px'
base_style = f'width: {cell_width}; height: {cell_width}; line-height: {cell_width}; text-align: center; border-radius: 50%; margin: 5px; font-size: 20px; font-weight: bold; border: 1px solid #444; box-shadow: 0 4px 8px rgba(0,0,0,0.4);'
unsorted_style = f'{base_style} background-color: #333; color: #fff;'
sorted_style = f'{base_style} background-color: #ffbf00; color: #000;'
label_style = f'font-size: 24px; width: {cell_width}; height: {cell_width}; line-height: {cell_width}; padding: 10px; text-align: center; margin: 5px; display: inline-block; font-weight: bold;' # Revertido para o estilo original de label horizontal

for label, (start, end) in BINGO_COLUMNS.items():
    row_html = f'<div style="display: flex; flex-direction: row; align-items: center;"><div style="{label_style}">{label}</div>'
    for number in range(start, end + 1):
        # Determine base style
        style = unsorted_style
        if number in st.session_state.drawn_numbers:
            style = sorted_style
        
        # Add gray box-shadow if it's the last drawn number
        if last_number is not None and number == last_number:
            style += ' box-shadow: 0 0 7px 3px #888888;' # Add gray glow
        
        row_html += f'<div style="{style}">{number}</div>'
    row_html += '</div>'
    st.markdown(row_html, unsafe_allow_html=True)

st.write("---") # Separador visual

if st.session_state.drawn_numbers:
    st.subheader('Números Sorteados:')
    # Exibe os números sorteados em um layout mais agradável
    drawn_numbers_str = [f'<div style="{sorted_style} margin: 2px;">{num}</div>' for num in sorted(st.session_state.drawn_numbers)]
    st.markdown(f'<div style="display: flex; flex-wrap: wrap; justify-content: center;">{"".join(drawn_numbers_str)}</div>', unsafe_allow_html=True)