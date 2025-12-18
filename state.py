import json
import os
import streamlit as st
from config import get_initial_numbers

# Função para salvar estado
def save_state(state, filename='state.json'):
    data = {
        'drawn_numbers': state.get('drawn_numbers', []),
        'remaining_numbers': state.get('remaining_numbers', []),
        'sound_enabled': state.get('sound_enabled', True)
    }
    try:
        with open(filename, 'w') as f:
            json.dump(data, f)
    except IOError as e:
        st.warning(f"Não foi possível salvar o estado do jogo em {filename}: {e}")

# Função para carregar estado
def load_state(filename='state.json'):
    if os.path.exists(filename):
        try:
            with open(filename, 'r') as f:
                return json.load(f)
        except (IOError, json.JSONDecodeError) as e:
            st.warning(f"Erro ao carregar o estado de {filename}: {e}. Um novo jogo será iniciado.")
            return {'drawn_numbers': [], 'remaining_numbers': get_initial_numbers(), 'sound_enabled': True}
    return {'drawn_numbers': [], 'remaining_numbers': get_initial_numbers(), 'sound_enabled': True}

# Função para carregar estado anterior
def load_previous_state(filename='previous_state.json'):
    if os.path.exists(filename):
        try:
            with open(filename, 'r') as f:
                return json.load(f)
        except (IOError, json.JSONDecodeError) as e:
            st.warning(f"Erro ao carregar o estado anterior de {filename}: {e}.")
            return {'drawn_numbers': [], 'remaining_numbers': get_initial_numbers(), 'sound_enabled': True}
    else:
        st.warning("Nenhum estado anterior encontrado.")
        return {'drawn_numbers': [], 'remaining_numbers': get_initial_numbers(), 'sound_enabled': True}

# Função para salvar estado atual como estado anterior
def save_current_as_previous(current_state):
    save_state(current_state, 'previous_state.json')
