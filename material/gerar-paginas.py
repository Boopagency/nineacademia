"""Gera as páginas institucionais e aplica cabeçalho/rodapé comuns na home.
Rodar na raiz: python3 -I material/gerar-paginas.py <Disciplinas_Nine.xlsx>. Atenção: sobrescreve as páginas internas."""
import re, sys, collections
import openpyxl
from PIL import Image

XLSX = sys.argv[1]
HOJE = "02/11/2026"
EMAIL = "contato@nine.com.br"
TBC = '<span class="tbc">[A CONFIRMAR]</span>'
ARROW = '<span class="btn__icon" aria-hidden="true"><svg viewBox="0 0 16 16"><path d="M5 11L11 5M6 5h5v5"/></svg></span>'
CROWN = '<i class="crown" aria-hidden="true"></i>'
PAGES = [("./", "Início"), ("a-faculdade.html", "A Faculdade"), ("curso.html", "Curso"),
         ("transparencia.html", "Transparência"), ("ouvidoria.html", "Ouvidoria")]


def img(id_, alt, full=True, eager=False, pos=None):
    p = f"assets/img/galeria/{id_}{'' if full else '-600'}.webp"
    w, h = Image.open(p).size
    extra = ' fetchpriority="high"' if eager else ' loading="lazy"'
    st = f' style="object-position:{pos}"' if pos else ""
    return f'<img src="{p}" width="{w}" height="{h}" alt="{alt}"{extra} decoding="async"{st}>'


def header(current):
    def li(href, label):
        cur = ' aria-current="page"' if href == current else ""
        return f'<li><a href="{href}"{cur}>{label}</a></li>'
    links = "\n          ".join(li(h, l) for h, l in PAGES)
    mlinks = "\n        ".join(li(h, l) for h, l in PAGES)
    return f'''  <nav class="a11y-bar" aria-label="Atalhos de acessibilidade">
    <ul>
      <li><a href="#conteudo" accesskey="1">Ir para o conteúdo [1]</a></li>
      <li><a href="#menu-principal" accesskey="2">Ir para o menu [2]</a></li>
      <li><a href="#rodape" accesskey="3">Ir para o rodapé [3]</a></li>
    </ul>
  </nav>
  <noscript><p class="noscript">Algumas animações dependem de JavaScript. Todo o conteúdo do site continua disponível sem ele.</p></noscript>

  <header class="nav" data-nav>
    <div class="container nav__inner">
      <a class="logo" href="./" aria-label="Faculdade Nine, página inicial">
        <span class="wm" aria-hidden="true">N<span class="wm__i">I{CROWN}</span>NE</span>
      </a>

      <nav class="nav__pill" id="menu-principal" aria-label="Principal">
        <ul>
          {links}
        </ul>
      </nav>

      <a class="btn nav__cta" data-magnetic href="./#aplicar">Inscrição {ARROW}</a>

      <button class="nav__burger" type="button" aria-expanded="false" aria-controls="menu-mobile" data-menu-toggle>
        <span class="sr-only">Abrir menu</span><span aria-hidden="true"></span><span aria-hidden="true"></span>
      </button>
    </div>
  </header>

  <div class="menu" id="menu-mobile" hidden data-menu>
    <button class="menu__close" type="button" data-menu-toggle><span class="sr-only">Fechar menu</span>×</button>
    <nav aria-label="Menu mobile">
      <ul>
        {mlinks}
        <li><a href="./#aplicar" class="menu__apply">Inscrição →</a></li>
      </ul>
    </nav>
  </div>
'''


FOOTER = f'''  <footer class="footer" id="rodape">
    <div class="container">
      <div class="footer__inst">
        <p class="footer__name">Faculdade Nine</p>
        <p>Mantida pelo Conselho Educacional Nine · CNPJ 61.991.971/0001-35</p>
        <p>Rua Engenheiro Niepce da Silva, 139 · Portão · Curitiba/PR</p>
      </div>
      <div class="footer__cols">
        <div>
          <p class="footer__title">Institucional</p>
          <ul>
            <li><a href="a-faculdade.html">A Faculdade</a></li>
            <li><a href="curso.html">Curso</a></li>
            <li><a href="./#aplicar">Processo seletivo</a></li>
          </ul>
        </div>
        <div>
          <p class="footer__title">Transparência</p>
          <ul>
            <li><a href="transparencia.html">Transparência Institucional</a></li>
            <li><a href="ouvidoria.html">Ouvidoria</a></li>
            <li><a href="privacidade.html">Política de privacidade</a></li>
          </ul>
        </div>
        <div>
          <p class="footer__title">Secretaria Geral</p>
          <ul>
            <li><a href="mailto:{EMAIL}">{EMAIL}</a></li>
            <li>Telefone <span class="tbc tbc--dark">[A CONFIRMAR]</span></li>
            <li><a href="https://www.instagram.com/nine.academia/">@nine.academia</a></li>
          </ul>
        </div>
        <div>
          <p class="footer__title">Cadastro e-MEC</p>
          <div class="emec" role="note">
            <span class="emec__qr" aria-hidden="true">QR</span>
            <p>Selo e QR Code do e-MEC <span class="tbc tbc--dark">[após o credenciamento]</span></p>
          </div>
          <p class="footer__small"><a href="https://emec.mec.gov.br/">Consulte instituições no e-MEC</a></p>
        </div>
      </div>
      <p class="footer__copy">© <span data-year></span> Faculdade Nine · Conselho Educacional Nine</p>
    </div>
    <p class="footer__wm" aria-hidden="true"><span class="wm">N<span class="wm__i">I{CROWN}</span>NE</span></p>
  </footer>
'''


def page(slug, title, desc, body):
    html = f'''<!doctype html>
<html lang="pt-BR">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title} | Faculdade Nine</title>
  <meta name="description" content="{desc}">
  <meta property="og:type" content="website">
  <meta property="og:locale" content="pt_BR">
  <meta property="og:title" content="{title} | Faculdade Nine">
  <meta property="og:description" content="{desc}">
  <link rel="icon" type="image/png" href="assets/logo/crown.png">
  <link rel="preload" as="font" type="font/woff2" href="assets/fonts/inter-tight-latin.woff2" crossorigin>
  <link rel="stylesheet" href="style.css">
  <script type="application/ld+json">{{"@context": "https://schema.org", "@type": "CollegeOrUniversity", "name": "Faculdade Nine", "alternateName": "Nine Academia de Influência", "url": "https://nineacademia.vercel.app/", "logo": "https://nineacademia.vercel.app/assets/logo/crown.png", "email": "contato@nine.com.br", "address": {{"@type": "PostalAddress", "streetAddress": "Rua Engenheiro Niepce da Silva, 139", "addressLocality": "Curitiba", "addressRegion": "PR", "addressCountry": "BR"}}, "parentOrganization": {{"@type": "Organization", "name": "Conselho Educacional Nine", "taxID": "61.991.971/0001-35"}}, "sameAs": ["https://www.instagram.com/nine.academia/"]}}</script>
  <script src="base.js" defer></script>
</head>
<body class="page">
{header(slug)}
  <main id="conteudo">
{body}
  </main>

{FOOTER}</body>
</html>
'''
    open(slug, "w").write(html)


def hero(id_, crumb, label, title, lead, photo=None, crown=True):
    ph = f'''
        <div class="photo page-hero__img" style="--ar: 21/8">{photo}</div>''' if photo else ""
    wm = '\n      <span class="wm-mark wm-mark--crown crown" aria-hidden="true" style="top:8%;right:3%;width:180px;rotate:-10deg"></span>' if crown else ""
    return f'''    <section class="page-hero" aria-labelledby="{id_}">{wm}
      <div class="container">
        <nav class="crumbs" aria-label="Você está em"><a href="./">Início</a> <span aria-hidden="true">/</span> <span aria-current="page">{crumb}</span></nav>
        <div class="page-hero__text">
          <p class="label">{label}</p>
          <h1 id="{id_}">{title}</h1>
          <p class="lead">{lead}</p>
        </div>{ph}
      </div>
    </section>
'''


def facts(rows):
    return "\n".join(f'          <div class="fact"><dt>{k}</dt><dd>{v}</dd></div>' for k, v in rows)


# ---------------------------------------------------------------- dados da matriz
wb = openpyxl.load_workbook(XLSX, data_only=True)
ws = wb.worksheets[0]
DISC = []
for r in list(ws.iter_rows(values_only=True))[1:]:
    if not r[0]:
        continue
    nome = str(r[0]).strip().replace("Enfase", "Ênfase")
    DISC.append(dict(nome=nome, comp=str(r[1]).strip(), eixo=str(r[2]).strip(), area=str(r[3]).strip(),
                     sem=str(r[4]).strip(), cod=str(r[5]).strip()))
SEMS = collections.OrderedDict()
for d in DISC:
    SEMS.setdefault(d["sem"], []).append(d)
EIXOS = collections.Counter(d["eixo"] for d in DISC)
COMPS = list(dict.fromkeys(d["comp"] for d in DISC if d["comp"] != "Projeto Integrador"))
N_PI = sum(1 for d in DISC if d["eixo"] == "Projeto Integrador")

# ---------------------------------------------------------------- A Faculdade
fotos_faculdade = [("06", "Turma em volta da mesa na oficina de joalheria"), ("v04-3", "Professora dando aula para a turma no auditório"),
                   ("23", "Duas alunas sorrindo para a câmera à mesa do jantar"), ("v05-39", "Turma reunida na visita ao Pequeno Cotolengo")]
page("a-faculdade.html", "A Faculdade",
     "Faculdade Nine: instituição de ensino superior mantida pelo Conselho Educacional Nine, em Curitiba/PR.",
     hero("t-faculdade", "A Faculdade", "Faculdade Nine", "Formar jovens que influenciam todas as áreas da sociedade.",
          "A Nine Academia de Influência está se tornando a Faculdade Nine: uma instituição de ensino superior em Curitiba, mantida pelo Conselho Educacional Nine.",
          img("24", "Turma da Faculdade Nine de jaleco reunida no laboratório", eager=True)) + f'''
    <section class="section" aria-labelledby="t-quem">
      <span class="wm-mark wm-mark--crown crown" aria-hidden="true" style="bottom:6%;left:4%;width:150px;rotate:10deg"></span>
      <div class="container grid-12">
        <h2 class="label section-aside" id="t-quem">Quem somos</h2>
        <div class="prose">
          <p class="prose__big">Acreditamos que todo jovem precisa descobrir seu propósito no início da vida adulta. E que esse propósito não fica só dentro da igreja: ele vai para os negócios, a política, a educação, a arte, a ciência e a comunicação.</p>
          <p>A formação da Nine se apoia em três pilares: <strong>conhecer</strong> a própria identidade, <strong>treinar</strong> habilidades e <strong>inspirar</strong> o mundo ao redor.</p>
        </div>
      </div>
    </section>

    <section class="section section--navy" aria-labelledby="t-ident">
      <span class="wm-mark wm-mark--nine" aria-hidden="true" style="bottom:-6%;right:-6vw;rotate:-3deg"></span>
      <div class="container grid-12">
        <h2 class="label section-aside" id="t-ident">Dados institucionais</h2>
        <dl class="facts">
{facts([("Instituição", "Faculdade Nine"), ("Mantenedora", "Conselho Educacional Nine"),
        ("CNPJ da mantenedora", "61.991.971/0001-35"),
        ("Endereço", "Rua Engenheiro Niepce da Silva, 139 · Portão · Curitiba/PR · CEP " + TBC),
        ("Direção-Geral", "Raul Cesar Sindlinger"),
        ("Código e-MEC", TBC), ("Ato de credenciamento", TBC)])}
        </dl>
      </div>
    </section>

    <section class="section" aria-labelledby="t-mvv">
      <div class="container grid-12">
        <h2 class="label section-aside" id="t-mvv">Missão, visão e valores</h2>
        <div class="cards cards--3">
          <article class="card"><h3>Missão</h3><p>{TBC} Conforme o Plano de Desenvolvimento Institucional (PDI).</p></article>
          <article class="card"><h3>Visão</h3><p>{TBC} Conforme o PDI.</p></article>
          <article class="card"><h3>Valores</h3><p>{TBC} Conforme o PDI.</p></article>
        </div>
      </div>
    </section>

    <section class="section section--tint" aria-labelledby="t-gov">
      <div class="container grid-12">
        <h2 class="label section-aside" id="t-gov">Gestão e órgãos colegiados</h2>
        <div class="cards cards--2">
          <article class="card"><h3>Direção-Geral</h3><p>Raul Cesar Sindlinger, Diretor-Geral. A Ouvidoria é vinculada diretamente à Direção-Geral.</p></article>
          <article class="card"><h3>Conselho Superior (CONSUP)</h3><p>Órgão colegiado superior da Faculdade. Composição: {TBC}</p></article>
          <article class="card"><h3>Comissão Própria de Avaliação (CPA)</h3><p>Conduz a autoavaliação institucional, nos termos da Lei nº 10.861/2004. Composição: {TBC}</p></article>
          <article class="card"><h3>Secretaria Geral</h3><p>Atendimento acadêmico: <a href="mailto:{EMAIL}">{EMAIL}</a> · Telefone {TBC}</p></article>
        </div>
        <p class="note">A composição atualizada do CONSUP e da CPA é publicada em <a href="transparencia.html">Transparência Institucional</a>.</p>
      </div>
    </section>

    <section class="section" aria-labelledby="t-vida">
      <div class="container">
        <header class="section-head grid-12">
          <h2 class="label section-aside" id="t-vida">Vida acadêmica</h2>
          <p class="prose__big strip-lead">Aula, oficina, serviço e convivência: a formação acontece dentro e fora da sala.</p>
        </header>
        <ul class="strip">
''' + "\n".join(f'          <li class="photo" style="--ar: 3/4">{img(i, a, full=False)}</li>' for i, a in fotos_faculdade) + '''
        </ul>
      </div>
    </section>
''')

# ---------------------------------------------------------------- Curso
def tabela(sem, ds):
    linhas = "\n".join(
        f'              <tr><td class="mono">{d["cod"]}</td><th scope="row">{d["nome"]}</th><td>{d["eixo"]}</td><td>{d["area"]}</td><td>{TBC}</td></tr>'
        for d in ds)
    aberto = " open" if sem == "1º" else ""
    return f'''        <details class="sem"{aberto}>
          <summary><span>{sem} semestre <span class="sem__count">{len(ds)} disciplinas</span></span></summary>
          <div class="table-wrap" tabindex="0" role="region" aria-label="Disciplinas do {sem} semestre (role para os lados)">
            <table class="table">
              <thead><tr><th scope="col">Código</th><th scope="col">Disciplina</th><th scope="col">Eixo formativo</th><th scope="col">Área</th><th scope="col">Carga horária</th></tr></thead>
              <tbody>
{linhas}
              </tbody>
            </table>
          </div>
        </details>'''

eixos_html = "\n".join(f'          <li><span class="eixo__n">{n}</span> {e}</li>' for e, n in EIXOS.most_common())
comps_html = "\n".join(f"            <li>{c}.</li>" for c in COMPS)
page("curso.html", "Curso",
     f"Curso superior da Faculdade Nine: {len(SEMS)} semestres, {len(DISC)} disciplinas, matriz curricular e forma de ingresso.",
     hero("t-curso", "Curso", "Graduação · Faculdade Nine", "Curso superior de [nome a confirmar]",
          f"Uma formação em gestão em {len(SEMS)} semestres, com {len(DISC)} disciplinas e {N_PI} projetos integradores, para quem quer liderar com propósito.",
          img("12", "Turma reunida ouvindo e debatendo com o professor", eager=True)) + f'''
    <section class="section section--tight" aria-labelledby="t-ficha">
      <div class="container grid-12">
        <h2 class="label section-aside" id="t-ficha">Ficha do curso</h2>
        <dl class="facts">
{facts([("Denominação", TBC), ("Grau", TBC), ("Modalidade", TBC), ("Duração", f"{len(SEMS)} semestres"),
        ("Disciplinas", f"{len(DISC)}, sendo {N_PI} projetos integradores"), ("Carga horária total", TBC),
        ("Turno e vagas", TBC), ("Ato autorizativo", TBC), ("Coordenação do curso", TBC)])}
        </dl>
      </div>
    </section>

    <section class="section section--navy" aria-labelledby="t-perfil">
      <span class="wm-mark wm-mark--nine" aria-hidden="true" style="top:4%;right:-8vw;rotate:3deg"></span>
      <div class="container grid-12">
        <h2 class="label section-aside" id="t-perfil">O que você vai aprender a fazer</h2>
        <div class="prose">
          <ul class="checks">
{comps_html}
          </ul>
        </div>
      </div>
    </section>

    <section class="section" aria-labelledby="t-eixos">
      <span class="wm-mark wm-mark--crown crown" aria-hidden="true" style="top:10%;left:3%;width:140px;rotate:-10deg"></span>
      <div class="container grid-12">
        <h2 class="label section-aside" id="t-eixos">Eixos formativos</h2>
        <ul class="eixos">
{eixos_html}
        </ul>
      </div>
    </section>

    <section class="section section--tint" id="matriz" aria-labelledby="t-matriz">
      <div class="container">
        <header class="section-head grid-12">
          <div class="section-aside"><p class="label">Matriz curricular</p></div>
          <div class="prose">
            <h2 id="t-matriz">Matriz curricular</h2>
            <p class="note">Última atualização: {HOJE}. A carga horária por disciplina será publicada com o Projeto Pedagógico do Curso (PPC).</p>
          </div>
        </header>
''' + "\n".join(tabela(s, ds) for s, ds in SEMS.items()) + f'''
      </div>
    </section>

    <section class="section" aria-labelledby="t-ingresso">
      <div class="container grid-12">
        <h2 class="label section-aside" id="t-ingresso">Forma de ingresso</h2>
        <div class="prose">
          <p class="prose__big">O ingresso é por processo seletivo, com regras publicadas em edital.</p>
          <p>Edital, datas, documentos exigidos e número de vagas: {TBC}</p>
          <p><a class="btn" href="./#aplicar">Fazer pré-inscrição {ARROW}</a></p>
          <p class="note">O Projeto Pedagógico do Curso (PPC) e os atos regulatórios ficam disponíveis em <a href="transparencia.html">Transparência Institucional</a>.</p>
        </div>
      </div>
    </section>
''')

# ---------------------------------------------------------------- Transparência
DOCS = [
    ("Plano de Desenvolvimento Institucional (PDI)", "Planejamento da Faculdade para o período vigente.", "a-publicar", None, None),
    ("Projeto Pedagógico Institucional (PPI)", "Quando constituir documento próprio.", "a-publicar", None, None),
    ("Regimento Interno", "Normas de organização e funcionamento da Faculdade.", "a-publicar", None, None),
    ("Regulamento da Ouvidoria e da Comunicação Institucional", "Canais, prazos e regras de transparência e de comunicação.", "em-aprovacao", None, "ouvidoria.html"),
    ("Projetos Pedagógicos dos Cursos (PPC)", "Projeto pedagógico de cada curso.", "a-publicar", None, None),
    ("Matrizes curriculares", "Disciplinas do curso por semestre.", "publicado", HOJE, "curso.html#matriz"),
    ("Calendário acadêmico", "Datas do período letivo.", "a-publicar", None, None),
    ("Atos regulatórios", "Credenciamento da Instituição e autorização, reconhecimento e renovação de reconhecimento dos cursos, quando houver.", "a-publicar", None, None),
    ("Composição do CONSUP e da CPA", "Membros do Conselho Superior e da Comissão Própria de Avaliação.", "a-publicar", None, None),
    ("Relatórios da Ouvidoria (síntese)", "Publicada em até 30 dias após a apreciação pelo CONSUP, sem dados pessoais.", "sem-registro", None, None),
    ("Resultados das avaliações interna e externa", "Relatório da CPA com resumo executivo e resultados do INEP/MEC.", "sem-registro", None, None),
    ("Política de privacidade e proteção de dados pessoais", "Como a Faculdade trata dados pessoais (Lei nº 13.709/2018).", "a-publicar", None, "privacidade.html"),
]
ST = {"publicado": "Publicado", "em-aprovacao": "Em aprovação no CONSUP", "a-publicar": "Em elaboração", "sem-registro": "Nenhum publicado até o momento"}


def doc(t, d, st, data, href):
    titulo = f'<a href="{href}">{t}</a>' if href else t
    return f'''          <li class="doc">
            <div class="doc__main"><h3>{titulo}</h3><p>{d}</p></div>
            <p class="status status--{st}">{ST[st]}</p>
            <p class="doc__date">Última atualização: {data or "—"}</p>
          </li>'''


page("transparencia.html", "Transparência Institucional",
     "Documentos institucionais, atos regulatórios, relatórios da Ouvidoria e resultados das avaliações da Faculdade Nine.",
     hero("t-transp", "Transparência Institucional", "Acesso livre, sem cadastro", "Transparência Institucional",
          "Documentos e informações institucionais da Faculdade Nine, publicados em formato pesquisável e mantidos atualizados, conforme o Regulamento da Ouvidoria e da Comunicação Institucional.",
          img("21", "Turma da Faculdade Nine reunida em um jantar sob o pergolado", eager=True)) + f'''
    <section class="section section--tight" aria-labelledby="t-docs">
      <div class="container">
        <h2 class="sr-only" id="t-docs">Documentos</h2>
        <ul class="docs">
{chr(10).join(doc(*d) for d in DOCS)}
        </ul>
        <p class="note">A área é revisada ao menos uma vez por período letivo. Os documentos são encaminhados pelos setores responsáveis em até 10 dias úteis após sua aprovação ou alteração. Não são publicados dados pessoais nem informações protegidas por sigilo legal.</p>
      </div>
    </section>

    <section class="section section--navy" aria-labelledby="t-emec">
      <span class="wm-mark wm-mark--nine" aria-hidden="true" style="bottom:-14%;right:-6vw;rotate:-3deg"></span>
      <div class="container grid-12">
        <h2 class="label section-aside" id="t-emec">Cadastro no e-MEC</h2>
        <div class="prose">
          <p class="prose__big">Situação regulatória da Faculdade e de seus cursos no Ministério da Educação.</p>
          <p>Selo, QR Code e link para o cadastro da Instituição no e-MEC: {TBC} Serão publicados aqui e no rodapé assim que disponibilizados pelo sistema.</p>
          <p><a href="https://emec.mec.gov.br/">Consultar instituições no e-MEC</a></p>
        </div>
      </div>
    </section>
''', )

# ---------------------------------------------------------------- Ouvidoria
page("ouvidoria.html", "Ouvidoria",
     "Ouvidoria da Faculdade Nine: canal para reclamações, denúncias, sugestões, elogios e pedidos de informação, com sigilo e prazos definidos.",
     hero("t-ouv", "Ouvidoria", "Canal institucional", "Ouvidoria",
          "Canal de comunicação entre a Faculdade Nine e as comunidades acadêmica e externa para receber, registrar, encaminhar e responder manifestações.",
          img("23", "Duas alunas sorrindo à mesa durante um encontro da turma", eager=True)) + f'''
    <section class="section section--tight" aria-labelledby="t-quem-pode">
      <span class="wm-mark wm-mark--crown crown" aria-hidden="true" style="bottom:8%;left:3%;width:150px;rotate:12deg"></span>
      <div class="container grid-12">
        <h2 class="label section-aside" id="t-quem-pode">Quem pode se manifestar</h2>
        <div class="prose">
          <p class="prose__big">Estudantes, docentes, técnicos-administrativos, egressos, candidatos, pais ou responsáveis e demais membros da comunidade externa.</p>
          <p>A Ouvidoria é vinculada diretamente à Direção-Geral, sem subordinação às demais direções e coordenações. Ela não substitui os requerimentos acadêmicos e administrativos da Secretaria Geral: procure-a quando não obtiver resposta ou atendimento adequado pelos canais ordinários.</p>
        </div>
      </div>
    </section>

    <section class="section section--tint" aria-labelledby="t-tipos">
      <div class="container grid-12">
        <h2 class="label section-aside" id="t-tipos">Tipos de manifestação</h2>
        <div class="cards cards--3">
          <article class="card"><h3>Reclamação</h3><p>Insatisfação com serviço, atendimento ou conduta.</p></article>
          <article class="card"><h3>Denúncia</h3><p>Comunicação de irregularidade ou de ato ilícito, inclusive assédio e discriminação.</p></article>
          <article class="card"><h3>Sugestão</h3><p>Proposta de melhoria.</p></article>
          <article class="card"><h3>Elogio</h3><p>Reconhecimento de serviço, atendimento ou conduta.</p></article>
          <article class="card"><h3>Solicitação de informação</h3><p>Pedido de esclarecimento não atendido pelos canais ordinários.</p></article>
        </div>
      </div>
    </section>

    <section class="section section--navy" aria-labelledby="t-prazos">
      <span class="wm-mark wm-mark--nine" aria-hidden="true" style="top:-4%;left:-6vw;rotate:3deg"></span>
      <div class="container grid-12">
        <h2 class="label section-aside" id="t-prazos">Prazos de atendimento</h2>
        <ol class="steps">
          <li><p class="steps__n">Registro</p><p>O sistema gera um número de protocolo e envia a confirmação, com cópia da manifestação, para o seu e-mail.</p></li>
          <li><p class="steps__n">Até 5 dias úteis</p><p>A Direção-Geral analisa a manifestação e a encaminha ao setor competente, ou a trata diretamente.</p></li>
          <li><p class="steps__n">Até 10 dias úteis</p><p>O setor responde à Ouvidoria com as providências adotadas.</p></li>
          <li><p class="steps__n">Até 20 dias úteis</p><p>Você recebe a resposta conclusiva por e-mail. O prazo pode ser prorrogado uma única vez, por igual período, com justificativa.</p></li>
        </ol>
      </div>
    </section>

    <section class="section section--tint" aria-labelledby="t-sigilo">
      <div class="container grid-12">
        <h2 class="label section-aside" id="t-sigilo">Sigilo e proteção de dados</h2>
        <div class="prose">
          <p>Sua identidade e o conteúdo da manifestação são mantidos em sigilo. No encaminhamento ao setor, a identidade é omitida, salvo quando indispensável e com a sua autorização, e você pode pedir que ela não seja revelada em nenhuma hipótese.</p>
          <p>Os dados pessoais são tratados conforme a Lei nº 13.709/2018 (LGPD), apenas para registro, resposta e relatórios. É vedada qualquer retaliação a quem se manifesta de boa-fé.</p>
          <p class="note">Relatórios semestrais, sem identificação dos manifestantes, são publicados em <a href="transparencia.html">Transparência Institucional</a>.</p>
        </div>
      </div>
    </section>

    <section class="aplicar" id="manifestacao" aria-labelledby="t-form">
      <div class="container grid-12">
        <header class="aplicar__head">
          <span class="aplicar__crown crown" aria-hidden="true"></span>
          <h2 id="t-form">Registre sua manifestação</h2>
          <p class="lead">Acesso livre, sem cadastro. Os campos marcados como opcionais podem ficar em branco.</p>
          <p class="lead">Se preferir, escreva para <a class="link-gold" href="mailto:{EMAIL}">{EMAIL}</a>.</p>
        </header>

        <form class="form" data-ouvidoria novalidate>
          <fieldset>
            <legend>Identificação</legend>
          <div class="field">
            <label for="o-nome">Nome</label>
            <input id="o-nome" name="nome" type="text" autocomplete="name" required>
          </div>
          <div class="field">
            <label for="o-email">E-mail</label>
            <input id="o-email" name="email" type="email" autocomplete="email" required>
          </div>
          <div class="field">
            <label for="o-vinculo">Vínculo com a Instituição</label>
            <select id="o-vinculo" name="vinculo" required>
              <option value="" selected disabled>Selecione</option>
              <option>Estudante</option><option>Docente</option><option>Técnico-administrativo</option><option>Egresso</option>
              <option>Candidato</option><option>Pai, mãe ou responsável</option><option>Comunidade externa</option>
            </select>
          </div>
          </fieldset>
          <fieldset>
            <legend>Manifestação</legend>
          <div class="field">
            <label for="o-tipo">Tipo de manifestação</label>
            <select id="o-tipo" name="tipo" required>
              <option value="" selected disabled>Selecione</option>
              <option>Reclamação</option><option>Denúncia</option><option>Sugestão</option><option>Elogio</option><option>Solicitação de informação</option>
            </select>
          </div>
          <div class="field field--full">
            <label for="o-descricao">Descrição dos fatos</label>
            <textarea id="o-descricao" name="descricao" rows="6" required></textarea>
          </div>
          <div class="field field--full">
            <label for="o-anexos">Anexos <span class="opt">(opcional)</span></label>
            <input id="o-anexos" name="anexos" type="file" multiple>
          </div>
          </fieldset>
          <div class="field field--hp" aria-hidden="true">
            <label for="o-website">Website</label>
            <input id="o-website" name="website" type="text" autocomplete="off">
          </div>
          <div class="field field--full field--check">
            <input id="o-sigilo" name="sigilo_total" type="checkbox">
            <label for="o-sigilo">Não quero que minha identidade seja revelada em nenhuma hipótese.</label>
          </div>
          <div class="field field--full field--check">
            <input id="o-lgpd" name="consentimento" type="checkbox" required>
            <label for="o-lgpd">Concordo com o tratamento dos meus dados para o registro e a resposta desta manifestação, conforme a <a href="privacidade.html">Política de privacidade</a>.</label>
          </div>
          <div class="field--full">
            <button class="btn btn--gold" type="submit">Enviar manifestação {ARROW}</button>
            <p class="form__status" data-status role="status" aria-live="polite"></p>
          </div>
        </form>
      </div>
    </section>
''')

# ---------------------------------------------------------------- Privacidade
page("privacidade.html", "Política de privacidade",
     "Política de privacidade e proteção de dados pessoais da Faculdade Nine.",
     hero("t-priv", "Política de privacidade", "Lei nº 13.709/2018 (LGPD)", "Política de privacidade",
          "Como a Faculdade Nine trata os dados pessoais de candidatos, estudantes, colaboradores e visitantes.",
          img("11", "Instrutor conduzindo uma oficina prática com a turma", eager=True)) + f'''
    <section class="section section--tight" aria-labelledby="t-priv-status">
      <span class="wm-mark wm-mark--crown crown" aria-hidden="true" style="bottom:10%;left:4%;width:150px;rotate:-8deg"></span>
      <div class="container grid-12">
        <h2 class="label section-aside" id="t-priv-status">Situação</h2>
        <div class="prose">
          <p class="prose__big">O texto completo da política está em elaboração e será publicado nesta página. {TBC}</p>
          <dl class="facts facts--1">
{facts([("Controlador", "Conselho Educacional Nine · CNPJ 61.991.971/0001-35"),
        ("Endereço", "Rua Engenheiro Niepce da Silva, 139 · Portão · Curitiba/PR"),
        ("Contato para assuntos de dados pessoais", f'<a href="mailto:{EMAIL}">{EMAIL}</a>'),
        ("Encarregado (DPO)", TBC)])}
          </dl>
          <p class="note">Enquanto isso, os dados enviados pelos formulários do site são usados apenas para a finalidade informada em cada um: pré-inscrição no processo seletivo ou registro e resposta de manifestações na Ouvidoria.</p>
        </div>
      </div>
    </section>
''')

# ---------------------------------------------------------------- Home: cabeçalho e rodapé comuns
h = open("index.html").read()
s = h.index('  <nav class="a11y-bar"') if '<nav class="a11y-bar"' in h else h.index('  <a class="skip" href="#conteudo">')
e = h.index('  <main id="conteudo">')
h = h[:s] + header("./") + "\n" + h[e:]
s = h.index('  <footer class="footer"'); e = h.index('  </footer>\n') + len('  </footer>\n')
h = h[:s] + FOOTER + h[e:]
open("index.html", "w").write(h)

# Jornada da home com os semestres reais
st = "\n".join(
    f'''          <li class="station" data-reveal="fade-up"><p class="station__month">{s} semestre</p><p class="station__focus">{len(ds)} disciplinas</p><ul class="station__list">{"".join(f"<li>{d['nome']}</li>" for d in ds)}</ul></li>'''
    for s, ds in SEMS.items())
h = open("index.html").read()
h = re.sub(r'(<ol class="jornada__track container">\n)(?:.*\n)*?(\s*</ol>)', lambda m: m.group(1) + st + "\n" + m.group(2).lstrip("\n"), h, count=1)
open("index.html", "w").write(h)
print("ok", len(DISC), "disciplinas;", {k: len(v) for k, v in SEMS.items()}, dict(EIXOS))


# ---------------------------------------------------------------- style="" -> classes utilitárias
import glob, hashlib, os
regras = {}
def _tag(m):
    tag = m.group(0)
    st = re.search(r'\s+style="([^"]*)"', tag)
    if not st:
        return tag
    nome = "u-" + hashlib.md5(st.group(1).strip().rstrip(";").encode()).hexdigest()[:6]
    regras[nome] = st.group(1).strip().rstrip(";")
    tag = tag.replace(st.group(0), "")
    if re.search(r'\sclass="', tag):
        return re.sub(r'\sclass="([^"]*)"', lambda c: f' class="{c.group(1)} {nome}"', tag, count=1)
    return tag[:-1].rstrip("/").rstrip() + f' class="{nome}">'
def _srcset(m):
    tag, base = m.group(0), m.group(1)
    if "srcset=" in tag or not os.path.exists(f"assets/img/galeria/{base}-320.webp"):
        return tag
    return tag.replace(f'src="assets/img/galeria/{base}-600.webp"',
        f'src="assets/img/galeria/{base}-600.webp" srcset="assets/img/galeria/{base}-320.webp 320w, assets/img/galeria/{base}-600.webp 600w" sizes="(min-width: 1024px) 30vw, 60vw"')
for arq in glob.glob("*.html"):
    t = re.sub(r"<[a-zA-Z][^<>]*>", _tag, open(arq).read())
    t = re.sub(r'<img [^>]*src="assets/img/galeria/([\w-]+)-600\.webp"[^>]*>', _srcset, t)
    assert ' style="' not in t, arq
    open(arq, "w").write(t)
css = open("style.css").read()
INI, FIM = "/* utilitários gerados (gerar-paginas.py) */", "/* fim dos utilitários gerados */"
if INI in css:  # mantém as regras de execuções anteriores (o HTML já convertido não as traz de volta)
    for k, v in re.findall(r"^\.(u-[0-9a-f]{6}) \{ (.*); \}$", css[css.index(INI):css.index(FIM)], re.M):
        regras.setdefault(k, v)
    css = css[:css.index(INI)] + css[css.index(FIM) + len(FIM):]
    css = css.rstrip() + "\n"
css += "\n" + INI + "\n" + "\n".join(f".{k} {{ {re.sub(r'rotate:\s*(-?[0-9.]+deg)', r'transform: rotate(\1)', v)}; }}" for k, v in sorted(regras.items())) + "\n" + FIM + "\n"
open("style.css", "w").write(css)
print(len(regras), "estilos inline viraram classes")


# ---------------------------------------------------------------- CSS embutido (evita a requisição que bloqueia a renderização)
# style.css continua sendo a fonte; cada página recebe a versão minificada dentro de <style id="css">.
def _minifica(css):
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    css = re.sub(r"\s+", " ", css)
    css = re.sub(r"\s*([{};,>])\s*", r"\1", css)
    css = re.sub(r":\s+", ":", css)  # só depois do ":" (antes dele o espaço muda o seletor, ex.: ".aplicar :focus")
    return css.replace(";}", "}").strip()
mini = _minifica(open("style.css").read())
for arq in glob.glob("*.html"):
    t = open(arq).read()
    bloco = f'<style id="css">{mini}</style>'
    t = re.sub(r'<link rel="stylesheet" href="style.css">|<style id="css">.*?</style>', lambda m: bloco, t, count=1, flags=re.S)
    open(arq, "w").write(t)
print("CSS embutido:", len(mini) // 1024, "KB")
