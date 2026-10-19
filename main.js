/* Nine Academia de Influência */

// Acervo do mural "Vida na Nine". Para trocar conteúdo: coloque os arquivos em
// assets/img/galeria/ (<id>-600.webp miniatura e <id>.webp ampliada) e edite esta lista.
// A ordem é a ordem de exibição; os filtros aparecem só para categorias com foto.
const GALERIA = [
  { id: "06", cat: "oficinas", legenda: "Oficina de joalheria", alt: "Turma em volta da mesa de ferramentas na oficina de joalheria", w: 600, h: 817 },
  { id: "22", cat: "jantares", legenda: "Jantar da turma", alt: "Dois alunos às gargalhadas durante o jantar", w: 600, h: 398 },
  { id: "24", cat: "aulas", legenda: "Aula no laboratório de ciências", alt: "Turma de jaleco reunida para foto no laboratório", w: 600, h: 438 },
  { id: "v05-39", cat: "servico", legenda: "Visita ao Pequeno Cotolengo", alt: "Turma reunida em roda durante a visita ao Complexo de Saúde Pequeno Cotolengo", w: 600, h: 1067 },
  { id: "13", cat: "oficinas", legenda: "Oficina de panificação", alt: "Aluna sorrindo para a câmera com a massa na mão", w: 600, h: 394 },
  { id: "17", cat: "oficinas", legenda: "Oficina de perfumaria", alt: "Aluno de olhos fechados sentindo uma fragrância na fita de papel", w: 600, h: 420 },
  { id: "v04-3", cat: "aulas", legenda: "Aula geral", alt: "Professora dando aula para a turma no auditório", w: 600, h: 1067 },
  { id: "23", cat: "jantares", legenda: "Jantar da turma", alt: "Duas alunas sorrindo para a câmera à mesa do jantar", w: 600, h: 420 },
  { id: "v07-12", cat: "servico", legenda: "Reforma da residência dos niners", alt: "Aluna pintando a grade de uma janela durante a reforma", w: 600, h: 1067 },
  { id: "27", cat: "oficinas", legenda: "Oficina de realidade virtual", alt: "Turma sentada experimentando óculos de realidade virtual", w: 600, h: 417 },
  { id: "11", cat: "oficinas", legenda: "Oficina de panificação", alt: "Instrutor polvilhando farinha enquanto a turma de avental observa", w: 600, h: 383 },
  { id: "25", cat: "aulas", legenda: "Aula no laboratório de ciências", alt: "Alunos de jaleco fazendo um experimento no laboratório", w: 600, h: 566 },
  { id: "04", cat: "jantares", legenda: "Refeição ao ar livre", alt: "Turma almoçando numa mesa longa ao ar livre", w: 600, h: 791 },
  { id: "v02-9", cat: "oficinas", legenda: "Oficina de pintura", alt: "Aluna de óculos pintando uma tela", w: 600, h: 1067 },
  { id: "v05-55", cat: "servico", legenda: "Visita ao Pequeno Cotolengo", alt: "Aluna entregando presentes da Nine durante a visita", w: 600, h: 1067 },
  { id: "30", cat: "jantares", legenda: "Degustação", alt: "Alunas se servindo numa tábua de degustação", w: 600, h: 824 },
  { id: "v01-21", cat: "oficinas", legenda: "Oficina de pizza", alt: "Aluna sorrindo enquanto abre a massa de pizza", w: 600, h: 1067 },
  { id: "v04-12", cat: "aulas", legenda: "Aula geral", alt: "Professora explicando um tema em sala de aula", w: 600, h: 1067 },
  { id: "21", cat: "jantares", legenda: "Jantar da turma", alt: "Turma jantando sob um pergolado iluminado à noite", w: 600, h: 391 },
  { id: "v07-43", cat: "servico", legenda: "Reforma da residência dos niners", alt: "Aluna lixando o teto durante a reforma da casa", w: 600, h: 1067 },
  { id: "12", cat: "oficinas", legenda: "Oficina de panificação", alt: "Turma sentada ouvindo o instrutor", w: 600, h: 397 },
  { id: "16", cat: "oficinas", legenda: "Oficina de perfumaria", alt: "Instrutora sorrindo diante da mesa de fragrâncias", w: 600, h: 409 },
  { id: "29", cat: "oficinas", legenda: "Oficina de realidade virtual", alt: "Aluno explorando um ambiente com óculos de realidade virtual", w: 600, h: 393 },
  { id: "v04-40", cat: "jantares", legenda: "Jantar da turma", alt: "Aluno de terno sorrindo durante o jantar", w: 600, h: 1067 },
  { id: "01", cat: "oficinas", legenda: "Oficina de café", alt: "Turma acompanhando uma degustação de café", w: 572, h: 846 },
  { id: "03", cat: "jantares", legenda: "Café da manhã da turma", alt: "Aluna sorrindo com um waffle na mão", w: 577, h: 788 },
  { id: "05", cat: "oficinas", legenda: "Oficina de joalheria", alt: "Professora testando uma pedra com um aparelho", w: 600, h: 800 },
  { id: "26", cat: "oficinas", legenda: "Oficina de realidade virtual", alt: "Aluno usando óculos de realidade virtual", w: 600, h: 398 },
  { id: "15", cat: "oficinas", legenda: "Oficina de panificação", alt: "Pão de fermentação natural recém-saído do forno", w: 600, h: 398 },
  { id: "20", cat: "oficinas", legenda: "Oficina de joalheria", alt: "Duas barrinhas de ouro na palma da mão", w: 600, h: 391 },
  { id: "28", cat: "oficinas", legenda: "Oficina de realidade virtual", alt: "Mãos segurando os controles de realidade virtual", w: 600, h: 402 },
];
const CATEGORIAS = { aulas: "Aulas", oficinas: "Oficinas", grupos: "Grupos", intercambio: "Intercâmbio", jantares: "Jantares", servico: "Serviço", formatura: "Formatura" };
const MURAL_INICIAL = 16;

// Ano do rodapé: nunca fixo
document.querySelectorAll("[data-year]").forEach((el) => (el.textContent = new Date().getFullYear()));

// Seções sem material real (Quem conduz, Depoimentos) só aparecem com ?rascunho
if (new URLSearchParams(location.search).has("rascunho")) {
  document.querySelectorAll("[data-draft]").forEach((el) => (el.hidden = false));
}

// Navbar: blur após 80px, esconde ao descer e reaparece ao subir
const nav = document.querySelector("[data-nav]");
let lastY = scrollY;
addEventListener("scroll", () => {
  const y = scrollY;
  nav.classList.toggle("is-scrolled", y > 80);
  nav.classList.toggle("is-hidden", y > lastY && y > 200);
  lastY = y;
}, { passive: true });

// Ponto dourado no link da seção visível
const pill = document.querySelector(".nav__pill");
const dot = pill.querySelector(".nav__dot");
const links = [...pill.querySelectorAll("a")];
const sections = links.map((a) => document.querySelector(a.hash));
const moveDot = (a) => {
  links.forEach((l) => l.removeAttribute("aria-current"));
  pill.classList.toggle("has-active", !!a);
  if (!a) return;
  a.setAttribute("aria-current", "true");
  dot.style.transform = `translateX(${a.offsetLeft + a.offsetWidth / 2 - 2.5}px)`;
};
const io = new IntersectionObserver((entries) => {
  entries.forEach((e) => {
    const a = links[sections.indexOf(e.target)];
    if (e.isIntersecting) moveDot(a);
    else if (a.hasAttribute("aria-current")) moveDot(null);
  });
}, { rootMargin: "-45% 0px -50% 0px" });
sections.forEach((s) => io.observe(s));

// Menu mobile fullscreen
const menu = document.querySelector("[data-menu]");
const burger = document.querySelector(".nav__burger");
const setMenu = (open) => {
  menu.hidden = !open;
  burger.setAttribute("aria-expanded", open);
  document.body.style.overflow = open ? "hidden" : "";
  (open ? menu.querySelector("a") : burger).focus();
};
document.querySelectorAll("[data-menu-toggle]").forEach((b) => b.addEventListener("click", () => setMenu(menu.hidden)));
menu.addEventListener("click", (e) => e.target.closest("a") && setMenu(false));
addEventListener("keydown", (e) => e.key === "Escape" && !menu.hidden && setMenu(false));

// ---------- Vida na Nine (Fase 3.5) ----------
const reduceMotion = matchMedia("(prefers-reduced-motion: reduce)");
const refreshScroll = () => window.ScrollTrigger && ScrollTrigger.refresh();

// Mural: fotos e filtros gerados a partir de GALERIA
const masonry = document.querySelector("[data-masonry]");
const moreBtn = document.querySelector("[data-more]");
masonry.innerHTML = GALERIA.map((f, i) => `<li data-cat="${f.cat}"${i >= MURAL_INICIAL ? " data-extra hidden" : ""}><figure>
  <button type="button" class="mural__open" data-i="${i}" aria-label="Ampliar: ${f.alt}"><img src="assets/img/galeria/${f.id}-600.webp" width="${f.w}" height="${f.h}" alt="${f.alt}" loading="lazy" decoding="async"></button>
  <figcaption>${f.legenda}</figcaption></figure></li>`).join("");
const muralItems = [...masonry.children];
const chipsEl = document.querySelector("[data-filter]");
const cats = ["tudo", ...Object.keys(CATEGORIAS).filter((k) => GALERIA.some((f) => f.cat === k))];
chipsEl.innerHTML = cats.map((k) =>
  `<button type="button" class="chip" aria-pressed="${k === "tudo"}" data-cat="${k}">${k === "tudo" ? "Tudo" : CATEGORIAS[k]}</button>`).join("");
let filtro = "tudo", expandido = false;

function aplicarFiltro() {
  const state = window.Flip && !reduceMotion.matches && Flip.getState(muralItems);
  muralItems.forEach((li) => (li.hidden = filtro === "tudo" ? !expandido && li.hasAttribute("data-extra") : li.dataset.cat !== filtro));
  moreBtn.hidden = expandido || filtro !== "tudo" || GALERIA.length <= MURAL_INICIAL;
  if (!state) return refreshScroll();
  Flip.from(state, {
    duration: .6, ease: "power2.inOut", absolute: true, onComplete: refreshScroll,
    onEnter: (els) => gsap.fromTo(els, { opacity: 0, scale: .92 }, { opacity: 1, scale: 1, duration: .4 }),
    onLeave: (els) => gsap.to(els, { opacity: 0, scale: .92, duration: .3 }),
  });
}
chipsEl.addEventListener("click", (e) => {
  const chip = e.target.closest(".chip");
  if (!chip) return;
  filtro = chip.dataset.cat;
  chipsEl.querySelectorAll(".chip").forEach((c) => c.setAttribute("aria-pressed", c === chip));
  aplicarFiltro();
});
moreBtn.addEventListener("click", () => {
  expandido = true;
  aplicarFiltro();
  masonry.querySelector("[data-extra] button").focus({ preventScroll: true });
});
moreBtn.hidden = GALERIA.length <= MURAL_INICIAL;

// Lightbox em <dialog>: setas, teclado (← → Esc), swipe e legenda
const lb = document.querySelector("[data-lightbox]");
const lbImg = lb.querySelector("[data-lb-img]"), lbCap = lb.querySelector("[data-lb-cap]");
let lbAtual = 0, lbX = null, lbSwipe = false;
const lbMostrar = (i) => {
  const f = GALERIA[(lbAtual = i)];
  lbImg.src = `assets/img/galeria/${f.id}.webp`;
  lbImg.alt = f.alt;
  lbCap.textContent = f.legenda;
};
const lbPasso = (d) => {
  const v = muralItems.filter((li) => !li.hidden).map((li) => +li.querySelector("[data-i]").dataset.i);
  lbMostrar(v[(v.indexOf(lbAtual) + d + v.length) % v.length]);
};
masonry.addEventListener("click", (e) => {
  const b = e.target.closest("[data-i]");
  if (b) { lbMostrar(+b.dataset.i); lb.showModal(); }
});
lb.querySelector("[data-lb-close]").addEventListener("click", () => lb.close());
lb.querySelector("[data-lb-prev]").addEventListener("click", () => lbPasso(-1));
lb.querySelector("[data-lb-next]").addEventListener("click", () => lbPasso(1));
lb.addEventListener("keydown", (e) => { if (e.key === "ArrowLeft") lbPasso(-1); if (e.key === "ArrowRight") lbPasso(1); });
lb.addEventListener("pointerdown", (e) => (lbX = e.clientX));
lb.addEventListener("pointerup", (e) => {
  lbSwipe = lbX !== null && Math.abs(e.clientX - lbX) > 50;
  if (lbSwipe) lbPasso(e.clientX < lbX ? 1 : -1);
  lbX = null;
});
lb.addEventListener("click", (e) => { if (e.target === lb && !lbSwipe) lb.close(); lbSwipe = false; });

// Vídeos com data-autoplay tocam só quando visíveis (e nunca com reduced motion)
const autoplayIO = new IntersectionObserver((es) => es.forEach((e) =>
  e.isIntersecting ? e.target.play().catch(() => {}) : e.target.pause()), { threshold: .25 });
if (!reduceMotion.matches) document.querySelectorAll("[data-autoplay]").forEach((v) => autoplayIO.observe(v));

// Parede de Reels: só o ativo toca (mudo); som opcional; no mobile, ativo = o centralizado
const reelsTrack = document.querySelector("[data-reels]");
const reelItems = [...reelsTrack.children];
let reelAtivo = reelsTrack.querySelector(".is-active"), reelsNaTela = false, somLigado = false;
function ativarReel(li) {
  reelAtivo = li;
  reelItems.forEach((r) => {
    const v = r.querySelector("video"), on = r === li;
    r.classList.toggle("is-active", on);
    v.muted = !(on && somLigado);
    if (on && reelsNaTela && (somLigado || !reduceMotion.matches)) v.play().catch(() => {});
    else v.pause();
    const b = r.querySelector(".reel__sound");
    b.setAttribute("aria-pressed", somLigado);
    b.setAttribute("aria-label", somLigado ? "Desativar som" : "Ativar som");
    b.firstChild.textContent = somLigado ? "🔊" : "🔇";
  });
}
reelsTrack.addEventListener("click", (e) => {
  const li = e.target.closest("[data-reel]");
  if (!li) return;
  if (e.target.closest(".reel__sound")) somLigado = !somLigado;
  else li.scrollIntoView({ inline: "center", block: "nearest", behavior: reduceMotion.matches ? "auto" : "smooth" });
  ativarReel(li);
});
new IntersectionObserver(([e]) => { reelsNaTela = e.isIntersecting; ativarReel(reelAtivo); }, { threshold: .3 }).observe(reelsTrack);
const centroIO = new IntersectionObserver((es) => es.forEach((e) => e.isIntersecting && e.target !== reelAtivo && ativarReel(e.target)),
  { root: reelsTrack, rootMargin: "0px -45% 0px -45%" });
reelsTrack.scrollLeft = reelAtivo.offsetLeft - (reelsTrack.clientWidth - reelAtivo.offsetWidth) / 2;
reelItems.forEach((li) => centroIO.observe(li));

// CTA fixo: aparece depois da faixa de CTA e some quando a Aplicação está na tela
const ctaFloat = document.querySelector("[data-cta-float]");
const ctaBand = document.querySelector(".cta-band"), aplicarSec = document.querySelector("#aplicar");
const updateCta = () => ctaFloat.classList.toggle("is-on",
  ctaBand.getBoundingClientRect().top < innerHeight / 2 && aplicarSec.getBoundingClientRect().top > innerHeight);
addEventListener("scroll", updateCta, { passive: true });
updateCta();

// Formulário: envio entra na Fase 4; por ora não recarrega a página
document.querySelector("[data-form]").addEventListener("submit", (e) => e.preventDefault());

/* ==========================================================================
   Fase 3 · Motion (GSAP + ScrollTrigger + SplitText + Lenis)
   ========================================================================== */
const EASE = { out: "power3.out", inOut: "power2.inOut", expo: "expo.out" };
const DUR = { fast: .4, base: .8, slow: 1.2 };
const STAGGER = .06;
const root = document.documentElement;
const $ = (s, el = document) => el.querySelector(s);

if (window.gsap && window.ScrollTrigger && window.SplitText) initMotion();
else root.classList.remove("intro");

function initMotion() {
  gsap.registerPlugin(ScrollTrigger, SplitText, Flip);
  const motionOk = matchMedia("(prefers-reduced-motion: no-preference)").matches;
  const introEnd = motionOk ? preloader() : 0;
  if (motionOk) heroIntro(introEnd);

  gsap.matchMedia().add({
    motion: "(prefers-reduced-motion: no-preference)",
    desktop: "(min-width: 1024px)",
    finePointer: "(pointer: fine)",
  }, ({ conditions: { motion, desktop, finePointer } }) => {
    if (!motion) {
      // Reduced motion: sem pin, sem scrub, sem Lenis. Só fades curtos.
      gsap.utils.toArray("[data-reveal]").forEach((el) =>
        gsap.from(el, { opacity: 0, duration: DUR.fast, scrollTrigger: once(el) }));
      return;
    }
    // Elementos dentro de seções pinadas são animados pela própria seção no desktop
    const free = (sel) => gsap.utils.toArray(sel)
      .filter((el) => !el.closest(".hero") && !(desktop && el.closest("[data-pin]")));

    const cleanups = [smoothScroll(introEnd), reveals(free), heroScroll(), desktop ? pinZoom() : null];
    cleanups.push(desktop ? pinPilares() : null, desktop ? pinJornada() : drawJornada());
    if (desktop && finePointer) cleanups.push(cursor(), magnetic());
    return () => cleanups.forEach((fn) => fn && fn());
  });
}

function once(trigger, start = "top 85%") { return { trigger, start, once: true }; }

function smoothScroll(introEnd) {
  const lenis = new Lenis();
  const raf = (t) => lenis.raf(t * 1000);
  lenis.on("scroll", ScrollTrigger.update);
  gsap.ticker.add(raf);
  gsap.ticker.lagSmoothing(0);
  if (introEnd) { lenis.stop(); gsap.delayedCall(introEnd + .45, () => lenis.start()); }

  // Âncoras passam pelo Lenis (ele já respeita o scroll-padding-top do CSS) e levam o foco junto
  const onClick = (e) => {
    const a = e.target.closest('a[href^="#"]:not(.skip)');
    const target = a && a.hash.length > 1 && $(a.hash);
    if (!target) return;
    e.preventDefault();
    lenis.scrollTo(target);
    history.pushState(null, "", a.hash);
    target.setAttribute("tabindex", "-1");
    target.focus({ preventScroll: true });
  };
  document.addEventListener("click", onClick);
  return () => {
    document.removeEventListener("click", onClick);
    gsap.ticker.remove(raf);
    gsap.ticker.lagSmoothing(500, 33);
    lenis.destroy();
  };
}

// Padrões reutilizáveis via atributo (seção 6)
function reveals(free) {
  free('[data-reveal="fade-up"]').forEach((el) =>
    gsap.from(el, { y: 40, opacity: 0, duration: DUR.base, ease: EASE.out, scrollTrigger: once(el) }));

  free('[data-reveal="lines"]').forEach((el) => SplitText.create(el, {
    type: "lines", mask: "lines", autoSplit: true,
    onSplit: (s) => gsap.from(s.lines, { yPercent: 100, duration: DUR.base, stagger: STAGGER * 1.5, ease: EASE.out, scrollTrigger: once(el) }),
  }));

  free('[data-reveal="image"]').forEach((el) => {
    const inner = el.querySelector("img, video") || el.firstElementChild;
    const tl = gsap.timeline({ scrollTrigger: once(el) })
      .fromTo(el, { clipPath: "inset(100% 0 0 0)" }, { clipPath: "inset(0% 0 0 0)", duration: DUR.slow, ease: EASE.expo });
    if (inner) tl.from(inner, { scale: 1.2, duration: DUR.slow, ease: EASE.expo }, 0);
  });

  gsap.utils.toArray('[data-scrub="words"]').forEach((el) => SplitText.create(el, {
    type: "words", autoSplit: true,
    onSplit: (s) => gsap.fromTo(s.words, { opacity: .3 }, {
      opacity: 1, stagger: .1, ease: "none",
      scrollTrigger: { trigger: el, start: "top 80%", end: "bottom 45%", scrub: true },
    }),
  }));

  gsap.utils.toArray("[data-count]").forEach((el) => {
    const n = { v: 0 };
    gsap.to(n, {
      v: +el.dataset.count, duration: DUR.slow, ease: EASE.out, scrollTrigger: once(el),
      onUpdate: () => (el.textContent = Math.round(n.v)),
    });
  });

  free("[data-draw]").forEach((p) => gsap.fromTo(p, undrawn(p),
    { strokeDashoffset: 0, duration: DUR.slow, ease: EASE.inOut, scrollTrigger: once(p.ownerSVGElement, "top 75%") }));
}

// Traço "apagado" sem o pontinho da ponta arredondada (gap longo + folga no offset)
function undrawn(p) {
  const len = p.getTotalLength();
  return { strokeDasharray: `${len} ${len * 2}`, strokeDashoffset: len + 10 };
}

// Preloader: 1 → 9, coroa cai sobre o "I", cortina sobe. ~1,6s, uma vez por sessão.
function preloader() {
  const el = $("[data-preloader]");
  if (!root.classList.contains("intro")) { el.remove(); return 0; }
  try { sessionStorage.setItem("nine-intro", "1"); } catch (e) {}
  const end = 1.15;
  gsap.timeline({ onComplete: () => { root.classList.remove("intro"); el.remove(); ScrollTrigger.refresh(); } })
    .to($(".preloader__digits", el), { yPercent: -100 * 8 / 9, duration: .7, ease: "power2.inOut" })
    .to($(".preloader__count", el), { yPercent: -40, opacity: 0, duration: .15, ease: "power2.in" }, .62)
    .fromTo(el.querySelectorAll(".ch"), { yPercent: 50, opacity: 0 }, { yPercent: 0, opacity: 1, stagger: .05, duration: .25, ease: EASE.out }, .76)
    .fromTo($("img", el), { y: -innerHeight / 2, opacity: 1 }, { y: 0, duration: .42, ease: "bounce.out" }, .8)
    .to(el, { clipPath: "inset(0% 0% 100% 0%)", duration: .45, ease: "power3.inOut" }, end);
  return end;
}

function heroIntro(delay) {
  const chars = SplitText.create(".hero__wordmark > span", { type: "chars", mask: "chars" }).chars;
  gsap.timeline({ delay })
    .from(".hero__media", { scale: 1.15, duration: DUR.slow * 1.4, ease: EASE.expo })
    .from(chars, { yPercent: 100, stagger: STAGGER, duration: DUR.slow, ease: EASE.expo }, .1)
    .from(".hero__bar", { opacity: 0, y: 20, duration: DUR.base, ease: EASE.out }, .5)
    .from(".hero__side", { opacity: 0, y: 40, duration: DUR.base, ease: EASE.out }, .6);
  SplitText.create("#hero-title", {
    type: "lines", mask: "lines", autoSplit: true,
    onSplit: (s) => gsap.from(s.lines, { yPercent: 100, stagger: .1, duration: DUR.base, ease: EASE.out, delay: delay + .35 }),
  });
}

function heroScroll() {
  const st = { trigger: ".hero__card", start: "top top", end: "bottom top", scrub: true };
  gsap.to(".hero__media", { yPercent: 10, ease: "none", scrollTrigger: st });
  gsap.to(".hero__wordmark > span", { yPercent: 10, ease: "none", scrollTrigger: { ...st } });
}

// Vida na Nine: o vídeo do centro cresce até a tela inteira e as 8 fotos se afastam (desktop)
function pinZoom() {
  const zoom = $("[data-zoom-grid]"), center = $(".zoom__center", zoom), video = $("video", center);
  const ring = gsap.utils.toArray(".zoom__item", zoom);
  const tilt = [-8, 6, -5, 9, -7, 5, -6, 8];
  zoom.classList.add("is-pinned");
  // clip inicial = a célula do meio do grid, medida dentro do quadro vertical do vídeo
  const cell = () => {
    const z = zoom.getBoundingClientRect(), c = center.getBoundingClientRect(), cs = getComputedStyle(zoom);
    const gap = parseFloat(cs.rowGap), pt = parseFloat(cs.paddingTop), pb = parseFloat(cs.paddingBottom);
    const w = (z.width - 2 * gap) / 3, h = (z.height - pt - pb - 2 * gap) / 3;
    const x = z.left + w + gap, y = z.top + pt + h + gap;
    return `inset(${y - c.top}px ${c.right - x - w}px ${c.bottom - y - h}px ${x - c.left}px round 16px)`;
  };
  const away = (axis) => (i, el) => axis === "x"
    ? (el.offsetLeft + el.offsetWidth / 2 - zoom.clientWidth / 2) * 1.3
    : (el.offsetTop + el.offsetHeight / 2 - zoom.clientHeight / 2) * 1.3;

  gsap.timeline({
    defaults: { ease: "power2.inOut" },
    scrollTrigger: { trigger: zoom, start: "top top", end: "+=150%", pin: true, scrub: .6, invalidateOnRefresh: true },
  })
    .fromTo(video, { clipPath: cell }, { clipPath: "inset(0px 0px 0px 0px round 0px)", duration: 1 }, 0)
    .to(ring, { x: away("x"), y: away("y"), rotation: (i) => tilt[i], opacity: 0, duration: .8, ease: "power2.in" }, 0)
    .fromTo(zoom, { "--bg": 0 }, { "--bg": 1, duration: .6 }, .3)
    .fromTo(".zoom__phrase", { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: .4 }, .65);
  return () => zoom.classList.remove("is-pinned");
}

// Pilares: 3 capítulos numa seção pinada (desktop)
function pinPilares() {
  const sec = $(".pilares"), stage = $(".pilares__stage", sec);
  const arts = gsap.utils.toArray(".pilar", stage);
  const part = (s) => arts.map((a) => $(s, a));
  const [texts, medias, arcs, bars] = [".pilar__text", ".pilar__media", ".arc", ".pilar__bar"].map(part);
  const brushes = arts.map((a) => [...a.querySelectorAll("[data-draw]")]);
  sec.classList.add("is-pinned");

  brushes.flat().forEach((p) => gsap.set(p, undrawn(p)));
  gsap.set(texts.slice(1), { autoAlpha: 0, y: 40 });
  gsap.set(arcs.slice(1), { clipPath: "inset(100% 0 0 0)" });

  const tl = gsap.timeline({
    defaults: { ease: "none" },
    scrollTrigger: { trigger: stage, start: "top top", end: () => "+=" + innerHeight * arts.length, pin: true, scrub: .6, invalidateOnRefresh: true },
  });
  arts.forEach((_, i) => {
    if (i) {
      tl.to(texts[i - 1], { autoAlpha: 0, y: -40, duration: .4, ease: EASE.inOut })
        .to(medias[i - 1], { scale: .95, autoAlpha: 0, duration: .5, ease: EASE.inOut }, "<")
        .to(arcs[i], { clipPath: "inset(0% 0 0 0)", duration: .6, ease: EASE.inOut }, "<")
        .to(texts[i], { autoAlpha: 1, y: 0, duration: .4, ease: EASE.inOut }, "<.2");
    }
    tl.to(brushes[i], { strokeDashoffset: 0, duration: .5, ease: EASE.inOut }, i ? "<" : 0)
      .fromTo(bars[i], { "--p": 0 }, { "--p": 1, duration: 1 });
  });
  return () => sec.classList.remove("is-pinned");
}

// Jornada: scroll horizontal pinado + "9" preenchendo (desktop)
function pinJornada() {
  const sec = $(".jornada"), wrap = $(".jornada__wrap", sec), track = $(".jornada__track", sec);
  sec.classList.add("is-pinned");
  const dist = () => track.scrollWidth - track.clientWidth;
  gsap.timeline({
    defaults: { ease: "none" },
    scrollTrigger: { trigger: wrap, start: "center center", end: () => "+=" + dist(), pin: true, scrub: .6, invalidateOnRefresh: true },
  })
    .to(track, { x: () => -dist() })
    .fromTo(".jornada__nine--fill", { clipPath: "inset(100% 0 0 0)" }, { clipPath: "inset(0% 0 0 0)" }, 0);
  return () => sec.classList.remove("is-pinned");
}

// Jornada no mobile: linha vertical desenhada no scroll
function drawJornada() {
  const sec = $(".jornada"), track = $(".jornada__track", sec);
  sec.classList.add("is-drawing");
  const st = { trigger: track, start: "top 70%", end: "bottom 70%", scrub: true };
  gsap.to(".jornada__line", { scaleY: 1, ease: "none", scrollTrigger: st });
  gsap.fromTo(".jornada__nine--fill", { clipPath: "inset(100% 0 0 0)" }, { clipPath: "inset(0% 0 0 0)", ease: "none", scrollTrigger: { ...st } });
  return () => sec.classList.remove("is-drawing");
}

// Cursor: segue o mouse com lerp; "Ver" sobre imagens/vídeos, encolhe sobre links
function cursor() {
  const c = document.createElement("div");
  c.className = "cursor";
  c.setAttribute("aria-hidden", "true");
  c.innerHTML = "<span>Ver</span>";
  document.body.append(c);
  gsap.set(c, { x: -100, y: -100, scale: .2 });
  const xTo = gsap.quickTo(c, "x", { duration: .35, ease: "power3" });
  const yTo = gsap.quickTo(c, "y", { duration: .35, ease: "power3" });
  const move = (e) => { xTo(e.clientX); yTo(e.clientY); };
  const over = (e) => {
    const view = e.target.closest("img, video, [role=img]");
    const link = !view && e.target.closest("a, button, summary, .path, label, input, select, textarea");
    gsap.to(c, { scale: view ? 1 : link ? .1 : .2, duration: .3, ease: EASE.out });
    gsap.to(c.firstChild, { opacity: view ? 1 : 0, duration: .2 });
  };
  addEventListener("pointermove", move);
  document.addEventListener("pointerover", over);
  return () => { removeEventListener("pointermove", move); document.removeEventListener("pointerover", over); c.remove(); };
}

// Botões que atraem levemente o cursor
function magnetic() {
  const offs = gsap.utils.toArray("[data-magnetic]").map((b) => {
    const xTo = gsap.quickTo(b, "x", { duration: .4, ease: "power3" });
    const yTo = gsap.quickTo(b, "y", { duration: .4, ease: "power3" });
    const move = (e) => {
      const r = b.getBoundingClientRect();
      xTo((e.clientX - r.left - r.width / 2) * .25);
      yTo((e.clientY - r.top - r.height / 2) * .25);
    };
    const leave = () => { xTo(0); yTo(0); };
    b.addEventListener("pointermove", move);
    b.addEventListener("pointerleave", leave);
    return () => { b.removeEventListener("pointermove", move); b.removeEventListener("pointerleave", leave); };
  });
  return () => offs.forEach((off) => off());
}
