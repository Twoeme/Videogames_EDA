from operator import index
from turtle import width

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st

## Configuración de la página
st.set_page_config(page_title="Analisis de Videojuegos", page_icon=":video_game:", layout="wide")
st.title("Analisis de Videojuegos", text_alignment="center")
st.markdown("Proyecto de ciencia de datos utilizando Streamlit para analizar un dataset de videojuegos. El objetivo es explorar las tendencias en la industria de los videojuegos, identificar patrones de éxito y fracaso, y comprender las preferencias de los jugadores a través de visualizaciones interactivas y análisis de datos.")

@st.cache_data

##Lectura del dataset
def cargar_datos():
    df = pd.read_csv("games.csv")

    ## Limpieza y transformacion de datos
    df.drop(columns=["Unnamed: 0", "Summary", "Backlogs","Wishlist","Reviews"], inplace=True)
    df.rename(columns={"Title":"titulo", "Release Date":"fecha_de_lanzamiento", "Team":"equipo", "Rating":"calificacion","Times Listed":"veces_mencionadas","Number of Reviews":"numero_de_resenas","Genres":"generos","Plays":"jugadores_totales","Playing":"jugadores_activos"}, inplace=True)
    df.drop_duplicates(inplace=True)
    df['equipo'].fillna(value="Hitsuji", inplace=True)
    df.dropna(subset=["calificacion"], inplace=True)

    ## Corrección de fechas de lanzamiento
    deltarune= df['titulo']== 'Deltarune'
    df.loc[deltarune, 'fecha_de_lanzamiento'] = df.loc[deltarune,'fecha_de_lanzamiento'].str.replace("releases on TBD","Jun 04, 2025")
    elden = df['titulo']== 'Elden Ring: Shadow of the Erdtree'
    df.loc[elden, 'fecha_de_lanzamiento'] = df.loc[elden,'fecha_de_lanzamiento'].str.replace("releases on TBD","Jun 20, 2024")

    df['fecha_de_lanzamiento']= pd.to_datetime(df['fecha_de_lanzamiento'])

    ## Cambios de formato
    df['veces_mencionadas'] = df['veces_mencionadas'].str.replace("K","", regex=False).astype(float)*1000
    df['veces_mencionadas'] = df['veces_mencionadas'].astype(int)
    df['numero_de_resenas']= df['numero_de_resenas'].str.replace("K","", regex=False).astype(float)*1000
    df['numero_de_resenas'] = df['numero_de_resenas'].astype(int)
    df['jugadores_totales'] = df['jugadores_totales'].str.replace("K","", regex=False).astype(float)*1000
    df['jugadores_totales'] = df['jugadores_totales'].astype(int)
    df['jugadores_activos'] = df['jugadores_activos'].str.replace("K","", regex=False).astype(float)*1000
    df['jugadores_activos'] = df['jugadores_activos'].astype(int)

    ## expansion de generos
    generos_por_juego = df['generos'].astype(str).str.strip("[]").str.replace(",","", regex=False).str.split(", ")
    return df, generos_por_juego

df, generos_por_juego = cargar_datos()

##Imagen 
imagen= "dataset-cover.png"
imagen1= plt.imread(imagen)
st.image(imagen1, width=700)
## Año de lanzamienton numero de titulos
ano_lanzamiento = df['fecha_de_lanzamiento'].dt.year
juegos_por_fecha = df.groupby(ano_lanzamiento)["titulo"].count().sort_values(ascending=False)
col1, col2 = st.columns(2)
with col1:
    st.selectbox("Seleccione el año de lanzamiento", options=juegos_por_fecha.index.unique(), key="fecha_lanzamiento")
    st.write(f"En el año {st.session_state.fecha_lanzamiento} se lanzaron {juegos_por_fecha[st.session_state.fecha_lanzamiento]} juegos.")
## Generos de los juegos
with col2:
    st.selectbox("Seleccione un juego", options=df['titulo'].unique(), key="juegos_genero")
    comparar_index = df[df['titulo'] == st.session_state.juegos_genero].index[0]
    generos_juego = generos_por_juego[comparar_index]
    st.write(f"Los generos de juego son: {', '.join(generos_juego).replace("'","")}")


with st.container():
    st.subheader("Categorias con mejor puntaje")
    categorias_calificacion = df.groupby("generos")["calificacion"].mean().sort_values(ascending=False).head(10)
    fig = go.Figure(data=[go.Bar(x=categorias_calificacion.index, y=categorias_calificacion.values)])
    st.plotly_chart(fig)

##with st.container():
   ## st.subheader("¿Qué es un videojuego?")
    ##st.markdown("Un videojuego es una forma de entretenimiento interactivo que se juega a través de una computadora, consola de videojuegos, dispositivo móvil u otras plataformas. Los videojuegos pueden variar en género, estilo y complejidad, y pueden incluir elementos como gráficos, sonido, narrativa y mecánicas de juego. Los jugadores pueden interactuar con el juego a través de controles físicos o virtuales, y el objetivo puede ser completar misiones, resolver acertijos, competir contra otros jugadores o simplemente disfrutar de la experiencia de juego.")


