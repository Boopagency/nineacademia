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
