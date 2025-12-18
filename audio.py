import streamlit as st
import pyttsx3

import streamlit as st
import os

def play_number_sound(number):
    if st.session_state.sound_enabled:
        file_path = os.path.join('audio', f'{number}.wav')
        if os.path.exists(file_path):
            try:
                with open(file_path, 'rb') as audio_file:
                    audio_bytes = audio_file.read()
                st.audio(audio_bytes, format='audio/wav', start_time=0, autoplay=True)
            except Exception as e:
                st.warning(f"Não foi possível tocar o arquivo de áudio {file_path}: {e}")
        else:
            st.warning(f"Arquivo de áudio não encontrado: {file_path}. O som não será tocado.")
