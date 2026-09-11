// Aetheria Query Interface
document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('query-form');
    const input = document.getElementById('query-input');
    const select = document.getElementById('domain-select');
    const results = document.getElementById('query-results');

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        const q = input.value;
        const domain = select.value;
        
        const resp = await fetch(`/query/search?q=${encodeURIComponent(q)}&domain=${domain}`);
        const data = await resp.json();
        
        results.innerHTML = `<p>${data.count} results for "${data.query}"</p>`;
        data.results.forEach(r => {
            results.innerHTML += `<div class="result-item">
                <h4>${r.title}</h4>
                <span class="domain">${r.domain}</span>
            </div>`;
        });
    });
});
