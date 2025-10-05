import streamlit as st
import pandas as pd

# Load and clean all sheets
xls = pd.ExcelFile("AriyavaiAaru_Songs_List_BOT.xlsx")

def clean_sheet(sheet):
    df = xls.parse(sheet, dtype=str)
    df.columns = df.columns.str.strip().str.lower()
    df = df.rename(columns={
        'composer': 'music director',
        'singer': 'singers',
        'lyricist': 'lyricist',
        'song': 'song',
        'movie': 'movie',
        'year': 'year',
        'date': 'date'
    })
    df = df.dropna(how='all')
    df = df.loc[:, ~df.columns.str.contains('^unnamed')]
    return df

df = pd.concat([clean_sheet(sheet) for sheet in xls.sheet_names], ignore_index=True)

# Ensure all expected columns exist
for col in ['song', 'movie', 'year', 'music director', 'singers', 'lyricist']:
    if col not in df.columns:
        df[col] = None

# Title-case columns for display
df.columns = [col.title() for col in df.columns]

# Normalize singer entries
def normalize_singers(s):
    return str(s).replace("மற்றும்", ",").replace("&", ",").replace("/", ",").replace(":", ",").replace(";", ",").replace("  ", " ").strip()

df['Singers'] = df['Singers'].apply(normalize_singers).str.lower()

# App title
st.title("🎶 Tamil Song Archive Chatbot")

# General query input
query = st.text_input("Ask me something about the songs:")

# Singer Explorer input
singer_query = st.text_input("🔍 Enter a singer's name to explore (e.g., உமா ரமணன்):")

# 🧪 Data Integrity Checker
if st.checkbox("🧪 Show rows with missing key fields"):
    key_fields = ['Song', 'Movie', 'Music Director', 'Singers']
    missing_info = df[key_fields].isnull() | df[key_fields].eq("")
    df_missing = df[missing_info.any(axis=1)].copy()
    if not df_missing.empty:
        df_missing['Missing Fields'] = missing_info.apply(lambda row: ', '.join([col for col in key_fields if row[col]]), axis=1)
        st.warning(f"⚠️ Found {len(df_missing)} rows with missing data.")
        st.dataframe(df_missing[['Song', 'Movie', 'Year', 'Music Director', 'Singers', 'Missing Fields']])
    else:
        st.success("✅ No missing data in key fields!")

# Helper functions
def songs_by_lyricist(name):
    return df[df['Lyricist'].str.contains(name, case=False, na=False)][['Song', 'Movie', 'Year']]

def songs_by_singer(name):
    return df[df['Singers'].str.contains(name.lower(), na=False)]

def songs_by_composer(name):
    return df[df['Music Director'].str.contains(name, case=False, na=False)][['Song', 'Movie', 'Year']]

def songs_by_year(year):
    return df[df['Year'].astype(str).str.contains(str(year), na=False)][['Song', 'Movie', 'Singers']]

def top_lyricists(n=5):
    return df['Lyricist'].value_counts().head(n)

def top_composers(n=5):
    return df['Music Director'].value_counts().head(n)

def top_singers(n=5):
    return df['Singers'].value_counts().head(n)

# General query handling
if query:
    query_lower = query.lower()

    if "songs by lyricist" in query_lower:
        name = query_lower.split("songs by lyricist")[-1].strip()
        results = songs_by_lyricist(name)
        if not results.empty:
            st.write(f"📝 Songs written by {name}:")
            st.dataframe(results)
        else:
            st.warning(f"No songs found for lyricist '{name}'.")

    elif "songs by singer" in query_lower:
        name = query_lower.split("songs by singer")[-1].strip()
        results = songs_by_singer(name)
        if not results.empty:
            st.write(f"🎤 Songs sung by {name}:")
            st.dataframe(results[['Song', 'Movie', 'Year']])
        else:
            st.warning(f"No songs found for singer '{name}'.")

    elif "songs by composer" in query_lower or "songs by music director" in query_lower:
        name = query_lower.split("songs by composer")[-1].strip()
        results = songs_by_composer(name)
        if not results.empty:
            st.write(f"🎼 Songs composed by {name}:")
            st.dataframe(results)
        else:
            st.warning(f"No songs found for composer '{name}'.")

    elif "songs in year" in query_lower:
        year = ''.join(filter(str.isdigit, query_lower))
        results = songs_by_year(year)
        if not results.empty:
            st.write(f"📅 Songs from the year {year}:")
            st.dataframe(results)
        else:
            st.warning(f"No songs found for year '{year}'.")

    elif "top lyricists" in query_lower:
        st.write("📝 Top Lyricists:")
        st.dataframe(top_lyricists())

    elif "top composers" in query_lower or "top music directors" in query_lower:
        st.write("🎼 Top Music Directors:")
        st.dataframe(top_composers())

    elif "top singers" in query_lower:
        st.write("🎤 Top Singers:")
        st.dataframe(top_singers())

    else:
        st.warning("Sorry, I didn't understand that. Try asking about songs by a lyricist, singer, composer, or year.")

# 🎤 Singer Explorer module
if singer_query:
    results = songs_by_singer(singer_query)
    total = len(results)
    if total > 0:
        st.subheader(f"🎤 Total songs sung by {singer_query}: {total}")
        expected_cols = ['Song', 'Movie', 'Year', 'Music Director', 'Singers']
        available_cols = [col for col in expected_cols if col in results.columns]
        st.dataframe(results[available_cols])
    else:
        st.warning(f"No songs found for singer '{singer_query}'.")