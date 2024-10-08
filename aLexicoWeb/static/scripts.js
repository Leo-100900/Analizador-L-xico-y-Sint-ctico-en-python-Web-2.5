document.getElementById('analyze-btn').addEventListener('click', function() {
    const code = document.getElementById('code-input').value;

    fetch('/analyze', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ code: code }),
    })
    .then(response => response.json())
    .then(data => {
        const tokensBody = document.getElementById('tokens-body');
        tokensBody.innerHTML = '';

        data.tokens.forEach(token => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${token.type}</td>
                <td>${token.value}</td>
                <td>${token.category}</td>
                <td>${token.lineno}</td>
            `;
            tokensBody.appendChild(row);
        });

        document.getElementById('syntax-output').textContent = data.syntax;
    })
    .catch(error => console.error('Error:', error));
});
