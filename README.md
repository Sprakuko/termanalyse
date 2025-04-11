# 🧠 WDF*IDF Analyse Tool (DE)

Ein interaktives SEO-Analyse-Tool mit Streamlit, das:

- die **Top 50 Begriffe** (nach Keyworddichte) visualisiert
- **Durchschnittliche Keyworddichte als Balken** + **Texte als Liniendiagramme** darstellt
- **Termfrequenz bei Hover** anzeigt
- die **Top 20 Begriffe pro Text mit Keyworddichte und Häufigkeit (TF)** listet
- eine **Drittelverteilung (Anfang, Mitte, Ende)** mit farblicher Hervorhebung bietet

## 🚀 Starten

1. Klone das Repository
2. Installiere die Abhängigkeiten
```bash
pip install -r requirements.txt
```

3. Starte die App
```bash
streamlit run wdf_idf_app.py
```

## 📝 Beispielhafte Eingaben
- Dein eigener Text
- Bis zu drei Wettbewerbertexte
- URL-Etiketten zur besseren Nachverfolgung

## 🔍 Features
- Fokus auf **deutsche Texte**
- **Stopwörter, Artikel und Präpositionen** werden automatisch ignoriert
- Visualisierung der Keyword-Streuung und Keyworddichte im Text