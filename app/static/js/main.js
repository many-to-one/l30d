document.addEventListener("DOMContentLoaded", () => {

    const form = document.getElementById('searchForm');
    const resultsDiv = document.getElementById('results');
    const summaryDiv = document.getElementById('summary');
    const loading = document.getElementById('loading');

    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        const query = document.getElementById('query').value.trim();
        if (!query) return;

        // Reset UI
        resultsDiv.innerHTML = '';
        summaryDiv.style.display = 'none';
        loading.style.display = 'block';

        try {
            const res = await fetch(`/api/last30days?query=${encodeURIComponent(query)}`);
            const data = await res.json();

            loading.style.display = 'none';
            resultsDiv.innerHTML = '';

            // Render results
            data.results.forEach(item => {
                const el = document.createElement('div');
                el.className = 'result-item';
                el.innerHTML = `
                    <a href="${item.url}" target="_blank"><h3>${item.title}</h3></a>
                    <p>💬 Komentarze: ${item.comments} | 👍 Score: ${item.score}</p>
                    <small>Źródło: ${item.source}</small>
                `;
                resultsDiv.appendChild(el);
            });

            // Render summary
            summaryDiv.textContent = data.summary;
            summaryDiv.style.display = 'block';

        } catch (err) {
            loading.style.display = 'none';
            resultsDiv.innerHTML = `<p style="color:red;">❌ Wystąpił błąd podczas pobierania danych.</p>`;
            console.error(err);
        }
    });

});
