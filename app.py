import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st

url = "games.csv"
juegos = pd.read_csv(url)
## Limpieza y transformacion de datos

juegos.drop(columns=["Unnamed: 0", "Summary", "Backlogs","Wishlist","Reviews"], inplace=True)
juegos.rename(columns={"Title":"titulo", "Release Date":"fecha_de_lanzamiento", "Team":"equipo", "Rating":"calificacion","Times Listed":"veces_mencionadas","Number of Reviews":"numero_de_resenas","Genres":"generos","Plays":"jugadores_totales","Playing":"jugadores_activos"}, inplace=True)
juegos.drop_duplicates(inplace=True)
juegos['equipo'].fillna(value="Hitsuji", inplace=True)
juegos.dropna(subset=["calificacion"], inplace=True)

## Corrección de fechas de lanzamiento
deltarune= juegos['titulo']== 'Deltarune'
juegos.loc[deltarune, 'fecha_de_lanzamiento'] = juegos.loc[deltarune,'fecha_de_lanzamiento'].str.replace("releases on TBD","Jun 04, 2025")
elden = juegos['titulo']== 'Elden Ring: Shadow of the Erdtree'
juegos.loc[elden, 'fecha_de_lanzamiento'] = juegos.loc[elden,'fecha_de_lanzamiento'].str.replace("releases on TBD","Jun 20, 2024")

juegos['fecha_de_lanzamiento']= pd.to_datetime(juegos['fecha_de_lanzamiento'])

## Cambios de formato
juegos['veces_mencionadas'] = juegos['veces_mencionadas'].str.replace("K","", regex=False).astype(float)*1000
juegos['veces_mencionadas'] = juegos['veces_mencionadas'].astype(int)
juegos['numero_de_resenas']= juegos['numero_de_resenas'].str.replace("K","", regex=False).astype(float)*1000
juegos['numero_de_resenas'] = juegos['numero_de_resenas'].astype(int)
juegos['jugadores_totales'] = juegos['jugadores_totales'].str.replace("K","", regex=False).astype(float)*1000
juegos['jugadores_totales'] = juegos['jugadores_totales'].astype(int)
juegos['jugadores_activos'] = juegos['jugadores_activos'].str.replace("K","", regex=False).astype(float)*1000
juegos['jugadores_activos'] = juegos['jugadores_activos'].astype(int)

imagen= "dataset-cover.png"
imagen1= plt.imread(imagen)

## Configuraciónn streamlit

st.set_page_config(page_title="Video Games Dataset", page_icon=":video_game:", layout="centered")
st.title("Video Games Dataset")
st.markdown("En el siguiente dashboard evaluaremos el dataset de videojuegos, con el fin de analizar su contenido y obtener información relevante sobre los juegos, sus características y su desempeño en el mercado.")

st.image(imagen1, width=700)
st.html("<h1>Video Juegos</h1><p>El dataset de videojuegos es una colección de datos relacionados con los juegos, incluyendo información sobre su título, plataforma, género, desarrollador, editor, fecha de lanzamiento, calificación de usuarios y críticos, entre otros aspectos. Este conjunto de datos es valioso para analizar tendencias en la industria de los videojuegos, identificar patrones de éxito y fracaso, y comprender las preferencias de los jugadores.</p>")
ano_lanzamiento = juegos['fecha_de_lanzamiento'].dt.year
juegos_por_fecha = juegos.groupby(ano_lanzamiento)["titulo"].count().sort_values(ascending=False)
st.selectbox("Seleccione el año de lanzamiento", options=juegos_por_fecha.index.unique(), key="fecha_lanzamiento")

st.write(f"En el año {st.session_state.fecha_lanzamiento} se lanzaron {juegos_por_fecha[st.session_state.fecha_lanzamiento]} juegos.")

with st.container():
    st.subheader("Categorias con mejor puntaje")
    categorias_calificacion = juegos.groupby("generos")["calificacion"].mean().sort_values(ascending=False).head(10)
    fig = go.Figure(data=[go.Bar(x=categorias_calificacion.index, y=categorias_calificacion.values)])
    st.plotly_chart(fig)

with st.container():
    st.subheader("¿Qué es un videojuego?")
    st.markdown("Un videojuego es una forma de entretenimiento interactivo que se juega a través de una computadora, consola de videojuegos, dispositivo móvil u otras plataformas. Los videojuegos pueden variar en género, estilo y complejidad, y pueden incluir elementos como gráficos, sonido, narrativa y mecánicas de juego. Los jugadores pueden interactuar con el juego a través de controles físicos o virtuales, y el objetivo puede ser completar misiones, resolver acertijos, competir contra otros jugadores o simplemente disfrutar de la experiencia de juego.")


