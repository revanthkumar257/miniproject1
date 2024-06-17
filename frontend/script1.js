document.getElementById('search-button').addEventListener('click', function() {
    const location = document.getElementById('location-input').value;
    const checkin = document.getElementById('checkin-input').value;
    const checkout = document.getElementById('checkout-input').value;
    const guests = document.getElementById('guests-input').value;

    // Sample data for places; replace this with your actual data
    const places = [
        { name: "New York", description: "A bustling city in the USA." },
        { name: "Los Angeles", description: "The city of angels in California." },
        { name: "Paris", description: "The romantic capital of France." },
        { name: "Tokyo", description: "A vibrant city in Japan." }
    ];

    const results = places.filter(place => place.name.toLowerCase().includes(location.toLowerCase()));

    const resultsContainer = document.getElementById('search-results');
    resultsContainer.innerHTML = '';

    if (results.length > 0) {
        results.forEach(result => {
            const resultElement = document.createElement('div');
            resultElement.className = 'result-item';
            resultElement.innerHTML = `<h3>${result.name}</h3><p>${result.description}</p>`;
            resultsContainer.appendChild(resultElement);
        });
    } else {
        resultsContainer.innerHTML = '<p>No results found.</p>';
    }
});
