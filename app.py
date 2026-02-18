import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st

url = "games.csv"
juegos = pd.read_csv(url)
imagen= "dataset-cover.png"
imagen1= plt.imread(imagen)

## Configuraciónn streamlit

st.set_page_config(page_title="Video Games Dataset", page_icon=":video_game:", layout="centered")
st.title("Video Games Dataset")
st.markdown("En el siguiente dashboard evaluaremos el dataset de videojuegos, con el fin de analizar su contenido y obtener información relevante sobre los juegos, sus características y su desempeño en el mercado.")
st.image(imagen1, use_column_width=True)
st.html("<h1>Video Juegos</h1><p>El dataset de videojuegos es una colección de datos relacionados con los juegos, incluyendo información sobre su título, plataforma, género, desarrollador, editor, fecha de lanzamiento, calificación de usuarios y críticos, entre otros aspectos. Este conjunto de datos es valioso para analizar tendencias en la industria de los videojuegos, identificar patrones de éxito y fracaso, y comprender las preferencias de los jugadores.</p>")

with st.container():
    st.subheader("¿Qué es un videojuego?")
    st.markdown("Un videojuego es una forma de entretenimiento interactivo que se juega a través de una computadora, consola de videojuegos, dispositivo móvil u otras plataformas. Los videojuegos pueden variar en género, estilo y complejidad, y pueden incluir elementos como gráficos, sonido, narrativa y mecánicas de juego. Los jugadores pueden interactuar con el juego a través de controles físicos o virtuales, y el objetivo puede ser completar misiones, resolver acertijos, competir contra otros jugadores o simplemente disfrutar de la experiencia de juego.")

