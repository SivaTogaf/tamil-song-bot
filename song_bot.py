import streamlit as st
import pandas as pd

# Load and merge all sheets from Excel
xls = pd.ExcelFile("AriyavaiAaru_Songs_List.xlsx")
df = pd.concat([xls.parse(sheet) for sheet in xls.sheet_names], ignore_index=True)

# Clean and standardize column names
df.columns = df.columns.str.strip()
df.columns = ['Date', 'Song', 'Movie', 'Year', 'Music Director', 'Lyricist', 'Singers']

# App title
st.title("🎶 Tamil Song Analysis Chatbot")

# User query input
query = st.text_input("Ask me something about the songs:")

# Helper functions
def songs_by_lyricist(name):
    return df[df['Lyricist'].str.contains(name, case=False, na=False)][['Song', 'Movie', 'Year']]

def songs_by_singer(name):
    return df[df['Singers'].str.contains(name, case=False, na=False)][['Song', 'Movie', 'Year']]

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

# Query handling
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
            st.dataframe(results)
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