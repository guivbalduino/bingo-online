import streamlit as st
import random
from config import BINGO_COLUMNS, get_initial_numbers
from state import load_state, save_state, load_previous_state, save_current_as_previous
from audio import get_number_audio_bytes

st.set_page_config(layout="wide", page_title="Bingo Online 🎰", initial_sidebar_state="expanded")

# --- Styling ---
st.markdown("""
<style>
    /* Last number display */
    .last-number-container {
        background-color: #ffbf00;
        color: #000;
        padding: 10px;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 20px;
    }
    .last-number-container h2 {
        color: #000;
        margin: 0;
    }
    .last-number-container p {
        font-size: 80px;
        font-weight: bold;
        color: #000;
        margin: 0;
    }

    /* Bingo grid cells */
    .bingo-cell {
        width: 60px;
        height: 60px;
        line-height: 60px;
        text-align: center;
        border-radius: 50%;
        margin: 5px;
        font-size: 20px;
        font-weight: bold;
        border: 1px solid #444;
        box-shadow: 0 4px 8px rgba(0,0,0,0.4);
    }
    .unsorted {
        background-color: #333;
        color: #fff;
    }
    .sorted {
        background-color: #ffbf00;
        color: #000;
    }
    .last-drawn {
        box-shadow: 0 0 15px 5px #ffc107; /* Brilho amarelo/dourado */
    }

    /* Bingo row label */
    .bingo-label {
        font-size: 24px;
        width: 60px;
        height: 60px;
        line-height: 60px;
        padding: 10px;
        text-align: center;
        margin: 5px;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

if st.session_state.get('new_number_drawn'):
    last_number_drawn = st.session_state.drawn_numbers[-1]
    st.session_state.audio_to_play = get_number_audio_bytes(last_number_drawn)
    st.session_state.new_number_drawn = False

def sound_setting_changed():
    save_state(st.session_state)

# --- State Initialization ---
if 'drawn_numbers' not in st.session_state:
    initial_state = load_state()
    st.session_state.drawn_numbers = initial_state['drawn_numbers']
    st.session_state.remaining_numbers = initial_state['remaining_numbers']
    st.session_state.sound_enabled = initial_state['sound_enabled']

last_number = st.session_state.drawn_numbers[-1] if st.session_state.drawn_numbers else None

st.title('Bingo Online 🎰')

# --- Sidebar ---
with st.sidebar:
    st.header("Controles")

    if last_number is not None:
        with st.container():
            st.markdown(f"""
            <div class="last-number-container">
                <h2>Último Número</h2>
                <p>{last_number}</p>
            </div>
            """, unsafe_allow_html=True)

    if st.session_state.get('audio_to_play') and st.session_state.sound_enabled:
        st.audio(st.session_state.audio_to_play, format='audio/wav', start_time=0, autoplay=True)
        st.session_state.audio_to_play = None # Clear the audio after playing

    st.subheader(f"Números restantes: {len(st.session_state.remaining_numbers)}")

    st.checkbox('Habilitar som', key='sound_enabled', on_change=sound_setting_changed)

    if st.button('Sortear Número'):
        if st.session_state.remaining_numbers:
            drawn_number = random.choice(st.session_state.remaining_numbers)
            st.session_state.drawn_numbers.append(drawn_number)
            st.session_state.remaining_numbers.remove(drawn_number)
            save_state(st.session_state)
            st.session_state.new_number_drawn = True
            st.rerun()

    with st.expander("Resetar Jogo"):
        if st.button("Clique para confirmar o reset", key='confirm_reset_button'):
            save_current_as_previous(st.session_state)
            st.session_state.drawn_numbers = []
            st.session_state.remaining_numbers = get_initial_numbers()
            save_state(st.session_state)
            st.rerun()

    with st.expander("Carregar Jogo Anterior"):
        if st.button("Clique para confirmar o carregamento", key='confirm_load_button'):
            previous_state = load_previous_state()
            st.session_state.drawn_numbers = previous_state['drawn_numbers']
            st.session_state.remaining_numbers = previous_state['remaining_numbers']
            st.session_state.sound_enabled = previous_state['sound_enabled']
            save_state(st.session_state)
            st.rerun()

    # Statistics Section
    st.write("---")
    st.header("Estatísticas")

    stats = {label: 0 for label in BINGO_COLUMNS.keys()}
    for number in st.session_state.drawn_numbers:
        for label, (start, end) in BINGO_COLUMNS.items():
            if start <= number <= end:
                stats[label] += 1
                break

    cols = st.columns(len(BINGO_COLUMNS))
    for i, (label, count) in enumerate(stats.items()):
        cols[i].metric(label, count)


# --- Main Content ---
st.header('Tabela de Números')

for label, (start, end) in BINGO_COLUMNS.items():
    cols = st.columns(16) # 1 for label + 15 for numbers
    with cols[0]:
        st.markdown(f'<div class="bingo-label">{label}</div>', unsafe_allow_html=True)

    for i, number in enumerate(range(start, end + 1)):
        with cols[i+1]:
            is_drawn = number in st.session_state.drawn_numbers
            is_last = number == last_number

            cell_class = "sorted" if is_drawn else "unsorted"
            if is_last:
                cell_class += " last-drawn"

            st.markdown(f'<div class="bingo-cell {cell_class}">{number}</div>', unsafe_allow_html=True)


st.write("---")

if st.session_state.drawn_numbers:
    st.header('Números Sorteados')
    
    sorted_drawn = sorted(st.session_state.drawn_numbers)
    
    # Display drawn numbers in rows of 15
    num_cols = 15
    for i in range(0, len(sorted_drawn), num_cols):
        cols = st.columns(num_cols)
        chunk = sorted_drawn[i:i + num_cols]
        for j, number in enumerate(chunk):
            with cols[j]:
                st.markdown(f'<div class="bingo-cell sorted">{number}</div>', unsafe_allow_html=True)