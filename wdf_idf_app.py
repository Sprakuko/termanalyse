import streamlit as st
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
import plotly.graph_objects as go

st.set_page_config(page_title="WDF*IDF Analyse", layout="wide")
st.title("📊 WDF*IDF Analyse: Top 50 Begriffe mit Scroll, Hover, Drittelverteilung & Tabelle")

main_text = st.text_area("📝 Dein Text", height=200)
main_url = st.text_input("🌐 URL zu deinem Text")

col1, col2, col3 = st.columns(3)
comp1 = col1.text_area("Vergleichstext 1", height=150)
url1 = col1.text_input("URL Vergleich 1")
comp2 = col2.text_area("Vergleichstext 2", height=150)
url2 = col2.text_input("URL Vergleich 2")
comp3 = col3.text_area("Vergleichstext 3", height=150)
url3 = col3.text_input("URL Vergleich 3")

texts = [main_text, comp1, comp2, comp3]
urls = [main_url, url1, url2, url3]

texts = [t for t in texts if t.strip()]
urls = [u for u in urls if u.strip()]

stopwords = set([
    "aber", "alle", "als", "am", "an", "auch", "auf", "aus", "bei", "bin", "bis", "bist", "da", "damit", "dann",
    "der", "die", "das", "dass", "deren", "dessen", "dem", "den", "denn", "dich", "dir", "du", "ein", "eine",
    "einem", "einen", "einer", "eines", "er", "es", "etwas", "euer", "eure", "für", "gegen", "gehabt", "hab",
    "habe", "haben", "hat", "hier", "hin", "hinter", "ich", "ihm", "ihn", "ihnen", "ihr", "ihre", "im", "in",
    "ist", "jede", "jedem", "jeden", "jeder", "jedes", "jener", "jenes", "jetzt", "kann", "kein", "keine",
    "keinem", "keinen", "keiner", "keines", "mich", "mir", "mit", "muss", "müssen", "nach", "nein", "nicht",
    "nichts", "noch", "nun", "nur", "ob", "oder", "ohne", "sehr", "sein", "seine", "seinem", "seinen", "seiner",
    "seines", "sie", "sind", "so", "soll", "sollen", "sollte", "sonst", "um", "und", "uns", "unser", "unter",
    "viel", "vom", "von", "vor", "war", "waren", "warst", "was", "weiter", "welche", "welchem", "welchen",
    "welcher", "welches", "wenn", "wer", "werde", "werden", "werdet", "weshalb", "wie", "wieder", "will", "wir",
    "wird", "wirst", "wo", "wollen", "wollte", "würde", "würden", "zu", "zum", "zur", "über"
])

def clean(text):
    return " ".join([w for w in text.lower().split() if w.isalpha() and w not in stopwords])

if st.button("🔍 Analyse starten"):
    if len(texts) < 2 or len(urls) < 2:
        st.warning("Bitte gib deinen Text und mindestens einen Vergleichstext + URLs ein.")
    else:
        cleaned = [clean(t) for t in texts]
        word_counts = [len(t.split()) for t in cleaned]
        vectorizer = CountVectorizer()
        matrix = vectorizer.fit_transform(cleaned)
        terms = vectorizer.get_feature_names_out()
        df_counts = pd.DataFrame(matrix.toarray(), columns=terms, index=urls).T
        df_density = df_counts.copy()

        for i, label in enumerate(urls):
            df_density[label] = (df_counts[label] / word_counts[i] * 100).round(2)

        df_avg = df_density.mean(axis=1)
        top_terms = df_avg.sort_values(ascending=False).head(50).index
        df_top_density = df_density.loc[top_terms]
        df_top_counts = df_counts.loc[top_terms]
        avg_top = df_top_density.mean(axis=1)

        st.subheader("📊 Interaktives Diagramm: Balken = Durchschnitt, Linien = Keyworddichte, Hover = Termfrequenz")
        fig = go.Figure()
        fig.add_trace(go.Bar(x=top_terms, y=avg_top, name="Durchschnitt", marker_color="lightgray"))
        for label in urls:
            fig.add_trace(go.Scatter(
                x=top_terms,
                y=df_top_density[label],
                mode='lines+markers',
                name=label,
                text=[f"TF: {df_top_counts[label][term]}" for term in top_terms],
                hoverinfo='text+y'
            ))
        fig.update_layout(
            height=500,
            width=1600,
            xaxis=dict(title="Top 50 Begriffe (nach durchschnittlicher Keyworddichte)", tickangle=45),
            yaxis=dict(title="Keyworddichte (%)"),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            margin=dict(l=40, r=40, t=40, b=100),
        )
        st.plotly_chart(fig, use_container_width=True)

        st.subheader("🏅 Top-20 Begriffe je Text (mit KD + TF)")
        top_table = pd.DataFrame(index=range(1, 21))
        for i, url in enumerate(urls):
            top_words = df_density[url].sort_values(ascending=False).head(20)
            formatted = [
                f"{term} (KD: {round(df_density[url][term], 2)}%, TF: {df_counts[url][term]})"
                for term in top_words.index
            ]
            st.markdown(f"**{url}** – Länge: {word_counts[i]} Wörter")
            top_table[url] = formatted
        st.dataframe(top_table)

        st.subheader("📍 Drittelverteilung der Begriffe")
        def split_counts(text, terms):
            words = [w for w in text.lower().split() if w.isalpha() and w not in stopwords]
            thirds = np.array_split(words, 3)
            result = []
            for part in thirds:
                count = pd.Series(part).value_counts()
                result.append([count.get(term, 0) for term in terms])
            return pd.DataFrame(result, index=["Anfang", "Mitte", "Ende"], columns=terms)

        def highlight_max_nonzero(col):
            max_val = col[col != 0].max()
            return ['background-color: #a7ecff' if val == max_val and val != 0 else '' for val in col]

        for i, raw in enumerate(texts[:len(urls)]):
            df_split = split_counts(raw, top_terms)
            st.markdown(f"**{urls[i]}**")
            styled = df_split.style.apply(highlight_max_nonzero, axis=0)
            st.dataframe(styled)
