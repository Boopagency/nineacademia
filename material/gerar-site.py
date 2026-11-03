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
C = "/cursos/processos-gerenciais/"

# Cursos da Faculdade. Curso novo: acrescente aqui (entra no menu, no rodapé, na home e em /cursos/) e crie a página dele.
CURSOS = [dict(url=C, nome="Processos Gerenciais", grau="Graduação tecnológica", lugar="Presencial · Curitiba", duracao="4 semestres",
               foto="curso", resumo="Organize processos, lidere equipes e decida com base em dados.")]

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

NAV = [("/transparencia.html", "Transparência"), ("/a-faculdade.html#onde-estamos", "Contato")]
SUB = [("/a-faculdade.html", "Sobre a Faculdade"), ("/a-faculdade.html#estrutura", "Estrutura organizacional"),
       ("/a-faculdade.html#cpa", "CPA · Comissão Própria de Avaliação"), ("/a-faculdade.html#onde-estamos", "Onde estamos"),
       ("/transparencia.html", "Transparência institucional"), ("/ouvidoria.html", "Ouvidoria"), ("/privacidade.html", "Privacidade e proteção de dados")]

DROPS = [("A Faculdade", "/a-faculdade.html", SUB),
         ("Cursos", "/cursos/", [("/cursos/", "Todos os cursos")] + [(c["url"], c["nome"]) for c in CURSOS])]

BRAND = '''<span class="crown" aria-hidden="true"></span><span class="brand__name"><b>NINE</b><small>Faculdade</small></span>'''


def header(atual):
    def a(href, txt):
        cur = ' aria-current="page"' if href == atual else ""
        return f'<a href="{href}"{cur}>{txt}</a>'
    nav = "\n".join(f"          <li>{a(h, t)}</li>" for h, t in NAV)
    mnav = "\n".join(f'        <li><a href="{h}">{t}</a></li>' for h, t in NAV)
    dd = "\n".join(f'''          <li>
            <details class="dd">
              <summary>{t}</summary>
              <ul class="dd__panel">
{"".join(f"                <li>{a(h, x)}</li>" + chr(10) for h, x in itens)}              </ul>
            </details>
          </li>''' for t, _, itens in DROPS)
    mdd = "\n".join(f'''        <li><a href="{u}">{t}</a>
          <ul class="menu__sub">
{"".join(f'            <li><a href="{h}">{x}</a></li>' + chr(10) for h, x in itens)}          </ul>
        </li>''' for t, u, itens in DROPS)
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
{dd}
{nav}
        </ul>
      </nav>
      <a class="btn btn--gold header__cta" href="/cursos/processos-gerenciais/#investimento">Inscrições em breve</a>
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
{mdd}
{mnav}
      </ul>
      <a class="btn btn--gold" href="/cursos/processos-gerenciais/#investimento">Inscrições em breve</a>
    </nav>
  </div>
'''


FOOTER = f'''  <footer class="footer" id="rodape">
    <div class="container footer__cols">
      <div>
        <h2>Cursos</h2>
        <ul>
          <li><a href="/cursos/">Todos os cursos</a></li>
          <li><a href="/cursos/processos-gerenciais/">{CURSO}</a></li>
          <li><a href="/cursos/processos-gerenciais/#matriz">Matriz curricular</a></li>
          <li><a href="/cursos/processos-gerenciais/areas-de-atuacao/">Áreas de atuação</a></li>
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
  <script>document.documentElement.classList.add("js")</script>
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

def crumbs(*trilha):
    """Migalhas: pares (link, texto) e, por último, o texto da página atual."""
    links = "".join(f'<a href="{h}">{x}</a> / ' for h, x in [("/", "Início"), *trilha[:-1]])
    return f'<nav class="crumbs" aria-label="Você está em">{links}<span aria-current="page">{trilha[-1]}</span></nav>'


def page_hero(titulo_id, crumb, titulo, lead, foto):
    return f'''    <section class="page-hero" aria-labelledby="{titulo_id}">
      <div class="page-hero__bg">{img(foto, eager=True, sizes="100vw")}</div>
      {wm("nine p-br", "dots p-tr")}
      <div class="container">
        {crumbs(*crumb) if isinstance(crumb, tuple) else crumbs(crumb)}
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

# ---------------------------------------------------------------- Ícones (traço simples, sem biblioteca)
ICON_PATHS = {
    "processos": "M4 5h6v6H4zM14 13h6v6h-6zM7 11v5h7M17 13V8h-7",
    "pessoas": "M9 11a3 3 0 1 0 0-6 3 3 0 0 0 0 6zM3 20c0-3.3 2.7-6 6-6s6 2.7 6 6M16 5.2a3 3 0 0 1 0 5.6M21 20c0-2.6-1.5-4.8-3.8-5.6",
    "financas": "M3 20h18M6 20v-6M11 20V9M16 20v-9M20 6l-5 4-4-3-6 5",
    "marketing": "M3 10v4l12 5V5L3 10zM15 9h2.5a3 3 0 0 1 0 6H15M7 15.5 8 20h3l-1-3.5",
    "logistica": "M2 6h11v10H2zM13 9h4.5l3.5 3.5V16h-8M6 19.5a1.5 1.5 0 1 0 0-.01M17 19.5a1.5 1.5 0 1 0 0-.01",
    "projetos": "M12 3a9 9 0 1 0 0 18 9 9 0 0 0 0-18zM12 7.5a4.5 4.5 0 1 0 0 9 4.5 4.5 0 0 0 0-9zM12 11.2a.8.8 0 1 0 0 1.6.8.8 0 0 0 0-1.6z",
    "dados": "M4 6c0-1.7 3.6-3 8-3s8 1.3 8 3-3.6 3-8 3-8-1.3-8-3zM4 6v12c0 1.7 3.6 3 8 3s8-1.3 8-3V6M4 12c0 1.7 3.6 3 8 3s8-1.3 8-3",
    "empreender": "M3 9 5 4h14l2 5M3 9h18v11H3zM9 20v-6h6v6M3 9c0 1.7 1.3 3 3 3s3-1.3 3-3c0 1.7 1.3 3 3 3s3-1.3 3-3c0 1.7 1.3 3 3 3s3-1.3 3-3",
    "pratica": "M4 4h7v7H4zM13 4h7v7h-7zM4 13h7v7H4zM13 13h7v7h-7z",
    "ia": "M7 7h10v10H7zM10 3v4M14 3v4M10 17v4M14 17v4M3 10h4M3 14h4M17 10h4M17 14h4",
    "local": "M12 21s-7-6.2-7-11a7 7 0 0 1 14 0c0 4.8-7 11-7 11zM12 12.5a2.5 2.5 0 1 0 0-5 2.5 2.5 0 0 0 0 5z",
    "proposito": "M12 20s-7-4.4-7-10a4 4 0 0 1 7-2.6A4 4 0 0 1 19 10c0 5.6-7 10-7 10z",
    "tempo": "M12 3a9 9 0 1 0 0 18 9 9 0 0 0 0-18zM12 7v5l3 2",
    "diploma": "M3 8l9-4 9 4-9 4-9-4zM7 10v5c0 1.1 2.2 3 5 3s5-1.9 5-3v-5",
    "empresa": "M4 21V5l8-2v18M12 21h8V9l-8-2M3 21h18M8 8v.01M8 12v.01M8 16v.01M16 12v.01M16 16v.01",
    "consultoria": "M3 8h18v12H3zM8 8V5h8v3M3 13h18",
    "publica": "M3 21h18M4 10h16L12 4 4 10zM6 10v8M10 10v8M14 10v8M18 10v8",
    "ensino": "M4 5a2 2 0 0 1 2-2h13v16H6a2 2 0 0 0-2 2zM4 21V5M8 7h7",
}


def icon(nome):
    return (f'<span class="icon" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" '
            f'stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="{ICON_PATHS[nome]}"/></svg></span>')


AREA_ICON = ["processos", "pessoas", "financas", "marketing", "logistica", "projetos", "dados", "empreender"]
ONDE_ICON = ["empresa", "consultoria", "publica", "empreender", "ensino"]


def tabs(nome, rotulo, itens, vertical=False):
    """Abas acessíveis. Sem JavaScript, todos os painéis aparecem um embaixo do outro."""
    botoes = "\n".join(
        f'          <button type="button" role="tab" id="tab-{nome}-{i}" aria-controls="painel-{nome}-{i}" aria-selected="{str(i == 0).lower()}">{t}</button>'
        for i, (t, _) in enumerate(itens))
    paineis = "\n".join(
        f'        <div class="tabs__panel" role="tabpanel" id="painel-{nome}-{i}" aria-labelledby="tab-{nome}-{i}" tabindex="0">\n{c}\n        </div>'
        for i, (_, c) in enumerate(itens))
    orient = ' aria-orientation="vertical"' if vertical else ""
    return f'''      <div class="tabs{' tabs--v' if vertical else ''}" data-tabs>
        <div class="tabs__list" role="tablist" aria-label="{rotulo}"{orient}>
{botoes}
        </div>
{paineis}
      </div>'''


# ---------------------------------------------------------------- Curso
semestres = []
for s, ds in SEMS.items():
    itens = "\n".join(f'''            <li><h3>{d["nome"]}</h3><p class="disc__meta"><span>{d["cod"]}</span><span>{d["eixo"]}</span></p><p class="disc__do"><b>O que você fará a partir daqui</b>{d["faz"]}</p></li>''' for d in ds)
    semestres.append((f"{s} semestre", f'          <p class="tabs__count">{len(ds)} disciplinas</p>\n          <ul class="disc">\n{itens}\n          </ul>'))

mercado = []
for (t, d, f, cods), ic in zip(AREAS, AREA_ICON):
    funcoes = "".join(f"<li>{x}</li>" for x in f)
    discs = " · ".join(POR_COD[c]["nome"] for c in cods[:3])
    mercado.append((t, f'''          {icon(ic)}
          <h3>{t}</h3>
          <p>{d}</p>
          <h4>Funções</h4>
          <ul class="tags">{funcoes}</ul>
          <p class="note">No curso: {discs}.</p>'''))

JORNADA = [("diploma", "1º semestre", "Base de gestão, ferramentas e pessoas."),
           ("processos", "2º semestre", "Marketing, finanças, direito e processos."),
           ("projetos", "3º semestre", "Projeto Integrador I, projetos e inovação."),
           ("ia", "4º semestre", "Projeto Integrador II, dados, IA e liderança.")]
POR_QUE = [("pratica", "Prática desde o início", f"{N_PI} projetos integradores com problemas reais de empresas."),
           ("ia", "Dados e IA", "Analytics, sistemas de informação e inteligência artificial aplicada aos negócios."),
           ("local", "Presencial em Curitiba", "Turma, professores e convivência no Portão."),
           ("proposito", "Gestão com propósito", "Teologia com ênfase social e ética na liderança.")]
COMPARA = [("Duração", "4 semestres (cerca de 2 anos)", "8 semestres (cerca de 4 anos)"),
           ("Foco", "Processos e rotinas de gestão, com aplicação prática", "Formação ampla em administração"),
           ("Tipo de curso", "Graduação", "Graduação"),
           ("Pós-graduação", "Pode cursar", "Pode cursar"),
           ("Registro profissional", "Conselho Regional de Administração", "Conselho Regional de Administração")]

CURSO_LD = {"@context": "https://schema.org", "@type": "Course", "name": f"Curso Superior de {CURSO}",
            "description": "Graduação tecnológica presencial em 4 semestres, eixo Gestão e Negócios.", "inLanguage": "pt-BR",
            "provider": {"@type": "CollegeOrUniversity", "name": "Faculdade Nine", "url": SITE + "/"},
            "educationalCredentialAwarded": CURSO,
            "hasCourseInstance": {"@type": "CourseInstance", "courseMode": "Onsite",
                                  "location": {"@type": "Place", "name": "Faculdade Nine", "address": ORG["address"]}}}
para_quem = "\n".join(f"            <li><b>{t}</b> {d}</li>" for t, d in PARA_QUEM)
page("cursos/processos-gerenciais/index.html", f"{CURSO} | Faculdade Nine",
     f"Curso superior de {CURSO}, presencial em Curitiba: 4 semestres, {len(DISC)} disciplinas e o que você fará em cada uma.",
     f'''    <section class="page-hero page-hero--course" aria-labelledby="t-curso">
      <div class="page-hero__bg">{img("curso", eager=True, sizes="100vw")}</div>
      {wm("nine p-br", "dots p-tr")}
      <div class="container">
        {crumbs(("/cursos/", "Cursos"), "Processos Gerenciais")}
        <h1 id="t-curso">{CURSO}</h1>
        <ul class="meta">
          <li>{icon("local")}Presencial · Curitiba</li>
          <li>{icon("tempo")}4 semestres</li>
          <li>{icon("diploma")}Graduação tecnológica</li>
        </ul>
      </div>
    </section>

    <section class="section section--first" aria-labelledby="t-sobre">
      {wm("crown p-bl")}
      <div class="container course-layout">
        <div class="prose">
{head("t-sobre", "Sobre o curso")}
          <p class="lead">Aprenda a organizar o trabalho de uma empresa, liderar a equipe e decidir com base em dados.</p>
          <p>O tecnólogo em Processos Gerenciais cuida de como uma organização funciona: atendimento, compras, produção, pessoas, finanças e vendas. Ele encontra o que trava o trabalho e propõe melhorias acompanhando os resultados.</p>
          <h3 id="para-quem">Para quem é</h3>
          <ul class="plain">
{para_quem}
          </ul>
        </div>
        <div class="aside-box aside-box--float" role="region" aria-labelledby="t-box">
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
{head("t-matriz", "Conheça a matriz curricular", "Escolha o semestre e veja o que você passa a fazer em cada disciplina.")}
{tabs("sem", "Semestres", semestres)}
        <p class="note">Atualizada em {HOJE}. A carga horária de cada disciplina será publicada com o Projeto Pedagógico do Curso.</p>
      </div>
    </section>

    <section class="section is-dark" aria-labelledby="t-jornada">
      {wm("crown p-tr", "dots p-bl")}
      <div class="container">
{head("t-jornada", "Como é a sua jornada")}
        <ol class="journey">
''' + "\n".join(f'          <li>{icon(ic)}<h3>{t}</h3><p>{d}</p></li>' for ic, t, d in JORNADA) + f'''
        </ol>
      </div>
    </section>

    <section class="section" aria-labelledby="t-mercado">
      {wm("nine p-br")}
      <div class="container">
        <div class="head-row">
{head("t-mercado", "Processos Gerenciais e o mercado de trabalho")}
          <a class="btn btn--outline" href="/cursos/processos-gerenciais/areas-de-atuacao/">Ver todas as áreas</a>
        </div>
{tabs("area", "Áreas de atuação", mercado, vertical=True)}
      </div>
    </section>

    <section class="section band-gold" aria-labelledby="t-porque">
      {wm("crown p-br", "nine p-tr")}
      <div class="container why">
{head("t-porque", "Por que fazer este curso?")}
        <ul class="why__grid">
''' + "\n".join(f'          <li class="card">{icon(ic)}<h3>{t}</h3><p>{d}</p></li>' for ic, t, d in POR_QUE) + f'''
        </ul>
      </div>
    </section>

    <section class="section" aria-labelledby="t-compara">
      {wm("dots p-tr")}
      <div class="container">
{head("t-compara", "Tecnólogo ou bacharelado?", "Os dois são cursos de graduação. A diferença está na duração e no foco.")}
        <div class="table-wrap" role="region" aria-label="Tabela comparativa: tecnólogo e bacharelado" tabindex="0">
          <table class="compare">
            <thead><tr><th scope="col"><span class="sr-only">Critério</span></th><th scope="col">Tecnólogo em Processos Gerenciais</th><th scope="col">Bacharelado em Administração</th></tr></thead>
            <tbody>
''' + "\n".join(f'              <tr><th scope="row">{a}</th><td>{b}</td><td>{c}</td></tr>' for a, b, c in COMPARA) + f'''
            </tbody>
          </table>
        </div>
      </div>
    </section>

    <section class="section is-dark" id="ingresso" aria-labelledby="t-faq">
      {wm("nine p-bl", "crown p-tr")}
      <div class="container faq-band">
        <div class="prose">
{head("t-faq", "Você pergunta, a gente responde")}
          <p>O curso não tem vestibular: basta ter concluído o ensino médio e se inscrever quando o período abrir.</p>
          <a class="btn btn--gold" href="{AVISE}">Quero ser avisado</a>
        </div>
        {faq([("O tecnólogo é um curso superior?", "Sim. É um curso de graduação e permite seguir para pós-graduação."),
              ("Precisa fazer vestibular?", "Não. Basta ter concluído o ensino médio. Documentos e datas: [A CONFIRMAR]"),
              ("Onde são as aulas?", "Na Faculdade Nine, Rua Engenheiro Niepce da Silva, 139, Portão, Curitiba/PR."),
              ("Quais são os dias e horários?", "[A CONFIRMAR]"),
              ("Quando abrem as inscrições?", "As datas e os valores serão divulgados em breve nesta página.")])}
      </div>
    </section>

{investimento()}''', "/cursos/processos-gerenciais/", CURSO_LD)

# ---------------------------------------------------------------- Áreas de atuação
areas_html = "\n".join(f'''          <li class="card card--area" id="area-{i+1}">
            {icon(ic)}
            <h3>{t}</h3>
            <p>{d}</p>
            <ul class="tags" aria-label="Funções">{"".join(f"<li>{x}</li>" for x in f)}</ul>
          </li>''' for i, ((t, d, f, _), ic) in enumerate(zip(AREAS, AREA_ICON)))
onde_html = "\n".join(f'          <li>{icon(ic)}<h3>{t}</h3><p>{d}</p></li>' for (t, d), ic in zip(ONDE, ONDE_ICON))
page("cursos/processos-gerenciais/areas-de-atuacao/index.html", "Áreas de atuação do tecnólogo em Processos Gerenciais | Faculdade Nine",
     "Onde trabalha e o que faz o tecnólogo em Processos Gerenciais: áreas, funções, ocupações na CBO e registro profissional.",
     page_hero("t-areas", (("/cursos/", "Cursos"), (C, "Processos Gerenciais"), "Áreas de atuação"), "Áreas de atuação do tecnólogo em Processos Gerenciais",
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

    <section class="stats band-gold" aria-labelledby="t-numeros">
      <h2 class="sr-only" id="t-numeros">Em números</h2>
      {wm("dots p-tr")}
      <div class="container">
        <ul class="stats__list">
          <li><b data-count="{len(AREAS)}">{len(AREAS)}</b><span>áreas de atuação</span></li>
          <li><b data-count="2">2</b><span>ocupações na CBO</span></li>
          <li><b>CRA</b><span>registro profissional</span></li>
          <li><b data-count="4">4</b><span>semestres de curso</span></li>
        </ul>
      </div>
    </section>

    <section class="section section--tint" aria-labelledby="t-lista">
      {wm("nine p-tr", "dots p-bl")}
      <div class="container">
{head("t-lista", "Áreas e funções")}
        <ul class="grid grid--4">
{areas_html}
        </ul>
      </div>
    </section>

    <section class="section is-dark" aria-labelledby="t-onde-trab">
      {wm("crown p-tr", "dots p-br")}
      <div class="container">
{head("t-onde-trab", "Onde trabalha")}
        <ul class="places">
{onde_html}
        </ul>
        <p class="note">Fonte: {FONTE}.</p>
      </div>
    </section>

{split("t-split-curso", "navy", "home-curso", "O curso", CURSO,
       "Graduação tecnológica presencial em Curitiba, em 4 semestres.",
       [("/cursos/processos-gerenciais/", "Sobre o curso"), ("/cursos/processos-gerenciais/#matriz", "Matriz curricular")])}''', "/cursos/processos-gerenciais/areas-de-atuacao/")


# ---------------------------------------------------------------- Cursos (cartões usados na home e em /cursos/)
def curso_card(c):
    return f'''          <li class="course-card">
            <div class="course-card__photo">{img(c["foto"], sizes="(min-width: 900px) 400px, 100vw")}</div>
            <div class="course-card__body">
              <p class="course-card__grau">{c["grau"]}</p>
              <h3><a href="{c["url"]}">{c["nome"]}</a></h3>
              <p>{c["resumo"]}</p>
              <ul class="course-card__meta"><li>{icon("local")}{c["lugar"]}</li><li>{icon("tempo")}{c["duracao"]}</li></ul>
              <span class="course-card__go" aria-hidden="true">Ver curso</span>
            </div>
          </li>'''


cards = "\n".join(curso_card(c) for c in CURSOS)

# ---------------------------------------------------------------- Início (carrossel de destaques + cursos + Faculdade)
SLIDES = [("Faculdade <span>Nine</span>", "Ensino superior em Curitiba, mantido pelo Conselho Educacional Nine.",
           [("/a-faculdade.html", "Conheça a Faculdade", "btn--gold"), ("/a-faculdade.html#onde-estamos", "Onde estamos", "btn--outline")], "home-faculdade"),
          ("Processos <span>Gerenciais</span>", "Graduação tecnológica presencial em Curitiba. Aprenda a organizar processos, liderar equipes e decidir com base em dados.",
           [(C, "Conheça o curso", "btn--gold"), (C + "areas-de-atuacao/", "Áreas de atuação", "btn--outline")], "home-hero"),
          ("Inscrições <span>em breve</span>", "Sem vestibular: basta ter concluído o ensino médio. Avisamos você quando as inscrições abrirem.",
           [(AVISE, "Quero ser avisado", "btn--gold"), (C + "#investimento", "Investimento", "btn--outline")], "home-curso")]
slides = "\n".join(f'''        <div class="slide{' is-active' if i == 0 else ''}" role="group" aria-roledescription="destaque" aria-label="{i + 1} de {len(SLIDES)}">
          <div class="container">
            <div class="hero__text">
              <h2 class="hero__title">{t}</h2>
              <p class="lead">{d}</p>
              <div class="btn-row">{"".join(f'<a class="btn {cl}" href="{h}">{x}</a>' for h, x, cl in bs)}</div>
            </div>
            <div class="hero__media"><div class="hero__img">{img(f, eager=i == 0)}</div></div>
          </div>
        </div>''' for i, (t, d, bs, f) in enumerate(SLIDES))
ATUAL = ' aria-current="true"'
pontos = "".join(f'<button type="button" class="carousel__dot" data-goto="{i}"{ATUAL if i == 0 else ""}><span class="sr-only">Destaque {i + 1}: {re.sub("<[^>]+>", "", t)}</span></button>'
                 for i, (t, *_) in enumerate(SLIDES))

page("index.html", "Faculdade Nine | Ensino superior presencial em Curitiba",
     f"Faculdade Nine, em Curitiba: curso superior de {CURSO}, presencial, em 4 semestres. Cursos, institucional, transparência e ouvidoria.",
     f'''    <section class="hero carousel" aria-roledescription="carrossel" aria-labelledby="t-hero" data-carousel>
      <h1 class="sr-only" id="t-hero">Faculdade Nine: ensino superior em Curitiba</h1>
      <span class="hero__ring" aria-hidden="true"></span>
      {wm("crown p-tl")}
      <div class="carousel__track" aria-live="off">
{slides}
      </div>
      <div class="carousel__ctrl">
        <div>
          <button type="button" class="carousel__btn carousel__play" data-play aria-label="Pausar destaques"></button>
          <button type="button" class="carousel__btn" data-step="-1" aria-label="Destaque anterior">‹</button>
          {pontos}
          <button type="button" class="carousel__btn" data-step="1" aria-label="Próximo destaque">›</button>
        </div>
      </div>
    </section>

    <section class="section" aria-labelledby="t-cursos">
      {wm("crown p-bl", "nine p-tr")}
      <div class="container courses">
        <div class="courses__intro">
{head("t-cursos", "Nossos cursos", "Graduação presencial em Curitiba, com prática desde o primeiro semestre.")}
          <a class="btn btn--outline" href="/cursos/">Todos os cursos</a>
        </div>
        <ul class="courses__list">
{cards}
        </ul>
      </div>
    </section>

{split("t-split-fac", "navy", "home-areas", "A Faculdade", "Faculdade Nine",
       "Mantida pelo Conselho Educacional Nine, em Curitiba.",
       [("/a-faculdade.html", "Sobre"), ("/a-faculdade.html#estrutura", "Estrutura"), ("/a-faculdade.html#cpa", "CPA"), ("/transparencia.html", "Transparência"), ("/ouvidoria.html", "Ouvidoria")])}
{ONDE_ESTAMOS}
{EMEC}''', "/")

# ---------------------------------------------------------------- Cursos (lista)
page("cursos/index.html", "Cursos | Faculdade Nine",
     "Cursos de graduação da Faculdade Nine, presenciais em Curitiba.",
     page_hero("t-lista-cursos", "Cursos", "Cursos", "Graduação presencial em Curitiba.", "faculdade") + f'''
    <section class="section" aria-labelledby="t-grad">
      {wm("crown p-br", "dots p-tl")}
      <div class="container">
{head("t-grad", "Graduação tecnológica", "Cursos superiores de curta duração, com foco no mercado de trabalho.")}
        <ul class="courses__list courses__list--page">
{cards}
        </ul>
      </div>
    </section>

{investimento()}''', "/cursos/")

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
    ("Matriz curricular", "publicado", HOJE, "/cursos/processos-gerenciais/#matriz"),
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
REVEAL = r'class="(?:[^"]*\s)?(head|card|split__body|split__photo|aside-box|soon__box|statement|place__info|map|disc|journey|why__grid|stats__list|places|emec-card|docs|timeline|facts|form|tabs|quote|compare|faq|plain)(?:\s[^"]*)?"'
def _rev(t):
    return re.sub(r"<(div|ul|ol|blockquote|dl|form|table|li)(\s[^>]*?)(" + REVEAL + r")([^>]*)>",
                  lambda m: m.group(0) if "data-reveal" in m.group(0) else f"<{m.group(1)}{m.group(2)}{m.group(3)}{m.group(5)} data-reveal>", t)
for arq in glob.glob("*.html") + glob.glob("academia/*.html") + glob.glob("cursos/**/*.html", recursive=True):
    t = open(arq).read()
    css = CSS["academia" if arq.startswith("academia/") else "faculdade"]
    if not arq.startswith("academia/") and "<main" in t:
        ini, fim = t.index("<main"), t.index("</main>")
        t = t[:ini] + _rev(t[ini:fim]) + t[fim:]
    t = re.sub(r'<link rel="stylesheet" href="/?(?:faculdade|style)\.css">|<style id="css">.*?</style>',
               lambda m: f'<style id="css">{css}</style>', t, count=1, flags=re.S)
    assert ' style="' not in t, arq
    open(arq, "w").write(t)

# sitemap e robots
urls = ["/", "/cursos/", "/cursos/processos-gerenciais/", "/cursos/processos-gerenciais/areas-de-atuacao/", "/a-faculdade.html", "/transparencia.html", "/ouvidoria.html", "/privacidade.html", "/academia/"]
open("sitemap.xml", "w").write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
                               + "".join(f"  <url><loc>{SITE}{u}</loc></url>\n" for u in urls) + "</urlset>\n")
open("robots.txt", "w").write(f"User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n")
print("ok:", len(DISC), "disciplinas,", len(SEMS), "semestres; CSS faculdade", len(CSS["faculdade"]) // 1024, "KB")
