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

def page_hero(titulo_id, crumb, titulo, lead, foto):
    return f'''    <section class="page-hero" aria-labelledby="{titulo_id}">
      <div class="page-hero__bg">{img(foto, eager=True, sizes="100vw")}</div>
      {wm("nine p-br", "dots p-tr")}
      <div class="container">
        <nav class="crumbs" aria-label="Você está em"><a href="/">Início</a> / <span aria-current="page">{crumb}</span></nav>
        <h1 id="{titulo_id}">{titulo}</h1>
        <p class="lead">{lead}</p>
      </div>
    </section>
'''


def wm(*marcas):
    """Marcas d'água decorativas: 'crown', 'nine' ou 'dots' + posição (p-tl, p-tr, p-bl, p-br, p-ml, p-mr)."""
    return "".join(f'<span class="wm wm--{m.split()[0]} {m.split()[1]}" aria-hidden="true"></span>' for m in marcas)


def head(id_, titulo, lead=None, centro=False):
    l = f'\n          <p class="lead">{lead}</p>' if lead else ""
    return f'''        <div class="head{' head--center' if centro else ''}">
          <h2 id="{id_}">{titulo}</h2>{l}
        </div>'''


def faq(itens):
    return '<div class="faq">\n' + "\n".join(
        f'          <details><summary>{q}</summary><div><p>{a}</p></div></details>' for q, a in itens) + '\n        </div>'


def facts(rows, cls="facts"):
    return f'<dl class="{cls}">\n' + "\n".join(f'          <div class="fact"><dt>{k}</dt><dd>{v}</dd></div>' for k, v in rows) + '\n        </dl>'


AVISE = f"mailto:{EMAIL}?subject=Quero%20ser%20avisado%20das%20inscri%C3%A7%C3%B5es"


def investimento():
    return f'''    <section class="section is-dark" id="investimento" aria-labelledby="t-investimento">
      {wm("crown p-tr", "dots p-bl")}
      <div class="container soon">
{head("t-investimento", "Investimento e inscrições", "Valores e período de inscrição da primeira turma serão divulgados nesta página.")}
        <div class="soon__box">
          <dl>
            <div><dt>Investimento</dt><dd>Em breve</dd></div>
            <div><dt>Inscrições</dt><dd>Em breve</dd></div>
            <div><dt>Bolsas e parcelamento</dt><dd>{TBC}</dd></div>
          </dl>
          <a class="btn btn--gold" href="{AVISE}">Quero ser avisado</a>
        </div>
      </div>
    </section>
'''


def split(id_, cor, foto, selo, titulo, texto, links, rev=False):
    pills = "\n".join(f'            <li><a class="pill" href="{h}">{t}</a></li>' for h, t in links)
    return f'''    <section aria-labelledby="{id_}">
      <div class="split split--{cor}{' split--rev' if rev else ''}">
        <div class="split__photo">{img(foto)}{DOTS}</div>
        <div class="split__body">
          {wm("nine p-br")}
          <p class="seal">{selo}</p>
          <h2 id="{id_}">{titulo}</h2>
          <p>{texto}</p>
          <ul class="pills">
{pills}
          </ul>
        </div>
      </div>
    </section>
'''


ONDE_ESTAMOS = f'''    <section class="section" id="onde-estamos" aria-labelledby="t-onde">
      {wm("crown p-bl")}
      <div class="container place">
        <div class="place__info">
          <h2 id="t-onde">Onde estamos</h2>
          <address>Rua Engenheiro Niepce da Silva, 139<br>Portão · Curitiba/PR · CEP 80610-240</address>
          <p class="note">Secretaria Geral: <a href="mailto:{EMAIL}">{EMAIL}</a> · Telefone {TBC}</p>
          <p><a class="btn" href="{ROTA}">Como chegar</a></p>
        </div>
        <div class="map"><iframe src="{MAPA}" title="Mapa: Faculdade Nine, Rua Engenheiro Niepce da Silva, 139, Curitiba" loading="lazy"></iframe></div>
      </div>
    </section>
'''

EMEC = f'''    <section id="emec" aria-labelledby="t-emec">
      <h2 class="sr-only" id="t-emec">Cadastro no e-MEC e transparência</h2>
      <div class="emec-band">
        <div>
          <div class="emec-card">
            <span class="emec-qr" aria-hidden="true">QR</span>
            <p><b>Consulte o cadastro da Instituição no e-MEC</b><br><span class="tbc">[Selo e QR Code após o credenciamento]</span></p>
          </div>
          <p><a href="https://emec.mec.gov.br/">emec.mec.gov.br</a></p>
        </div>
        <div>
          <p class="lead">Documentos institucionais, CPA e Ouvidoria</p>
          <div class="btn-row"><a class="btn" href="/transparencia.html">Transparência</a><a class="btn btn--outline" href="/ouvidoria.html">Ouvidoria</a></div>
        </div>
      </div>
    </section>
'''

PARA_QUEM = [("Acabou o ensino médio", "e quer uma graduação curta que já leva para o mercado."),
             ("Já trabalha em empresa", "e quer assumir funções de coordenação e gestão."),
             ("Quer empreender", "e precisa organizar as finanças, as vendas e a equipe do próprio negócio."),
             ("Atua em igrejas, ONGs ou projetos sociais", "e quer gerir com método o que já faz.")]

# ---------------------------------------------------------------- Início
page("index.html", f"Faculdade Nine | {CURSO} presencial em Curitiba",
     f"Faculdade Nine: curso superior de {CURSO}, presencial em Curitiba, em 4 semestres. Matriz curricular, áreas de atuação e inscrições.",
     f'''    <section class="hero" aria-labelledby="t-hero">
      <span class="hero__ring" aria-hidden="true"></span>
      {wm("dots p-bl", "crown p-tl")}
      <div class="container">
        <div class="hero__text">
          <h1 id="t-hero">Processos <span>Gerenciais</span></h1>
          <p class="lead">Curso superior de tecnologia da Faculdade Nine, presencial em Curitiba.</p>
          <div class="btn-row">
            <a class="btn btn--gold" href="/curso.html">Conheça o curso</a>
            <a class="btn btn--outline" href="/areas-de-atuacao.html">Áreas de atuação</a>
          </div>
        </div>
        <div class="hero__media"><div class="hero__img">{img("home-hero", eager=True)}</div></div>
      </div>
    </section>
    <div class="facts-bar">
      <div class="container">
        <ul>
          <li><b>4 semestres</b><span>cerca de 2 anos</span></li>
          <li><b>{len(DISC)} disciplinas</b><span>e {N_PI} projetos integradores</span></li>
          <li><b>Presencial</b><span>Portão, Curitiba/PR</span></li>
          <li><b>Inscrições</b><span>em breve</span></li>
        </ul>
      </div>
    </div>

    <section class="section" aria-labelledby="t-statement">
      {wm("crown p-bl", "nine p-tr")}
      <div class="container statement">
        <h2 id="t-statement">Por que Processos Gerenciais</h2>
        <div class="prose">
          <p class="lead">Toda empresa depende de processos: atender, vender, comprar, contratar, entregar.</p>
          <p>No curso de <strong>{CURSO}</strong> você aprende a organizar esse trabalho, liderar a equipe e decidir com base em dados.</p>
        </div>
      </div>
    </section>

{split("t-split-curso", "navy", "home-curso", "O curso", CURSO,
       "Graduação tecnológica presencial, em 4 semestres.",
       [("/curso.html", "Sobre o curso"), ("/curso.html#matriz", "Matriz curricular"), ("/curso.html#para-quem", "Para quem é"), ("/curso.html#investimento", "Investimento")])}
{split("t-split-areas", "gold", "home-areas", "Carreira", "Áreas de atuação",
       "Onde trabalha e o que faz o tecnólogo em Processos Gerenciais.",
       [(f"/areas-de-atuacao.html#area-{i+1}", a[0]) for i, a in enumerate(AREAS[:6])], rev=True)}
{split("t-split-fac", "navy", "home-faculdade", "A Faculdade", "Faculdade Nine",
       "Mantida pelo Conselho Educacional Nine, em Curitiba.",
       [("/a-faculdade.html", "Sobre"), ("/a-faculdade.html#estrutura", "Estrutura"), ("/a-faculdade.html#cpa", "CPA"), ("/transparencia.html", "Transparência"), ("/ouvidoria.html", "Ouvidoria")])}
{investimento()}
{ONDE_ESTAMOS}
{EMEC}''', "/")

# ---------------------------------------------------------------- Curso
disc_html = "\n".join(f'''        <details class="sem"{" open" if s == "1º" else ""}>
          <summary><span>{s} semestre<small>{len(ds)} disciplinas</small></span></summary>
          <ul class="disc">
''' + "\n".join(f'''            <li><h3>{d["nome"]}</h3><p class="disc__meta"><span>{d["cod"]}</span><span>{d["eixo"]}</span></p><p class="disc__do"><b>O que você fará a partir daqui</b>{d["faz"]}</p></li>''' for d in ds) + '''
          </ul>
        </details>''' for s, ds in SEMS.items())
CURSO_LD = {"@context": "https://schema.org", "@type": "Course", "name": f"Curso Superior de {CURSO}",
            "description": "Graduação tecnológica presencial em 4 semestres, eixo Gestão e Negócios.", "inLanguage": "pt-BR",
            "provider": {"@type": "CollegeOrUniversity", "name": "Faculdade Nine", "url": SITE + "/"},
            "educationalCredentialAwarded": CURSO,
            "hasCourseInstance": {"@type": "CourseInstance", "courseMode": "Onsite",
                                  "location": {"@type": "Place", "name": "Faculdade Nine", "address": ORG["address"]}}}
para_quem = "\n".join(f"            <li><b>{t}</b> {d}</li>" for t, d in PARA_QUEM)
page("curso.html", f"{CURSO} | Faculdade Nine",
     f"Curso superior de {CURSO}, presencial em Curitiba: 4 semestres, {len(DISC)} disciplinas e o que você fará em cada uma.",
     page_hero("t-curso", "O Curso", CURSO, "Graduação tecnológica presencial em Curitiba, em 4 semestres.", "curso") + f'''
    <section class="section" aria-labelledby="t-sobre">
      {wm("crown p-br")}
      <div class="container course-layout">
        <div class="prose">
{head("t-sobre", "Sobre o curso")}
          <p>O tecnólogo em Processos Gerenciais cuida de como uma organização funciona: atendimento, compras, produção, pessoas, finanças e vendas. Ele encontra o que trava o trabalho e propõe melhorias acompanhando os resultados.</p>
          <p>Em cada semestre há disciplinas de gestão, análise, liderança e tecnologia. No 3º e no 4º, os projetos integradores levam o que você aprendeu para problemas reais de empresas. Como é um curso de graduação, depois dele você pode fazer pós-graduação.</p>
          <h3 id="para-quem">Para quem é</h3>
          <ul class="plain">
{para_quem}
          </ul>
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
          <a class="btn btn--gold" href="{AVISE}">Quero ser avisado</a>
        </div>
      </div>
    </section>

    <section class="section section--tint" id="matriz" aria-labelledby="t-matriz">
      {wm("nine p-tr", "dots p-bl")}
      <div class="container">
{head("t-matriz", "Matriz curricular", f"Abra cada semestre para ver as disciplinas e o que você passa a fazer com cada uma.")}
{disc_html}
        <p class="note">Atualizada em {HOJE}. A carga horária de cada disciplina será publicada com o Projeto Pedagógico do Curso.</p>
      </div>
    </section>

{split("t-split-areas", "gold", "areas", "Carreira", "Onde você pode trabalhar",
       "Processos, pessoas, finanças, marketing, logística, projetos, dados ou o próprio negócio.",
       [("/areas-de-atuacao.html", "Ver as áreas de atuação")])}
    <section class="section" id="ingresso" aria-labelledby="t-ingresso">
      {wm("crown p-tr")}
      <div class="container course-layout">
        <div class="prose">
{head("t-ingresso", "Como ingressar")}
          <p>O curso não tem vestibular. Basta ter concluído o ensino médio e fazer a inscrição quando o período for aberto.</p>
          <p>Documentos e datas: {TBC}</p>
        </div>
        <div>
          <h2 class="h-small" id="t-faq">Perguntas frequentes</h2>
          {faq([("O tecnólogo é um curso superior?", "Sim. É um curso de graduação e permite seguir para pós-graduação."),
                ("Onde são as aulas?", "Na Faculdade Nine, Rua Engenheiro Niepce da Silva, 139, Portão, Curitiba/PR."),
                ("Quais são os dias e horários?", "[A CONFIRMAR]"),
                ("Quando abrem as inscrições?", "As datas e os valores serão divulgados em breve nesta página.")])}
        </div>
      </div>
    </section>

{investimento()}''', "/curso.html", CURSO_LD)

# ---------------------------------------------------------------- Áreas de atuação
areas_html = "\n".join(f'''          <li class="card" id="area-{i+1}">
            <h3>{t}</h3>
            <p>{d}</p>
            <ul class="tags" aria-label="Funções">{"".join(f"<li>{x}</li>" for x in f)}</ul>
          </li>''' for i, (t, d, f, _) in enumerate(AREAS))
onde_html = "\n".join(f"          <li><b>{t}</b> {d}</li>" for t, d in ONDE)
page("areas-de-atuacao.html", "Áreas de atuação do tecnólogo em Processos Gerenciais | Faculdade Nine",
     "Onde trabalha e o que faz o tecnólogo em Processos Gerenciais: áreas, funções, ocupações na CBO e registro profissional.",
     page_hero("t-areas", "Áreas de atuação", "Áreas de atuação do tecnólogo em Processos Gerenciais",
               "Onde este profissional trabalha e o que ele faz.", "areas") + f'''
    <section class="section" aria-labelledby="t-faz">
      {wm("crown p-bl")}
      <div class="container course-layout">
        <div class="prose">
{head("t-faz", "O que faz")}
          <blockquote class="quote"><p>{PERFIL}</p><cite>{FONTE}</cite></blockquote>
        </div>
        <div class="aside-box" role="region" aria-labelledby="t-cbo">
          <h2 id="t-cbo">Ocupações e registro</h2>
          <dl>
            <div><dt>Tecnólogo em gestão administrativo-financeira</dt><dd>CBO 1421-20</dd></div>
            <div><dt>Analista administrativo</dt><dd>CBO 2521-05</dd></div>
          </dl>
          <p class="note">Registro profissional no Conselho Regional de Administração (CRA).</p>
        </div>
      </div>
    </section>

    <section class="section section--tint" aria-labelledby="t-lista">
      {wm("nine p-tr", "dots p-bl")}
      <div class="container">
{head("t-lista", "Áreas e funções")}
        <ul class="grid grid--2">
{areas_html}
        </ul>
      </div>
    </section>

    <section class="section is-dark" aria-labelledby="t-onde-trab">
      {wm("crown p-tr", "dots p-br")}
      <div class="container">
{head("t-onde-trab", "Onde trabalha")}
        <ul class="plain plain--cols">
{onde_html}
        </ul>
        <p class="note">Fonte: {FONTE}.</p>
      </div>
    </section>

{split("t-split-curso", "navy", "home-curso", "O curso", CURSO,
       "Graduação tecnológica presencial em Curitiba, em 4 semestres.",
       [("/curso.html", "Sobre o curso"), ("/curso.html#matriz", "Matriz curricular")])}''', "/areas-de-atuacao.html")

# ---------------------------------------------------------------- A Faculdade
page("a-faculdade.html", "A Faculdade | Faculdade Nine",
     "Faculdade Nine: instituição de ensino superior em Curitiba mantida pelo Conselho Educacional Nine. Dados institucionais, estrutura organizacional, CPA e localização.",
     page_hero("t-fac", "A Faculdade", "Faculdade Nine", "Instituição de ensino superior em Curitiba, mantida pelo Conselho Educacional Nine.", "faculdade") + f'''
    <section class="section" aria-labelledby="t-quem">
      {wm("crown p-bl", "dots p-tr")}
      <div class="container statement">
        <h2 id="t-quem">Quem somos</h2>
        <div class="prose">
          <p class="lead">A Faculdade Nine nasce da experiência da Nine Academia de Influência na formação de jovens.</p>
          <p>Missão, visão e valores: {TBC}</p>
        </div>
      </div>
    </section>

    <section class="section is-dark" aria-labelledby="t-dados">
      {wm("nine p-br")}
      <div class="container">
{head("t-dados", "Dados institucionais")}
        {facts([("Instituição", "Faculdade Nine"), ("Mantenedora", "Conselho Educacional Nine"), ("CNPJ da mantenedora", "61.991.971/0001-35"),
                ("Endereço", ENDERECO), ("Direção-Geral", "Raul Cesar Sindlinger"), ("Código e-MEC", TBC), ("Ato de credenciamento", TBC)])}
      </div>
    </section>

    <section class="section" id="estrutura" aria-labelledby="t-estr">
      {wm("crown p-tr")}
      <div class="container">
{head("t-estr", "Estrutura organizacional")}
        <ul class="grid grid--3">
          <li class="card"><h3>Direção-Geral</h3><p>Raul Cesar Sindlinger</p></li>
          <li class="card"><h3>Conselho Superior (CONSUP)</h3><p>Composição: {TBC}</p></li>
          <li class="card" id="cpa"><h3>Comissão Própria de Avaliação (CPA)</h3><p>Autoavaliação institucional. Resultados em <a href="/transparencia.html">Transparência</a>. Composição: {TBC}</p></li>
          <li class="card"><h3>Coordenação do curso</h3><p>{TBC}</p></li>
          <li class="card"><h3>Secretaria Geral</h3><p><a href="mailto:{EMAIL}">{EMAIL}</a> · Telefone {TBC}</p></li>
          <li class="card"><h3>Ouvidoria</h3><p>Vinculada à Direção-Geral. <a href="/ouvidoria.html">Acessar</a></p></li>
        </ul>
      </div>
    </section>

{ONDE_ESTAMOS}''', "/a-faculdade.html")

# ---------------------------------------------------------------- Transparência (art. 26 do Regulamento)
DOCS = [
    ("PDI · Plano de Desenvolvimento Institucional", "a-publicar", None, None),
    ("PPI · Projeto Pedagógico Institucional", "a-publicar", None, None),
    ("Regimento Interno", "a-publicar", None, None),
    ("Regulamento da Ouvidoria e da Comunicação Institucional", "em-aprovacao", None, "/ouvidoria.html"),
    ("PPC · Projeto Pedagógico do Curso", "a-publicar", None, None),
    ("Matriz curricular", "publicado", HOJE, "/curso.html#matriz"),
    ("Calendário acadêmico", "a-publicar", None, None),
    ("Atos regulatórios (credenciamento e autorização do curso)", "a-publicar", None, None),
    ("Composição do CONSUP e da CPA", "a-publicar", None, None),
    ("Relatórios da Ouvidoria", "sem-registro", None, None),
    ("Resultados das avaliações interna (CPA) e externa (INEP/MEC)", "sem-registro", None, None),
    ("Política de privacidade e proteção de dados", "a-publicar", None, "/privacidade.html"),
]
ST = {"publicado": "Publicado", "em-aprovacao": "Em aprovação", "a-publicar": "Em elaboração", "sem-registro": "Nenhum até o momento"}
docs_html = "\n".join(f'''          <li class="doc">
            <h3>{f'<a href="{href}">{t}</a>' if href else t}</h3>
            <p class="status status--{st}">{ST[st]}</p>
            <p class="doc__date">Atualizado em {data or "—"}</p>
          </li>''' for t, st, data, href in DOCS)
page("transparencia.html", "Transparência Institucional | Faculdade Nine",
     "Documentos institucionais, atos regulatórios, CPA, relatórios da Ouvidoria e resultados das avaliações da Faculdade Nine, em acesso livre.",
     page_hero("t-transp", "Transparência Institucional", "Transparência Institucional",
               "Documentos institucionais da Faculdade Nine, em acesso livre.", "transparencia") + f'''
    <section class="section" aria-labelledby="t-docs">
      {wm("crown p-tr", "dots p-bl")}
      <div class="container">
{head("t-docs", "Documentos")}
        <ul class="docs">
{docs_html}
        </ul>
        <p class="note">Revisado a cada período letivo. Não são publicados dados pessoais.</p>
      </div>
    </section>
{EMEC}''', "/transparencia.html")

# ---------------------------------------------------------------- Ouvidoria
page("ouvidoria.html", "Ouvidoria | Faculdade Nine",
     "Ouvidoria da Faculdade Nine: reclamações, denúncias, sugestões, elogios e pedidos de informação, com sigilo e prazos definidos.",
     page_hero("t-ouv", "Ouvidoria", "Ouvidoria",
               "Para estudantes, professores, funcionários, candidatos, famílias e comunidade. Use quando não tiver resposta pelos canais da Secretaria.",
               "ouvidoria") + f'''
    <section class="section" aria-labelledby="t-tipos">
      {wm("crown p-bl")}
      <div class="container">
{head("t-tipos", "O que você pode registrar")}
        <ul class="grid grid--3">
          <li class="card"><h3>Reclamação</h3><p>Sobre um serviço, atendimento ou conduta.</p></li>
          <li class="card"><h3>Denúncia</h3><p>Irregularidades, inclusive assédio e discriminação.</p></li>
          <li class="card"><h3>Sugestão</h3><p>Uma ideia de melhoria.</p></li>
          <li class="card"><h3>Elogio</h3><p>Reconhecimento de um serviço ou de uma pessoa.</p></li>
          <li class="card"><h3>Solicitação de informação</h3><p>Quando a Secretaria não respondeu.</p></li>
        </ul>
      </div>
    </section>

    <section class="section is-dark" aria-labelledby="t-prazos">
      {wm("nine p-br", "dots p-tr")}
      <div class="container">
{head("t-prazos", "Prazos")}
        <ol class="timeline">
          <li><b>Na hora</b><p>Você recebe o número de protocolo por e-mail.</p></li>
          <li><b>5 dias úteis</b><p>A manifestação é encaminhada ao setor responsável.</p></li>
          <li><b>10 dias úteis</b><p>O setor responde à Ouvidoria.</p></li>
          <li><b>20 dias úteis</b><p>Você recebe a resposta final. Prorrogável uma vez, com justificativa.</p></li>
        </ol>
        <p class="note">Sua identidade fica em sigilo e você pode pedir que ela não seja revelada em nenhuma hipótese. Dados tratados conforme a LGPD.</p>
      </div>
    </section>

    <section class="section" id="manifestacao" aria-labelledby="t-form">
      {wm("crown p-tr")}
      <div class="container form-wrap">
{head("t-form", "Registrar manifestação", f'Sem cadastro. Se preferir, escreva para <a href="mailto:{EMAIL}">{EMAIL}</a>.')}
        <form class="form form--light" data-ouvidoria novalidate>
          <fieldset>
            <legend>Identificação</legend>
            <div class="field"><label for="o-nome">Nome</label><input id="o-nome" name="nome" type="text" autocomplete="name" required></div>
            <div class="field"><label for="o-email">E-mail</label><input id="o-email" name="email" type="email" autocomplete="email" required></div>
            <div class="field field--full"><label for="o-vinculo">Vínculo com a Instituição</label>
              <select id="o-vinculo" name="vinculo" required><option value="" selected disabled>Selecione</option><option>Estudante</option><option>Docente</option><option>Técnico-administrativo</option><option>Egresso</option><option>Candidato</option><option>Pai, mãe ou responsável</option><option>Comunidade externa</option></select></div>
          </fieldset>
          <fieldset>
            <legend>Manifestação</legend>
            <div class="field field--full"><label for="o-tipo">Tipo</label>
              <select id="o-tipo" name="tipo" required><option value="" selected disabled>Selecione</option><option>Reclamação</option><option>Denúncia</option><option>Sugestão</option><option>Elogio</option><option>Solicitação de informação</option></select></div>
            <div class="field field--full"><label for="o-descricao">Descrição</label><textarea id="o-descricao" name="descricao" rows="6" required></textarea></div>
            <div class="field field--full"><label for="o-anexos">Anexos <span class="opt">(opcional)</span></label><input id="o-anexos" name="anexos" type="file" multiple></div>
          </fieldset>
          <div class="field field--hp" aria-hidden="true"><label for="o-website">Website</label><input id="o-website" name="website" type="text" autocomplete="off"></div>
          <div class="field field--check"><input id="o-sigilo" name="sigilo_total" type="checkbox"><label for="o-sigilo">Não quero que minha identidade seja revelada.</label></div>
          <div class="field field--check"><input id="o-lgpd" name="consentimento" type="checkbox" required><label for="o-lgpd">Concordo com o uso dos meus dados para esta manifestação, conforme a <a href="/privacidade.html">Política de privacidade</a>.</label></div>
          <div><button class="btn btn--gold" type="submit">Enviar</button><p class="form__status" data-status role="status" aria-live="polite"></p></div>
        </form>
      </div>
    </section>''', "/ouvidoria.html")

# ---------------------------------------------------------------- Privacidade
page("privacidade.html", "Política de privacidade | Faculdade Nine",
     "Política de privacidade e proteção de dados pessoais da Faculdade Nine (LGPD).",
     page_hero("t-priv", "Política de privacidade", "Política de privacidade",
               "Como a Faculdade Nine trata dados pessoais, conforme a Lei nº 13.709/2018 (LGPD).", "privacidade") + f'''
    <section class="section" aria-labelledby="t-priv-st">
      {wm("crown p-br", "dots p-tl")}
      <div class="container statement">
        <h2 id="t-priv-st">Em elaboração</h2>
        <div class="prose">
          <p class="lead">O texto completo será publicado nesta página. {TBC}</p>
          {facts([("Controlador", "Conselho Educacional Nine · CNPJ 61.991.971/0001-35"), ("Endereço", ENDERECO),
                  ("Contato", f'<a href="mailto:{EMAIL}">{EMAIL}</a>'), ("Encarregado (DPO)", TBC)])}
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
