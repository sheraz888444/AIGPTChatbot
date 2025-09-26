document.getElementById('askForm').addEventListener('submit', async function(event) {
    event.preventDefault();
    const question = document.getElementById('question').value;
    const responseDiv = document.getElementById('response');
    
    responseDiv.textContent = 'Loading...';
    
    try {
        const res = await fetch('http://localhost:5000/ask', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ question })
        });
        
        const data = await res.json();
        
        if (res.ok) {
            responseDiv.textContent = data.response;
        } else {
            responseDiv.textContent = 'Error: ' + data.error;
        }
    } catch (error) {
        responseDiv.textContent = 'Error: ' + error.message;
    }
});
