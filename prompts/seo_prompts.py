def get_seo_content_prompt(brand_name, website_url, content_brief):
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
