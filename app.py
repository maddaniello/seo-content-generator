import streamlit as st
import sys
import os

# Aggiungi il path corrente per gli import
sys.path.append(os.path.dirname(__file__))

# Import diretti senza struttura a pacchetti
try:
    from config import PAGE_TITLE, PAGE_ICON
except ImportError:
    PAGE_TITLE = "SEO Content Generator"
    PAGE_ICON = "📝"

import openai
from openai import OpenAI
import re

# Configurazioni inline
OPENAI_MODEL = "gpt-4-turbo-preview"
MAX_TOKENS = 4000
TEMPERATURE = 0.7

# Classe ContentGenerator inline
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
    
    def get_seo_content_prompt(self, brand_name, website_url, content_brief):
        return f"""
Sei un esperto SEO Copywriter specializzato nella creazione di contenuti ottimizzati per i motori di ricerca.

INFORMAZIONI SUL CLIENTE:
- Brand: {brand_name}
- Website: {website_url}
- Content Brief: {content_brief}

ISTRUZIONI:
Crea un articolo SEO ottimizzato seguendo rigorosamente gli standard E-E-A-T di Google:

1. **EXPERIENCE (Esperienza)**:
   - Includi esempi pratici e diversificati
   - Presenta scenari del mondo reale
   - Aggiungi casi studio specifici
   - Utilizza testimonianze credibili

2. **EXPERTISE (Competenza)**:
   - Dimostra conoscenza approfondita dell'argomento
   - Includi dati statistici e insight originali
   - Usa terminologia tecnica appropriata
   - Fornisci analisi dettagliate

3. **AUTHORITATIVENESS (Autorevolezza)**:
   - Cita fonti autorevoli e studi accademici
   - Referenzia normative e regolamentazioni
   - Includi citazioni da esperti del settore
   - Aggiungi link a risorse credibili

4. **TRUSTWORTHINESS (Affidabilità)**:
   - Mantieni un tono trasparente e oggettivo
   - Discuti limitazioni e possibili conflitti
   - Includi disclaimer dove necessario
   - Fornisci informazioni complete e bilanciate

STRUTTURA RICHIESTA:
- Utilizza una struttura H1, H2, H3 logica e SEO-friendly
- Includi elenchi puntati per migliorare la leggibilità
- Usa il grassetto per evidenziare concetti chiave
- Scrivi paragrafi di 3-4 righe massimo
- Includi una introduzione coinvolgente e una conclusione con CTA

LUNGHEZZA: 1500-2000 parole

FORMAT: Markdown con formattazione completa

Inizia ora la creazione del contenuto seguendo tutti questi requisiti.
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
            r'(?:/?|[/?]\S+)

# Configurazione pagina
st.set_page_config(
    page_title=PAGE_TITLE,
    page_icon=PAGE_ICON,
    layout="wide",
    initial_sidebar_state="expanded"
)
def main():
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
                height=300,
                placeholder="Inserisci qui la scaletta dettagliata del contenuto...",
                help="Fornisci una scaletta dettagliata con titoli, sottotitoli, target e keyword"
            )
            
            submitted = st.form_submit_button("🚀 Genera Contenuto SEO", type="primary")
            
            if submitted:
                if not all([brand_name, website_url, content_brief]):
                    st.error("❌ Tutti i campi contrassegnati con * sono obbligatori")
                else:
                    # Genera il contenuto
                    success, result = st.session_state.content_generator.generate_seo_content(
                        api_key, brand_name, website_url, content_brief
                    )
                    
                    if success:
                        st.session_state.generated_content = result
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
        tab1, tab2, tab3 = st.tabs(["📖 Anteprima", "📝 Markdown", "📊 Statistiche"])
        
        with tab1:
            st.markdown("### Anteprima del Contenuto")
            st.markdown(st.session_state.generated_content)
        
        with tab2:
            st.markdown("### Codice Markdown")
            st.code(st.session_state.generated_content, language="markdown")
            
            # Bottone per copiare
            if st.button("📋 Copia Markdown"):
                st.write("Contenuto copiato negli appunti!")
        
        with tab3:
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
        
        # Sezione download
        st.header("💾 Download")
        col1, col2 = st.columns(2)
        
        with col1:
            st.download_button(
                label="📄 Scarica come .txt",
                data=st.session_state.generated_content,
                file_name=f"contenuto_seo_{brand_name.lower().replace(' ', '_') if 'brand_name' in locals() else 'content'}.txt",
                mime="text/plain"
            )
        
        with col2:
            st.download_button(
                label="📝 Scarica come .md",
                data=st.session_state.generated_content,
                file_name=f"contenuto_seo_{brand_name.lower().replace(' ', '_') if 'brand_name' in locals() else 'content'}.md",
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
    main(), re.IGNORECASE)
        return url_pattern.match(url) is not None
    
    def generate_content(self, prompt):
        """Genera contenuto utilizzando l'API OpenAI"""
        if not self.client:
            raise Exception("Client OpenAI non inizializzato")
        
        try:
            response = self.client.chat.completions.create(
                model=OPENAI_MODEL,
                messages=[
                    {
                        "role": "system",
                        "content": "Sei un esperto SEO Copywriter specializzato nella creazione di contenuti ottimizzati per i motori di ricerca, con particolare attenzione agli standard E-E-A-T di Google."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=MAX_TOKENS,
                temperature=TEMPERATURE
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            raise Exception(f"Errore nella generazione del contenuto: {str(e)}")
    
    def test_connection(self):
        """Testa la connessione con l'API OpenAI"""
        if not self.client:
            return False, "Client non inizializzato"
        
        try:
            response = self.client.chat.completions.create(
                model=OPENAI_MODEL,
                messages=[{"role": "user", "content": "Test"}],
                max_tokens=10
            )
            return True, "Connessione riuscita"
        except Exception as e:
            return False, f"Errore di connessione: {str(e)}"
    
    def generate_seo_content(self, api_key, brand_name, website_url, content_brief):
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
            prompt = self.get_seo_content_prompt(brand_name, website_url, content_brief)
            
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
                height=300,
                placeholder="Inserisci qui la scaletta dettagliata del contenuto...",
                help="Fornisci una scaletta dettagliata con titoli, sottotitoli, target e keyword"
            )
            
            submitted = st.form_submit_button("🚀 Genera Contenuto SEO", type="primary")
            
            if submitted:
                if not all([brand_name, website_url, content_brief]):
                    st.error("❌ Tutti i campi contrassegnati con * sono obbligatori")
                else:
                    # Genera il contenuto
                    success, result = st.session_state.content_generator.generate_seo_content(
                        api_key, brand_name, website_url, content_brief
                    )
                    
                    if success:
                        st.session_state.generated_content = result
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
        tab1, tab2, tab3 = st.tabs(["📖 Anteprima", "📝 Markdown", "📊 Statistiche"])
        
        with tab1:
            st.markdown("### Anteprima del Contenuto")
            st.markdown(st.session_state.generated_content)
        
        with tab2:
            st.markdown("### Codice Markdown")
            st.code(st.session_state.generated_content, language="markdown")
            
            # Bottone per copiare
            if st.button("📋 Copia Markdown"):
                st.write("Contenuto copiato negli appunti!")
        
        with tab3:
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
        
        # Sezione download
        st.header("💾 Download")
        col1, col2 = st.columns(2)
        
        with col1:
            st.download_button(
                label="📄 Scarica come .txt",
                data=st.session_state.generated_content,
                file_name=f"contenuto_seo_{brand_name.lower().replace(' ', '_') if 'brand_name' in locals() else 'content'}.txt",
                mime="text/plain"
            )
        
        with col2:
            st.download_button(
                label="📝 Scarica come .md",
                data=st.session_state.generated_content,
                file_name=f"contenuto_seo_{brand_name.lower().replace(' ', '_') if 'brand_name' in locals() else 'content'}.md",
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
