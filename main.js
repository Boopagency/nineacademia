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
