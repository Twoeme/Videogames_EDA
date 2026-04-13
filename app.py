import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st

## Page configuration
st.set_page_config(page_title="Video Games Analysis", page_icon=":video_game:", layout="wide")
def apply_custom_css():
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&display=swap');
        
        html, body, .stApp, .stMarkdown, .stText, p, h1, h2, h3, h4, th, td, label, div[data-testid="stMarkdownContainer"] {
            font-family: 'Outfit', sans-serif !important;
        }
        
        /* Fix for Streamlit icons */
        .material-symbols-rounded, .material-icons, span[class*="icon"] {
            font-family: 'Material Symbols Rounded', 'Material Icons' !important;
        }
        
        /* Main App Background - Steam-like Dark Theme */
        .stApp {
            background: radial-gradient(circle at center, #1b2838 0%, #171d25 100%);
            color: #dcdedf;
        }

        /* Sidebar Styling */
        [data-testid="stSidebar"] {
            background-color: #171a21 !important;
            border-right: 1px solid #2a475e;
            box-shadow: inset -5px 0 15px rgba(0, 0, 0, 0.3);
        }

        /* Gradient for Titles */
        h1, h2, h3 {
            background: linear-gradient(135deg, #66c0f4 0%, #c7d5e0 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-shadow: 0px 4px 20px rgba(102, 192, 244, 0.2);
            font-weight: 800;
        }

        /* Awesome Button Styles */
        .stButton > button {
            background: linear-gradient(to right, #2a475e, #2d7397);
            color: #66c0f4 !important;
            border: 1px solid #66c0f4;
            border-radius: 6px;
            padding: 0.6rem 1.2rem;
            font-weight: 600;
            width: 100%;
            transition: all 0.3s ease;
            box-shadow: 0 4px 6px rgba(0,0,0,0.3);
        }

        .stButton > button:hover {
            background: linear-gradient(to right, #66c0f4, #2d7397);
            color: #171d25 !important;
            border-color: #c7d5e0;
            transform: translateY(-2px);
            box-shadow: 0 0 15px rgba(102, 192, 244, 0.5);
        }

        /* Inputs & Selectboxes */
        div[data-baseweb="select"] > div, 
        input {
            background-color: #1b2838 !important;
            border-radius: 4px !important;
            border: 1px solid #2a475e !important;
            color: #dcdedf !important;
            transition: all 0.3s ease;
        }

        div[data-baseweb="select"] > div:hover,
        input:hover {
            border-color: #66c0f4 !important;
            box-shadow: 0 0 8px rgba(102, 192, 244, 0.3);
        }

        /* DataFrame / Tables styling */
        [data-testid="stTable"], .stDataFrame, .stTable {
            background-color: rgba(27, 40, 56, 0.7);
            border-radius: 8px;
            padding: 10px;
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
            backdrop-filter: blur(4px);
            border: 1px solid rgba(102, 192, 244, 0.18);
        }

        [data-testid="stTable"] th, [data-testid="stTable"] td, .stDataFrame th, .stDataFrame td {
            color: #dcdedf !important;
        }

        /* Hide Top Menu and Footer */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}

        /* Custom Scrollbar */
        ::-webkit-scrollbar {
            width: 10px;
            height: 10px;
        }
        ::-webkit-scrollbar-track {
            background: #171d25; 
        }
        ::-webkit-scrollbar-thumb {
            background: #2a475e; 
            border-radius: 5px;
        }
        ::-webkit-scrollbar-thumb:hover {
            background: #66c0f4; 
        }
        </style>
        """,
        unsafe_allow_html=True
    )

apply_custom_css()

@st.cache_data

##---------------------------Dataset reading--------------------

def load_data():
    df = pd.read_csv("games.csv")

    ## Data cleaning and transformation
    df.drop(columns=["Unnamed: 0", "Backlogs","Wishlist","Reviews"], inplace=True)
    df.rename(columns={"Title":"title", "Release Date":"release_date", "Team":"team", "Rating":"rating","Times Listed":"times_listed","Number of Reviews":"number_of_reviews","Genres":"genres","Plays":"total_players","Playing":"active_players","Summary":"summary"}, inplace=True)
    df.drop_duplicates(inplace=True)
    df['team'].fillna(value="Hitsuji", inplace=True)
    df.dropna(subset=["rating"], inplace=True)

    ## Release date corrections
    deltarune= df['title']== 'Deltarune'
    df.loc[deltarune, 'release_date'] = df.loc[deltarune,'release_date'].str.replace("releases on TBD","Jun 04, 2025")
    elden = df['title']== 'Elden Ring: Shadow of the Erdtree'
    df.loc[elden, 'release_date'] = df.loc[elden,'release_date'].str.replace("releases on TBD","Jun 20, 2024")

    df['release_date']= pd.to_datetime(df['release_date'])

    ## Format changes
    df['times_listed'] = df['times_listed'].str.replace("K","", regex=False).astype(float)*1000
    df['times_listed'] = df['times_listed'].astype(int)
    df['number_of_reviews']= df['number_of_reviews'].str.replace("K","", regex=False).astype(float)*1000
    df['number_of_reviews'] = df['number_of_reviews'].astype(int)
    df['total_players'] = df['total_players'].str.replace("K","", regex=False).astype(float)*1000
    df['total_players'] = df['total_players'].astype(int)
    df['active_players'] = df['active_players'].str.replace("K","", regex=False).astype(float)*1000
    df['active_players'] = df['active_players'].astype(int)

    ## genre expansion
    
    genres_per_game = df['genres'].astype(str).str.strip("[]").str.replace(",","", regex=False).str.split(", ")
    return df, genres_per_game

df, genres_per_game = load_data()

##---------------------------Screen change function---------------------------

def change_view(active_view):
    states = ['home_section', 'by_year', 'by_rating', 'activeplayers', 
               'genres_by_year', 'game_title', 'conclusions', 'esports']
    for state in states:
        st.session_state[state] = (state == active_view)
##---------------------------Title----------------------------------------
if 'home_section' not in st.session_state:
    st.session_state.home_section = True
def home():
    change_view('home_section')

if st.session_state.home_section:
    st.title("Video Games Analysis", text_alignment="center")
    st.markdown("Data science project using Streamlit to analyze a video games dataset. The goal is to explore trends in the video game industry, identify patterns of success and failure, and understand player preferences through interactive visualizations and data analysis.") 
    st.image("dataset-cover.png", width="stretch")

##---------------------------Project body---------------------------



##---------------------------Games by year table---------------------------
if 'by_year' not in st.session_state:
    st.session_state.by_year = False
def filter_by_release_date():
    change_view('by_year')

if st.session_state.by_year:
    with st.container():
        st.subheader("Video Games by Release Year")
        st.selectbox("Select Release Year", options=df['release_date'].dt.year.unique(), key="year_filter") 
        release_year = df['release_date'].dt.year
        st.write(f"In the year {st.session_state.year_filter}, {release_year[release_year == st.session_state.year_filter].count()} games were released.")
        #genres_per_game = df['genres'].astype(str).str.strip("[]").str.replace(",","", regex=False).str.split(", ")
        games_by_date = df.loc[release_year == st.session_state.year_filter, ['title', 'release_date', 'genres']]
        st.table(games_by_date)

##---------------------------Rating page---------------------------

if 'by_rating' not in st.session_state:
    st.session_state.by_rating = False
def rating():
    change_view('by_rating')     
    
if st.session_state.by_rating:
    with st.container():
        st.subheader("Top Categories with Highest Rating")
        st.slider("Select the number of categories to display", min_value=1, max_value=20, value=5, key="num_categories") 
        df['genre_per_game'] = df['genres'].str.strip("[]").str.strip("'").str.split(", ").str[0]
        df['genre_per_game'] = df['genre_per_game'].replace('', np.nan)
        rating_by_genre = df[df['genre_per_game'].notna()].groupby('genre_per_game')['rating'].mean().sort_values(ascending=False)
        figure = go.Figure(data=[go.Bar(x=rating_by_genre.index[:st.session_state.num_categories], y=rating_by_genre.values[:st.session_state.num_categories])])
        st.plotly_chart(figure)

##---------------------------Total vs Active Players---------------------------

if 'activeplayers' not in st.session_state:
    st.session_state.activeplayers = False
def total_vs_active_players():
    change_view('activeplayers')

if st.session_state.activeplayers:    
    fig = go.Figure()
    total_players= df.groupby(df['release_date'].dt.year)['total_players'].mean().reset_index()
    fig.add_trace(go.Scatter(x=total_players['release_date'], y=total_players['total_players'], name='Total Players'))
    active_players= df.groupby(df['release_date'].dt.year)['active_players'].mean().reset_index()
    fig.add_trace(go.Scatter(x=active_players['release_date'], y=active_players['active_players'], name='Active Players'))
    fig.update_layout(title='Total Players vs Active Players by Release Year', xaxis_title='Release Year', yaxis_title='Number of Players')
    st.plotly_chart(fig)

##---------------------------Genre distribution by year---------------------------
if 'genres_by_year' not in st.session_state:
    st.session_state.genres_by_year = False
def genres_by_year():
    change_view('genres_by_year')
    

if st.session_state.genres_by_year:   
    df['genre_per_game'] = df['genres'].str.strip("[]").str.strip("'").str.split(", ").str[0]
    df['genre_per_game'] = df['genre_per_game'].replace('', np.nan)
    genre_release_by_year = df.groupby([df['release_date'].dt.year, df['genre_per_game']]).size().reset_index(name='count')
    
    unique_years = genre_release_by_year['release_date'].unique().tolist()
    default_index = unique_years.index(2020) if 2020 in unique_years else 0
    st.selectbox("Select release year", options=unique_years, index=default_index, key="year_genre_filter")
    
    fig = go.Figure()
    fig.add_trace(go.Pie(labels=genre_release_by_year[genre_release_by_year['release_date'] == st.session_state.year_genre_filter]['genre_per_game'], values=genre_release_by_year[genre_release_by_year['release_date'] == st.session_state.year_genre_filter]['count']))
    fig.update_layout(title='Genre distribution by release year')
    st.plotly_chart(fig)
##---------------------------Detailed game info---------------------------
if 'game_title' not in st.session_state:
    st.session_state.game_title = False

def game_title():
    change_view('game_title')

if st.session_state.game_title:  
    st.subheader("Detailed Game Information")
    chosen_game = st.session_state.game_search
    df_game = df[df['title'].str.contains(chosen_game, case=False, na=False)].copy()
    df_game['team'] = df_game['team'].str.strip("[]").str.strip("'").str.split(", ").str[0]
    df_game['genres'] = df_game['genres'].str.strip("[]").str.strip("'").str.split(", ")
    if df_game.empty:
        st.write("No games found with that title.") 
    else: 
        table = go.Figure(data=[go.Table(header=dict(values=list(df_game[['title', 'summary', 'release_date', 'team', 'genres', 'active_players', 'rating']].columns.str.capitalize().str.replace('_', ' ')),fill_color='gray', font=dict(size=18), align='center'), cells=dict(values=[df_game['title'], df_game['summary'],df_game['release_date'],df_game['team'], df_game['genres'],df_game['active_players'], df_game['rating']],fill_color="white", font=dict(size=16,color='black'), align='left'))])
        st.plotly_chart(table)

##---------------------------Esports--------------------------
if 'esports' not in st.session_state:
    st.session_state.esports = False

def esports():
    change_view('esports')

if st.session_state.esports:
    st.subheader("Esports Overview")
    st.markdown("Esports (electronic sports) are organized competitive video gaming events. Many popular games have a huge esports scene, drawing millions of viewers worldwide.")
    
    st.write("### Popular Esports Genres")
    esports_genres = ['Shooter', 'Fighting', 'MOBA', 'Strategy', 'Sports', 'Racing']
    df_esports = df[df['genres'].astype(str).str.contains('|'.join(esports_genres), case=False, na=False)].copy()
    
    if not df_esports.empty:
        top_esports = df_esports.sort_values(by='total_players', ascending=False).head(10)
        st.write("Top games that fall into typical Esports genres (Shooter, Fighting, MOBA, Strategy, Sports, Racing) based on Total Players:")
        
        fig = px.bar(top_esports, x='title', y='total_players', color='rating', hover_data=['genres', 'team'], title="Top Games in Typical Esports Genres by Total Players")
        st.plotly_chart(fig)
    else:
        st.write("No esports genre games found in the dataset.")

##---------------------------Conclusions--------------------------
if 'conclusions' not in st.session_state:
    st.session_state.conclusions = False

def conclusions():
    change_view('conclusions')

if st.session_state.conclusions:  
    st.subheader("Conclusions")
    st.html("<h3>1. The gaming industry has been growing in the number of titles released per year. <br>"
    "2. The categories with the best ratings are Music, Point and Click, and Platformers. <br>"
    "3. A large peak of active players was detected between 2020 and 2021, which could be associated with the pandemic. Total players have increased exponentially over recent years, as have the number of games and their categories. <br>"
    "4. One of the most popular video game genres is the Adventure genre, while other genres have their ups and downs depending on the year."
    )
    st.subheader("Recommendations")
    st.html("<h3>1. The world of video games has been expanding and is not static. Therefore, trying different genres and game styles can be valuable in the industry. <br>"
            "2. Adventure games are the most consistently popular over time, making it an important genre to target.</h3>")
##---------------------------Sidebar---------------------------
sidebar = st.sidebar
with sidebar:
    st.button("Home", on_click=home, use_container_width=True)
    st.text_input("Search for a game by its title", key="game_search")
    st.button("Game Info", on_click=game_title, use_container_width=True)
    st.markdown("---")
    st.markdown("**Explore Dataset**")
    st.button("Games by Year", on_click=filter_by_release_date, use_container_width=True)
    st.button("Top Categories", on_click=rating, use_container_width=True)
    st.button("Player Activity", on_click=total_vs_active_players, use_container_width=True)
    st.button("Genres by Year", on_click=genres_by_year, use_container_width=True)
    st.markdown("---")
    st.button("Esports Info", on_click=esports, use_container_width=True)
    st.button("Conclusions", on_click=conclusions, use_container_width=True) 

    #st.markdown('Time filters')
## Release year number of titles


#col1, col2 = st.columns(2)
#with col1:
  #  st.selectbox("Select the release year", options=games_by_date.index.unique(), key="release_date_filter")
 #   st.write(f"In the year {st.session_state.release_date_filter} there were {games_by_date[st.session_state.release_date_filter]} games released.")
## Game genres
#with col2:
  #  st.selectbox("Select a game", options=df['title'].unique(), key="genre_games")
   # compare_index = df[df['title'] == st.session_state.genre_games].index[0]
   # game_genres = genres_per_game[compare_index]
   # st.write(f"The game genres are: {', '.join(game_genres).replace("'","")}")


#with st.container():
    #st.subheader("Categories with highest score")
    #genre_ratings = df.groupby("genres")["rating"].mean().sort_values(ascending=False).head(10)
    #fig = go.Figure(data=[go.Bar(x=genre_ratings.index, y=genre_ratings.values)])
    #st.plotly_chart(fig)

##with st.container():
   ## st.subheader("What is a video game?")
    ##st.markdown("A video game is a form of interactive entertainment played via a computer, video game console, mobile device, or other platforms. Video games can vary in genre, style, and complexity, and can include elements such as graphics, sound, narrative, and game mechanics. Players can interact with the game via physical or virtual controls, and the goal may be to complete missions, solve puzzles, compete against other players, or simply enjoy the gaming experience.")


