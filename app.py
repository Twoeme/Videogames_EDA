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


@st.cache_data

##---------------------------Lectura del dataset--------------------

def cargar_datos():
    df = pd.read_csv("games.csv")

    ## Limpieza y transformacion de datos
    df.drop(columns=["Unnamed: 0", "Backlogs","Wishlist","Reviews"], inplace=True)
    df.rename(columns={"Title":"titulo", "Release Date":"fecha_de_lanzamiento", "Team":"equipo", "Rating":"calificacion","Times Listed":"veces_mencionadas","Number of Reviews":"numero_de_resenas","Genres":"generos","Plays":"jugadores_totales","Playing":"jugadores_activos","Summary":"resumen"}, inplace=True)
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

##---------------------------Titulo----------------------------------------
if 'inicioseccion' not in st.session_state:
    st.session_state.inicioseccion = True
def inicio():
    st.session_state.inicioseccion = True
    st.session_state.por_anio = False
    st.session_state.por_rating = False
    st.session_state.jugadoresactivos = False
    st.session_state.generos_por_año = False
    st.session_state.titulo_de_juego = False

if st.session_state.inicioseccion:
    st.title("Analisis de Videojuegos", text_alignment="center")
    st.markdown("Proyecto de ciencia de datos utilizando Streamlit para analizar un dataset de videojuegos. El objetivo es explorar las tendencias en la industria de los videojuegos, identificar patrones de éxito y fracaso, y comprender las preferencias de los jugadores a través de visualizaciones interactivas y análisis de datos.") 
    st.image("dataset-cover.png", width="stretch")

##---------------------------Cuerpo del proyecto---------------------------

##---------------------------Juegos por año tabla---------------------------
if 'por_anio' not in st.session_state:
    st.session_state.por_anio = False
def filtrar_por_fecha_lanzamiento():
    st.session_state.por_anio = True
    st.session_state.por_rating = False
    st.session_state.inicioseccion = False 
    st.session_state.jugadoresactivos = False
    st.session_state.generos_por_año = False
    st.session_state.titulo_de_juego = False

if st.session_state.por_anio:
    with st.container():
        st.subheader("Videojuego por año de lanzamiento")
        st.selectbox("Seleccione Año de lanzamiento", options=df['fecha_de_lanzamiento'].dt.year.unique(), key="filtro_año") 
        ano_lanzamiento = df['fecha_de_lanzamiento'].dt.year
        st.write(f"En el año {st.session_state.filtro_año} se lanzaron {ano_lanzamiento[ano_lanzamiento == st.session_state.filtro_año].count()} juegos.")
        #generos_por_juego = df['generos'].astype(str).str.strip("[]").str.replace(",","", regex=False).str.split(", ")
        juegos_por_fecha = df.loc[ano_lanzamiento == st.session_state.filtro_año, ['titulo', 'fecha_de_lanzamiento', 'generos']]
        st.table(juegos_por_fecha)

##---------------------------Pagina rating---------------------------

if 'por_rating' not in st.session_state:
    st.session_state.por_rating = False
def rating():
    st.session_state.por_anio = False
    st.session_state.por_rating = True
    st.session_state.inicioseccion = False
    st.session_state.jugadoresactivos = False
    st.session_state.generos_por_año = False
    st.session_state.titulo_de_juego = False
if st.session_state.por_rating:
    with st.container():
        st.subheader("Top Categorias con mejor puntaje")
        st.slider("Seleccione el número de categorias a mostrar", min_value=1, max_value=20, value=5, key="num_categorias") 
        df['generos_por_juego'] = df['generos'].str.strip("[]").str.strip("'").str.split(", ").str[0]
        df['generos_por_juego'] = df['generos_por_juego'].replace('', np.nan)
        calificacion_por_genero = df[df['generos_por_juego'].notna()].groupby('generos_por_juego')['calificacion'].mean().sort_values(ascending=False)
        figura = go.Figure(data=[go.Bar(x=calificacion_por_genero.index[:st.session_state.num_categorias], y=calificacion_por_genero.values[:st.session_state.num_categorias])])
        st.plotly_chart(figura)

##---------------------------Jugadores Totales vs Activos---------------------------

if 'jugadoresactivos' not in st.session_state:
    st.session_state.jugadoresactivos = False
def jugadores_totales_vs_activos():
    st.session_state.por_anio = False
    st.session_state.por_rating = False
    st.session_state.inicioseccion = False
    st.session_state.jugadoresactivos = True
    st.session_state.generos_por_año = False    
    st.session_state.titulo_de_juego = False

if st.session_state.jugadoresactivos:    
    fig = go.Figure()
    jugadores_totales= df.groupby(df['fecha_de_lanzamiento'].dt.year)['jugadores_totales'].mean().reset_index()
    fig.add_trace(go.Scatter(x=jugadores_totales['fecha_de_lanzamiento'], y=jugadores_totales['jugadores_totales'], name='Jugadores Totales'))
    jugadores_activos= df.groupby(df['fecha_de_lanzamiento'].dt.year)['jugadores_activos'].mean().reset_index()
    fig.add_trace(go.Scatter(x=jugadores_activos['fecha_de_lanzamiento'], y=jugadores_activos['jugadores_activos'], name='Jugadores Activos'))
    fig.update_layout(title='Jugadores Totales vs Jugadores Activos por Año de Lanzamiento', xaxis_title='Año de Lanzamiento', yaxis_title='Número de Jugadores')
    st.plotly_chart(fig)

##---------------------------Distribución de géneros por año---------------------------
if 'generos_por_año' not in st.session_state:
    st.session_state.generos_por_año = False
def generos_por_año():
    st.session_state.por_anio = False
    st.session_state.por_rating = False
    st.session_state.inicioseccion = False
    st.session_state.jugadoresactivos = False
    st.session_state.generos_por_año = True
    st.session_state.titulo_de_juego = False

if st.session_state.generos_por_año:   
    df['generos_por_juego'] = df['generos'].str.strip("[]").str.strip("'").str.split(", ").str[0]
    df['generos_por_juego'] = df['generos_por_juego'].replace('', np.nan)
    lanzamiento_de_genero_por_año = df.groupby([df['fecha_de_lanzamiento'].dt.year, df['generos_por_juego']]).size().reset_index(name='conteo')
    st.selectbox("Seleccione año de lanzamiento", options=lanzamiento_de_genero_por_año['fecha_de_lanzamiento'].unique(), index=lanzamiento_de_genero_por_año['fecha_de_lanzamiento'].unique().tolist().index(2020), key="filtro_año_genero")
    fig = go.Figure()
    fig.add_trace(go.Pie(labels=lanzamiento_de_genero_por_año[lanzamiento_de_genero_por_año['fecha_de_lanzamiento'] == st.session_state.filtro_año_genero]['generos_por_juego'], values=lanzamiento_de_genero_por_año[lanzamiento_de_genero_por_año['fecha_de_lanzamiento'] == st.session_state.filtro_año_genero]['conteo']))
    fig.update_layout(title='Distribución de géneros por año de lanzamiento')
    st.plotly_chart(fig)
##---------------------------Distribución de géneros por año---------------------------
if 'titulo_de_juego' not in st.session_state:
    st.session_state.titulo_de_juego = False

def titulo_de_juego():
    st.session_state.por_anio = False
    st.session_state.por_rating = False
    st.session_state.inicioseccion = False
    st.session_state.jugadoresactivos = False
    st.session_state.generos_por_año = False
    st.session_state.titulo_de_juego = True

if st.session_state.titulo_de_juego:  
    st.subheader("Información detallada del juego")
    juego_escogido = st.session_state.busqueda_juego
    df_juego = df[df['titulo'].str.contains(juego_escogido, case=False, na=False)]
    df_juego['equipo'] = df_juego['equipo'].str.strip("[]").str.strip("'").str.split(", ").str[0]
    df_juego['generos'] = df_juego['generos'].str.strip("[]").str.strip("'").str.split(", ")
    if df_juego.empty:
        st.write("No se encontró ningún juego con ese título.") 
    else: 
        tabla = go.Figure(data=[go.Table(header=dict(values=list(df_juego[['titulo', 'resumen', 'fecha_de_lanzamiento', 'equipo', 'generos', 'jugadores_activos', 'calificacion']].columns.str.capitalize().str.replace('_', ' ')),fill_color='gray', font=dict(size=18), align='center'), cells=dict(values=[df_juego['titulo'], df_juego['resumen'],df_juego['fecha_de_lanzamiento'],df_juego['equipo'], df_juego['generos'],df_juego['jugadores_activos'], df_juego['calificacion']],fill_color="white", font=dict(size=16,color='black'), align='left'))])
        st.plotly_chart(tabla)
##---------------------------Conclusiones--------------------------
if 'conclusiones' not in st.session_state:
    st.session_state.conclusiones = False

def conclusiones():
    st.session_state.por_anio = False
    st.session_state.por_rating = False
    st.session_state.inicioseccion = False
    st.session_state.jugadoresactivos = False
    st.session_state.generos_por_año = False
    st.session_state.titulo_de_juego = False
    st.session_state.conclusiones = True

if st.session_state.conclusiones:  
    st.subheader("Conclusiones")
    st.markdown("1. La industria de los juegos a ido creciendo en cantidad de titulos lanzados por año." \
    "2. Las categorias con mejores puntajes serian Musica, Point and click y plataformas." \
    "3. Se detecto un gran pico de jugadores activos entre el año 2020 y 2021, que podria estar asociado a la pandemia, los jugadores totales han aumentado exponencialmente durante los ultimos años, han aumentado el numero de juegos y sus categorias." \
    "4. Uno genero mas populares de los videojuegos es el genero de aventura, los demas generos tienen sus subidas y bajadas dependiendo del año."
    )
    st.subheader("Recomendaciones")
    st.markdown("1. El mundo de los videojuegos ha ido ampliando, entonces no es estatico, por lo tal probar diferentes generos y estilos de juegos, es algo que puede llegar a ser valioso en la industria." \
                "2. Los juegos de aventura son los mas populares al pasar de los tiempo, por lo tanto, es uno de los generos que puede ser importante impactar.")
##---------------------------Barra lateral---------------------------
sidebar = st.sidebar
with sidebar:
    st.button("Inicio", on_click=inicio)
    st.text_input("Busca un juego por su título", key="busqueda_juego")
    st.button("Información detallada del juego", on_click=titulo_de_juego)
    st.markdown("Utilice los siguientes Botones para explorar el dataset de videojuegos:")
    st.button("Juegos por año de lanzamiento", on_click=filtrar_por_fecha_lanzamiento)
    st.button("Categorias con mejor puntaje", on_click=rating)
    st.button("Jugadores totales vs activos", on_click=jugadores_totales_vs_activos)
    st.button("Distribución de géneros por año", on_click=generos_por_año)

    #st.markdown('Filtros de tiempo')
## Año de lanzamienton numero de titulos


#col1, col2 = st.columns(2)
#with col1:
  #  st.selectbox("Seleccione el año de lanzamiento", options=juegos_por_fecha.index.unique(), key="fecha_lanzamiento")
 #   st.write(f"En el año {st.session_state.fecha_lanzamiento} se lanzaron {juegos_por_fecha[st.session_state.fecha_lanzamiento]} juegos.")
## Generos de los juegos
#with col2:
  #  st.selectbox("Seleccione un juego", options=df['titulo'].unique(), key="juegos_genero")
   # comparar_index = df[df['titulo'] == st.session_state.juegos_genero].index[0]
   # generos_juego = generos_por_juego[comparar_index]
   # st.write(f"Los generos de juego son: {', '.join(generos_juego).replace("'","")}")


#with st.container():
    #st.subheader("Categorias con mejor puntaje")
    #categorias_calificacion = df.groupby("generos")["calificacion"].mean().sort_values(ascending=False).head(10)
    #fig = go.Figure(data=[go.Bar(x=categorias_calificacion.index, y=categorias_calificacion.values)])
    #st.plotly_chart(fig)

##with st.container():
   ## st.subheader("¿Qué es un videojuego?")
    ##st.markdown("Un videojuego es una forma de entretenimiento interactivo que se juega a través de una computadora, consola de videojuegos, dispositivo móvil u otras plataformas. Los videojuegos pueden variar en género, estilo y complejidad, y pueden incluir elementos como gráficos, sonido, narrativa y mecánicas de juego. Los jugadores pueden interactuar con el juego a través de controles físicos o virtuales, y el objetivo puede ser completar misiones, resolver acertijos, competir contra otros jugadores o simplemente disfrutar de la experiencia de juego.")

