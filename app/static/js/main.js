form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const query = document.getElementById('query').value;
    resultsDiv.innerHTML = '';
    summaryDiv.style.display = 'none';
    document.getElementById('loading').style.display = 'block';

    const res = await fetch(`/api/last30days?query=${encodeURIComponent(query)}`);
    const data = await res.json();

    document.getElementById('loading').style.display = 'none';
    resultsDiv.innerHTML = '';
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

    summaryDiv.textContent = data.summary;
    summaryDiv.style.display = 'block';
});
