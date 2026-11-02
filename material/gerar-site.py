"""Gera o site da Faculdade Nine (raiz) e prepara as páginas para publicação.
Rodar na raiz do repositório:  python3 -I material/gerar-site.py <Disciplinas_Nine.xlsx>

- Faculdade (raiz): index, curso, areas-de-atuacao, a-faculdade, transparencia, ouvidoria, privacidade
- Academia (/academia/index.html) é mantida à mão; aqui só recebe o CSS embutido e o srcset das fotos.
Para trocar fotos, edite FOTOS abaixo (arquivos em assets/img/galeria/<id>.webp, -600 e -320)."""
import collections, glob, json, os, re, sys
import openpyxl
from PIL import Image

HOJE = "02/11/2026"
EMAIL = "contato@nine.com.br"
SITE = "https://nineacademia.vercel.app"
ENDERECO = "Rua Engenheiro Niepce da Silva, 139 · Portão · Curitiba/PR · CEP 80610-240"
TBC = '<span class="tbc">[A CONFIRMAR]</span>'
CURSO = "Tecnólogo em Processos Gerenciais"

# Fotos de cada lugar do site (provisórias: fotos reais da Nine até chegarem as imagens corporativas)
FOTOS = {
    "home-hero": ("12", "Turma em sala de aula ouvindo e debatendo com o professor"),
    "home-curso": ("v04-12", "Professora explicando um tema em sala de aula"),
    "home-areas": ("16", "Instrutora apresentando um projeto para a turma"),
    "home-faculdade": ("24", "Turma da Faculdade Nine reunida"),
    "curso": ("25", "Alunos trabalhando juntos em uma atividade prática"),
    "areas": ("16", "Profissional apresentando resultados para a equipe"),
    "faculdade": ("24", "Turma da Faculdade Nine reunida"),
    "transparencia": ("21", "Comunidade acadêmica reunida em um encontro"),
    "ouvidoria": ("23", "Duas alunas conversando e sorrindo"),
    "privacidade": ("11", "Instrutor conduzindo uma atividade com a turma"),
}

# Mapa (OpenStreetMap, sem cookies) e link de rota
LAT, LON = -25.4712556, -49.2929375
MAPA = f"https://www.openstreetmap.org/export/embed.html?bbox={LON-.006:.4f},{LAT-.004:.4f},{LON+.006:.4f},{LAT+.004:.4f}&layer=mapnik&marker={LAT:.5f},{LON:.5f}"
ROTA = "https://www.google.com/maps/search/?api=1&query=Rua+Engenheiro+Niepce+da+Silva+139+Curitiba+PR"

# ---------------------------------------------------------------- dados da matriz (planilha)
ws = openpyxl.load_workbook(sys.argv[1], data_only=True).worksheets[0]
DISC = []
for r in list(ws.iter_rows(values_only=True))[1:]:
    if r[0]:
        DISC.append(dict(nome=str(r[0]).strip().replace("Enfase", "Ênfase"), faz=str(r[1]).strip(), eixo=str(r[2]).strip(),
                         area=str(r[3]).strip(), sem=str(r[4]).strip(), cod=str(r[5]).strip()))
SEMS = collections.OrderedDict()
for d in DISC:
    SEMS.setdefault(d["sem"], []).append(d)
POR_COD = {d["cod"]: d for d in DISC}
N_PI = sum(d["eixo"] == "Projeto Integrador" for d in DISC)

# ---------------------------------------------------------------- peças comuns
def img(key_or_id, alt=None, eager=False, sizes="(min-width: 900px) 50vw, 100vw"):
    if key_or_id in FOTOS:
        key_or_id, alt = FOTOS[key_or_id]
    base = f"/assets/img/galeria/{key_or_id}"
    w, h = Image.open(f"assets/img/galeria/{key_or_id}.webp").size
    srcset = f"{base}-320.webp 320w, {base}-600.webp 600w, {base}.webp {w}w"
    load = ' fetchpriority="high"' if eager else ' loading="lazy"'
    return f'<img src="{base}.webp" srcset="{srcset}" sizes="{sizes}" width="{w}" height="{h}" alt="{alt}"{load} decoding="async">'

DOTS = '<span class="dots" aria-hidden="true">' + "<i></i>" * 21 + "</span>"
WM = lambda pos: f'<span class="wm-crown crown {pos}" aria-hidden="true"></span>'

NAV = [("/curso.html", "O Curso"), ("/areas-de-atuacao.html", "Áreas de atuação"), ("/transparencia.html", "Transparência"),
       ("/a-faculdade.html#onde-estamos", "Contato")]
SUB = [("/a-faculdade.html", "Sobre a Faculdade"), ("/a-faculdade.html#estrutura", "Estrutura organizacional"),
       ("/a-faculdade.html#cpa", "CPA · Comissão Própria de Avaliação"), ("/a-faculdade.html#onde-estamos", "Onde estamos"),
       ("/transparencia.html", "Transparência institucional"), ("/ouvidoria.html", "Ouvidoria"), ("/privacidade.html", "Privacidade e proteção de dados")]

BRAND = '''<span class="crown" aria-hidden="true"></span><span class="brand__name"><b>NINE</b><small>Faculdade</small></span>'''


def header(atual):
    def a(href, txt):
        cur = ' aria-current="page"' if href == atual else ""
        return f'<a href="{href}"{cur}>{txt}</a>'
    sub = "\n".join(f"              <li>{a(h, t)}</li>" for h, t in SUB)
    nav = "\n".join(f"          <li>{a(h, t)}</li>" for h, t in NAV)
    msub = "\n".join(f'          <li><a href="{h}">{t}</a></li>' for h, t in SUB)
    mnav = "\n".join(f'        <li><a href="{h}">{t}</a></li>' for h, t in NAV)
    return f'''  <nav class="a11y-bar" aria-label="Atalhos de acessibilidade">
    <ul>
      <li><a href="#conteudo" accesskey="1">Ir para o conteúdo [1]</a></li>
      <li><a href="#menu-principal" accesskey="2">Ir para o menu [2]</a></li>
      <li><a href="#rodape" accesskey="3">Ir para o rodapé [3]</a></li>
    </ul>
  </nav>
  <noscript><p class="noscript">Algumas funções dependem de JavaScript. Todo o conteúdo do site continua disponível sem ele.</p></noscript>

  <div class="topbar" role="region" aria-label="Acesso rápido">
    <div class="container">
      <p class="topbar__place">Faculdade Nine · Curitiba/PR</p>
      <nav aria-label="Links de acesso rápido">
        <ul>
          <li><a href="/transparencia.html">Transparência</a></li>
          <li><a href="/ouvidoria.html">Ouvidoria</a></li>
          <li><a href="/transparencia.html#emec">e-MEC</a></li>
          <li><a href="mailto:{EMAIL}">{EMAIL}</a></li>
        </ul>
      </nav>
    </div>
  </div>

  <header class="header">
    <div class="container">
      <a class="brand" href="/" aria-label="Faculdade Nine, página inicial">{BRAND}</a>
      <nav class="mainnav" id="menu-principal" aria-label="Principal">
        <ul>
          <li>
            <details class="dd">
              <summary>A Faculdade</summary>
              <ul class="dd__panel">
{sub}
              </ul>
            </details>
          </li>
{nav}
        </ul>
      </nav>
      <a class="btn btn--gold header__cta" href="/curso.html#investimento">Inscrições em breve</a>
      <button class="burger" type="button" aria-expanded="false" aria-controls="menu-mobile" data-menu-toggle>
        <span class="sr-only">Abrir menu</span><span aria-hidden="true"></span><span aria-hidden="true"></span>
      </button>
    </div>
  </header>

  <div class="menu" id="menu-mobile" hidden data-menu>
    <button class="menu__close" type="button" data-menu-toggle><span class="sr-only">Fechar menu</span>×</button>
    <nav aria-label="Menu mobile">
      <ul>
        <li><a href="/">Início</a></li>
        <li><a href="/a-faculdade.html">A Faculdade</a>
          <ul class="menu__sub">
{msub}
          </ul>
        </li>
{mnav}
      </ul>
      <a class="btn btn--gold" href="/curso.html#investimento">Inscrições em breve</a>
    </nav>
  </div>
'''


FOOTER = f'''  <footer class="footer" id="rodape">
    <div class="container footer__cols">
      <div>
        <h2>O Curso</h2>
        <ul>
          <li><a href="/curso.html">{CURSO}</a></li>
          <li><a href="/curso.html#matriz">Matriz curricular</a></li>
          <li><a href="/areas-de-atuacao.html">Áreas de atuação</a></li>
          <li><a href="/curso.html#investimento">Investimento e inscrição</a></li>
        </ul>
      </div>
      <div>
        <h2>A Faculdade</h2>
        <ul>
          <li><a href="/a-faculdade.html">Sobre a Faculdade</a></li>
          <li><a href="/a-faculdade.html#estrutura">Estrutura organizacional</a></li>
          <li><a href="/a-faculdade.html#cpa">CPA</a></li>
          <li><a href="/a-faculdade.html#onde-estamos">Onde estamos</a></li>
        </ul>
      </div>
      <div>
        <h2>Transparência</h2>
        <ul>
          <li><a href="/transparencia.html">Transparência institucional</a></li>
          <li><a href="/ouvidoria.html">Ouvidoria</a></li>
          <li><a href="/privacidade.html">Política de privacidade</a></li>
          <li><a href="https://emec.mec.gov.br/">Consulte o e-MEC</a></li>
        </ul>
      </div>
      <div>
        <h2>Contato</h2>
        <address>
          <ul>
            <li>Secretaria Geral</li>
            <li><a href="mailto:{EMAIL}">{EMAIL}</a></li>
            <li>Telefone <span class="tbc">[A CONFIRMAR]</span></li>
            <li>Rua Engenheiro Niepce da Silva, 139<br>Portão · Curitiba/PR · 80610-240</li>
          </ul>
        </address>
      </div>
    </div>
    <div class="footer__bottom">
      <div class="container">
        <a class="brand" href="/" aria-label="Faculdade Nine, página inicial">{BRAND}</a>
        <p>© <span data-year></span> Faculdade Nine · Mantida pelo Conselho Educacional Nine · CNPJ 61.991.971/0001-35</p>
      </div>
    </div>
  </footer>
'''

ORG = {"@context": "https://schema.org", "@type": "CollegeOrUniversity", "name": "Faculdade Nine", "url": SITE + "/",
       "logo": SITE + "/assets/logo/crown.png", "email": EMAIL,
       "address": {"@type": "PostalAddress", "streetAddress": "Rua Engenheiro Niepce da Silva, 139", "addressLocality": "Curitiba",
                   "addressRegion": "PR", "postalCode": "80610-240", "addressCountry": "BR"},
       "geo": {"@type": "GeoCoordinates", "latitude": LAT, "longitude": LON},
       "parentOrganization": {"@type": "Organization", "name": "Conselho Educacional Nine", "taxID": "61.991.971/0001-35"}}


def page(arq, titulo, desc, corpo, atual, extra_ld=None, robots=None):
    ld = [ORG] + ([extra_ld] if extra_ld else [])
    lds = "\n".join(f'  <script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>' for x in ld)
    rob = f'\n  <meta name="robots" content="{robots}">' if robots else ""
    html = f'''<!doctype html>
<html lang="pt-BR">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{titulo}</title>
  <meta name="description" content="{desc}">{rob}
  <meta property="og:type" content="website">
  <meta property="og:locale" content="pt_BR">
  <meta property="og:title" content="{titulo}">
  <meta property="og:description" content="{desc}">
  <link rel="icon" type="image/png" href="/assets/logo/crown.png">
  <link rel="preload" as="font" type="font/woff2" href="/assets/fonts/inter-tight-latin.woff2" crossorigin>
  <link rel="stylesheet" href="/faculdade.css">
{lds}
  <script src="/base.js" defer></script>
</head>
<body>
{header(atual)}
  <main id="conteudo">
{corpo}
  </main>

{FOOTER}</body>
</html>
'''
    os.makedirs(os.path.dirname(arq) or ".", exist_ok=True)
    open(arq, "w").write(html)


def page_hero(titulo_id, crumb, kicker, titulo, lead, foto, extra=""):
    return f'''    <section class="page-hero" aria-labelledby="{titulo_id}">
      <div class="page-hero__bg">{img(foto, eager=True, sizes="100vw")}</div>
      <div class="container">
        <nav class="crumbs" aria-label="Você está em"><a href="/">Início</a> / <span aria-current="page">{crumb}</span></nav>
        <p class="kicker">{kicker}</p>
        <h1 id="{titulo_id}">{titulo}</h1>
        <p class="lead">{lead}</p>{extra}
      </div>
    </section>
'''


def faq(itens):
    return '<div class="faq">\n' + "\n".join(
        f'          <details><summary>{q}</summary><div><p>{a}</p></div></details>' for q, a in itens) + '\n        </div>'


def facts(rows, cls="facts"):
    return f'<dl class="{cls}">\n' + "\n".join(f'          <div class="fact"><dt>{k}</dt><dd>{v}</dd></div>' for k, v in rows) + '\n        </dl>'


def soon_block(id_="investimento"):
    return f'''    <section class="section is-dark" id="{id_}" aria-labelledby="t-{id_}">
      {WM("u-wm-r")}
      <div class="container soon">
        <div class="head">
          <p class="kicker">Investimento e inscrição</p>
          <h2 id="t-{id_}">Inscrições em breve</h2>
          <p class="lead">Valores, condições de pagamento e o período de inscrição para a primeira turma do curso de {CURSO} serão publicados aqui.</p>
          <div class="btn-row">
            <a class="btn btn--gold" href="mailto:{EMAIL}?subject=Quero%20ser%20avisado%20das%20inscri%C3%A7%C3%B5es">Quero ser avisado</a>
            <a class="btn btn--outline" href="/curso.html#matriz">Ver a matriz curricular</a>
          </div>
        </div>
        <div class="soon__box">
          <p class="label">Investimento</p>
          <p class="soon__value">Em breve</p>
          <p class="soon__status">Inscrições em breve</p>
          <p>Curso presencial em Curitiba · 4 semestres. Formas de pagamento e eventuais bolsas: {TBC}</p>
        </div>
      </div>
    </section>
'''


# ---------------------------------------------------------------- conteúdo: áreas de atuação
AREAS = [
    ("Processos e qualidade", "Mapear como o trabalho acontece, encontrar gargalos e implantar melhorias com indicadores e padrões de qualidade.",
     ["Analista de processos", "Analista da qualidade", "Assistente de melhoria contínua"], ["AN241", "AN342", "QA441", "AN442"]),
    ("Pessoas e liderança", "Organizar rotinas de recrutamento, desenvolvimento e acompanhamento de equipes, e liderar pessoas com clareza.",
     ["Analista de recursos humanos", "Supervisor(a) de equipe", "Coordenador(a) administrativo(a)"], ["LI141", "LI441", "GE142"]),
    ("Finanças e custos", "Acompanhar custos, orçamento e resultados para apoiar decisões financeiras da empresa e de projetos.",
     ["Analista administrativo-financeiro", "Assistente de controladoria", "Analista de custos"], ["GE222", "GE441", "GE241", "FE181"]),
    ("Marketing e comercial", "Planejar ações de mercado, comunicação e relacionamento com clientes a partir de dados.",
     ["Analista de marketing", "Assistente comercial", "Analista de relacionamento com o cliente"], ["GE291", "GE142"]),
    ("Logística e operações", "Planejar compras, estoques, produção e distribuição para que a operação funcione com menos desperdício.",
     ["Analista de logística", "Programador(a) de produção", "Analista de suprimentos"], ["GE491", "AN341", "QA341"]),
    ("Projetos e estratégia", "Transformar objetivos em planos, coordenar projetos e acompanhar se a estratégia está funcionando.",
     ["Analista de planejamento", "Assistente de projetos", "Analista de estratégia"], ["LI391", "GE151", "PI3111", "PI4111"]),
    ("Dados e tecnologia para gestão", "Usar sistemas, painéis e inteligência artificial para medir resultados e apoiar decisões.",
     ["Analista de dados de negócio", "Analista de sistemas de gestão (ERP)", "Assistente de BI"], ["FE191", "FE342", "AN441", "FE441", "FE341"]),
    ("Empreendedorismo", "Abrir, organizar e fazer crescer o próprio negócio, ou apoiar pequenas empresas como consultor(a).",
     ["Empreendedor(a)", "Consultor(a) de gestão", "Gestor(a) de pequenos negócios"], ["GE341", "GE221"]),
]
for _, _, _, cods in AREAS:
    for c in cods:
        assert c in POR_COD, c
PERFIL = ("Analisa e avalia o ambiente interno e externo e formula objetivos e estratégias gerenciais. Planeja, projeta, gerencia e "
          "promove os processos organizacionais e os sistemas da organização. Desenvolve e gerencia processos logísticos, financeiros "
          "e de custos. Otimiza os recursos da organização, por meio de melhorias nos processos. Promove a gestão e governança por "
          "processos e consequentemente o desenvolvimento de sistemas, a gestão do conhecimento, o redesenho e a melhoria. Promove a "
          "mudança organizacional planejada. Vistoria, realiza perícia, avalia, emite laudo e parecer técnico em sua área de formação.")
FONTE = "Catálogo Nacional de Cursos Superiores de Tecnologia (MEC, 2016, p. 48)"
ONDE = [("Empresas em geral", "Indústria, comércio e serviços, de pequenas empresas a grandes grupos."),
        ("Consultoria e projetos", "Empresas de planejamento, desenvolvimento de projetos, assessoramento técnico e consultoria."),
        ("Gestão pública", "Órgãos e instituições públicas que precisam de processos organizados e transparentes."),
        ("Negócio próprio", "Abrir e gerir o próprio empreendimento com método e indicadores."),
        ("Pesquisa e ensino", "Institutos e centros de pesquisa; instituições de ensino, conforme a formação exigida pela legislação.")]

PARA_QUEM = [("Quem terminou o ensino médio", "e quer uma graduação objetiva, em dois anos, que já prepara para o mercado de trabalho."),
             ("Quem já trabalha", "em empresas e quer crescer para funções de coordenação, supervisão e gestão."),
             ("Quem quer empreender", "e precisa de método para organizar, financiar e fazer crescer o próprio negócio."),
             ("Quem quer servir com propósito", "levando boa gestão para empresas, igrejas, organizações e para a sociedade.")]
POR_QUE = [("2 anos", "Graduação tecnológica em 4 semestres, presencial em Curitiba.", "card--navy"),
           (f"{N_PI} projetos integradores", "Você aplica o que aprende em problemas reais de organizações.", "card--gold"),
           ("Dados e IA", "Analytics, sistemas de informação e inteligência artificial aplicada aos negócios.", "card--navy"),
           ("Gestão com propósito", "Teologia com ênfase social e ética na prática da liderança.", "card--gold")]

# ---------------------------------------------------------------- páginas
HOME_LD = None
splits = f'''    <section aria-labelledby="t-split-curso">
      <div class="split split--navy">
        <div class="split__photo">{img("home-curso")}{DOTS}</div>
        <div class="split__body">
          <p class="seal">O curso</p>
          <h2 id="t-split-curso">{CURSO}</h2>
          <p>Uma graduação tecnológica presencial, em 4 semestres, para aprender a organizar, medir e melhorar os processos de qualquer organização.</p>
          <ul class="pills">
            <li><a class="pill" href="/curso.html">Sobre o curso</a></li>
            <li><a class="pill" href="/curso.html#matriz">Matriz curricular</a></li>
            <li><a class="pill" href="/curso.html#para-quem">Para quem é</a></li>
            <li><a class="pill" href="/curso.html#investimento">Investimento</a></li>
          </ul>
        </div>
      </div>
    </section>
    <section aria-labelledby="t-split-areas">
      <div class="split split--gold split--rev">
        <div class="split__photo">{img("home-areas")}{DOTS}</div>
        <div class="split__body">
          <p class="seal">Áreas de atuação</p>
          <h2 id="t-split-areas">Onde o tecnólogo em Processos Gerenciais trabalha</h2>
          <p>Empresas de todos os setores, consultorias, gestão pública e o próprio negócio. Veja as áreas e as funções.</p>
          <ul class="pills">
''' + "\n".join(f'            <li><a class="pill" href="/areas-de-atuacao.html#area-{i+1}">{a[0]}</a></li>' for i, a in enumerate(AREAS[:6])) + f'''
          </ul>
        </div>
      </div>
    </section>
    <section aria-labelledby="t-split-fac">
      <div class="split split--navy">
        <div class="split__photo">{img("home-faculdade")}{DOTS}</div>
        <div class="split__body">
          <p class="seal">A Faculdade</p>
          <h2 id="t-split-fac">Faculdade Nine</h2>
          <p>Instituição de ensino superior em Curitiba, mantida pelo Conselho Educacional Nine.</p>
          <ul class="pills">
            <li><a class="pill" href="/a-faculdade.html">Sobre</a></li>
            <li><a class="pill" href="/a-faculdade.html#estrutura">Estrutura</a></li>
            <li><a class="pill" href="/a-faculdade.html#cpa">CPA</a></li>
            <li><a class="pill" href="/transparencia.html">Transparência</a></li>
            <li><a class="pill" href="/ouvidoria.html">Ouvidoria</a></li>
          </ul>
        </div>
      </div>
    </section>
'''

onde = f'''    <section class="section" id="onde-estamos" aria-labelledby="t-onde">
      <div class="container place">
        <div class="place__info">
          <p class="kicker">Onde estamos</p>
          <h2 id="t-onde">Presencial em Curitiba</h2>
          <address>Rua Engenheiro Niepce da Silva, 139<br>Portão · Curitiba/PR · CEP 80610-240</address>
          <p class="note">Secretaria Geral: <a href="mailto:{EMAIL}">{EMAIL}</a> · Telefone {TBC}</p>
          <p><a class="btn" href="{ROTA}">Como chegar</a></p>
        </div>
        <div class="map"><iframe src="{MAPA}" title="Mapa: Faculdade Nine, Rua Engenheiro Niepce da Silva, 139, Curitiba" loading="lazy"></iframe></div>
      </div>
    </section>
'''

emec = f'''    <section id="emec" aria-labelledby="t-emec">
      <h2 class="sr-only" id="t-emec">Cadastro no e-MEC</h2>
      <div class="emec-band">
        <div>
          <p class="kicker">e-MEC</p>
          <div class="emec-card">
            <span class="emec-qr" aria-hidden="true">QR</span>
            <p><b>Consulte aqui o cadastro da Instituição no Sistema e-MEC.</b><br><span class="tbc">[Selo e QR Code após o credenciamento]</span></p>
          </div>
          <p><a href="https://emec.mec.gov.br/">emec.mec.gov.br</a></p>
        </div>
        <div>
          <p class="kicker">Transparência</p>
          <p class="lead">Documentos institucionais, CPA, Ouvidoria e resultados das avaliações em acesso livre.</p>
          <div class="btn-row"><a class="btn" href="/transparencia.html">Transparência institucional</a><a class="btn btn--outline" href="/ouvidoria.html">Ouvidoria</a></div>
        </div>
      </div>
    </section>
'''

page("index.html", f"Faculdade Nine | {CURSO} presencial em Curitiba",
     f"Faculdade Nine: curso superior de {CURSO}, presencial em Curitiba, em 4 semestres. Matriz curricular, áreas de atuação e inscrições.",
     f'''    <section class="hero" aria-labelledby="t-hero">
      <span class="hero__ring" aria-hidden="true"></span>
      <div class="container">
        <div class="hero__text">
          <p class="hero__badge">Graduação tecnológica · Presencial em Curitiba</p>
          <h1 id="t-hero">Processos <span>Gerenciais</span></h1>
          <p class="lead">Aprenda a organizar, liderar e melhorar empresas por dentro. Curso superior de tecnologia em 4 semestres na Faculdade Nine.</p>
          <div class="btn-row">
            <a class="btn btn--gold" href="/curso.html">Conheça o curso</a>
            <a class="btn btn--outline" href="/curso.html#investimento">Inscrições em breve</a>
          </div>
        </div>
        <div class="hero__media"><div class="hero__img">{img("home-hero", eager=True)}</div>{DOTS}</div>
      </div>
    </section>
    <div class="facts-bar">
      <div class="container">
        <ul>
          <li><b>4 semestres</b><span>cerca de 2 anos</span></li>
          <li><b>{len(DISC)} disciplinas</b><span>com {N_PI} projetos integradores</span></li>
          <li><b>Presencial</b><span>em Curitiba/PR</span></li>
          <li><b>Em breve</b><span>inscrições e valores</span></li>
        </ul>
      </div>
    </div>

    <section class="section" aria-labelledby="t-statement">
      {WM("u-wm-l")}
      <div class="container statement">
        <h2 id="t-statement">Faculdade Nine: formamos gestores com propósito.</h2>
        <div class="prose">
          <p class="lead">Toda organização depende de processos bem feitos: atender, vender, comprar, produzir, contratar, decidir.</p>
          <p>O curso de <strong>{CURSO}</strong> forma profissionais que entendem como uma empresa funciona por dentro e sabem melhorar cada parte dela, com método, dados e ética.</p>
          <p><strong>Para quem quer entrar rápido no mercado, crescer na carreira ou empreender.</strong></p>
        </div>
      </div>
    </section>

{splits}
    <section class="section section--tint" id="para-quem" aria-labelledby="t-paraquem">
      <div class="container">
        <div class="head"><p class="kicker">Para quem é</p><h2 id="t-paraquem">Feito para quem quer fazer a gestão acontecer</h2></div>
        <ul class="grid grid--4">
''' + "\n".join(f'          <li class="card"><span class="card__icon" aria-hidden="true">{i+1}</span><h3>{t}</h3><p>{d}</p></li>' for i, (t, d) in enumerate(PARA_QUEM)) + f'''
        </ul>
      </div>
    </section>

    <section class="section" aria-labelledby="t-porque">
      <div class="container">
        <div class="head"><p class="kicker">Por que fazer</p><h2 id="t-porque">Por que estudar Processos Gerenciais na Nine</h2></div>
        <ul class="grid grid--4">
''' + "\n".join(f'          <li class="card {c}"><h3>{t}</h3><p>{d}</p></li>' for t, d, c in POR_QUE) + f'''
        </ul>
      </div>
    </section>

{soon_block()}
{onde}
{emec}''', "/")

# ---- Curso
disc_html = "\n".join(f'''        <details class="sem"{" open" if s == "1º" else ""}>
          <summary><span>{s} semestre<small>{len(ds)} disciplinas</small></span></summary>
          <ul class="disc">
''' + "\n".join(f'''            <li><h3>{d["nome"]}</h3><p class="disc__meta"><span>{d["cod"]}</span><span>{d["eixo"]}</span><span>Carga horária {TBC}</span></p><p class="disc__do"><b>O que você fará a partir daqui</b>{d["faz"]}</p></li>''' for d in ds) + '''
          </ul>
        </details>''' for s, ds in SEMS.items())

JORNADA = [("Base de gestão", "Ferramentas, fundamentos de estratégia, comunicação e pessoas para entender como uma organização funciona."),
           ("Gestão na prática", "Marketing, economia, contabilidade, direito e modelagem de processos para decidir com critério."),
           ("Projetos e inovação", "Projeto Integrador I, gestão de projetos, inovação, estatística e tecnologias digitais."),
           ("Liderança e resultados", "Projeto Integrador II, logística, qualidade, finanças, analytics, IA e liderança 4.0.")]
CURSO_LD = {"@context": "https://schema.org", "@type": "Course", "name": f"Curso Superior de {CURSO}",
            "description": "Graduação tecnológica presencial em 4 semestres, eixo Gestão e Negócios.", "inLanguage": "pt-BR",
            "provider": {"@type": "CollegeOrUniversity", "name": "Faculdade Nine", "url": SITE + "/"},
            "educationalCredentialAwarded": f"{CURSO}",
            "hasCourseInstance": {"@type": "CourseInstance", "courseMode": "Onsite", "location": {"@type": "Place", "name": "Faculdade Nine",
                                  "address": ORG["address"]}}}
page("curso.html", f"{CURSO} | Faculdade Nine",
     f"Curso superior de {CURSO}, presencial em Curitiba: 4 semestres, {len(DISC)} disciplinas, o que você fará em cada uma, áreas de atuação e inscrições.",
     page_hero("t-curso", "O Curso", "Graduação tecnológica · Eixo Gestão e Negócios", CURSO,
               "Aprenda a organizar, medir e melhorar os processos de uma organização: pessoas, finanças, marketing, logística, qualidade e dados.",
               "curso", '''
        <ul class="chips"><li><b>Presencial</b> Curitiba/PR</li><li><b>4 semestres</b> cerca de 2 anos</li><li><b>Tecnólogo</b> curso de graduação</li></ul>''') + f'''
    <section class="section" aria-labelledby="t-sobre">
      <div class="container course-layout">
        <div class="prose">
          <p class="kicker">Sobre o curso</p>
          <h2 id="t-sobre">O que é o curso de {CURSO}</h2>
          <p class="lead">É uma graduação tecnológica (curso superior de tecnologia) focada em como as organizações funcionam e em como fazê-las funcionar melhor.</p>
          <p>Ao longo de 4 semestres você estuda estratégia, processos, pessoas, finanças, marketing, logística, qualidade, projetos e tecnologia, sempre ligando teoria à prática em {N_PI} projetos integradores. O tecnólogo é um profissional de nível superior e pode seguir para pós-graduação.</p>
          <blockquote class="quote"><p>{PERFIL}</p><cite>Perfil profissional do tecnólogo em Processos Gerenciais · {FONTE}</cite></blockquote>
          <p><a class="btn" href="/areas-de-atuacao.html">Ver as áreas de atuação</a></p>
        </div>
        <div class="aside-box" role="region" aria-labelledby="t-box">
          <h2 id="t-box">Informações do curso</h2>
          <dl>
            <div><dt>Modalidade</dt><dd>Presencial</dd></div>
            <div><dt>Local</dt><dd>Curitiba/PR</dd></div>
            <div><dt>Duração</dt><dd>4 semestres</dd></div>
            <div><dt>Grau</dt><dd>Tecnólogo</dd></div>
            <div><dt>Investimento</dt><dd>Em breve</dd></div>
            <div><dt>Inscrições</dt><dd>Em breve</dd></div>
            <div><dt>Ato autorizativo</dt><dd>{TBC}</dd></div>
          </dl>
          <a class="btn btn--gold" href="#investimento">Inscrições em breve</a>
          <a class="btn btn--outline" href="mailto:{EMAIL}?subject=Quero%20ser%20avisado%20das%20inscri%C3%A7%C3%B5es">Quero ser avisado</a>
        </div>
      </div>
    </section>

    <section class="section section--tint" id="para-quem" aria-labelledby="t-paraquem">
      <div class="container">
        <div class="head"><p class="kicker">Para quem é</p><h2 id="t-paraquem">Para quem é este curso</h2></div>
        <ul class="grid grid--4">
''' + "\n".join(f'          <li class="card"><span class="card__icon" aria-hidden="true">{i+1}</span><h3>{t}</h3><p>{d}</p></li>' for i, (t, d) in enumerate(PARA_QUEM)) + f'''
        </ul>
      </div>
    </section>

    <section class="section" id="matriz" aria-labelledby="t-matriz">
      {WM("u-wm-r")}
      <div class="container">
        <div class="head">
          <p class="kicker">Matriz curricular</p>
          <h2 id="t-matriz">Conheça a matriz curricular</h2>
          <p class="lead">{len(DISC)} disciplinas em {len(SEMS)} semestres. Em cada uma, veja o que você passa a fazer a partir dali.</p>
          <p class="note">Última atualização: {HOJE}. A carga horária por disciplina será publicada com o Projeto Pedagógico do Curso (PPC).</p>
        </div>
{disc_html}
      </div>
    </section>

    <section class="section is-dark" aria-labelledby="t-jornada">
      <div class="container">
        <div class="head"><p class="kicker">Sua jornada</p><h2 id="t-jornada">Como será a sua jornada no curso</h2></div>
        <ol class="steps">
''' + "\n".join(f'          <li><b aria-hidden="true">{i+1}</b><h3>{i+1}º semestre · {t}</h3><p>{d}</p></li>' for i, (t, d) in enumerate(JORNADA)) + f'''
        </ol>
      </div>
    </section>

    <section class="section" aria-labelledby="t-mercado">
      <div class="container">
        <div class="head"><p class="kicker">Mercado de trabalho</p><h2 id="t-mercado">Onde você pode atuar</h2>
          <p class="lead">Empresas de todos os setores precisam de gente que organize processos, pessoas e resultados.</p></div>
        <ul class="grid grid--4">
''' + "\n".join(f'          <li class="card"><h3>{a[0]}</h3><p>{a[1]}</p></li>' for a in AREAS[:4]) + f'''
        </ul>
        <p class="btn-row"><a class="btn" href="/areas-de-atuacao.html">Ver todas as áreas e funções</a></p>
      </div>
    </section>

    <section class="section section--tint" aria-labelledby="t-porque">
      <div class="container">
        <div class="head"><p class="kicker">Por que fazer</p><h2 id="t-porque">Por que fazer este curso</h2></div>
        <ul class="grid grid--4">
''' + "\n".join(f'          <li class="card {c}"><h3>{t}</h3><p>{d}</p></li>' for t, d, c in POR_QUE) + f'''
        </ul>
      </div>
    </section>

    <section class="section" id="ingresso" aria-labelledby="t-ingresso">
      <div class="container course-layout">
        <div class="prose">
          <p class="kicker">Forma de ingresso</p>
          <h2 id="t-ingresso">Sem vestibular</h2>
          <p class="lead">Para ingressar no curso é preciso ter concluído o ensino médio e fazer a inscrição quando o período for aberto.</p>
          <p>Documentos, datas e etapas do ingresso: {TBC}</p>
        </div>
        <div>
          <h2 class="kicker">Perguntas frequentes</h2>
          {faq([("Quanto tempo dura o curso?", "São 4 semestres, cerca de 2 anos."),
                ("O curso é presencial? Onde?", "Sim. As aulas são presenciais na Faculdade Nine, na Rua Engenheiro Niepce da Silva, 139, Portão, Curitiba/PR."),
                ("O tecnólogo é um curso superior?", "Sim. O curso superior de tecnologia é um curso de graduação. Depois dele, você pode fazer pós-graduação."),
                ("Qual é o valor e quando abrem as inscrições?", "Valores e período de inscrição serão divulgados em breve nesta página."),
                ("Em quais dias e horários são as aulas?", "[A CONFIRMAR]")])}
        </div>
      </div>
    </section>

{soon_block()}''', "/curso.html", CURSO_LD)

# ---- Áreas de atuação
areas_html = "\n".join(f'''          <li class="card" id="area-{i+1}">
            <span class="card__icon" aria-hidden="true">{i+1:02d}</span>
            <h3>{t}</h3>
            <p>{d}</p>
            <p class="disc__do"><b>Funções</b>{" · ".join(f)}</p>
            <p class="disc__do"><b>Disciplinas do curso</b>{" · ".join(POR_COD[c]["nome"] for c in cods)}</p>
          </li>''' for i, (t, d, f, cods) in enumerate(AREAS))
page("areas-de-atuacao.html", f"Áreas de atuação do tecnólogo em Processos Gerenciais | Faculdade Nine",
     "Onde trabalha e o que faz o tecnólogo em Processos Gerenciais: áreas, funções, ocupações na CBO e registro profissional.",
     page_hero("t-areas", "Áreas de atuação", "Carreira", "Áreas de atuação do tecnólogo em Processos Gerenciais",
               "Toda organização tem processos para organizar e melhorar. Veja onde este profissional trabalha, o que faz e quais disciplinas do curso preparam para cada área.",
               "areas") + f'''
    <section class="section" aria-labelledby="t-faz">
      <div class="container course-layout">
        <div class="prose">
          <p class="kicker">O que faz</p>
          <h2 id="t-faz">O que faz um tecnólogo em Processos Gerenciais</h2>
          <p class="lead">É o profissional que entende como a empresa funciona por dentro e sabe planejar, executar e melhorar seus processos.</p>
          <blockquote class="quote"><p>{PERFIL}</p><cite>{FONTE}</cite></blockquote>
        </div>
        <div class="aside-box" role="region" aria-labelledby="t-cbo">
          <h2 id="t-cbo">Ocupações e registro</h2>
          <dl>
            <div><dt>Tecnólogo em gestão administrativo-financeira</dt><dd>CBO 1421-20</dd></div>
            <div><dt>Analista administrativo</dt><dd>CBO 2521-05</dd></div>
          </dl>
          <p class="note">O tecnólogo em Processos Gerenciais pode obter registro profissional no Conselho Regional de Administração (CRA).</p>
          <a class="btn btn--gold" href="/curso.html">Conheça o curso</a>
        </div>
      </div>
    </section>

    <section class="section section--tint" aria-labelledby="t-lista">
      {WM("u-wm-r")}
      <div class="container">
        <div class="head"><p class="kicker">Áreas</p><h2 id="t-lista">Em quais áreas você pode trabalhar</h2>
          <p class="lead">Cada área abaixo mostra exemplos de funções e as disciplinas do curso que preparam você para ela.</p></div>
        <ul class="grid grid--2">
{areas_html}
        </ul>
      </div>
    </section>

    <section class="section is-dark" aria-labelledby="t-onde-trab">
      <div class="container">
        <div class="head"><p class="kicker">Onde trabalhar</p><h2 id="t-onde-trab">Onde o tecnólogo em Processos Gerenciais trabalha</h2></div>
        <ul class="steps">
''' + "\n".join(f'          <li><b aria-hidden="true">{i+1}</b><h3>{t}</h3><p>{d}</p></li>' for i, (t, d) in enumerate(ONDE[:4])) + f'''
        </ul>
        <p class="note">Também: {ONDE[4][1]} Fonte: {FONTE}.</p>
      </div>
    </section>

{soon_block()}''', "/areas-de-atuacao.html")

# ---- A Faculdade
page("a-faculdade.html", "A Faculdade | Faculdade Nine",
     "Faculdade Nine: instituição de ensino superior em Curitiba mantida pelo Conselho Educacional Nine. Dados institucionais, estrutura organizacional, CPA e localização.",
     page_hero("t-fac", "A Faculdade", "Faculdade Nine", "Formar gestores com propósito para todas as áreas da sociedade.",
               "Instituição de ensino superior em Curitiba, mantida pelo Conselho Educacional Nine.", "faculdade") + f'''
    <section class="section" aria-labelledby="t-quem">
      {WM("u-wm-l")}
      <div class="container statement">
        <h2 id="t-quem">Quem somos</h2>
        <div class="prose">
          <p class="lead">A Faculdade Nine nasce da experiência da Nine Academia de Influência na formação de jovens.</p>
          <p>Acreditamos que todo jovem precisa descobrir seu propósito no início da vida adulta, e que boa gestão é uma forma concreta de servir: nas empresas, na gestão pública, nas organizações e no próprio negócio.</p>
          <p>Missão, visão e valores: {TBC} (conforme o Plano de Desenvolvimento Institucional).</p>
        </div>
      </div>
    </section>

    <section class="section is-dark" aria-labelledby="t-dados">
      <div class="container">
        <div class="head"><p class="kicker">Dados institucionais</p><h2 id="t-dados">Faculdade Nine</h2></div>
        {facts([("Instituição", "Faculdade Nine"), ("Mantenedora", "Conselho Educacional Nine"), ("CNPJ da mantenedora", "61.991.971/0001-35"),
                ("Endereço", ENDERECO), ("Direção-Geral", "Raul Cesar Sindlinger"), ("Código e-MEC", TBC), ("Ato de credenciamento", TBC)])}
      </div>
    </section>

    <section class="section" id="estrutura" aria-labelledby="t-estr">
      <div class="container">
        <div class="head"><p class="kicker">Estrutura organizacional</p><h2 id="t-estr">Gestão e órgãos colegiados</h2></div>
        <ul class="grid grid--3">
          <li class="card card--navy"><h3>Direção-Geral</h3><p>Raul Cesar Sindlinger, Diretor-Geral. A Ouvidoria é vinculada diretamente à Direção-Geral.</p></li>
          <li class="card"><h3>Conselho Superior (CONSUP)</h3><p>Órgão colegiado superior da Faculdade. Composição: {TBC}</p></li>
          <li class="card" id="cpa"><h3>Comissão Própria de Avaliação (CPA)</h3><p>Conduz a autoavaliação institucional (Lei nº 10.861/2004) e publica seus resultados em <a href="/transparencia.html">Transparência</a>. Composição: {TBC}</p></li>
          <li class="card"><h3>Coordenação do Curso</h3><p>{CURSO}. Coordenador(a): {TBC}</p></li>
          <li class="card"><h3>Secretaria Geral</h3><p>Atendimento acadêmico: <a href="mailto:{EMAIL}">{EMAIL}</a> · Telefone {TBC}</p></li>
          <li class="card card--gold"><h3>Ouvidoria</h3><p>Canal para reclamações, denúncias, sugestões, elogios e pedidos de informação. <a href="/ouvidoria.html">Acessar a Ouvidoria</a></p></li>
        </ul>
      </div>
    </section>

{onde}''', "/a-faculdade.html")

# ---- Transparência (documentos do art. 26 do Regulamento)
DOCS = [
    ("pdi", "Plano de Desenvolvimento Institucional (PDI)", "Planejamento da Faculdade para o período vigente.", "a-publicar", None, None),
    ("ppi", "Projeto Pedagógico Institucional (PPI)", "Quando constituir documento próprio.", "a-publicar", None, None),
    ("regimento", "Regimento Interno", "Normas de organização e funcionamento da Faculdade.", "a-publicar", None, None),
    ("regulamento-ouvidoria", "Regulamento da Ouvidoria e da Comunicação Institucional", "Canais, prazos e regras de transparência e de comunicação.", "em-aprovacao", None, "/ouvidoria.html"),
    ("ppc", "Projeto Pedagógico do Curso (PPC)", f"Projeto pedagógico do curso de {CURSO}.", "a-publicar", None, None),
    ("matriz", "Matriz curricular", f"Disciplinas do curso de {CURSO} por semestre.", "publicado", HOJE, "/curso.html#matriz"),
    ("calendario", "Calendário acadêmico", "Datas do período letivo.", "a-publicar", None, None),
    ("atos", "Atos regulatórios", "Credenciamento da Instituição e autorização, reconhecimento e renovação de reconhecimento do curso, quando houver.", "a-publicar", None, None),
    ("consup-cpa", "Composição do CONSUP e da CPA", "Membros do Conselho Superior e da Comissão Própria de Avaliação.", "a-publicar", None, None),
    ("ouvidoria-relatorios", "Relatórios da Ouvidoria (síntese)", "Publicada em até 30 dias após a apreciação pelo CONSUP, sem dados pessoais.", "sem-registro", None, None),
    ("avaliacoes", "Resultados das avaliações interna e externa", "Relatório da CPA com resumo executivo e resultados do INEP/MEC.", "sem-registro", None, None),
    ("privacidade", "Política de privacidade e proteção de dados pessoais", "Como a Faculdade trata dados pessoais (Lei nº 13.709/2018).", "a-publicar", None, "/privacidade.html"),
]
ST = {"publicado": "Publicado", "em-aprovacao": "Em aprovação no CONSUP", "a-publicar": "Em elaboração", "sem-registro": "Nenhum publicado até o momento"}
docs_html = "\n".join(f'''          <li class="doc" data-doc="{slug}">
            <div class="doc__main"><h3>{f'<a href="{href}">{t}</a>' if href else t}</h3><p>{d}</p></div>
            <p class="status status--{st}">{ST[st]}</p>
            <p class="doc__date">Última atualização: {data or "—"}</p>
          </li>''' for slug, t, d, st, data, href in DOCS)
page("transparencia.html", "Transparência Institucional | Faculdade Nine",
     "Documentos institucionais, atos regulatórios, CPA, relatórios da Ouvidoria e resultados das avaliações da Faculdade Nine, em acesso livre.",
     page_hero("t-transp", "Transparência Institucional", "Acesso livre, sem cadastro", "Transparência Institucional",
               "Documentos e informações institucionais da Faculdade Nine, em formato pesquisável e mantidos atualizados, conforme o Regulamento da Ouvidoria e da Comunicação Institucional.",
               "transparencia") + f'''
    <section class="section" aria-labelledby="t-docs">
      <div class="container">
        <div class="head"><p class="kicker">Documentos</p><h2 id="t-docs">Documentos institucionais</h2></div>
        <ul class="docs">
{docs_html}
        </ul>
        <p class="note">A área é revisada ao menos uma vez por período letivo. Os setores responsáveis encaminham cada documento em até 10 dias úteis após sua aprovação ou alteração. Não são publicados dados pessoais nem informações protegidas por sigilo legal.</p>
      </div>
    </section>
{emec}''', "/transparencia.html")

# ---- Ouvidoria
page("ouvidoria.html", "Ouvidoria | Faculdade Nine",
     "Ouvidoria da Faculdade Nine: reclamações, denúncias, sugestões, elogios e pedidos de informação, com sigilo e prazos definidos.",
     page_hero("t-ouv", "Ouvidoria", "Canal institucional", "Ouvidoria",
               "Canal de comunicação entre a Faculdade Nine e as comunidades acadêmica e externa para receber, registrar, encaminhar e responder manifestações.",
               "ouvidoria") + f'''
    <section class="section" aria-labelledby="t-quem-pode">
      <div class="container statement">
        <h2 id="t-quem-pode">Quem pode se manifestar</h2>
        <div class="prose">
          <p class="lead">Estudantes, docentes, técnicos-administrativos, egressos, candidatos, pais ou responsáveis e demais membros da comunidade externa.</p>
          <p>A Ouvidoria é vinculada diretamente à Direção-Geral. Ela não substitui os requerimentos da Secretaria Geral: procure-a quando não obtiver resposta ou atendimento adequado pelos canais ordinários.</p>
        </div>
      </div>
    </section>

    <section class="section section--tint" aria-labelledby="t-tipos">
      <div class="container">
        <div class="head"><p class="kicker">Manifestações</p><h2 id="t-tipos">Tipos de manifestação</h2></div>
        <ul class="grid grid--3">
          <li class="card"><h3>Reclamação</h3><p>Insatisfação com serviço, atendimento ou conduta.</p></li>
          <li class="card"><h3>Denúncia</h3><p>Comunicação de irregularidade ou de ato ilícito, inclusive assédio e discriminação.</p></li>
          <li class="card"><h3>Sugestão</h3><p>Proposta de melhoria.</p></li>
          <li class="card"><h3>Elogio</h3><p>Reconhecimento de serviço, atendimento ou conduta.</p></li>
          <li class="card"><h3>Solicitação de informação</h3><p>Pedido de esclarecimento não atendido pelos canais ordinários.</p></li>
          <li class="card card--navy"><h3>Sigilo garantido</h3><p>Sua identidade é preservada e é vedada qualquer retaliação a quem se manifesta de boa-fé.</p></li>
        </ul>
      </div>
    </section>

    <section class="section is-dark" aria-labelledby="t-prazos">
      <div class="container">
        <div class="head"><p class="kicker">Prazos</p><h2 id="t-prazos">Prazos de atendimento</h2></div>
        <ol class="timeline">
          <li><b>Registro</b><p>O sistema gera um número de protocolo e envia a confirmação, com cópia da manifestação, para o seu e-mail.</p></li>
          <li><b>Até 5 dias úteis</b><p>A Direção-Geral analisa a manifestação e a encaminha ao setor competente, ou a trata diretamente.</p></li>
          <li><b>Até 10 dias úteis</b><p>O setor responde à Ouvidoria com as providências adotadas.</p></li>
          <li><b>Até 20 dias úteis</b><p>Você recebe a resposta conclusiva por e-mail. O prazo pode ser prorrogado uma vez, por igual período, com justificativa.</p></li>
        </ol>
      </div>
    </section>

    <section class="section" aria-labelledby="t-sigilo">
      <div class="container statement">
        <h2 id="t-sigilo">Sigilo e proteção de dados</h2>
        <div class="prose">
          <p>Sua identidade e o conteúdo da manifestação são mantidos em sigilo. No encaminhamento ao setor, a identidade é omitida, salvo quando indispensável e com a sua autorização, e você pode pedir que ela não seja revelada em nenhuma hipótese.</p>
          <p>Os dados pessoais são tratados conforme a Lei nº 13.709/2018 (LGPD), apenas para registro, resposta e relatórios. Relatórios semestrais, sem identificação dos manifestantes, são publicados em <a href="/transparencia.html">Transparência Institucional</a>.</p>
        </div>
      </div>
    </section>

    <section class="section is-dark" id="manifestacao" aria-labelledby="t-form">
      <div class="container course-layout">
        <form class="form" data-ouvidoria novalidate>
          <fieldset>
            <legend>Identificação</legend>
            <div class="field"><label for="o-nome">Nome</label><input id="o-nome" name="nome" type="text" autocomplete="name" required></div>
            <div class="field"><label for="o-email">E-mail</label><input id="o-email" name="email" type="email" autocomplete="email" required></div>
            <div class="field field--full"><label for="o-vinculo">Vínculo com a Instituição</label>
              <select id="o-vinculo" name="vinculo" required><option value="" selected disabled>Selecione</option><option>Estudante</option><option>Docente</option><option>Técnico-administrativo</option><option>Egresso</option><option>Candidato</option><option>Pai, mãe ou responsável</option><option>Comunidade externa</option></select></div>
          </fieldset>
          <fieldset>
            <legend>Manifestação</legend>
            <div class="field field--full"><label for="o-tipo">Tipo de manifestação</label>
              <select id="o-tipo" name="tipo" required><option value="" selected disabled>Selecione</option><option>Reclamação</option><option>Denúncia</option><option>Sugestão</option><option>Elogio</option><option>Solicitação de informação</option></select></div>
            <div class="field field--full"><label for="o-descricao">Descrição dos fatos</label><textarea id="o-descricao" name="descricao" rows="6" required></textarea></div>
            <div class="field field--full"><label for="o-anexos">Anexos <span class="opt">(opcional)</span></label><input id="o-anexos" name="anexos" type="file" multiple></div>
          </fieldset>
          <div class="field field--hp" aria-hidden="true"><label for="o-website">Website</label><input id="o-website" name="website" type="text" autocomplete="off"></div>
          <div class="field field--check"><input id="o-sigilo" name="sigilo_total" type="checkbox"><label for="o-sigilo">Não quero que minha identidade seja revelada em nenhuma hipótese.</label></div>
          <div class="field field--check"><input id="o-lgpd" name="consentimento" type="checkbox" required><label for="o-lgpd">Concordo com o tratamento dos meus dados para o registro e a resposta desta manifestação, conforme a <a href="/privacidade.html">Política de privacidade</a>.</label></div>
          <div><button class="btn btn--gold" type="submit">Enviar manifestação</button><p class="form__status" data-status role="status" aria-live="polite"></p></div>
        </form>
        <div class="prose">
          <h2 id="t-form">Registre sua manifestação</h2>
          <p>Acesso livre, sem cadastro. Se preferir, escreva para <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
        </div>
      </div>
    </section>''', "/ouvidoria.html")

# ---- Privacidade
page("privacidade.html", "Política de privacidade | Faculdade Nine",
     "Política de privacidade e proteção de dados pessoais da Faculdade Nine (LGPD).",
     page_hero("t-priv", "Política de privacidade", "Lei nº 13.709/2018 (LGPD)", "Política de privacidade",
               "Como a Faculdade Nine trata os dados pessoais de candidatos, estudantes, colaboradores e visitantes.", "privacidade") + f'''
    <section class="section" aria-labelledby="t-priv-st">
      <div class="container statement">
        <h2 id="t-priv-st">Situação</h2>
        <div class="prose">
          <p class="lead">O texto completo da política está em elaboração e será publicado nesta página. {TBC}</p>
          {facts([("Controlador", "Conselho Educacional Nine · CNPJ 61.991.971/0001-35"), ("Endereço", ENDERECO),
                  ("Contato para assuntos de dados pessoais", f'<a href="mailto:{EMAIL}">{EMAIL}</a>'), ("Encarregado (DPO)", TBC)])}
          <p class="note">Enquanto isso, os dados enviados pelos formulários do site são usados apenas para a finalidade informada em cada um.</p>
        </div>
      </div>
    </section>''', "/privacidade.html")

# ---------------------------------------------------------------- pós-processamento das páginas (Faculdade + Academia)
def minifica(css):
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    css = re.sub(r"\s+", " ", css)
    css = re.sub(r"\s*([{};,>])\s*", r"\1", css)
    css = re.sub(r":\s+", ":", css)  # só depois do ":" (antes dele o espaço muda o seletor)
    return css.replace(";}", "}").strip()

CSS = {"faculdade": minifica(open("faculdade.css").read()), "academia": minifica(open("style.css").read())}
for arq in glob.glob("*.html") + glob.glob("academia/*.html"):
    t = open(arq).read()
    css = CSS["academia" if arq.startswith("academia/") else "faculdade"]
    t = re.sub(r'<link rel="stylesheet" href="/?(?:faculdade|style)\.css">|<style id="css">.*?</style>',
               lambda m: f'<style id="css">{css}</style>', t, count=1, flags=re.S)
    assert ' style="' not in t, arq
    open(arq, "w").write(t)

# sitemap e robots
urls = ["/", "/curso.html", "/areas-de-atuacao.html", "/a-faculdade.html", "/transparencia.html", "/ouvidoria.html", "/privacidade.html", "/academia/"]
open("sitemap.xml", "w").write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
                               + "".join(f"  <url><loc>{SITE}{u}</loc></url>\n" for u in urls) + "</urlset>\n")
open("robots.txt", "w").write(f"User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n")
print("ok:", len(DISC), "disciplinas,", len(SEMS), "semestres; CSS faculdade", len(CSS["faculdade"]) // 1024, "KB")
