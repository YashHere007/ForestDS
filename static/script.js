document.getElementById('prediction-form').addEventListener('submit', async function(event) {
    event.preventDefault();
    
    const formData = new FormData(this);
    const data = {};
    formData.forEach((value, key) => {
        data[key] = parseFloat(value);
    });
    
    const resultDiv = document.getElementById('result');
    resultDiv.classList.remove('success', 'error');
    resultDiv.textContent = 'Predicting...';
    
    try {
        const response = await fetch('/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });
        
        const result = await response.json();
        
        if (response.ok) {
            resultDiv.classList.add('success');
            resultDiv.textContent = `Prediction: ${result.prediction} (Fire Probability: ${(result.fire_probability * 100).toFixed(2)}%)`;
        } else {
            resultDiv.classList.add('error');
            resultDiv.textContent = `Error: ${result.error}`;
        }
    } catch (error) {
        resultDiv.classList.add('error');
        resultDiv.textContent = `Error: ${error.message}`;
    }
});