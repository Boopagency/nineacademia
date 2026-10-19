# Nine Academia de Influência: guia de construção do site

> Coloque este arquivo na raiz do projeto com o nome `CLAUDE.md`. O Claude Code lê automaticamente e usa como briefing em toda sessão.
> Tudo marcado com **[A CONFIRMAR]** é dado que ainda precisa vir da Nine. Nunca invente esses dados: deixe um placeholder visível.

**Arquivos de referência no repositório (abra antes de começar):**
- `referencias/site-atual.png`: print completo do site atual (9ai.com.br). Base de conteúdo e das colagens, e exemplo do que NÃO repetir no layout.
- `referencias/referencia-oxford.png`: referência visual de estrutura (hero, grid, nav, cards de números).
- `assets/logo/nine-logo-branco.png`: logo atual (coroa dourada + "NINE" branco, fundo transparente). Só funciona sobre fundo escuro; ver seção 3 › Logo.

---

## 1. Contexto

**Cliente:** Nine Academia de Influência (domínio atual `9ai.com.br`, Instagram `@nine.academia`)
**O que é:** curso de formação cristão de 9 meses para jovens no início da vida adulta. Lema: **Conhecer, Treinar, Inspirar**.
**Objetivo do site:** transmitir uma instituição séria e desejável (nível "universidade de elite") e **converter em aplicações** para a próxima turma.
**Conversão principal:** formulário de aplicação no próprio site.

### O que está errado no site atual (não repetir)
- Nenhum caminho de conversão: os botões "Quero fazer parte!" não levam a lugar nenhum útil, e não há preço, data nem vagas.
- Nenhum rosto: não há fundadores, mentores, alunos nem depoimentos.
- Texto miúdo e cinza, com pouco contraste e hierarquia fraca.
- Conteúdo escondido em accordions, como se fosse FAQ.
- Seção "Mundo sofisticado" sem contexto.
- Rodapé "2023", erros de digitação e textos duplicados.

### O que está CERTO e deve ser mantido
- **Navy + dourado** da marca.
- **Coroa** do logo.
- **As colagens**: fotos P&B em retícula (halftone) de atletas vintage com pinceladas coloridas, dentro de molduras em **arco**. É o ativo visual mais original da Nine e é o que vai fazer o site "fora do padrão".
- A estrutura dos 3 pilares e das trilhas.

---

## 2. Direção criativa: "Instituição + Movimento"

Duas camadas, sempre em tensão:

| Camada | De onde vem | Como aparece |
|---|---|---|
| **Instituição** | Referência Oxford (Aryan Choudhary / LX Studio) | Fundo claro, grid com linhas verticais finas visíveis, nav em "pílulas", hero em card arredondado com wordmark gigante translúcido, frase-manifesto em dois tons, cards de números com rótulo dourado, botões navy com ícone de seta em caixa |
| **Movimento** | DNA da Nine (colagens + coroa) | Colagens em arco, pinceladas coloridas que se "desenham" no scroll, cor de acento por pilar, coroa como elemento de motion |

**Regra de ouro:** 80% Instituição (calmo, branco, navy, muito respiro) e 20% Movimento (cor e energia nos momentos-chave). A cor saturada só aparece nas colagens, nos traços e nos acentos de cada pilar, nunca em blocos de fundo grandes.

**Sensação alvo:** "Isso aqui é sério, é bonito e é pra mim." Nada de estética de igreja genérica (fundo de céu, pomba, gradiente roxo).

### Princípio central: gerar VONTADE, não só informar
A força da Nine está nas redes: gente real, turma, energia. O site precisa provocar no visitante o "meu Deus, eu quero entrar nisso". Regras:
1. **Mostrar antes de explicar.** A galeria vem logo depois do manifesto, antes dos detalhes do programa. Primeiro a pessoa sente, depois entende.
2. **Gente em toda dobra.** Cada seção tem pelo menos um rosto real. Texto sem pessoas por perto esfria.
3. **Pertencimento.** Fale com "você" e "sua turma". O desejo é fazer parte de um grupo, não "comprar um curso".
4. **Transformação.** Depoimentos no formato *antes → depois* ("entrei sem saber o que fazer da vida; hoje...").
5. **Escassez honesta.** Vagas e prazo aparecem só se forem reais.
6. **CTA sempre à mão.** Depois da galeria, um CTA fixo acompanha o scroll até o formulário.

---

## 3. Design tokens

### Cores (amostradas do logo e do site atual)
```css
:root {
  /* Base */
  --navy:        #111749;  /* cor principal: títulos, botões, rodapé */
  --navy-90:     #1C2257;
  --gold:        #F5B310;  /* coroa e rótulos SOBRE navy */
  --paper:       #FAFAF7;  /* fundo principal */
  --paper-2:     #F2F2EE;  /* cards */
  --ink:         #111749;
  --ink-muted:   #6B6F8A;  /* texto secundário */
  --line:        rgba(17, 23, 73, .08); /* linhas do grid */

  /* Acentos das colagens: uso decorativo */
  --green:  #21CF8A;  /* Pilar 01 · Conhecer */
  --coral:  #FF4645;  /* Pilar 02 · Treinar  */
  --violet: #8B3BEB;  /* Pilar 03 · Inspirar */
  --blue:   #1A2BFA;
  --lime:   #BBEA00;
  --orange: #FF6A13;
}
```

**Contraste (obrigatório):**
- Dourado sobre branco tem contraste ≈ 1,8:1 e **reprova**. Use dourado como texto **só sobre navy** (≈ 9:1). Sobre fundo claro, ele é só decoração (coroa, traços, ícones) ou rótulo grande ≥ 24px em negrito, e mesmo assim evite.
- Verde e lime sobre branco: apenas decoração.
- Coral sobre branco (≈ 3,4:1): só em texto grande.
- Texto corrido sempre `--navy` ou `--ink-muted` sobre `--paper`.

### Tipografia
- **Família única:** `Inter Tight` (Google Fonts), pesos 400 / 500 / 600 / 700. Grotesca, limpa e próxima da referência.
- Display com tracking negativo (`letter-spacing: -0.03em`), line-height 0.95–1.05.
- Escala fluida:
```css
--fs-mega:  clamp(5rem, 18vw, 20rem);   /* wordmark NINE no hero e no rodapé */
--fs-h1:    clamp(2.75rem, 6vw, 5.5rem);
--fs-h2:    clamp(2rem, 4vw, 3.5rem);
--fs-h3:    clamp(1.25rem, 2vw, 1.75rem);
--fs-body:  clamp(1rem, 1.1vw, 1.125rem);
--fs-label: .8125rem; /* uppercase, tracking .08em */
```
- Corpo de texto **mínimo 16px**. O site atual usa ~12px cinza, e isso é parte do problema.

### Forma e espaço
- Grid de 12 colunas, `max-width: 1440px`, gutter 24px, margem lateral `clamp(16px, 4vw, 48px)`.
- **Linhas verticais do grid visíveis** (1px `--line`) em `position: fixed` atrás do conteúdo, como na referência. Use 5 linhas no desktop e 3 no mobile.
- Raio: `--r-card: 24px`, `--r-btn: 12px`, `--r-pill: 999px`.
- **Máscara em arco** para imagens dos pilares: `border-radius: 999px 999px 24px 24px`.
- Espaçamento vertical entre seções: `clamp(96px, 14vw, 200px)`.

### Logo
- O PNG atual tem coroa dourada e "NINE" **branco**, então só funciona sobre navy ou foto escura.
- **Pedir ou vetorizar em SVG** com `fill="currentColor"` no wordmark, para gerar a versão navy (fundo claro) e a branca (fundo escuro) a partir do mesmo arquivo. A coroa fica sempre `--gold`.

---

## 4. Stack (simples de propósito)

```
/
├── CLAUDE.md
├── index.html
├── style.css
├── main.js
├── assets/
│   ├── img/      (AVIF/WebP + fallback JPG)
│   ├── video/    (MP4 H.264, curtos, sem áudio)
│   └── logo/     (nine-logo-branco.png hoje; nine.svg + crown.svg quando vetorizar)
└── referencias/  (prints de referência: NÃO publicar, não linkar no site)
```

- **HTML, CSS e JS puros.** Sem framework e sem build.
- Bibliotecas via CDN, com versão fixa:
  - `gsap` + `ScrollTrigger` + `SplitText` (todos gratuitos desde a versão 3.13)
  - `lenis` (smooth scroll)
- Fonte: Google Fonts (`Inter Tight`), com `preconnect` + `display=swap`.
- Formulário: **Supabase** (insert direto via REST, RLS de só inserção). Ver seção 8.
- Deploy: **Vercel** (estático).

Nada além disso. Se aparecer vontade de adicionar React, Tailwind ou um slider pronto, não adicione.

---

## 5. Mapa da página (one-page) e o que cada seção faz

Nav: `Sobre · Vida na Nine · Programa · Trilhas · FAQ` com o botão **Aplicar** (navy) à direita.

**Ordem na página:** Preloader → Nav → Hero → Manifesto → **Vida na Nine (galeria)** → Números → Pilares → Jornada → Trilhas → Quem conduz → Depoimentos → FAQ → Aplicação → Rodapé.

### 0. Preloader (máx. 1,6s, só na primeira visita)
- Fundo navy. Contador `1 → 9` em `--fs-mega` (dígitos rolando verticalmente). No 9, a **coroa cai** de cima com leve bounce e encaixa sobre o "I" do wordmark, que aparece letra por letra.
- Sai com uma cortina de baixo pra cima (`clip-path: inset()`), revelando o hero.
- Grava `sessionStorage` (em try/catch) para não repetir na mesma sessão.

### 1. Navbar
- Estilo referência: links agrupados em **pílulas** com fundo branco e borda `--line`. Logo navy à esquerda e botão **Aplicar** à direita.
- Esconde ao rolar para baixo e reaparece ao rolar para cima. Usa `backdrop-filter: blur(12px)` depois de 80px de scroll.
- Link ativo: um ponto dourado desliza entre os itens (indicador animado).
- Mobile: menu fullscreen navy, com links grandes entrando com stagger.

### 2. Hero (estrutura da referência Oxford)
- **Card arredondado** (`--r-card`) com margem lateral, ocupando ~88vh, com uma **vídeo-montagem de 10–15s feita dos Reels da Nine**: risadas, aula, palco, abraço, turma reunida. Gente real em movimento já no primeiro segundo. Use uma foto forte como `poster`.
- **"NINE" gigante** em branco a ~70% de opacidade atravessando a imagem. Com uma foto recortada (PNG sem fundo) em camada acima, o texto fica **atrás da pessoa** (efeito revista). Sem recorte, o texto vai por cima.
- Canto inferior esquerdo: `Turma 2027` **[A CONFIRMAR]**. No centro-inferior, a chamada curta com o link "Inscrições abertas →". À direita, setas ‹ › se o hero tiver mais de uma imagem.
- Abaixo do card: H1 + subtítulo + 2 botões.
- **Motion:** a imagem entra com `scale 1.15 → 1` e o wordmark sobe letra por letra (SplitText, `yPercent 100 → 0`, stagger .06). No scroll, a imagem faz parallax leve (`yPercent: 10`) e o wordmark se move mais devagar que ela.

### 3. Sobre / Manifesto
- Layout da referência: rótulo pequeno `Sobre a Nine` na coluna esquerda e a frase-manifesto grande na direita.
- **Motion:** a frase começa em `--ink-muted` a 30% e cada palavra vira `--navy` conforme o scroll avança (SplitText em palavras + ScrollTrigger com `scrub`). Na referência isso aparece estático, e aqui ganha vida.

### 4. Vida na Nine (galeria): a seção que gera vontade
É a seção mais importante para a emoção. O objetivo não é documentar, é fazer o visitante **se ver ali**. São três movimentos em sequência:

**4a. Zoom de entrada: "Imagine você aqui."** (desktop, seção pinada)
- Grid **3×3 (o 9 de novo)** de fotos, com um vídeo no centro.
- No scroll, o vídeo central **cresce até ocupar a tela inteira** enquanto as 8 fotos ao redor se afastam para fora e somem com leve rotação.
- Com o vídeo em tela cheia, surge em `--fs-h1` branco: **"Imagine você aqui."**
- Mobile: sem pin. Vídeo em largura total com a frase sobreposta, e as 8 fotos viram uma faixa com `scroll-snap` logo abaixo.

**4b. Mural da turma** (galeria filtrável)
- Chips de filtro: `Tudo · Aulas · Oficinas · Grupos · Intercâmbio · Jantares · Serviço · Formatura`.
- Layout masonry com CSS nativo (`columns: 4` / 3 / 2 conforme a largura). Cada foto tem `data-cat`.
- Na troca de filtro, as fotos se reorganizam suavemente com **GSAP Flip** (gratuito, mesmo pacote do GSAP).
- Hover (desktop): a foto dá zoom de 1.05 e aparece a legenda curta, por exemplo "Oficina de oratória · mês 3".
- Clique: abre **lightbox** em `<dialog>` nativo, com setas, teclado (← → Esc), swipe no mobile e legenda.
- Mostrar 12–16 fotos e depois um botão "Ver mais momentos" que revela o resto. Nada de paginação.

**4c. Parede de Reels**
- Faixa horizontal com 5–7 vídeos verticais (9:16) **exportados do Instagram da Nine e hospedados no próprio site**.
- Só o vídeo do centro toca (muted), e os outros ficam em pausa com o poster. Botão de som no vídeo ativo.
- Mobile: swipe com `scroll-snap`, e toca o vídeo que estiver centralizado.
- Fechamento: "Tem muito mais no **@nine.academia**" com link para o perfil.

**4d. Faixa de CTA**
- Fundo navy, foto da turma em baixa opacidade: **"Na próxima turma, a foto pode ser sua."** + botão **Quero aplicar**.
- A partir daqui aparece o **CTA fixo**: pílula flutuante no desktop (canto inferior direito) e barra inferior no mobile, com o texto "Inscrições abertas · Aplicar →". Ele se esconde quando a seção de Aplicação está visível.

**Regras de curadoria (passar para quem for montar o acervo)**
- **Só fotos reais da Nine.** Banco de imagem mata a vontade na hora.
- Prefira momentos espontâneos a fotos posadas: rostos, grupos, gargalhada, concentração, palco.
- Selecione 30–60 fotos e aplique **o mesmo tratamento de cor em todas** (um preset leve e quente). Isso transforma "fotos de celular" em "feed premium".
- **Autorização de uso de imagem** dos alunos (LGPD). Se algum aluno for menor de idade, a autorização tem que ser dos responsáveis.

**Por que não incorporar o feed do Instagram:** o embed oficial é pesado, quebra o visual e tira o visitante do site. Exportar e curar o conteúdo dá controle total sobre a estética e a velocidade.

**Performance da galeria**
- Miniaturas em AVIF de 600px e versão do lightbox em 1600px, tudo com `loading="lazy"`.
- Reels em 720p, ≤ 1,5MB cada, `preload="none"` + `poster`, e só tocam quando visíveis (IntersectionObserver).

### 5. Nine em números
- Cards `--paper-2` como na referência: rótulo em cima (dourado **só se o card for navy**; nos claros, `--ink-muted`) e número gigante embaixo.
- Dados reais disponíveis: **9** meses · **3** pilares · **7** trilhas · **12+** oficinas práticas. Opcionais: alunos formados e mentores **[A CONFIRMAR]**.
- Um dos cards é navy, para quebrar o ritmo.
- **Motion:** os números contam de 0 ao valor quando entram na tela, uma vez só.

### 6. Os 3 pilares: a seção-assinatura
Seção **pinada** com três capítulos que trocam no scroll (desktop):
- **Esquerda (sticky):** número grande `01 / 02 / 03`, título, frase e uma barra de progresso vertical na cor do pilar.
- **Direita:** colagem em **máscara de arco**. Na troca de capítulo, a nova imagem é revelada com `clip-path` de baixo pra cima e a anterior faz `scale .95` + fade.
- **Pinceladas SVG** (paths com `stroke-dasharray`) se **desenham** ao redor do arco na cor do pilar a cada troca.
- Abaixo do texto ficam os 3 itens do pilar como **cards pequenos sempre visíveis**, não accordion. Cada card tem título e uma linha.
- Mobile: sem pin. Os 3 pilares empilhados, cada um com reveal próprio.

| Pilar | Cor | Itens |
|---|---|---|
| 01 · Conhecer sua identidade | `--green` | Teologia Livre (Fatemi) · Grupos de alinhamento · Grupos de acompanhamento |
| 02 · Treinar suas habilidades | `--coral` | Oficinas práticas · Módulos intensivos · Serviço voluntário |
| 03 · Inspirar o seu mundo | `--violet` | Aulas gerais semanais · Palestras e depoimentos · Intercâmbio cultural |

### 7. A jornada de 9 meses
- **Scroll horizontal pinado** (desktop) com 9 "estações" numa linha do tempo, cada uma com mês, foco e uma frase.
- Um **"9" gigante em outline** no fundo vai sendo **preenchido** (stroke → fill, ou máscara subindo) conforme o progresso.
- Marco visual entre os meses que separam o 1º e o 2º semestre: "Início dos Paths".
- Conteúdo de cada mês: **[A CONFIRMAR]**. Por enquanto, use 1º semestre = base (identidade + oficinas) e 2º semestre = Paths.
- Mobile: lista vertical com uma linha conectando os pontos, desenhada no scroll.

### 8. Trilhas (Paths)
- 7 painéis lado a lado (desktop). Em hover/foco, o painel **expande** (`flex-grow`) e mostra descrição e imagem, enquanto os outros encolhem e exibem só o nome na vertical.
- Mobile: carrossel com `scroll-snap` nativo, sem biblioteca.
- Texto de apoio: "No 2º semestre, você escolhe onde quer influenciar e aprende com professores convidados que são referência na área."

### 9. Quem conduz
- Grid de mentores/professores com foto P&B que ganha cor no hover, nome e área.
- Parceria acadêmica: **Fatemi** (Teologia Livre), com logo se autorizado.
- Nomes, fotos e cargos: **[A CONFIRMAR]**. Enquanto não chegarem, **esconda a seção** em vez de mostrar placeholders genéricos.

### 10. Depoimentos
- Formato **transformação**: uma frase curta de *antes* ("Entrei sem saber que curso fazer...") e uma de *depois* ("...hoje lidero um projeto social na minha cidade"), com foto, nome, idade e trilha.
- Cards de vídeo vertical (9:16) com play, muted por padrão. Os melhores vêm dos Reels de depoimento que a Nine já postou.
- **[A CONFIRMAR]**. Não usar depoimentos inventados. Sem material real, a seção não vai ao ar.

### 11. FAQ
Accordion nativo (`<details>/<summary>`) com animação de altura via CSS (`interpolate-size` ou fallback em JS). Perguntas, todas com resposta **[A CONFIRMAR]**:
- Quem pode participar? (idade mínima)
- Quando começa a próxima turma e quais são os dias e horários?
- É presencial? Onde?
- Quanto custa? Tem bolsa ou parcelamento?
- Preciso ser de alguma igreja específica?
- Como funciona a escolha da trilha?
- Consigo conciliar com faculdade ou trabalho?

### 12. Aplicação (formulário)
- Seção navy, título grande "Sua turma começa aqui." e coroa dourada.
- Formulário em 2 colunas (1 no mobile). Detalhes na seção 8.
- Estado de sucesso: a coroa faz um pequeno "pulo" e aparece a mensagem "Recebemos sua aplicação. Nossa equipe vai falar com você pelo WhatsApp em até X dias. **[A CONFIRMAR]**"

### 13. Rodapé
- Navy. Wordmark **NINE gigante** (`--fs-mega`) **cortado na base** da página, com a coroa dourada.
- Colunas: Programa · Contato (`contato@9ai.com.br`) · Instagram · Política de privacidade.
- `© <ano atual> Nine Academia de Influência`, com o ano gerado por JS. Nunca escrever o ano fixo.

---

## 6. Sistema de motion

### Princípios
1. **Toda animação explica algo** (progresso, hierarquia, transição de capítulo). Nada de animação só por animar.
2. Anime **apenas `transform`, `opacity` e `clip-path`**.
3. Cada coisa anima **uma vez** ao entrar na tela (`once: true`), exceto o que é `scrub`.
4. **No máximo 3 seções pinadas** na página: zoom da galeria, Pilares e Jornada. Nunca duas pinadas seguidas.

### Tokens
```js
const EASE = { out: "power3.out", inOut: "power2.inOut", expo: "expo.out" };
const DUR  = { fast: .4, base: .8, slow: 1.2 };
const STAGGER = .06;
```

### Padrões reutilizáveis (implemente uma vez e use via atributo)
| Atributo | Efeito |
|---|---|
| `data-reveal="lines"` | Texto entra linha por linha, de baixo, com máscara |
| `data-reveal="fade-up"` | `y: 40 → 0`, `opacity 0 → 1` |
| `data-reveal="image"` | `clip-path: inset(100% 0 0 0) → inset(0)` + `scale 1.2 → 1` na imagem interna |
| `data-scrub="words"` | Palavras de muted para navy conforme o scroll (manifesto) |
| `data-count="9"` | Contador numérico |
| `data-draw` | Path SVG se desenha (`stroke-dashoffset`) |
| `data-magnetic` | Botão atrai levemente o cursor (desktop) |
| `data-zoom-grid` | Grid 3×3 em que o item central cresce até tela cheia no scroll (galeria 4a) |
| `data-filter` | Filtro com reorganização via GSAP Flip (galeria 4b) |
| `data-reel` | Vídeo que toca quando centralizado e pausa fora (galeria 4c) |

### Cursor (só desktop, `pointer: fine`)
Círculo pequeno navy com `mix-blend-mode: difference` que segue o mouse com lerp. Sobre imagens ou vídeos, cresce e mostra "Ver". Sobre links, encolhe. No touch, não existe.

### Acessibilidade de motion (obrigatório)
```css
@media (prefers-reduced-motion: reduce) { /* sem pin, sem scrub, sem preloader, só fades curtos */ }
```
No JS: `gsap.matchMedia()` com `(prefers-reduced-motion: no-preference)` envolvendo tudo que for decorativo. Lenis desligado com reduced motion.

---

## 7. Copy (PT-BR revisado)

**Hero**
- Rótulo: `Academia de Influência · Inscrições abertas`
- H1: **Conhecer. Treinar. Inspirar.**
- Sub: Um programa de 9 meses para jovens que querem descobrir seu propósito em Deus e levá-lo para todas as áreas da sociedade.
- Botões: **Quero aplicar** · Conhecer o programa

**Manifesto**
> Acreditamos que todo jovem precisa descobrir seu propósito no início da vida adulta. E que esse propósito não fica só dentro da igreja: ele vai para os negócios, a política, a educação, a arte, a ciência e a comunicação.

**Vida na Nine**
- Rótulo: `Vida na Nine`
- Frase do zoom: **Imagine você aqui.**
- Subtítulo do mural: Nove meses de aula, conversa até tarde, palco, serviço e amizades que ficam pra vida.
- Faixa de CTA: **Na próxima turma, a foto pode ser sua.**
- CTA fixo: Inscrições abertas · Aplicar →

**Pilar 01: Conhecer sua identidade**
"Antes de influenciar o mundo, você precisa saber quem é."
- *Teologia Livre (Fatemi):* conhecer a Deus e a Bíblia de forma profunda, o fundamento de tudo.
- *Grupos de alinhamento:* debates sobre os temas das aulas, conduzidos por um mentor.
- *Grupos de acompanhamento:* encontros semanais em pequenos grupos, liderados por um casal, para suporte emocional e espiritual.

**Pilar 02: Treinar suas habilidades**
"Propósito sem preparo não sai do papel."
- *Oficinas práticas:* inglês, vendas, finanças, oratória, fotografia, design, carreira, produtividade, esporte, robótica, música, informática e mais.
- *Módulos intensivos:* imersões curtas e profundas em temas específicos.
- *Serviço voluntário:* horas de serviço à comunidade, colocando em prática o que você aprende.

**Pilar 03: Inspirar o seu mundo**
"Sair da bolha para entender o mundo que você vai transformar."
- *Aulas gerais semanais:* política, economia, educação, saúde e sociedade, arte e cultura, comunicação e ciência.
- *Palestras e depoimentos:* histórias reais de quem influencia em cada área.
- *Intercâmbio cultural:* vivências que ampliam sua visão de mundo.

**Trilhas (2º semestre)**
| Trilha | Linha |
|---|---|
| Negócios | Empreender e liderar com propósito e ética. |
| Política | Servir o bem comum com responsabilidade pública. |
| Educação | Formar as próximas gerações. |
| Arte e Cultura | Criar beleza que aponta para algo maior. |
| Ciência e Tecnologia | Investigar, construir e inovar. |
| Serviço Social | Estar onde a necessidade é maior. |
| Comunicação e Entretenimento | Contar histórias que movem pessoas. |

**Fechamento / Aplicação**
- H2: **Sua turma começa aqui.**
- Sub: As vagas são limitadas e cada aplicação é lida pela nossa equipe. **[A CONFIRMAR: nº de vagas e prazo]**

---

## 8. Formulário de aplicação + Supabase

### Campos
| Campo | Tipo | Obrigatório |
|---|---|---|
| Nome completo | text | ✓ |
| E-mail | email | ✓ |
| WhatsApp | tel (máscara BR) | ✓ |
| Idade | number | ✓ |
| Cidade / UF | text | ✓ |
| Igreja que frequenta | text | — |
| Trilha de interesse | select (7 trilhas + "Ainda não sei") | ✓ |
| Por que você quer fazer parte da Nine? | textarea (máx. 800) | ✓ |
| Como conheceu a Nine? | select | — |
| Consentimento LGPD | checkbox + link para a política | ✓ |
| `website` | **honeypot** escondido (anti-spam) | — |

UX: validação nativa (`required`, `type`) + mensagens em PT-BR, botão com estado de carregando, foco no primeiro erro, sucesso sem recarregar a página.

### SQL (rodar no Supabase)
```sql
create table public.aplicacoes (
  id          uuid primary key default gen_random_uuid(),
  created_at  timestamptz not null default now(),
  nome        text not null,
  email       text not null,
  whatsapp    text not null,
  idade       int  not null check (idade between 14 and 99),
  cidade      text not null,
  igreja      text,
  trilha      text not null,
  motivacao   text not null check (char_length(motivacao) <= 800),
  origem      text,
  consentimento boolean not null check (consentimento)
);

alter table public.aplicacoes enable row level security;

-- Visitante só INSERE. Ninguém lê pela chave pública.
create policy "aplicacao publica - insert"
  on public.aplicacoes for insert to anon
  with check (true);
```

### Envio (main.js)
```js
const SUPABASE_URL = "https://XXXX.supabase.co";
const SUPABASE_ANON = "eyJ...";

async function enviarAplicacao(dados) {
  const r = await fetch(`${SUPABASE_URL}/rest/v1/aplicacoes`, {
    method: "POST",
    headers: {
      apikey: SUPABASE_ANON,
      Authorization: `Bearer ${SUPABASE_ANON}`,
      "Content-Type": "application/json",
      Prefer: "return=minimal",
    },
    body: JSON.stringify(dados),
  });
  if (!r.ok) throw new Error(await r.text());
}
```
- A chave `anon` é pública por design. A segurança está no RLS (só insert).
- Se o honeypot vier preenchido, finja sucesso e não envie.
- Aviso para a equipe (opcional): Database Webhook do Supabase → n8n → WhatsApp/e-mail.

---

## 9. Qualidade (critérios de aceite)

**Performance**
- Lighthouse mobile ≥ 90 em Performance, Acessibilidade, Boas práticas e SEO.
- Imagens em AVIF/WebP com `width`/`height` definidos, `loading="lazy"` (exceto o hero) e `fetchpriority="high"` no hero.
- Vídeos: `muted playsinline loop autoplay preload="none"` + `poster`, ≤ 2MB cada, pausados fora da tela (IntersectionObserver).
- JS das animações carregado com `defer`.

**Acessibilidade**
- HTML semântico (`header`, `nav`, `main`, `section` com `aria-labelledby`, `footer`).
- Tudo navegável por teclado, com foco visível (outline dourado sobre navy, navy sobre claro).
- `alt` descritivo em todas as imagens. Colagens: `alt` sobre a cena, não "imagem decorativa".
- Contraste conforme a seção 3.
- `prefers-reduced-motion` respeitado.

**SEO**
- `<title>`: Nine Academia de Influência | Formação cristã de 9 meses para jovens
- Meta description, Open Graph (imagem 1200×630 com coroa + NINE) e favicon da coroa.
- JSON-LD `EducationalOrganization` + `Course`.
- `lang="pt-BR"`.

**Responsivo**
- Testar em 360, 390, 768, 1024, 1440 e 1920px.
- Sem scroll horizontal em nenhuma largura (fora as áreas pinadas no desktop).
- Seções pinadas viram empilhadas abaixo de 1024px.

---

## 10. Deploy

1. Repositório no GitHub.
2. Vercel → *Import Project* → Framework: **Other** (estático, sem build).
3. Domínio: adicionar `9ai.com.br` e `www.9ai.com.br` na Vercel e apontar o DNS (A / CNAME) conforme a Vercel indicar.
4. Antes de trocar o DNS, validar tudo na URL `*.vercel.app`.

---

## 11. Plano de execução no Claude Code (prompts prontos)

Rode uma fase por vez, revise no navegador e só depois avance.

**Fase 1: Estrutura e tokens**
> Leia o CLAUDE.md. Crie index.html, style.css e main.js conforme a seção 4. Implemente os tokens da seção 3, as linhas verticais do grid, a navbar (seção 5.1) e o HTML semântico de todas as seções da seção 5 com a copy da seção 7. Ainda sem animações. Use placeholders cinza com o texto [A CONFIRMAR] onde faltar dado.

**Fase 2: Layout fiel**
> Refine o layout de cada seção para ficar fiel à seção 5: hero em card arredondado com wordmark gigante, manifesto em 2 colunas, cards de números, máscara em arco nos pilares e painéis expansíveis das trilhas. Garanta o responsivo da seção 9.

**Fase 3: Motion**
> Adicione GSAP, ScrollTrigger, SplitText, Flip e Lenis via CDN com versão fixa. Implemente o sistema de motion da seção 6: os data-attributes reutilizáveis primeiro, depois preloader, hero, manifesto com scrub, a seção pinada dos pilares (com pinceladas SVG) e a jornada horizontal. Envolva tudo em gsap.matchMedia respeitando reduced motion e desktop/mobile.

**Fase 3.5: Galeria "Vida na Nine"**
> Implemente a seção 5.4 completa: zoom 3×3 pinado com "Imagine você aqui.", mural masonry com filtros via GSAP Flip e lightbox em <dialog>, parede de Reels que toca só o vídeo centralizado, faixa de CTA e o CTA fixo que some na seção de Aplicação. As imagens ficam em assets/img/galeria/ e a lista de fotos (src, categoria, legenda) em um array no topo do main.js, para facilitar trocar o conteúdo.

**Fase 4: Formulário**
> Implemente o formulário da seção 8 com validação, honeypot, máscara de WhatsApp, estados de loading/erro/sucesso e envio ao Supabase. Deixe SUPABASE_URL e SUPABASE_ANON no topo do main.js.

**Fase 5: Polimento e QA**
> Faça uma auditoria contra a seção 9: Lighthouse mobile, contraste, teclado, alt, SEO e JSON-LD. Corrija o que reprovar e liste o que ainda depende de [A CONFIRMAR].

---

## 12. Checklist de material para pedir à Nine

- [ ] Logo em **SVG** (ou AI/PDF vetorial)
- [ ] **Colagens originais** em alta resolução (as dos pilares do site atual) e arquivos-fonte, se existirem
- [ ] **30 a 60 fotos reais** em alta, separadas por categoria (aulas, oficinas, grupos, intercâmbio, jantares, serviço, formatura)
- [ ] **5 a 7 Reels** em arquivo original (não baixados do app, que comprime), para a parede de Reels
- [ ] Brutos de vídeo para a **montagem do hero** (10–15s) e do vídeo central da galeria
- [ ] **Autorização de uso de imagem** dos alunos que aparecem (dos responsáveis, se houver menores)
- [ ] Nomes, fotos e áreas dos **fundadores e mentores**
- [ ] **Turma:** datas, dias/horários, local, formato, idade mínima, nº de vagas
- [ ] **Investimento:** valor, parcelamento, bolsas
- [ ] Cronograma dos **9 meses**
- [ ] 3+ **depoimentos reais** (vídeo ou texto + foto + nome + autorização)
- [ ] Respostas do **FAQ**
- [ ] Autorização para usar o nome e o logo da **Fatemi**
- [ ] Texto da **política de privacidade** (LGPD)
- [ ] Acesso ao **DNS** do domínio `9ai.com.br`
