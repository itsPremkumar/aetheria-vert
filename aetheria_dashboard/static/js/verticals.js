// Aetheria Vertical Cards
document.addEventListener('DOMContentLoaded', async () => {
    const resp = await fetch('/verticals/list');
    const verticals = await resp.json();
    const grid = document.getElementById('verticals-grid');
    
    verticals.forEach(v => {
        const card = document.createElement('div');
        card.className = 'vertical-card';
        card.innerHTML = `
            <div class="vertical-icon">${v.icon}</div>
            <h3>${v.name}</h3>
            <p>${v.description}</p>
        `;
        grid.appendChild(card);
    });
});
