import streamlit as st
import os

def get_number_audio_bytes(number):
    if st.session_state.sound_enabled:
        file_path = os.path.join('audio', f'{number}.wav')
        if os.path.exists(file_path):
            try:
                with open(file_path, 'rb') as audio_file:
                    return audio_file.read()
            except Exception as e:
                st.warning(f"Não foi possível ler o arquivo de áudio {file_path}: {e}")
                return None
        else:
            st.warning(f"Arquivo de áudio não encontrado: {file_path}. O som não será tocado.")
            return None
    return None