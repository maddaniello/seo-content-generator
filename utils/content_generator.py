import streamlit as st
from utils.openai_client import OpenAIClient
from prompts.seo_prompt import get_seo_content_prompt
import re

class ContentGenerator:
    def __init__(self):
        self.openai_client = OpenAIClient()
    
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
    
    def generate_seo_content(self, api_key, brand_name, website_url, content_brief):
        """Genera il contenuto SEO ottimizzato"""
        
        # Valida gli input
        validation_errors = self.validate_inputs(brand_name, website_url, content_brief)
        if validation_errors:
            return False, validation_errors
        
        try:
            # Inizializza il client OpenAI
            if not self.openai_client.initialize_client(api_key):
                return False, ["Errore nell'inizializzazione del client OpenAI"]
            
            # Testa la connessione
            connection_ok, connection_msg = self.openai_client.test_connection()
            if not connection_ok:
                return False, [f"Errore di connessione: {connection_msg}"]
            
            # Genera il prompt
            prompt = get_seo_content_prompt(brand_name, website_url, content_brief)
            
            # Genera il contenuto
            with st.spinner("🔄 Generazione contenuto in corso..."):
                content = self.openai_client.generate_content(prompt)
            
            return True, content
            
        except Exception as e:
            return False, [f"Errore durante la generazione: {str(e)}"]
    
    def format_content_preview(self, content):
        """Formatta il contenuto per l'anteprima"""
        # Qui puoi aggiungere ulteriori formattazioni se necessario
        return content
    
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
