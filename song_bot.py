import streamlit as st
import pandas as pd

# Load your Excel file
xls = pd.ExcelFile("AriyavaiAaru_Songs_List.xlsx")
df = pd.concat([xls.parse(sheet) for sheet in xls.sheet_names], ignore_index=True)

# Clean column names
df.columns = df.columns.str.strip()
df.columns = ['Date', 'Song', 'Movie', 'Year', 'Music Director', 'Lyricist', 'Singers']

st.title("🎶 Tamil Song Analysis Bot")

def songs_by_lyricist(name):
    return df[df['Lyricist'].str.contains(name, case=False, na=False)][['Song', 'Movie', 'Year']]

# User input
query = st.text_input("Ask me something about the songs:")

# Basic query handling
if query:
    query_lower = query.lower()
    
    if "top singers" in query_lower:
        top_singers = df['Singers'].value_counts().head(5)
        st.write("🎤 Top 5 Singers:")
        st.dataframe(top_singers)
    
    elif "top composers" in query_lower or "top music directors" in query_lower:
        top_composers = df['Music Director'].value_counts().head(5)
        st.write("🎼 Top 5 Music Directors:")
        st.dataframe(top_composers)
    
    elif "songs by" in query_lower:
        name = query_lower.split("songs by")[-1].strip()
        results = df[df['Singers'].str.contains(name, case=False, na=False)]
        st.write(f"🎵 Songs sung by {name}:")
        st.dataframe(results[['Song', 'Movie', 'Year']])
    
    elif "songs in" in query_lower and "year" in query_lower:
        year = ''.join(filter(str.isdigit, query_lower))
        results = df[df['Year'].astype(str).str.contains(year)]
        st.write(f"📅 Songs from the year {year}:")
        st.dataframe(results[['Song', 'Movie', 'Singers']])
elif "songs by lyricist" in query_lower:
    name = query_lower.split("songs by lyricist")[-1].strip()
    results = songs_by_lyricist(name)
    if not results.empty:
        st.write(f"📝 Songs written by {name}:")
        st.dataframe(results)
    else:
        st.warning(f"No songs found for lyricist '{name}'.")    
    else:
        st.warning("Sorry, I didn't understand that. Try asking about top singers, composers, or songs by a specific artist.")
