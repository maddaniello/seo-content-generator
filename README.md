# 📝 SEO Content Generator

Un'applicazione Streamlit per generare contenuti SEO ottimizzati seguendo gli standard E-E-A-T di Google, utilizzando l'API di OpenAI.

## 🚀 Funzionalità

- **Generazione automatica** di contenuti SEO ottimizzati
- **Standard E-E-A-T** (Experience, Expertise, Authoritativeness, Trustworthiness)
- **Interfaccia intuitiva** costruita con Streamlit
- **Statistiche dettagliate** del contenuto generato
- **Download** in formato .txt e .md
- **Anteprima in tempo reale** del contenuto

## 🛠️ Installazione

### Requisiti
- Python 3.8 o superiore
- Account OpenAI con API Key

### Setup locale

1. **Clona il repository:**
```bash
git clone https://github.com/[tuo-username]/seo-content-generator.git
cd seo-content-generator
```

2. **Crea un ambiente virtuale:**
```bash
python -m venv venv
source venv/bin/activate  # Su Windows: venv\Scripts\activate
```

3. **Installa le dipendenze:**
```bash
pip install -r requirements.txt
```

4. **Configura le variabili d'ambiente:**
```bash
cp .env.example .env
# Modifica .env con la tua API Key OpenAI
```

5. **Avvia l'applicazione:**
```bash
streamlit run app.py
```

## 🌐 Deploy su Streamlit Cloud

1. **Fork questo repository** su GitHub
2. Vai su [share.streamlit.io](https://share.streamlit.io)
3. Clicca "New app" e seleziona il tuo repository
4. Aggiungi le variabili d'ambiente in "Advanced settings"
5. Deploy!

## 📋 Come utilizzare

1. **Inserisci la tua OpenAI API Key** nella sidebar
2. **Compila il form** con:
   - Nome del brand
   - URL del sito
   - Content brief/scaletta editoriale
3. **Clicca "Genera Contenuto SEO"**
4. **Visualizza il risultato** in tre modalità:
   - Anteprima formattata
   - Codice Markdown
   - Statistiche del contenuto
5. **Scarica** il contenuto nei formati disponibili

## 🎯 Standard E-E-A-T implementati

- **Experience**: Esempi pratici e casi studio
- **Expertise**: Terminologia tecnica e analisi approfondite
- **Authoritativeness**: Citazioni da fonti autorevoli
- **Trustworthiness**: Trasparenza e obiettività

## 📁 Struttura del progetto

```
seo-content-generator/
├── app.py                 # App principale Streamlit
├── requirements.txt       # Dipendenze Python
├── config.py             # Configurazioni
├── utils/
│   ├── openai_client.py  # Client OpenAI
│   └── content_generator.py # Logica generazione
├── prompts/
│   └── seo_prompt.py     # Template prompts
└── README.md
```

## 🔧 Configurazione

Modifica `config.py` per personalizzare:
- Modello OpenAI utilizzato
- Numero massimo di token
- Temperatura per la generazione
- Altre impostazioni

## 🤝 Contribuire

1. Fork il progetto
2. Crea un branch per la tua feature (`git checkout -b feature/AmazingFeature`)
3. Commit le tue modifiche (`git commit -m 'Add some AmazingFeature'`)
4. Push sul branch (`git push origin feature/AmazingFeature`)
5. Apri una Pull Request

## 📄 Licenza

Questo progetto è distribuito sotto la licenza MIT. Vedi `LICENSE` per maggiori informazioni.

## 🆘 Supporto

Se hai problemi o domande:
- Apri un issue su GitHub
- Controlla la documentazione di [Streamlit](https://docs.streamlit.io)
- Consulta la documentazione di [OpenAI](https://platform.openai.com/docs)

---

**Sviluppato da Daniele Pisciottano 🦕**
