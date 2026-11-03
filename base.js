/* Nine · comportamento comum aos dois sites (Faculdade e Academia) */

// Ano do rodapé: nunca fixo
document.querySelectorAll("[data-year]").forEach((el) => (el.textContent = new Date().getFullYear()));

// Seções sem material real só aparecem com ?rascunho
if (new URLSearchParams(location.search).has("rascunho")) {
  document.querySelectorAll("[data-draft]").forEach((el) => (el.hidden = false));
}

// Navbar: blur após 80px, esconde ao descer e reaparece ao subir
const nav = document.querySelector("[data-nav]");
let lastY = scrollY;
if (nav) addEventListener("scroll", () => {
  const y = scrollY;
  nav.classList.toggle("is-scrolled", y > 80);
  nav.classList.toggle("is-hidden", y > lastY && y > 200);
  lastY = y;
}, { passive: true });

// Menu mobile fullscreen
const menu = document.querySelector("[data-menu]");
const burger = document.querySelector(".nav__burger, .burger");
const setMenu = (open) => {
  menu.hidden = !open;
  burger.setAttribute("aria-expanded", open);
  document.body.style.overflow = open ? "hidden" : "";
  (open ? menu.querySelector("a") : burger).focus();
};
document.querySelectorAll("[data-menu-toggle]").forEach((b) => b.addEventListener("click", () => setMenu(menu.hidden)));
menu.addEventListener("click", (e) => e.target.closest("a") && setMenu(false));
addEventListener("keydown", (e) => e.key === "Escape" && !menu.hidden && setMenu(false));

// Submenu "A Faculdade": fecha ao clicar fora ou com Esc
const submenus = document.querySelectorAll("details.dd");
document.addEventListener("click", (e) => submenus.forEach((d) => !d.contains(e.target) && (d.open = false)));
addEventListener("keydown", (e) => {
  if (e.key !== "Escape") return;
  submenus.forEach((d) => { if (d.open) { d.open = false; d.querySelector("summary").focus(); } });
});

// Formulário da Ouvidoria: validação nativa; o envio (protocolo + e-mail) entra junto com o webhook da planilha
const ouvidoria = document.querySelector("[data-ouvidoria]");
if (ouvidoria) ouvidoria.addEventListener("submit", (e) => {
  e.preventDefault();
  if (!ouvidoria.reportValidity()) return;
  ouvidoria.querySelector("[data-status]").textContent =
    "O registro online está em implantação. Enquanto isso, envie sua manifestação para contato@nine.com.br.";
});

// Acordeões (FAQ e semestres da matriz): abre e fecha com altura animada; com movimento reduzido, abre direto
const semMovimento = matchMedia("(prefers-reduced-motion: reduce)");
document.querySelectorAll(".faq details, details.sem, .faq__list details").forEach((d) => {
  const summary = d.querySelector("summary");
  let anim = null;
  summary.addEventListener("click", (e) => {
    if (semMovimento.matches) return;
    e.preventDefault();
    const abrindo = !d.open || anim?.reverseClose;
    const de = d.offsetHeight;
    if (abrindo) d.open = true;
    const para = abrindo ? d.scrollHeight : summary.offsetHeight;
    anim?.cancel();
    anim = d.animate({ height: [`${de}px`, `${para}px`] }, { duration: 380, easing: "cubic-bezier(.2, .7, .2, 1)" });
    anim.reverseClose = !abrindo;
    anim.onfinish = () => {
      if (!abrindo) d.open = false;
      anim = null;
      window.ScrollTrigger && ScrollTrigger.refresh();
    };
  });
});

// ---------- Faculdade: motion leve (sem biblioteca) ----------
// Elementos com data-reveal entram suavemente quando chegam na tela (CSS faz a animação)
const revealIO = "IntersectionObserver" in window && new IntersectionObserver((es) => es.forEach((e) => {
  if (!e.isIntersecting) return;
  e.target.classList.add("is-in");
  revealIO.unobserve(e.target);
}), { rootMargin: "0px 0px -8% 0px" });
document.querySelectorAll("[data-reveal]").forEach((el) => (revealIO ? revealIO.observe(el) : el.classList.add("is-in")));

// Números que contam até o valor ao aparecer
const countIO = "IntersectionObserver" in window && new IntersectionObserver((es) => es.forEach((e) => {
  if (!e.isIntersecting) return;
  countIO.unobserve(e.target);
  const fim = +e.target.dataset.count, t0 = performance.now();
  if (semMovimento.matches) return;
  const passo = (t) => {
    const p = Math.min((t - t0) / 900, 1);
    e.target.textContent = Math.round(fim * (1 - Math.pow(1 - p, 3)));
    if (p < 1) requestAnimationFrame(passo);
  };
  requestAnimationFrame(passo);
}), { threshold: .6 });
if (countIO) document.querySelectorAll(".stats [data-count]").forEach((el) => countIO.observe(el));

// Cabeçalho ganha sombra ao rolar
const cabecalho = document.querySelector(".header");
if (cabecalho) addEventListener("scroll", () => cabecalho.classList.toggle("is-scrolled", scrollY > 8), { passive: true });

// Abas acessíveis (setas do teclado, Home/End)
document.querySelectorAll("[data-tabs]").forEach((box) => {
  const abas = [...box.querySelectorAll('[role="tab"]')];
  const paineis = abas.map((a) => document.getElementById(a.getAttribute("aria-controls")));
  const ativar = (i, foco) => {
    abas.forEach((a, k) => {
      a.setAttribute("aria-selected", k === i);
      a.tabIndex = k === i ? 0 : -1;
      paineis[k].hidden = k !== i;
      paineis[k].classList.toggle("is-active", k === i);
    });
    if (foco) abas[i].focus();
  };
  abas.forEach((a, i) => {
    a.addEventListener("click", () => ativar(i));
    a.addEventListener("keydown", (e) => {
      const n = abas.length, mapa = { ArrowRight: 1, ArrowDown: 1, ArrowLeft: -1, ArrowUp: -1 };
      if (e.key in mapa) { e.preventDefault(); ativar((i + mapa[e.key] + n) % n, true); }
      if (e.key === "Home") { e.preventDefault(); ativar(0, true); }
      if (e.key === "End") { e.preventDefault(); ativar(n - 1, true); }
    });
  });
  ativar(0);
  paineis[0].classList.remove("is-active");
});

// Carrossel da home: a barra dourada do ponto ativo marca o tempo; quando termina, passa para o próximo.
// Pausa com mouse ou foco dentro dele (CSS) e pelo botão; com movimento reduzido, começa parado.
document.querySelectorAll("[data-carousel]").forEach((box) => {
  const slides = [...box.querySelectorAll(".slide")], pontos = [...box.querySelectorAll("[data-goto]")];
  const play = box.querySelector("[data-play]"), trilho = box.querySelector(".carousel__track");
  let atual = 0;
  const ir = (n) => {
    atual = (n + slides.length) % slides.length;
    slides.forEach((s, k) => s.classList.toggle("is-active", k === atual));
    pontos.forEach((p, k) => (k === atual ? p.setAttribute("aria-current", "true") : p.removeAttribute("aria-current")));
  };
  const parar = (sim) => {
    box.classList.toggle("is-stopped", sim);
    play.setAttribute("aria-label", sim ? "Retomar destaques" : "Pausar destaques");
    trilho.setAttribute("aria-live", sim ? "polite" : "off");
  };
  pontos.forEach((p, k) => p.addEventListener("click", () => ir(k)));
  box.querySelectorAll("[data-step]").forEach((b) => b.addEventListener("click", () => ir(atual + +b.dataset.step)));
  play.addEventListener("click", () => parar(!box.classList.contains("is-stopped")));
  box.addEventListener("animationend", (e) => e.animationName === "slide-time" && ir(atual + 1));
  let x0 = null;
  trilho.addEventListener("touchstart", (e) => (x0 = e.touches[0].clientX), { passive: true });
  trilho.addEventListener("touchend", (e) => {
    const dx = e.changedTouches[0].clientX - x0;
    if (Math.abs(dx) > 50) ir(atual + (dx < 0 ? 1 : -1));
  });
  parar(semMovimento.matches);
  // Os outros destaques (e suas fotos) só entram depois que a página carregou
  addEventListener("load", () => box.classList.add("is-ready"));
});
