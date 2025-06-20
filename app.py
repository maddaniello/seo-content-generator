import streamlit as st
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
    
    def get_seo_content_prompt(self, brand_name, website_url, content_brief, tone_reference="", internal_links="", content_example=""):
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

        return f"""
Sei un esperto SEO Copywriter specializzato nella creazione di contenuti ottimizzati per i motori di ricerca.

INFORMAZIONI SUL CLIENTE:
- Brand: {brand_name}
- Website: {website_url}
- Content Brief: {content_brief}

{tone_instruction}

{example_instruction}

{links_instruction}

ISTRUZIONI FONDAMENTALI:
DEVI SCRIVERE UN ARTICOLO COMPLETO E DETTAGLIATO DI ALMENO 1500-2000 PAROLE. NON limitarti a esempi o bozze.

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

LUNGHEZZA: OBBLIGATORIA 1500-2000 parole (scrivi tutto il contenuto richiesto)

FORMAT: Markdown con formattazione completa

IMPORTANTE: Non limitarti a bozze o esempi. Scrivi l'articolo completo seguendo tutti questi requisiti e replicando lo stile del contenuto di esempio fornito.
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
    
    def generate_seo_content(self, api_key, brand_name, website_url, content_brief, tone_reference="", internal_links="", content_example=""):
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
            prompt = self.get_seo_content_prompt(brand_name, website_url, content_brief, tone_reference, internal_links, content_example)
            
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
        
        return {
            'words': words,
            'characters': characters,
            'characters_no_spaces': characters_no_spaces,
            'h1_count': h1_count,
            'h2_count': h2_count,
            'h3_count': h3_count,
            'bullet_points': bullet_points,
            'numbered_lists': numbered_lists
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
                st.markdown("**Esempio di Content Brief:**")
                st.code("""
H1: Sospensione delle rate del mutuo
H2: Quando è possibile sospendere?
H2: Come fare richiesta
H2: Cosa comporta la sospensione
H2: Fondo Gasparrini

Target: Proprietari casa con mutuo
Keyword: sospensione rate mutuo
Lunghezza: 1500-1800 parole
                """, language="text")
            
            content_brief = st.text_area(
                "Content Brief / Scaletta Editoriale *",
                height=200,
                placeholder="Inserisci qui la scaletta dettagliata del contenuto...",
                help="Fornisci una scaletta dettagliata con titoli, sottotitoli, target e keyword"
            )
            
            # Nuovo campo per tone of voice
            st.markdown("### 🎯 Personalizzazione Stile e Contenuto")
            
            col_left, col_right = st.columns(2)
            
            with col_left:
                tone_reference = st.text_area(
                    "Riferimento Tone of Voice (opzionale)",
                    height=150,
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
                    height=250,
                    placeholder="Incolla qui un articolo completo del tuo sito che funziona bene...",
                    help="Un contenuto completo che ti piace per struttura, stile e approccio. L'AI studierà come è scritto per replicare lo stesso metodo."
                )
                
                if content_example:
                    word_count = len(content_example.split())
                    st.caption(f"📊 Parole: {word_count} - {'✅ Ottimo per l\'analisi' if word_count > 200 else '⚠️ Troppo breve, aggiungi più contenuto'}")
            
            # Info box esplicativo
            st.info("""
            💡 **Differenza tra i campi:**
            - **Tone of Voice**: Breve estratto per capire il tono comunicativo
            - **Contenuto di Esempio**: Articolo completo per studiare struttura, approccio e metodologia di scrittura
            """)
            
            submitted = st.form_submit_button("🚀 Genera Contenuto SEO", type="primary")
            
            if submitted:
                if not all([brand_name, website_url, content_brief]):
                    st.error("❌ Tutti i campi contrassegnati con * sono obbligatori")
                else:
                    # Genera il contenuto
                    success, result = st.session_state.content_generator.generate_seo_content(
                        api_key, brand_name, website_url, content_brief, tone_reference, internal_links, content_example
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
        tab_names = ["📖 Anteprima", "📝 Markdown", "📊 Statistiche"]
        if 'content_example' in st.session_state and st.session_state.get('content_example', '').strip():
            tab_names.append("🔍 Confronto con Esempio")
        
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
        
        with tabs[2]:  # Statistiche
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
        
        # Tab confronto (solo se c'è un esempio)
        if len(tabs) > 3:
            with tabs[3]:  # Confronto
                st.markdown("### 🔍 Confronto con Contenuto di Esempio")
                
                # Statistiche comparative
                example_content = st.session_state.get('content_example', '')
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
        col1, col2 = st.columns(2)
        
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

    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: #666;'>
            <p>🔧 Creato con Streamlit | 🤖 Powered by OpenAI GPT-4</p>
            <p>📊 Ottimizzato per gli standard E-E-A-T di Google</p>
        </div>
        """, 
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
