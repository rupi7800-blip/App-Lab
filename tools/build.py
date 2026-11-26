import os, re, hashlib
OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EMAIL = "info@example.com"  # DA SOSTITUIRE
SITE = "https://rupi7800-blip.github.io/App-Lab/"  # aggiornare se si usa un dominio proprio
NAV = [("index.html", "Home"), ("servizi.html", "Servizi"), ("come-lavoriamo.html", "Come lavoriamo"),
       ("esempi.html", "Esempi"), ("progetti.html", "Progetti"), ("contatti.html", "Contatti")]

ICONS = {
 "ruler": '<path d="M3 17 17 3l4 4L7 21z"/><path d="m7 13 2 2M10 10l2 2M13 7l2 2"/>',
 "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3.5 2"/>',
 "devices": '<rect x="2.5" y="4" width="14" height="11" rx="2"/><path d="M7 19h5M9.5 15v4"/><rect x="18" y="9" width="3.5" height="9" rx="1"/>',
 "chat": '<path d="M4 5h16v11H9.5L4 20z"/><path d="M8 9.5h8M8 12.5h5"/>',
 "blocks": '<rect x="3" y="3" width="8" height="8" rx="1.5"/><rect x="13" y="3" width="8" height="8" rx="1.5"/><rect x="3" y="13" width="8" height="8" rx="1.5"/><path d="M17 13v8M13 17h8"/>',
 "gear": '<circle cx="12" cy="12" r="3"/><circle cx="12" cy="12" r="7"/><path d="M12 2.5V5M12 19v2.5M2.5 12H5M19 12h2.5M5.3 5.3l1.8 1.8M16.9 16.9l1.8 1.8M18.7 5.3l-1.8 1.8M7.1 16.9l-1.8 1.8"/>',
 "link": '<path d="M10 14a4 4 0 0 0 5.7 0l3-3a4 4 0 0 0-5.7-5.7l-1 1"/><path d="M14 10a4 4 0 0 0-5.7 0l-3 3a4 4 0 0 0 5.7 5.7l1-1"/>',
 "lifebuoy": '<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="3.5"/><path d="m5.6 5.6 3.9 3.9M14.5 14.5l3.9 3.9M18.4 5.6l-3.9 3.9M9.5 14.5l-3.9 3.9"/>',
 "calendar": '<rect x="3" y="5" width="18" height="16" rx="2"/><path d="M3 10h18M8 3v4M16 3v4"/>',
 "doc": '<path d="M6 3h8l5 5v13H6z"/><path d="M14 3v5h5M9 13h7M9 17h7"/>',
 "users": '<circle cx="9" cy="8" r="3.5"/><path d="M2.5 20c0-3.6 2.9-6 6.5-6s6.5 2.4 6.5 6"/><circle cx="17.5" cy="9" r="2.5"/><path d="M17 14c2.8 0 4.5 1.8 4.5 4.5"/>',
 "box": '<path d="m3 8 9-5 9 5v9l-9 5-9-5z"/><path d="m3 8 9 5 9-5M12 13v9"/>',
 "bars": '<path d="M5 20V11M11 20V4M17 20v-6M3 20h18"/>',
 "bell": '<path d="M4 17h16M6 17a6 6 0 0 1 12 0M12 8V5.5M9.5 5.5h5"/>',
 "helm": '<circle cx="12" cy="12" r="3"/><circle cx="12" cy="12" r="8"/><path d="M12 2v4M12 18v4M2 12h4M18 12h4M5 5l2.8 2.8M16.2 16.2 19 19M19 5l-2.8 2.8M7.8 16.2 5 19"/>',
 "leaf": '<path d="M5 19C5 10 10 5 20 5c0 10-5 15-14 15"/><path d="M5 19c3-5 6-8 10-10"/>',
 "pulse": '<path d="M3 12h4l2.5-6 4 12 2.5-6H21"/>',
 "plus": '<circle cx="12" cy="12" r="9" stroke-dasharray="3 3"/><path d="M12 8v8M8 12h8"/>',
}

def svg(name):
    return f'<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false">{ICONS[name]}</svg>'

def ver(path):
    return hashlib.md5(open(os.path.join(OUT, path), "rb").read()).hexdigest()[:8]

def page(fname, title, desc, body, head=None, base=False):
    items = ""
    for href, label in NAV:
        if href == "contatti.html":
            cur = ' aria-current="page"' if fname == href else ""
            items += f'<li><a class="btn" href="{href}"{cur}>Parliamone</a></li>\n'
        else:
            cur = ' aria-current="page"' if fname == href else ""
            items += f'<li><a href="{href}"{cur}>{label}</a></li>\n'
    foot = "".join(f'<li><a href="{h}">{l}</a></li>' for h, l in NAV) + '<li><a href="privacy.html">Privacy</a></li>'
    url = SITE if fname == "index.html" else SITE + fname
    seo_tags = '<meta name="robots" content="noindex">' if base else f'''<link rel="canonical" href="{url}">
<meta property="og:type" content="website">
<meta property="og:locale" content="it_IT">
<meta property="og:site_name" content="App-Lab">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}img/logo.png">'''
    skip_link = "" if base else '<a class="skip" href="#main">Vai al contenuto</a>\n'
    base_tag = '<base href="/App-Lab/">\n' if base else ""
    html = f"""<!doctype html>
<html lang="it">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
{base_tag}<link rel="icon" href="favicon.svg" type="image/svg+xml">
<link rel="icon" href="favicon.png" type="image/png" sizes="192x192">
<meta name="theme-color" content="#010c15">
{seo_tags}
<link rel="stylesheet" href="css/style.css?v={ver("css/style.css")}">
</head>
<body>
{skip_link}<header>
  <div class="wrap nav">
    <a class="logo" href="index.html" aria-label="App-Lab – Home"><img src="img/mark.png" alt="" width="36" height="36"><span class="wm">App-<span>Lab</span></span></a>
    <nav aria-label="Principale">
      <button type="button" class="menu-btn" aria-expanded="false" aria-controls="menu">Menu</button>
      <ul id="menu">
{items}      </ul>
    </nav>
  </div>
</header>
<main id="main">
{body}
</main>
<footer>
  <div class="wrap foot">
    <span><strong>App-Lab</strong> · Laboratorio di applicazioni web su misura<br>© 2026 App-Lab</span>
    <nav aria-label="Piè di pagina"><ul>{foot}</ul></nav>
  </div>
</footer>
<script src="js/main.js?v={ver("js/main.js")}"></script>
</body>
</html>
"""
    html = html.replace('<div class="ico">', '<div class="ico" aria-hidden="true">')
    html = re.sub(r'\[\[ic:(\w+)\]\]', lambda m: svg(m.group(1)), html)
    with open(os.path.join(OUT, fname), "w", encoding="utf-8") as f:
        f.write(html)

BAND = """<section><div class="wrap"><div class="band">
<h2>Hai qualcosa che vorresti semplificare?</h2>
<p>Raccontaci come lavori oggi. Il primo confronto è gratuito e senza impegno.</p>
<a class="btn" href="contatti.html">Parliamone</a></div></div></section>"""

# ---------- PROGETTI (url=None -> "In arrivo", senza link)
PROJECTS = [
 dict(icon="helm", name="Timone", status="Disponibile", url="https://rupi7800-blip.github.io/Timone-sito/",
      text="Controllo e analisi aziendale per le imprese italiane: bilanci, indici, budget e scenari in un unico strumento.", cta="Scopri Timone"),
 dict(icon="bell", name="Maggiordomo-IA", status="In arrivo", url=None,
      text="Un assistente personale con intelligenza artificiale per le attività di ogni giorno."),
 dict(icon="leaf", name="Assistente del giardino", status="In arrivo", url=None,
      text="Giardino, orto e prato: schede, calendario delle attività, meteo e consigli, anche senza connessione."),
 dict(icon="pulse", name="Consulente del Movimento", status="In arrivo", url=None,
      text="Un consulente digitale per il movimento. Maggiori dettagli a breve."),
 dict(icon="plus", name="Prossimo progetto", status="In definizione", url=None,
      text="Un altro strumento pensato per il mondo del lavoro. Ne parleremo presto."),
]

def project_cards(items):
    out = ""
    for pj in items:
        live = pj["url"] is not None
        tag = f'<span class="status {"live" if live else "soon"}">{pj["status"]}</span>'
        link = (f'<a class="btn" href="{pj["url"]}" target="_blank" rel="noopener">{pj["cta"]}<span aria-hidden="true"> ↗</span>'
                f'<span class="sr">, si apre in una nuova scheda</span></a>') if live else ""
        out += (f'<div class="card project{"" if live else " soon"}"><div class="pj-head"><div class="ico">[[ic:{pj["icon"]}]]</div>{tag}</div>'
                f'<h3>{pj["name"]}</h3><p>{pj["text"]}</p>{link}</div>')
    return f'<div class="projects">{out}</div>'

# ---------- HOME
page("index.html", "App-Lab – Applicazioni web su misura per professionisti e piccole imprese",
 "Applicazioni web su misura per professionisti, artigiani, commercianti, ristorazione, ricettività e piccole imprese. Meno lavoro ripetitivo.",
 """<section class="hero"><div class="wrap hero-grid"><div>
<div class="eyebrow">Laboratorio di applicazioni web su misura</div>
<h1>App su misura per il tuo lavoro.</h1>
<p class="lead">Creiamo applicazioni web per liberi professionisti, artigiani, commercianti, attività ricettive e ristorazione, ditte individuali e PMI. Strumenti semplici che tolgono carta, fogli Excel e compiti ripetitivi, e ti restituiscono tempo.</p>
<div class="cta"><a class="btn" href="contatti.html">Raccontaci cosa ti serve</a><a class="btn ghost" href="esempi.html">Guarda cosa possiamo fare</a></div>
<ul class="chips" aria-label="Esempi di applicazioni"><li>[[ic:calendar]]Agende e prenotazioni</li><li>[[ic:doc]]Preventivi</li><li>[[ic:users]]Clienti</li><li>[[ic:box]]Magazzino</li></ul>
</div><img class="hero-logo" src="img/logo.webp" width="640" height="640" alt="App-Lab, laboratorio di applicazioni web su misura" fetchpriority="high"></div></section>

<section class="alt"><div class="wrap">
<h2>Non un software generico. Il tuo.</h2>
<p class="sub">I programmi “per tutti” ti obbligano a cambiare il modo di lavorare. Noi facciamo il contrario: partiamo da come lavori tu e costruiamo lo strumento intorno a te.</p>
<div class="grid four">
<div class="card"><div class="ico">[[ic:ruler]]</div><h3>Su misura</h3><p>Solo le funzioni che ti servono, con le parole e i passaggi del tuo mestiere.</p></div>
<div class="card"><div class="ico">[[ic:clock]]</div><h3>Meno lavoro ripetitivo</h3><p>Preventivi, promemoria, schede clienti, scadenze: ciò che oggi fai a mano può diventare automatico.</p></div>
<div class="card"><div class="ico">[[ic:devices]]</div><h3>Da qualsiasi dispositivo</h3><p>Si usano dal browser di PC, tablet e smartphone. Non c’è nulla da installare.</p></div>
<div class="card"><div class="ico">[[ic:chat]]</div><h3>Un solo interlocutore</h3><p>Parli con chi progetta e sviluppa, in italiano semplice, senza gergo tecnico.</p></div>
</div></div></section>

<section><div class="wrap split">
<div><h2>Pensato per chi ha un’attività da portare avanti</h2>
<p class="sub">Non servono competenze informatiche. Serve solo sapere cosa vorresti fosse più semplice.</p>
<ul class="check">
<li><strong>Liberi professionisti</strong> – consulenti, tecnici, terapisti, formatori</li>
<li><strong>Artigiani</strong> – installatori, officine, laboratori, imprese edili</li>
<li><strong>Commercianti</strong> – negozi, botteghe, attività di vendita al dettaglio</li>
<li><strong>Attività ricettive e ristorazione</strong> – hotel, B&amp;B, agriturismi, ristoranti, bar, pizzerie</li>
<li><strong>Ditte individuali</strong> – piccole attività che fanno tutto da sole</li>
<li><strong>Piccole e medie imprese</strong> – team che hanno superato i fogli di calcolo</li></ul></div>
<div class="card"><h3>Un’idea ancora vaga?</h3><p>Va benissimo. Molti progetti nascono da una frase come “vorrei non dover rifare sempre le stesse cose”. Ti aiutiamo a trasformarla in uno strumento concreto.</p></div>
</div></section>

<section class="alt"><div class="wrap">
<h2>Come funziona, in breve</h2>
<p class="sub">In sintesi: dal primo confronto alla consegna e al supporto.</p>
<ol class="steps">
<li><h3>Ascolto</h3><p>Ci racconti la tua giornata e dove perdi più tempo.</p></li>
<li><h3>Proposta</h3><p>Ti diciamo cosa faremo, in quanto tempo e a che costo.</p></li>
<li><h3>Sviluppo a tappe</h3><p>Vedi l’avanzamento man mano e puoi correggere la rotta.</p></li>
<li><h3>Consegna e supporto</h3><p>Ti affianchiamo all’avvio e dopo.</p></li>
</ol>
<p class="mt"><a href="come-lavoriamo.html">Scopri il metodo nel dettaglio →</a></p>
</div></section>

<section><div class="wrap">
<h2>I nostri progetti</h2>
<p class="sub">Oltre ai lavori su misura, sviluppiamo strumenti nostri pensati per il mondo del lavoro.</p>
""" + project_cards(PROJECTS[:3]) + """
<p class="mt"><a href="progetti.html">Vedi tutti i progetti →</a></p>
</div></section>
""" + BAND)

# ---------- SERVIZI
page("servizi.html", "Servizi – App-Lab", "Cosa realizziamo: applicazioni web su misura, automazioni, integrazioni e assistenza continua.",
 """<section class="page-head"><div class="wrap"><div class="eyebrow">Servizi</div>
<h1>Cosa possiamo fare per te</h1>
<p class="lead">Quattro aree di lavoro. Spesso un progetto ne unisce più di una.</p></div></section>
<section><div class="wrap"><div class="grid four">
<div class="card"><div class="ico">[[ic:blocks]]</div><h3>Applicazioni web su misura</h3><p>Gestionali, agende, schede clienti, portali riservati. Progettati sui tuoi processi, non adattati da un modello generico.</p></div>
<div class="card"><div class="ico">[[ic:gear]]</div><h3>Automazione di attività</h3><p>Promemoria, riepiloghi, documenti, calcoli: i compiti ripetitivi li svolge l’applicazione al posto tuo.</p></div>
<div class="card"><div class="ico">[[ic:link]]</div><h3>Collegamenti tra strumenti</h3><p>Mettiamo in comunicazione i programmi che già usi, così i dati non si ricopiano più a mano.</p></div>
<div class="card"><div class="ico">[[ic:lifebuoy]]</div><h3>Assistenza e miglioramenti</h3><p>Dopo la consegna restiamo disponibili per correzioni, nuove funzioni e formazione di chi la usa.</p></div>
</div></div></section>
<section class="alt faq"><div class="wrap"><h2>Domande frequenti</h2><p class="sub">Le cose che ci chiedono più spesso.</p>
<details><summary>Devo capire di informatica?</summary><p>No. Ti guidiamo noi e ti spieghiamo tutto in modo semplice. Tu devi solo conoscere il tuo lavoro.</p></details>
<details><summary>Cosa significa “applicazione web”?</summary><p>È un programma che si apre dal browser, come un sito, ma fa cose utili al tuo lavoro. Funziona su computer, tablet e telefono, senza installazioni.</p></details>
<details><summary>Quanto costa?</summary><p>Dipende da cosa serve. Dopo il primo confronto ti diamo una proposta scritta con costi e tempi, prima di iniziare.</p></details>
<details><summary>I miei dati sono al sicuro?</summary><p>Trattiamo i dati con attenzione e li gestiamo nel rispetto della normativa. Ne parliamo insieme nella fase di proposta.</p></details>
<details><summary>Posso far modificare l’applicazione in futuro?</summary><p>Sì. Un’applicazione cresce con la tua attività: possiamo aggiungere funzioni e modifiche quando servono.</p></details>
</div></section>
""" + BAND)

# ---------- COME LAVORIAMO
page("come-lavoriamo.html", "Come lavoriamo – App-Lab", "Il metodo di App-Lab: ascolto, proposta, sviluppo a tappe, consegna e supporto.",
 """<section class="page-head"><div class="wrap"><div class="eyebrow">Metodo</div>
<h1>Un percorso semplice, senza sorprese</h1>
<p class="lead">Sai sempre a che punto siamo e cosa succede dopo.</p></div></section>
<section><div class="wrap"><ol class="steps">
<li><h3>Ascolto</h3><p>Un primo colloquio, anche online, per capire la tua attività e i punti che ti fanno perdere tempo. Gratuito e senza impegno.</p></li>
<li><h3>Proposta</h3><p>Ti presentiamo cosa realizzeremo, con tempi e costi chiari, prima di iniziare qualsiasi lavoro.</p></li>
<li><h3>Sviluppo a tappe</h3><p>Costruiamo a piccoli passi e ti mostriamo il risultato spesso. Così correggiamo subito ciò che non va.</p></li>
<li><h3>Consegna e avvio</h3><p>Pubblichiamo l’applicazione e ti insegniamo a usarla. Trovi tutto già pronto.</p></li>
<li><h3>Supporto</h3><p>Restiamo disponibili per assistenza, modifiche e nuove idee man mano che la tua attività cresce.</p></li>
</ol></div></section>
<section class="alt"><div class="wrap split">
<div><h2>I nostri principi</h2></div>
<ul class="check">
<li><strong>Chiarezza:</strong> parole semplici, nessun gergo inutile.</li>
<li><strong>Semplicità:</strong> poche funzioni, fatte bene, facili da usare.</li>
<li><strong>Trasparenza:</strong> costi e tempi concordati prima di iniziare.</li>
<li><strong>Tuo il risultato:</strong> costruiamo intorno al tuo modo di lavorare.</li></ul>
</div></section>
""" + BAND)

# ---------- ESEMPI
cards = [("[[ic:calendar]]","Agende e prenotazioni","Appuntamenti online per i tuoi clienti, con promemoria automatici che riducono le assenze.","Liberi professionisti"),
("[[ic:doc]]","Preventivi e documenti","Preventivi, schede di lavoro e riepiloghi in pochi clic, con il tuo stile e i tuoi listini.","Artigiani"),
("[[ic:users]]","Gestione clienti","Anagrafiche, storico dei lavori, note e scadenze in un unico posto sempre aggiornato.","Ditte individuali"),
("[[ic:box]]","Magazzino e ordini","Controllo di scorte, forniture e ordini, al posto di fogli di calcolo sparsi.","Commercianti"),
("[[ic:bars]]","Pannelli di controllo","Numeri chiave dell’attività a colpo d’occhio: incassi, lavori aperti, scadenze.","PMI"),
("[[ic:bell]]","Prenotazioni e ospiti","Tavoli, camere e arrivi in un unico calendario, con conferme e promemoria automatici agli ospiti.","Attività ricettive e ristorazione")]
cx = "".join(f'<div class="card"><div class="ico">{i}</div><span class="tag">{t}</span><h3>{h}</h3><p>{p}</p></div>' for i,h,p,t in cards)
page("esempi.html", "Esempi di applicazioni – App-Lab", "Esempi del tipo di applicazioni web su misura che App-Lab può realizzare per la tua attività.",
 f"""<section class="page-head"><div class="wrap"><div class="eyebrow">Esempi</div>
<h1>Il tipo di strumenti che realizziamo</h1>
<p class="lead">Idee per capire cosa è possibile. Ogni applicazione viene poi disegnata sulla tua attività.</p></div></section>
<section><div class="wrap"><div class="grid">{cx}</div>
<p class="note mt">Questi sono esempi illustrativi del tipo di lavoro, non progetti di clienti.</p></div></section>
""" + BAND)

# ---------- PROGETTI
page("progetti.html", "I nostri progetti – App-Lab", "Gli strumenti sviluppati da App-Lab per il mondo del lavoro: Timone e i prossimi progetti in arrivo.",
 """<section class="page-head"><div class="wrap"><div class="eyebrow">Progetti</div>
<h1>Gli strumenti che sviluppiamo per conto nostro</h1>
<p class="lead">Accanto alle app su misura per i clienti, costruiamo strumenti pensati per chi lavora. Alcuni sono già disponibili, altri arriveranno presto.</p></div></section>
<section><div class="wrap">""" + project_cards(PROJECTS) + """
<p class="note mt">I progetti “in arrivo” non sono ancora disponibili: i collegamenti compariranno qui quando saranno pronti.</p>
</div></section>
""" + BAND)

# ---------- CONTATTI
page("contatti.html", "Contatti – App-Lab", "Contatta App-Lab: raccontaci cosa vorresti semplificare nella tua attività. Primo confronto gratuito.",
 f"""<section class="page-head"><div class="wrap"><div class="eyebrow">Contatti</div>
<h1>Parliamone</h1>
<p class="lead">Descrivi in poche righe la tua attività e cosa vorresti semplificare. Ti rispondiamo con calma, senza impegno.</p></div></section>
<section><div class="wrap split">
<form id="contact" data-email="{EMAIL}">
<label>Nome e cognome<input name="nome" required autocomplete="name"></label>
<label>Email<input type="email" name="email" required autocomplete="email"></label>
<label>Che attività svolgi?<select name="tipo"><option>Libero professionista</option><option>Artigiano</option><option>Commerciante</option><option>Attività ricettiva o ristorazione</option><option>Ditta individuale</option><option>PMI</option><option>Altro</option></select></label>
<label>Cosa vorresti semplificare?<textarea name="messaggio" required></textarea></label>
<button class="btn" type="submit">Invia richiesta</button>
<p class="note">Si aprirà il tuo programma di posta con il messaggio già pronto. Leggi la <a href="privacy.html">informativa privacy</a>.</p>
</form>
<div class="card"><h3>Oppure scrivici direttamente</h3><p><a href="mailto:{EMAIL}">{EMAIL}</a></p>
<p>Il primo colloquio è gratuito: serve a capire se e come possiamo aiutarti.</p></div>
</div></section>""")

# ---------- PRIVACY
page("privacy.html", "Privacy – App-Lab", "Informativa sul trattamento dei dati personali di App-Lab.",
 """<section class="page-head"><div class="wrap"><h1>Informativa privacy</h1></div></section>
<section><div class="wrap prose">
<p><strong>Bozza da completare prima della pubblicazione</strong> con i dati del titolare e la verifica di un consulente.</p>
<h2>Titolare del trattamento</h2><p>[Ragione sociale, indirizzo, partita IVA, email di contatto]</p>
<h2>Dati raccolti</h2><p>Questo sito non usa cookie di profilazione. I dati che ci invii tramite il modulo di contatto (nome, email, messaggio) vengono usati solo per risponderti.</p>
<h2>Conservazione e diritti</h2><p>Conserviamo i messaggi per il tempo necessario a gestire la tua richiesta. Puoi chiedere accesso, rettifica o cancellazione scrivendoci.</p>
</div></section>""")

# 404 (base href: se si usa un dominio proprio alla radice, rimuovere base=True)
# 404, robots, sitemap
page("404.html", "Pagina non trovata – App-Lab", "Pagina non trovata.",
 '<section class="hero"><div class="wrap"><h1>Pagina non trovata</h1><p class="lead">Il link potrebbe essere errato o la pagina spostata.</p><a class="btn" href="index.html">Torna alla home</a></div></section>', base=True)

pages=[h for h,_ in NAV]+["privacy.html"]
open(os.path.join(OUT,"sitemap.xml"),"w").write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+"".join(f"<url><loc>{SITE}{'' if h=='index.html' else h}</loc></url>\n" for h in pages)+'</urlset>\n')
open(os.path.join(OUT,"robots.txt"),"w").write(f"User-agent: *\nAllow: /\nSitemap: {SITE}sitemap.xml\n")
