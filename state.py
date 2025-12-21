import json
import os
import tempfile
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
        # Create a temporary file in the same directory
        temp_dir = os.path.dirname(filename)
        if not temp_dir:
            temp_dir = '.'
        with tempfile.NamedTemporaryFile('w', delete=False, dir=temp_dir, prefix=os.path.basename(filename) + '~') as temp_f:
            json.dump(data, temp_f)
            temp_f.flush()
            os.fsync(temp_f.fileno())
        # Rename the temporary file to the final filename
        os.rename(temp_f.name, filename)
    except (IOError, OSError) as e:
        st.warning(f"Não foi possível salvar o estado do jogo em {filename}: {e}")
        # Clean up the temporary file if it exists
        if 'temp_f' in locals() and os.path.exists(temp_f.name):
            os.remove(temp_f.name)

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
