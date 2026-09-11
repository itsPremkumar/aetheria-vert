// Aetheria API Client
document.addEventListener('DOMContentLoaded', async () => {
    const resp = await fetch('/api-client/endpoints');
    const data = await resp.json();
    const container = document.getElementById('api-endpoints');
    
    data.endpoints.forEach(ep => {
        const div = document.createElement('div');
        div.className = 'endpoint-item';
        div.innerHTML = `
            <span class="method">${ep.method}</span>
            <span class="path">${ep.path}</span>
            <p>${ep.description}</p>
        `;
        container.appendChild(div);
    });

    document.getElementById('send-request').addEventListener('click', async () => {
        const url = document.getElementById('api-url').value;
        try {
            const resp = await fetch(url);
            const json = await resp.json();
            document.getElementById('api-response').textContent = JSON.stringify(json, null, 2);
        } catch (e) {
            document.getElementById('api-response').textContent = `Error: ${e.message}`;
        }
    });
});
