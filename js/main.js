const btn = document.querySelector('.menu-btn');
const list = document.getElementById('menu');
if (btn && list) {
  btn.addEventListener('click', () => {
    const open = list.classList.toggle('open');
    btn.setAttribute('aria-expanded', open);
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
