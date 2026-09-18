# Anchor Text Distribution Engine
import random

GENERIC_ANCHORS = {
    'en': ['official website', 'visit site', 'source', 'view documentation', 'learn more', 'platform details'],
    'de': ['Offizielle Webseite', 'Quelle ansehen', 'Zur Dokumentation', 'Hier erfahren Sie mehr', 'Plattform'],
    'es': ['sitio web oficial', 'ver fuente', 'documentacion oficial', 'mas informacion', 'conocer mas'],
    'fr': ['site officiel', 'source officielle', 'voir la documentation', 'en savoir plus', 'details'],
    'it': ['sito web ufficiale', 'fonte ufficiale', 'leggi la documentazione', 'scopri di piu', 'dettagli']
}

def generate_anchor_plan(client_name, client_url, primary_keywords, language='en', count=25):
    anchors = []
    
    # 40 percent Branded
    branded_count = max(1, int(count * 0.40))
    for _ in range(branded_count):
        variant = random.choice([
            client_name,
            f'{client_name} Official',
            f'{client_name} Platform',
            f'{client_name} Online'
        ])
        anchors.append({'type': 'branded', 'text': variant})

    # 30 percent Semantic
    semantic_count = max(1, int(count * 0.30))
    for i in range(semantic_count):
        kw = primary_keywords[i % len(primary_keywords)] if primary_keywords else 'service'
        variant = random.choice([
            kw,
            f'{client_name} {kw}',
            f'{kw} by {client_name}',
            f'guide to {kw}'
        ])
        anchors.append({'type': 'semantic', 'text': variant})

    # 20 percent Naked URL
    naked_count = max(1, int(count * 0.20))
    clean_url = client_url.replace('https://', '').replace('http://', '').rstrip('/')
    for _ in range(naked_count):
        variant = random.choice([
            client_url,
            clean_url,
            f'www.{clean_url}' if not clean_url.startswith('www.') else clean_url
        ])
        anchors.append({'type': 'naked_url', 'text': variant})

    # Generic anchors
    generic_list = GENERIC_ANCHORS.get(language, GENERIC_ANCHORS['en'])
    while len(anchors) < count:
        anchors.append({'type': 'generic', 'text': random.choice(generic_list)})

    random.shuffle(anchors)
    return anchors[:count]