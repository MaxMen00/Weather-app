async function fetchCities(query) {
    const response = await fetch(`/cities/?query=${encodeURIComponent(query)}`);
    const cities = await response.json();
    return cities;
}

document.getElementById('city').addEventListener('input', async function () {
    const input = this.value;
    const suggestions = document.getElementById('suggestions');
    suggestions.innerHTML = '';
    if (input) {
        const filteredCities = await fetchCities(input);
        filteredCities.forEach(city => {
            const div = document.createElement('div');
            div.textContent = city;
            div.classList.add('suggestion-item');
            div.addEventListener('click', function () {
                document.getElementById('city').value = city;
                suggestions.innerHTML = '';
            });
            suggestions.appendChild(div);
        });
    }
});