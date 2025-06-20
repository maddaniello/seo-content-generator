# Tips per migliorare i risultati
        with st.expander("💡 Tips per risultati migliori"):
            st.markdown("""
            **📋 Content Brief efficace:**
            - Specifica il target audience dettagliato
            - Includi keyword principali e secondarie
            - Definisci struttura H1, H2, H3
            - Indica scopo e obiettivi specifici
            
            **🎯 Strategia vs Competitor:**
            - Analizza cosa manca nei contenuti esistenti
            - Specifica elementi differenzianti
            - Indica fonti uniche da citare
            
            **👥 Target Audience:**
            - Età, professione, problematiche
            - Livello di conoscenza del topic
            - Dove si informano abitualmente
            
            **📢 Call to Action:**
            - 2-3 CTA diverse per articolo
            - CTA primaria e secondarie
            - Posizionamento strategico (inizio, metà, fine)
            
            **🔍 Meta Tags:**
            - Title: max 60 caratteri, include keyword principale
            - Description: max 160 caratteri, invito all'azione
            
            **🏆 E-E-A-T Specifico:**
            - Fonti autorevoli del settore
            - Certificazioni o credenziali
            - Dati statistici recenti
            - Case study e testimonianze
            """)
        
        # Esempio pratico
        with st.expander("📖 Esempio Pratico Completo"):
            st.markdown("""
            **Intento**: Informativo - Come sospendere rate mutuo
            **Obiettivo**: Educare lettori e generare contatti qualificati
            **Target**: Proprietari casa 30-50 anni, difficoltà economiche temporanee
            **Vs Competitor**: Più esempi pratici, infografiche, normative aggiornate
            **E-E-A-T**: Citare CONSAP, Banca d'Italia, avvocati specializzati
            **CTA**: "Contatta esperto TassoMutuo", "Calcola rata post-sospensione"
            **Meta Title**: "Sospensione Rate Mutuo 2025: Guida Completa | TassoMutuo"
            **Meta Desc**: "Scopri come sospendere le rate del mutuo: requisiti, procedure e conseguenze. Guida aggiornata 2025 con esempi pratici."
            """)
        
        #import streamlit as st
import openai
from openai import OpenAI
import re

# Configurazioni
PAGE_TITLE = "SEO Content Generator"
PAGE_ICON = "📝"
OPENAI_MODEL = "gpt-4-turbo-preview"
MAX_TOKENS = 4000
TEMPERATURE = 0.3  # Ridotta per maggiore coerenza

# Configurazione pagina
st.set_page_config(
    page_title=PAGE_TITLE,
    page_icon=PAGE_ICON,
    layout="wide",
    initial_sidebar_state="expanded"
)

class ContentGenerator:
    def __init__(self):
        self.client = None
    
    def initialize_client(self, api_key):
        """Inizializza il client OpenAI con la chiave API fornita"""
        try:
            self.client = OpenAI(api_key=api_key)
            return True
        except Exception as e:
            st.error(f"Errore nell'inizializzazione del client OpenAI: {str(e)}")
            return False
    
    def get_seo_content_prompt(self, brand_name, website_url, content_brief, tone_reference="", internal_links="", content_example="", search_intent="", article_objective="", target_audience="", competitor_strategy="", content_length="", meta_title="", meta_description="", eeat_suggestions="", cta_suggestions=""):
        tone_instruction = ""
        if tone_reference.strip():
            tone_instruction = f"""
RIFERIMENTO TONE OF VOICE:
Analizza il seguente contenuto del sito per comprendere lo stile di scrittura, il tono e l'approccio comunicativo da utilizzare:

{tone_reference}

Mantieni lo stesso tono di voce, stile narrativo e approccio comunicativo mostrato nel riferimento."""

        example_instruction = ""
        if content_example.strip():
            example_instruction = f"""
CONTENUTO DI ESEMPIO CHE FUNZIONA:
Studia attentamente questo contenuto di successo del sito per comprendere:
- Come strutturare l'articolo
- Come integrare informazioni tecniche
- Come bilanciare teoria e pratica
- Come coinvolgere il lettore
- Come organizzare le informazioni
- Che livello di dettaglio utilizzare

CONTENUTO DI RIFERIMENTO:
{content_example}

IMPORTANTE: Replica questo STILE e APPROCCIO (non il contenuto) per creare il nuovo articolo."""

        links_instruction = ""
        if internal_links.strip():
            links_instruction = f"""
LINK INTERNI DA INCLUDERE:
{internal_links}

IMPORTANTE: Inserisci questi link in modo NATURALE nel testo, utilizzando le ancore fornite come testo del link quando appropriate per il contesto."""

        # Informazioni strategiche
        strategic_info = f"""
INFORMAZIONI STRATEGICHE:
- Brand: {brand_name}
- Website: {website_url}
- Intento di ricerca: {search_intent if search_intent else 'Non specificato'}
- Obiettivo dell'articolo: {article_objective if article_objective else 'Non specificato'}
- Target audience: {target_audience if target_audience else 'Non specificato'}
- Strategia vs competitor: {competitor_strategy if competitor_strategy else 'Non specificata'}
- Lunghezza target: {content_length if content_length else '1500-2000 parole'}
- Meta title richiesto: {meta_title if meta_title else 'Da generare automaticamente'}
- Meta description richiesta: {meta_description if meta_description else 'Da generare automaticamente'}

SUGGERIMENTI E-E-A-T SPECIFICI:
{eeat_suggestions if eeat_suggestions else 'Applica standard E-E-A-T generali'}

CALL TO ACTION DA INTEGRARE:
{cta_suggestions if cta_suggestions else 'Crea CTA appropriate per il contesto'}"""

        return f"""
Sei un esperto SEO Copywriter specializzato nella creazione di contenuti ottimizzati per i motori di ricerca.

{strategic_info}

CONTENT BRIEF:
{content_brief}

{tone_instruction}

{example_instruction}

{links_instruction}

ISTRUZIONI FONDAMENTALI:
DEVI SCRIVERE UN ARTICOLO COMPLETO E DETTAGLIATO. NON limitarti a esempi o bozze.

Crea un articolo SEO ottimizzato seguendo rigorosamente gli standard E-E-A-T di Google:

1. **EXPERIENCE (Esperienza)** - INTEGRA NATURALMENTE:
   - Esempi pratici integrati nel testo in modo fluido
   - Scenari del mondo reale spiegati nel contesto
   - Casi studio come parte naturale della narrazione
   - NON usare formule artificiose come "Esperienza reale:" o "Caso studio:"

2. **EXPERTISE (Competenza)**:
   - Dimostra conoscenza approfondita dell'argomento
   - Includi dati statistici e insight quando pertinenti
   - Usa terminologia tecnica appropriata spiegata chiaramente
   - Fornisci analisi dettagliate

3. **AUTHORITATIVENESS (Autorevolezza)**:
   - Cita fonti autorevoli in modo naturale nel testo
   - Referenzia normative e regolamentazioni pertinenti
   - Includi riferimenti a esperti del settore
   - Aggiungi link a risorse credibili

4. **TRUSTWORTHINESS (Affidabilità)**:
   - Mantieni un tono trasparente e oggettivo
   - Discuti limitazioni e possibili problematiche
   - Includi disclaimer dove necessario
   - Fornisci informazioni complete e bilanciate

STRUTTURA E STILE:
- Utilizza una struttura H1, H2, H3 logica e SEO-friendly
- Includi elenchi puntati per migliorare la leggibilità
- Usa il grassetto per evidenziare concetti chiave
- Scrivi paragrafi di 3-4 righe massimo per mantenere la leggibilità
- Includi una introduzione coinvolgente e una conclusione con CTA
- Integra esempi e esperienze in modo NATURALE nel flusso del testo
- Integra le call-to-action fornite in modo naturale nel corso dell'articolo

LUNGHEZZA TARGET: {content_length if content_length else '1500-2000 parole'}

FORMAT: Markdown con formattazione completa

IMPORTANTE: 
- Scrivi l'articolo completo seguendo tutti questi requisiti
- Replicando lo stile del contenuto di esempio fornito (se presente)
- Targettizzando specificamente il pubblico indicato
- Seguendo la strategia per battere i competitor
- Integrando le CTA in modo naturale

ALLA FINE DELL'ARTICOLO, AGGIUNGI SEMPRE UNA SEZIONE:

---

## 📊 SEO Meta Tags

**Meta Title**: {meta_title if meta_title else '[Genera un meta title ottimizzato di max 60 caratteri]'}

**Meta Description**: {meta_description if meta_description else '[Genera una meta description ottimizzata di max 160 caratteri]'}

---
"""
    
    def validate_inputs(self, brand_name, website_url, content_brief):
        """Valida gli input dell'utente"""
        errors = []
        
        if not brand_name.strip():
            errors.append("Il nome del brand è obbligatorio")
        
        if not website_url.strip():
            errors.append("L'URL del sito è obbligatorio")
        elif not self._is_valid_url(website_url):
            errors.append("L'URL del sito non è valido")
        
        if not content_brief.strip():
            errors.append("Il content brief è obbligatorio")
        elif len(content_brief.strip()) < 100:
            errors.append("Il content brief deve contenere almeno 100 caratteri")
        
        return errors
    
    def _is_valid_url(self, url):
        """Valida l'URL fornito"""
        url_pattern = re.compile(
            r'^https?://'  # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
            r'localhost|'  # localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        return url_pattern.match(url) is not None
    
    def generate_content(self, prompt):
        """Genera contenuto utilizzando l'API OpenAI"""
        if not self.client:
            raise Exception("Client OpenAI non inizializzato")
        
        # Usa le configurazioni dalla session state se disponibili
        model = st.session_state.get('model_choice', OPENAI_MODEL)
        temperature = st.session_state.get('temperature', TEMPERATURE)
        max_tokens = st.session_state.get('max_tokens', MAX_TOKENS)
        
        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=[
                    {
                        "role": "system",
                        "content": "Sei un esperto SEO Copywriter specializzato nella creazione di contenuti ottimizzati per i motori di ricerca, con particolare attenzione agli standard E-E-A-T di Google. Scrivi SEMPRE contenuti completi e dettagliati, mai bozze o esempi parziali."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=max_tokens,
                temperature=temperature
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            raise Exception(f"Errore nella generazione del contenuto: {str(e)}")
    
    def test_connection(self):
        """Testa la connessione con l'API OpenAI"""
        if not self.client:
            return False, "Client non inizializzato"
        
        # Usa il modello dalla session state se disponibile
        model = st.session_state.get('model_choice', OPENAI_MODEL)
        
        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": "Test"}],
                max_tokens=10
            )
            return True, "Connessione riuscita"
        except Exception as e:
            return False, f"Errore di connessione: {str(e)}"
    
    def generate_seo_content(self, api_key, brand_name, website_url, content_brief, tone_reference="", internal_links="", content_example="", search_intent="", article_objective="", target_audience="", competitor_strategy="", content_length="", meta_title="", meta_description="", eeat_suggestions="", cta_suggestions=""):
        """Genera il contenuto SEO ottimizzato"""
        
        # Valida gli input
        validation_errors = self.validate_inputs(brand_name, website_url, content_brief)
        if validation_errors:
            return False, validation_errors
        
        try:
            # Inizializza il client OpenAI
            if not self.initialize_client(api_key):
                return False, ["Errore nell'inizializzazione del client OpenAI"]
            
            # Testa la connessione
            connection_ok, connection_msg = self.test_connection()
            if not connection_ok:
                return False, [f"Errore di connessione: {connection_msg}"]
            
            # Genera il prompt
            prompt = self.get_seo_content_prompt(
                brand_name, website_url, content_brief, tone_reference, internal_links, 
                content_example, search_intent, article_objective, target_audience, 
                competitor_strategy, content_length, meta_title, meta_description, 
                eeat_suggestions, cta_suggestions
            )
            
            # Genera il contenuto
            with st.spinner("🔄 Generazione contenuto in corso..."):
                content = self.generate_content(prompt)
            
            return True, content
            
        except Exception as e:
            return False, [f"Errore durante la generazione: {str(e)}"]
    
    def get_content_stats(self, content):
        """Calcola statistiche sul contenuto generato"""
        if not content:
            return {}
        
        words = len(content.split())
        characters = len(content)
        characters_no_spaces = len(content.replace(' ', ''))
        
        # Conta i titoli
        h1_count = content.count('# ')
        h2_count = content.count('## ')
        h3_count = content.count('### ')
        
        # Conta le liste
        bullet_points = content.count('- ')
        numbered_lists = len(re.findall(r'\d+\. ', content))
        
    def analyze_seo_content(self, content, target_keywords=""):
        """Analizza il contenuto per metriche SEO"""
        if not content:
            return {}
        
        # Statistiche base
        words = content.split()
        word_count = len(words)
        char_count = len(content)
        char_no_spaces = len(content.replace(' ', ''))
        
        # Analisi struttura
        h1_count = content.count('# ')
        h2_count = content.count('## ')
        h3_count = content.count('### ')
        
        # Analisi liste e formattazione
        bullet_points = content.count('- ')
        numbered_lists = len(re.findall(r'\d+\. ', content))
        bold_text = content.count('**')
        
        # Analisi link
        internal_links = len(re.findall(r'\[.*?\]\(.*?\)', content))
        
        # Analisi meta tags
        meta_title = ""
        meta_description = ""
        if "Meta Title" in content:
            meta_match = re.search(r'Meta Title.*?:\s*(.*?)(?:\n|$)', content)
            if meta_match:
                meta_title = meta_match.group(1).strip()
        
        if "Meta Description" in content:
            meta_match = re.search(r'Meta Description.*?:\s*(.*?)(?:\n|$)', content, re.DOTALL)
            if meta_match:
                meta_description = meta_match.group(1).strip()
        
        # Analisi keyword density (se fornite)
        keyword_density = {}
        if target_keywords:
            keywords = [kw.strip().lower() for kw in target_keywords.split(',')]
            text_lower = content.lower()
            total_words = len(words)
            
            for keyword in keywords:
                if keyword:
                    count = text_lower.count(keyword)
                    density = (count / total_words) * 100 if total_words > 0 else 0
                    keyword_density[keyword] = {
                        'count': count,
                        'density': round(density, 2)
                    }
        
        # Valutazione readability (approssimativa)
        sentences = len(re.split(r'[.!?]+', content))
        avg_words_per_sentence = word_count / max(sentences, 1)
        
        # Punteggi SEO
        seo_score = 0
        seo_issues = []
        seo_recommendations = []
        
        # Check lunghezza
        if word_count >= 1500:
            seo_score += 20
        elif word_count >= 1000:
            seo_score += 15
            seo_recommendations.append("Considera di espandere il contenuto per raggiungere 1500+ parole")
        else:
            seo_issues.append("Contenuto troppo breve per un buon ranking SEO")
        
        # Check struttura
        if h1_count == 1:
            seo_score += 10
        elif h1_count == 0:
            seo_issues.append("Manca il titolo H1 principale")
        else:
            seo_issues.append("Troppi titoli H1 (dovrebbe essere solo 1)")
        
        if h2_count >= 3:
            seo_score += 15
        elif h2_count >= 1:
            seo_score += 10
        else:
            seo_issues.append("Aggiungi più sottotitoli H2 per migliorare la struttura")
        
        # Check formattazione
        if bullet_points > 0 or numbered_lists > 0:
            seo_score += 10
        else:
            seo_recommendations.append("Aggiungi elenchi puntati per migliorare la leggibilità")
        
        if bold_text >= 5:
            seo_score += 5
        else:
            seo_recommendations.append("Usa più testo in grassetto per evidenziare concetti chiave")
        
        # Check link interni
        if internal_links >= 2:
            seo_score += 10
        elif internal_links >= 1:
            seo_score += 5
        else:
            seo_recommendations.append("Aggiungi link interni per migliorare l'architettura del sito")
        
        # Check meta tags
        if meta_title and len(meta_title) <= 60:
            seo_score += 10
        elif meta_title and len(meta_title) > 60:
            seo_issues.append("Meta title troppo lungo (>60 caratteri)")
        else:
            seo_issues.append("Meta title mancante")
        
        if meta_description and 120 <= len(meta_description) <= 160:
            seo_score += 10
        elif meta_description and len(meta_description) > 160:
            seo_issues.append("Meta description troppo lunga (>160 caratteri)")
        elif meta_description and len(meta_description) < 120:
            seo_recommendations.append("Meta description troppo breve, espandi a 120-160 caratteri")
        else:
            seo_issues.append("Meta description mancante")
        
        # Check readability
        if avg_words_per_sentence <= 20:
            seo_score += 10
        else:
            seo_recommendations.append("Accorcia le frasi per migliorare la leggibilità")
        
        return {
            'word_count': word_count,
            'char_count': char_count,
            'char_no_spaces': char_no_spaces,
            'h1_count': h1_count,
            'h2_count': h2_count,
            'h3_count': h3_count,
            'bullet_points': bullet_points,
            'numbered_lists': numbered_lists,
            'bold_text': bold_text // 2,  # Diviso per 2 perché ** conta come 2
            'internal_links': internal_links,
            'meta_title': meta_title,
            'meta_description': meta_description,
            'meta_title_length': len(meta_title) if meta_title else 0,
            'meta_description_length': len(meta_description) if meta_description else 0,
            'keyword_density': keyword_density,
            'avg_words_per_sentence': round(avg_words_per_sentence, 1),
            'seo_score': min(seo_score, 100),  # Cap a 100
            'seo_issues': seo_issues,
            'seo_recommendations': seo_recommendations
        }

def main():
    st.title("📝 SEO Content Generator")
    st.markdown("**Genera contenuti SEO ottimizzati seguendo gli standard E-E-A-T di Google**")
    
    # Inizializza il generatore di contenuti
    if 'content_generator' not in st.session_state:
        st.session_state.content_generator = ContentGenerator()
    
    # Sidebar per configurazione
    with st.sidebar:
        st.header("🔧 Configurazione")
        
        # API Key OpenAI
        api_key = st.text_input(
            "OpenAI API Key",
            type="password",
            help="Inserisci la tua chiave API OpenAI"
        )
        
        if not api_key:
            st.warning("⚠️ Inserisci la tua API Key OpenAI per continuare")
            st.markdown("🔗 [Ottieni la tua API Key](https://platform.openai.com/api-keys)")
        
        # Configurazioni avanzate
        with st.expander("⚙️ Configurazioni Avanzate"):
            model_choice = st.selectbox(
                "Modello OpenAI",
                ["gpt-4-turbo-preview", "gpt-4", "gpt-3.5-turbo"],
                index=0,
                help="Scegli il modello di AI da utilizzare"
            )
            
            temperature = st.slider(
                "Creatività (Temperature)",
                min_value=0.0,
                max_value=1.0,
                value=0.3,
                step=0.1,
                help="0 = più coerente, 1 = più creativo"
            )
            
            max_tokens = st.slider(
                "Lunghezza massima",
                min_value=1000,
                max_value=4000,
                value=4000,
                step=500,
                help="Numero massimo di token per la risposta"
            )
        
        # Tips per migliorare i risultati
        with st.expander("💡 Tips per risultati migliori"):
            st.markdown("""
            **Content Brief efficace:**
            - Specifica il target audience
            - Includi keyword principali
            - Definisci la lunghezza desiderata
            - Indica lo scopo del contenuto
            
            **Tone of Voice:**
            - Breve estratto rappresentativo del tuo stile
            - Focus su tono e linguaggio utilizzato
            
            **Contenuto di Esempio:**
            - Articolo completo che ti piace (500+ parole)
            - L'AI studierà struttura, approccio e metodologia
            - Più dettagliato = risultati migliori
            
            **Link Interni:**
            - Usa formato: [Testo](URL)
            - Specifica dove inserirli nel brief
            - Massimo 5-7 link per articolo
            """)
        
        # Analisi del contenuto di esempio
        if 'content_example' in locals() and content_example:
            with st.expander("📊 Analisi Contenuto di Esempio"):
                words = len(content_example.split())
                chars = len(content_example)
                h_tags = content_example.count('#')
                lists = content_example.count('-') + content_example.count('*')
                
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Parole", words)
                with col2:
                    st.metric("Caratteri", chars)
                with col3:
                    st.metric("Titoli H", h_tags)
                with col4:
                    st.metric("Liste", lists)
                
                if words > 500:
                    st.success("✅ Contenuto ottimo per l'analisi dello stile")
                elif words > 200:
                    st.warning("⚠️ Contenuto buono, ma più testo migliorerebbe l'analisi")
                else:
                    st.error("❌ Contenuto troppo breve per un'analisi efficace")
        
        # Store delle configurazioni avanzate
        if 'model_choice' not in st.session_state:
            st.session_state.model_choice = model_choice
        if 'temperature' not in st.session_state:
            st.session_state.temperature = temperature
        if 'max_tokens' not in st.session_state:
            st.session_state.max_tokens = max_tokens
        
        st.session_state.model_choice = model_choice
        st.session_state.temperature = temperature
        st.session_state.max_tokens = max_tokens
    
    # Form principale
    if api_key:
        st.header("📋 Informazioni del Progetto")
        
        with st.form("content_form"):
            # Informazioni base
            st.markdown("### 🏢 Informazioni Base")
            col1, col2 = st.columns(2)
            
            with col1:
                brand_name = st.text_input(
                    "Nome del Brand *",
                    placeholder="Es: TassoMutuo",
                    help="Il nome del brand per cui stai creando il contenuto"
                )
                
                website_url = st.text_input(
                    "URL del Sito *",
                    placeholder="https://www.esempio.com",
                    help="L'URL completo del sito web"
                )
            
            with col2:
                search_intent = st.text_input(
                    "Intento di Ricerca",
                    placeholder="Es: Informativo - Come sospendere rate mutuo",
                    help="Che cosa cerca l'utente? (Informativo, Transazionale, Navigazionale)"
                )
                
                article_objective = st.text_input(
                    "Obiettivo dell'Articolo",
                    placeholder="Es: Educare i lettori su sospensione mutui e generare lead",
                    help="Quale risultato vuoi ottenere con questo contenuto?"
                )
            
            # Strategia e target
            st.markdown("### 🎯 Strategia e Target")
            col3, col4 = st.columns(2)
            
            with col3:
                target_audience = st.text_area(
                    "Target Audience",
                    height=80,
                    placeholder="Es: Proprietari di casa con mutuo, età 30-50 anni, in difficoltà economiche...",
                    help="Descrivi il pubblico di riferimento in dettaglio"
                )
                
                content_length = st.selectbox(
                    "Lunghezza Target",
                    ["1500-2000 parole", "1000-1500 parole", "2000-3000 parole", "500-1000 parole", "3000+ parole"],
                    help="Lunghezza desiderata per l'articolo"
                )
            
            with col4:
                competitor_strategy = st.text_area(
                    "Strategia vs Competitor",
                    height=80,
                    placeholder="Es: Fornire più esempi pratici, includere infografiche, analisi normative aggiornate...",
                    help="Come vuoi superare i competitor su questo argomento?"
                )
                
                eeat_suggestions = st.text_area(
                    "Suggerimenti E-E-A-T Specifici",
                    height=80,
                    placeholder="Es: Citare CONSAP, includere statistiche recenti, aggiungere disclaimer legali...",
                    help="Suggerimenti specifici per migliorare Experience, Expertise, Authoritativeness, Trustworthiness"
                )
            
            # Content brief
            st.markdown("### 📝 Content Brief")
            content_brief = st.text_area(
                "Content Brief / Scaletta Editoriale *",
                height=150,
                placeholder="Inserisci qui la scaletta dettagliata del contenuto...",
                help="Fornisci una scaletta dettagliata con titoli, sottotitoli, target e keyword"
            )
            
            # CTA e Meta tags
            st.markdown("### 📢 Call to Action e Meta Tags")
            col5, col6 = st.columns(2)
            
            with col5:
                cta_suggestions = st.text_area(
                    "Call to Action da Integrare",
                    height=100,
                    placeholder="Es: 'Contatta un esperto TassoMutuo', 'Calcola la tua rata', 'Richiedi consulenza gratuita'...",
                    help="Suggerisci le CTA che vuoi integrare naturalmente nell'articolo"
                )
                
                meta_title = st.text_input(
                    "Meta Title (opzionale)",
                    placeholder="Max 60 caratteri - se vuoto verrà generato automaticamente",
                    help="Il titolo che apparirà nei risultati di ricerca"
                )
            
            with col6:
                meta_description = st.text_area(
                    "Meta Description (opzionale)",
                    height=100,
                    placeholder="Max 160 caratteri - se vuota verrà generata automaticamente",
                    help="La descrizione che apparirà nei risultati di ricerca"
                )
                
                # Contatori caratteri per meta tags
                if meta_title:
                    title_len = len(meta_title)
                    if title_len > 60:
                        st.error(f"⚠️ Meta title troppo lungo: {title_len}/60 caratteri")
                    else:
                        st.success(f"✅ Meta title: {title_len}/60 caratteri")
                
                if meta_description:
                    desc_len = len(meta_description)
                    if desc_len > 160:
                        st.error(f"⚠️ Meta description troppo lunga: {desc_len}/160 caratteri")
                    else:
                        st.success(f"✅ Meta description: {desc_len}/160 caratteri")
            
            # Personalizzazione stile e contenuto
            st.markdown("### 🎨 Personalizzazione Stile e Contenuto")
            
            col_left, col_right = st.columns(2)
            
            with col_left:
                tone_reference = st.text_area(
                    "Riferimento Tone of Voice (opzionale)",
                    height=120,
                    placeholder="Incolla qui un breve estratto per il tone of voice...",
                    help="Estratto del tuo sito per il tono di voce e stile comunicativo"
                )
                
                internal_links = st.text_area(
                    "Link Interni da Includere (opzionale)",
                    height=100,
                    placeholder="Es:\n- [Mutuo Consap](https://www.tuosito.it/mutuo-consap)\n- [Guida ai Mutui](https://www.tuosito.it/guida-mutui)",
                    help="Link interni da inserire nell'articolo. Formato: [Testo](URL)"
                )
            
            with col_right:
                content_example = st.text_area(
                    "📄 Contenuto di Esempio che Funziona (opzionale)",
                    height=220,
                    placeholder="Incolla qui un articolo completo del tuo sito che funziona bene...",
                    help="Un contenuto completo che ti piace per struttura, stile e approccio. L'AI studierà come è scritto per replicare lo stesso metodo."
                )
                
                if content_example:
                    word_count = len(content_example.split())
                    st.caption(f"📊 Parole: {word_count} - {'✅ Ottimo per l\'analisi' if word_count > 200 else '⚠️ Troppo breve, aggiungi più contenuto'}")
            
            # Info box esplicativo
            st.info("""
            💡 **Nuovo workflow completo:**
            1. **Strategia**: Definisci intento, obiettivo, target e come battere i competitor
            2. **Contenuto**: Scrivi il brief e suggerisci CTA specifiche
            3. **SEO**: Imposta meta tags e strategia E-E-A-T
            4. **Stile**: Fornisci riferimenti per tone of voice e struttura
            """)
            
            submitted = st.form_submit_button("🚀 Genera Contenuto SEO", type="primary")
            
            if submitted:
                if not all([brand_name, website_url, content_brief]):
                    st.error("❌ Tutti i campi contrassegnati con * sono obbligatori")
                else:
                    # Genera il contenuto con tutti i parametri
                    success, result = st.session_state.content_generator.generate_seo_content(
                        api_key, brand_name, website_url, content_brief, tone_reference, 
                        internal_links, content_example, search_intent, article_objective, 
                        target_audience, competitor_strategy, content_length, meta_title, 
                        meta_description, eeat_suggestions, cta_suggestions
                    )
                    
                    if success:
                        st.session_state.generated_content = result
                        st.session_state.brand_name = brand_name  # Salva per il download
                        st.session_state.content_example = content_example  # Salva per il confronto
                        st.success("✅ Contenuto generato con successo!")
                        st.rerun()
                    else:
                        st.error("❌ Errore nella generazione del contenuto:")
                        for error in result:
                            st.error(f"• {error}")
    
    # Mostra il contenuto generato
    if 'generated_content' in st.session_state:
        st.header("📄 Contenuto Generato")
        
        # Tabs per visualizzazione
        tab_names = ["📖 Anteprima", "📝 Markdown", "📊 Statistiche", "🔍 Analisi SEO"]
        if 'content_example' in st.session_state and st.session_state.get('content_example', '').strip():
            tab_names.append("🆚 Confronto con Esempio")
        
        tabs = st.tabs(tab_names)
        
        with tabs[0]:  # Anteprima
            st.markdown("### Anteprima del Contenuto")
            st.markdown(st.session_state.generated_content)
        
        with tabs[1]:  # Markdown
            st.markdown("### Codice Markdown")
            st.code(st.session_state.generated_content, language="markdown")
            
            # Bottone per copiare
            if st.button("📋 Copia Markdown"):
                st.write("Contenuto copiato negli appunti!")
        
        with tabs[2]:  # Statistiche base
            st.markdown("### Statistiche del Contenuto")
            stats = st.session_state.content_generator.get_content_stats(st.session_state.generated_content)
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Parole", stats.get('words', 0))
                st.metric("H1", stats.get('h1_count', 0))
            
            with col2:
                st.metric("Caratteri", stats.get('characters', 0))
                st.metric("H2", stats.get('h2_count', 0))
            
            with col3:
                st.metric("Caratteri (no spazi)", stats.get('characters_no_spaces', 0))
                st.metric("H3", stats.get('h3_count', 0))
            
            with col4:
                st.metric("Elenchi puntati", stats.get('bullet_points', 0))
                st.metric("Elenchi numerati", stats.get('numbered_lists', 0))
        
        with tabs[3]:  # Analisi SEO
            st.markdown("### 🔍 Analisi SEO Completa")
            
            # Input per keyword target
            target_keywords = st.text_input(
                "Keyword Target (separate da virgola)",
                placeholder="es: sospensione mutuo, rate mutuo, fondo gasparrini",
                help="Inserisci le keyword principali per analizzare la density"
            )
            
            # Analisi SEO
            seo_analysis = st.session_state.content_generator.analyze_seo_content(
                st.session_state.generated_content, target_keywords
            )
            
            # SEO Score
            col_score, col_meta = st.columns([1, 2])
            
            with col_score:
                score = seo_analysis.get('seo_score', 0)
                if score >= 80:
                    st.success(f"🎯 SEO Score: {score}/100")
                elif score >= 60:
                    st.warning(f"⚠️ SEO Score: {score}/100")
                else:
                    st.error(f"❌ SEO Score: {score}/100")
                
                # Progress bar
                st.progress(score / 100)
            
            with col_meta:
                # Meta Tags
                st.markdown("**Meta Tags:**")
                meta_title = seo_analysis.get('meta_title', '')
                meta_desc = seo_analysis.get('meta_description', '')
                
                if meta_title:
                    title_len = seo_analysis.get('meta_title_length', 0)
                    color = "🟢" if title_len <= 60 else "🔴"
                    st.write(f"{color} **Title** ({title_len}/60): {meta_title[:80]}...")
                else:
                    st.write("🔴 **Title**: Non trovato")
                
                if meta_desc:
                    desc_len = seo_analysis.get('meta_description_length', 0)
                    color = "🟢" if 120 <= desc_len <= 160 else "🔴"
                    st.write(f"{color} **Description** ({desc_len}/160): {meta_desc[:100]}...")
                else:
                    st.write("🔴 **Description**: Non trovata")
            
            # Metriche SEO dettagliate
            st.markdown("#### 📊 Metriche Dettagliate")
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Parole", seo_analysis.get('word_count', 0))
                st.metric("Titoli H2", seo_analysis.get('h2_count', 0))
                st.metric("Link Interni", seo_analysis.get('internal_links', 0))
            
            with col2:
                st.metric("Titoli H1", seo_analysis.get('h1_count', 0))
                st.metric("Titoli H3", seo_analysis.get('h3_count', 0))
                st.metric("Testo in Grassetto", seo_analysis.get('bold_text', 0))
            
            with col3:
                st.metric("Elenchi Puntati", seo_analysis.get('bullet_points', 0))
                st.metric("Elenchi Numerati", seo_analysis.get('numbered_lists', 0))
                st.metric("Parole/Frase", seo_analysis.get('avg_words_per_sentence', 0))
            
            with col4:
                # Valutazioni colorate
                word_count = seo_analysis.get('word_count', 0)
                if word_count >= 1500:
                    st.success("✅ Lunghezza OK")
                elif word_count >= 1000:
                    st.warning("⚠️ Lunghezza Media")
                else:
                    st.error("❌ Troppo Breve")
                
                h2_count = seo_analysis.get('h2_count', 0)
                if h2_count >= 3:
                    st.success("✅ Struttura OK")
                elif h2_count >= 1:
                    st.warning("⚠️ Pochi H2")
                else:
                    st.error("❌ Mancano H2")
                
                avg_words = seo_analysis.get('avg_words_per_sentence', 0)
                if avg_words <= 20:
                    st.success("✅ Leggibilità OK")
                else:
                    st.warning("⚠️ Frasi Lunghe")
            
            # Keyword Density
            if target_keywords and seo_analysis.get('keyword_density'):
                st.markdown("#### 🎯 Analisi Keyword Density")
                
                keyword_data = []
                for keyword, data in seo_analysis['keyword_density'].items():
                    density = data['density']
                    count = data['count']
                    
                    # Valutazione density
                    if 0.5 <= density <= 2.5:
                        status = "🟢 Ottima"
                    elif density < 0.5:
                        status = "🔴 Troppo Bassa"
                    else:
                        status = "🔴 Troppo Alta"
                    
                    keyword_data.append({
                        "Keyword": keyword.title(),
                        "Occorrenze": count,
                        "Density %": f"{density}%",
                        "Valutazione": status
                    })
                
                if keyword_data:
                    st.dataframe(keyword_data, use_container_width=True)
            
            # Issues e Raccomandazioni
            col_issues, col_recs = st.columns(2)
            
            with col_issues:
                if seo_analysis.get('seo_issues'):
                    st.markdown("#### ❌ Problemi SEO")
                    for issue in seo_analysis['seo_issues']:
                        st.error(f"• {issue}")
                else:
                    st.success("#### ✅ Nessun problema critico rilevato")
            
            with col_recs:
                if seo_analysis.get('seo_recommendations'):
                    st.markdown("#### 💡 Raccomandazioni")
                    for rec in seo_analysis['seo_recommendations']:
                        st.info(f"• {rec}")
                else:
                    st.success("#### 🎯 SEO ottimale raggiunto!")
        
        # Tab confronto (solo se c'è un esempio)
        if len(tabs) > 4:
            with tabs[4]:  # Confronto
                st.markdown("### 🔍 Confronto con Contenuto di Esempio")
                
                # Statistiche comparative
                example_content = st.session_state.get('content_example', '')
                if example_content:
                    example_stats = st.session_state.content_generator.get_content_stats(example_content)
                    generated_stats = st.session_state.content_generator.get_content_stats(st.session_state.generated_content)
                    
                    st.markdown("#### 📊 Confronto Statistiche")
                    
                    comparison_data = {
                        "Metrica": ["Parole", "Caratteri", "H1", "H2", "H3", "Elenchi puntati"],
                        "Esempio": [
                            example_stats.get('words', 0),
                            example_stats.get('characters', 0),
                            example_stats.get('h1_count', 0),
                            example_stats.get('h2_count', 0),
                            example_stats.get('h3_count', 0),
                            example_stats.get('bullet_points', 0)
                        ],
                        "Generato": [
                            generated_stats.get('words', 0),
                            generated_stats.get('characters', 0),
                            generated_stats.get('h1_count', 0),
                            generated_stats.get('h2_count', 0),
                            generated_stats.get('h3_count', 0),
                            generated_stats.get('bullet_points', 0)
                        ]
                    }
                    
                    st.table(comparison_data)
                    
                    # Analisi della somiglianza strutturale
                    st.markdown("#### 🎯 Analisi Strutturale")
                    
                    # Rapporto parole simile
                    word_ratio = generated_stats.get('words', 0) / max(example_stats.get('words', 1), 1)
                    if 0.8 <= word_ratio <= 1.2:
                        st.success(f"✅ Lunghezza simile all'esempio (rapporto: {word_ratio:.2f})")
                    elif word_ratio > 1.2:
                        st.info(f"📈 Contenuto più lungo dell'esempio (rapporto: {word_ratio:.2f})")
                    else:
                        st.warning(f"📉 Contenuto più breve dell'esempio (rapporto: {word_ratio:.2f})")
                    
                    # Struttura titoli
                    if generated_stats.get('h2_count', 0) >= example_stats.get('h2_count', 0):
                        st.success("✅ Struttura dei titoli ben sviluppata")
                    else:
                        st.warning("⚠️ Potrebbe beneficiare di più sottosezioni")
                    
                    # Confronto visivo affiancato
                    st.markdown("#### 👥 Confronto Visivo")
                    col_left, col_right = st.columns(2)
                    
                    with col_left:
                        st.markdown("**📄 Contenuto di Esempio**")
                        st.markdown(example_content[:1000] + "..." if len(example_content) > 1000 else example_content)
                    
                    with col_right:
                        st.markdown("**🆕 Contenuto Generato**")
                        generated_preview = st.session_state.generated_content[:1000] + "..." if len(st.session_state.generated_content) > 1000 else st.session_state.generated_content
                        st.markdown(generated_preview)_example', '')
                if example_content:
                    example_stats = st.session_state.content_generator.get_content_stats(example_content)
                    generated_stats = stats
                    
                    st.markdown("#### 📊 Confronto Statistiche")
                    
                    comparison_data = {
                        "Metrica": ["Parole", "Caratteri", "H1", "H2", "H3", "Elenchi puntati"],
                        "Esempio": [
                            example_stats.get('words', 0),
                            example_stats.get('characters', 0),
                            example_stats.get('h1_count', 0),
                            example_stats.get('h2_count', 0),
                            example_stats.get('h3_count', 0),
                            example_stats.get('bullet_points', 0)
                        ],
                        "Generato": [
                            generated_stats.get('words', 0),
                            generated_stats.get('characters', 0),
                            generated_stats.get('h1_count', 0),
                            generated_stats.get('h2_count', 0),
                            generated_stats.get('h3_count', 0),
                            generated_stats.get('bullet_points', 0)
                        ]
                    }
                    
                    st.table(comparison_data)
                    
                    # Analisi della somiglianza strutturale
                    st.markdown("#### 🎯 Analisi Strutturale")
                    
                    # Rapporto parole simile
                    word_ratio = generated_stats.get('words', 0) / max(example_stats.get('words', 1), 1)
                    if 0.8 <= word_ratio <= 1.2:
                        st.success(f"✅ Lunghezza simile all'esempio (rapporto: {word_ratio:.2f})")
                    elif word_ratio > 1.2:
                        st.info(f"📈 Contenuto più lungo dell'esempio (rapporto: {word_ratio:.2f})")
                    else:
                        st.warning(f"📉 Contenuto più breve dell'esempio (rapporto: {word_ratio:.2f})")
                    
                    # Struttura titoli
                    if generated_stats.get('h2_count', 0) >= example_stats.get('h2_count', 0):
                        st.success("✅ Struttura dei titoli ben sviluppata")
                    else:
                        st.warning("⚠️ Potrebbe beneficiare di più sottosezioni")
                    
                    # Confronto visivo affiancato
                    st.markdown("#### 👥 Confronto Visivo")
                    col_left, col_right = st.columns(2)
                    
                    with col_left:
                        st.markdown("**📄 Contenuto di Esempio**")
                        st.markdown(example_content[:1000] + "..." if len(example_content) > 1000 else example_content)
                    
                    with col_right:
                        st.markdown("**🆕 Contenuto Generato**")
                        generated_preview = st.session_state.generated_content[:1000] + "..." if len(st.session_state.generated_content) > 1000 else st.session_state.generated_content
                        st.markdown(generated_preview)
        
        # Sezione download
        st.header("💾 Download")
        
        # Statistiche rapide prima del download
        quick_stats = st.session_state.content_generator.get_content_stats(st.session_state.generated_content)
        col_stats1, col_stats2, col_stats3, col_stats4 = st.columns(4)
        
        with col_stats1:
            st.metric("📝 Parole", quick_stats.get('words', 0))
        with col_stats2:
            st.metric("📑 Caratteri", quick_stats.get('characters', 0))
        with col_stats3:
            st.metric("🔗 Link Interni", quick_stats.get('bullet_points', 0))
        with col_stats4:
            # Quick SEO check
            word_count = quick_stats.get('words', 0)
            if word_count >= 1500:
                st.metric("🎯 SEO", "✅ Ottimo")
            elif word_count >= 1000:
                st.metric("🎯 SEO", "⚠️ Buono")
            else:
                st.metric("🎯 SEO", "❌ Breve")
        
        # Opzioni di download
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.download_button(
                label="📄 Scarica come .txt",
                data=st.session_state.generated_content,
                file_name=f"contenuto_seo_{st.session_state.get('brand_name', 'content').lower().replace(' ', '_')}.txt",
                mime="text/plain"
            )
        
        with col2:
            st.download_button(
                label="📝 Scarica come .md",
                data=st.session_state.generated_content,
                file_name=f"contenuto_seo_{st.session_state.get('brand_name', 'content').lower().replace(' ', '_')}.md",
                mime="text/markdown"
            )
        
        with col3:
            # Crea un report completo
            seo_analysis = st.session_state.content_generator.analyze_seo_content(st.session_state.generated_content)
            
            report_content = f"""# Report SEO - {st.session_state.get('brand_name', 'Brand')}

## 📊 Statistiche Contenuto
- **Parole**: {seo_analysis.get('word_count', 0)}
- **Caratteri**: {seo_analysis.get('char_count', 0)}
- **Titoli H1**: {seo_analysis.get('h1_count', 0)}
- **Titoli H2**: {seo_analysis.get('h2_count', 0)}
- **Titoli H3**: {seo_analysis.get('h3_count', 0)}
- **Link Interni**: {seo_analysis.get('internal_links', 0)}
- **Elenchi Puntati**: {seo_analysis.get('bullet_points', 0)}

## 🎯 SEO Score: {seo_analysis.get('seo_score', 0)}/100

## 📋 Meta Tags
- **Title**: {seo_analysis.get('meta_title', 'N/A')} ({seo_analysis.get('meta_title_length', 0)}/60 caratteri)
- **Description**: {seo_analysis.get('meta_description', 'N/A')} ({seo_analysis.get('meta_description_length', 0)}/160 caratteri)

## ❌ Problemi SEO
{chr(10).join([f"- {issue}" for issue in seo_analysis.get('seo_issues', [])]) if seo_analysis.get('seo_issues') else "Nessun problema critico rilevato"}

## 💡 Raccomandazioni
{chr(10).join([f"- {rec}" for rec in seo_analysis.get('seo_recommendations', [])]) if seo_analysis.get('seo_recommendations') else "SEO ottimale raggiunto"}

---

## 📄 Contenuto Completo

{st.session_state.generated_content}
"""
            
            st.download_button(
                label="📊 Scarica Report SEO",
                data=report_content,
                file_name=f"report_seo_{st.session_state.get('brand_name', 'content').lower().replace(' ', '_')}.md",
                mime="text/markdown"
            )
        
        # Azioni aggiuntive
        st.markdown("---")
        st.markdown("### 🔄 Azioni Aggiuntive")
        
        col_actions1, col_actions2, col_actions3 = st.columns(3)
        
        with col_actions1:
            if st.button("🔄 Rigenera Contenuto", help="Genera una nuova versione con gli stessi parametri"):
                st.info("💡 Per rigenerare, modifica leggermente il content brief e clicca nuovamente 'Genera'")
        
        with col_actions2:
            if st.button("📋 Copia negli Appunti", help="Copia il contenuto markdown negli appunti"):
                st.success("✅ Contenuto copiato! (Usa Ctrl+V per incollare)")
        
        with col_actions3:
            if st.button("🗑️ Cancella Risultati", help="Cancella i risultati generati"):
                for key in ['generated_content', 'brand_name', 'content_example']:
                    if key in st.session_state:
                        del st.session_state[key]
                st.rerun()

    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: #666; margin-top: 50px;'>
            <h4>🚀 SEO Content Generator Pro</h4>
            <p>🔧 Creato con Streamlit | 🤖 Powered by OpenAI GPT-4 | 📊 Ottimizzato per gli standard E-E-A-T di Google</p>
            <p><strong>Funzionalità principali:</strong></p>
            <p>✅ Analisi SEO completa | ✅ Meta tags automatici | ✅ Strategia competitor | ✅ Target specifico | ✅ CTA integrate</p>
            <p style='font-size: 0.8em; margin-top: 20px;'>
                💡 <strong>Suggerimento:</strong> Per risultati ottimali, compila tutti i campi strategici e fornisci esempi di contenuti che funzionano bene
            </p>
        </div>
        """, 
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
