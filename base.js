/* Faculdade Nine · comportamento comum a todas as páginas */

// Ano do rodapé: nunca fixo
document.querySelectorAll("[data-year]").forEach((el) => (el.textContent = new Date().getFullYear()));

// Seções sem material real só aparecem com ?rascunho
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

// Formulário da Ouvidoria: validação nativa; o envio (protocolo + e-mail) entra junto com o webhook da planilha
const ouvidoria = document.querySelector("[data-ouvidoria]");
if (ouvidoria) ouvidoria.addEventListener("submit", (e) => {
  e.preventDefault();
  if (!ouvidoria.reportValidity()) return;
  ouvidoria.querySelector("[data-status]").textContent =
    "O registro online está em implantação. Enquanto isso, envie sua manifestação para contato@nine.com.br.";
});
