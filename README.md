# 🎮 Video Games Analysis Dashboard

An interactive Streamlit dashboard for exploring and analyzing a large video games dataset. Built as a Data Science portfolio project, it covers the full pipeline: data cleaning, multi-section EDA, interactive visualizations, and data-driven conclusions about the gaming industry.

---

## 📌 Overview

This project analyzes a comprehensive video games dataset (`games.csv`) to uncover trends in the gaming industry — from release patterns by year to genre popularity, player engagement, and the esports landscape.

The app uses a **Steam-inspired dark UI** with gradient typography, glassmorphism cards, and smooth interactive charts powered by Plotly.

---

## 🎯 Features

### 🏠 Home
- Project introduction and cover image.
- Quick narrative describing the analysis goals.

### 🔍 Game Info Search
- Search any game title using the sidebar text input.
- View detailed information: summary, release date, development team, genres, active players, and rating.

### 📅 Games by Year
- Filter the full catalog by release year.
- Table showing all titles released in the selected year with genres and release dates.

### ⭐ Top Categories by Rating
- Interactive slider to control how many categories are shown (1–20).
- Bar chart ranking genres by their average community rating.

### 👥 Player Activity
- Line chart comparing **Total Players** vs **Active Players** by release year.
- Highlights trends in long-term player retention.

### 🗓️ Genres by Year
- Pie chart showing the distribution of game genres for any selected year.
- Reveals how genre popularity has shifted over time.

### 🏆 Esports Overview
- Filters games belonging to typical esports genres (Shooter, Fighting, MOBA, Strategy, Sports, Racing).
- Bar chart of the top 10 esports games by total player count, color-coded by rating.

### 📝 Conclusions
- 4 key findings from the analysis.
- 2 actionable recommendations for the gaming industry.

---

## 🗂️ Dataset

| Column | Description |
|---|---|
| `title` | Game title |
| `release_date` | Release date (parsed to datetime) |
| `team` | Development studio |
| `rating` | Community rating score |
| `times_listed` | Times added to users' lists |
| `number_of_reviews` | Total user reviews |
| `genres` | Game genres (list format) |
| `total_players` | Cumulative players who played the game |
| `active_players` | Players currently active |
| `summary` | Short game description |

> Source: [Video Games Dataset — Backloggd / Kaggle](https://www.kaggle.com/)

**Data cleaning applied:**
- Removed unused columns (`Backlogs`, `Wishlist`, `Reviews`).
- Parsed `K`-notation numbers (e.g. `"2.3K"`) into proper integers.
- Corrected release dates for specific titles (`Deltarune`, `Elden Ring: Shadow of the Erdtree`).
- Dropped rows with missing `rating` values.

---

## 🚀 How to Run

### 1. Install dependencies

```bash
pip install streamlit pandas numpy plotly
```

Or using the requirements file (if available):

```bash
pip install -r requirements.txt
```

### 2. Launch the app

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`.

---

## 🛠️ Tech Stack

| Tool | Purpose |
|---|---|
| Python 3.11+ | Core language |
| Pandas | Data loading, cleaning, and aggregation |
| NumPy | Numeric operations |
| Streamlit | Interactive web app framework |
| Plotly Graph Objects | Bar, line, scatter, and pie charts |
| Plotly Express | High-level chart API |

---

## 📁 Project Structure

```
Videogames_Work/
├── app.py                    # Main Streamlit application
├── app1.ipynb                # Exploratory data analysis notebook
├── games.csv                 # Video games dataset
├── dataset-cover.png         # Cover image shown on the home page
├── requirements.txt          # Python dependencies
└── Esquema_trabajo_final.txt # Project structure reference
```

---

## 📊 Key Findings

1. **Growing industry** — The number of titles released per year has grown consistently.
2. **Top-rated genres** — Music, Point & Click, and Platformers have the highest average ratings.
3. **Pandemic peak** — A notable spike in active players occurred between 2020–2021, likely tied to global lockdowns. Total player counts have increased exponentially in recent years.
4. **Genre dominance** — Adventure is the most persistently popular genre; others fluctuate by year.

## 💡 Recommendations

1. Diversifying across genres and gameplay styles is valuable — the market rewards variety.
2. Adventure games are the most consistently popular over time, making them an important genre to target for maximum reach.

---

## 👤 Author

Developed as part of a Data Science portfolio.
