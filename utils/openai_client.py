import openai
from openai import OpenAI
import streamlit as st
from config import OPENAI_API_KEY, OPENAI_MODEL, MAX_TOKENS, TEMPERATURE

class OpenAIClient:
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
