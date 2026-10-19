/* Nine Academia de Influência · Fase 1: comportamento base, sem GSAP */

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

// Filtro do mural (Fase 3.5 troca por GSAP Flip)
const chips = document.querySelectorAll("[data-filter] .chip");
const photos = document.querySelectorAll("[data-masonry] li");
chips.forEach((chip) => chip.addEventListener("click", () => {
  chips.forEach((c) => c.setAttribute("aria-pressed", c === chip));
  photos.forEach((p) => (p.hidden = chip.dataset.cat !== "tudo" && p.dataset.cat !== chip.dataset.cat));
}));

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

    const cleanups = [smoothScroll(introEnd), reveals(free), heroScroll()];
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
