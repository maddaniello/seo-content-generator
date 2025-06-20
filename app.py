import streamlit as st
from utils.content_generator import ContentGenerator
from config import PAGE_TITLE, PAGE_ICON
import os

# Configurazione pagina
st.set_page_config(
    page_title=PAGE_TITLE,
    page_icon=PAGE_ICON,
    layout="wide",
    initial_sidebar_state="expanded"
)

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