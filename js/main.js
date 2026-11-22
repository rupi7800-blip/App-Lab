const btn = document.querySelector('.menu-btn');
const list = document.getElementById('menu');
function setMenu(open) {
  list.classList.toggle('open', open);
  btn.setAttribute('aria-expanded', open);
}
if (btn && list) {
  btn.addEventListener('click', () => setMenu(!list.classList.contains('open')));
  list.addEventListener('click', (e) => { if (e.target.closest('a')) setMenu(false); });
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && list.classList.contains('open')) { setMenu(false); btn.focus(); }
  });
}
const form = document.getElementById('contact');
if (form) {
  form.addEventListener('submit', (e) => {
    e.preventDefault();
    const d = new FormData(form);
    const body = `Nome: ${d.get('nome')}\nEmail: ${d.get('email')}\nAttività: ${d.get('tipo')}\n\n${d.get('messaggio')}`;
    location.href = `mailto:${form.dataset.email}?subject=${encodeURIComponent('Richiesta dal sito App Lab')}&body=${encodeURIComponent(body)}`;
  });
}
