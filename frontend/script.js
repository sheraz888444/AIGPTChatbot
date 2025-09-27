document.getElementById('askForm').addEventListener('submit', async function(event) {
    event.preventDefault();
    const questionInput = document.getElementById('question');
    const submitButton = document.querySelector('#askForm button');
    const responseDiv = document.getElementById('response');
    
    const question = questionInput.value;
    
    // Disable form and show loading state
    questionInput.disabled = true;
    submitButton.disabled = true;
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
    } finally {
        // Re-enable form elements after getting a response or error
        questionInput.disabled = false;
        submitButton.disabled = false;
    }
});
