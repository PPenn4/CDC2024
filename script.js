document.getElementById("fetchDataButton").addEventListener("click", function() {
    setTimeout(() => {
        document.getElementById("map-container").classList.remove("hidden");
        document.getElementById("results").classList.remove("hidden");
        document.getElementById("graph-container").classList.remove("hidden");
        document.getElementById("graph").classList.remove("hidden");
        document.getElementById("results_header").classList.remove("hidden");
        document.getElementById("results_table").classList.remove("hidden");
    }, 3000);
});


document.getElementById('fetchDataButton').addEventListener('click', () => {
    const city = document.getElementById('city').value;
    const category = document.getElementById('category').value;

    fetchTourismData(city, category);
});

async function fetchTourismData(city, category) {
    const url = `http://tour-pedia.org/api/getPlaces?location=${city}&category=${category}`;

    try {
        const response = await fetch(url);
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        const data = await response.json();
        
        if (data.length === 0) {
            document.getElementById('results').innerHTML = `<p>No data available for ${city} - ${category}</p>`;
            return;
        }

        data.forEach(item => {
            item.numReviews = Number(item.numReviews) || 0;
        });
        data.sort((a, b) => b.numReviews - a.numReviews);

        const top15 = data.slice(0, 15);

        for (let place of top15) {
            place.englishReviews = await countEnglishReviewsWithRetry(place.reviews, 3); 
        }

        let maxEnglishReviews = Math.max(...top15.map(place => place.englishReviews));
        let minEnglishReviews = Math.min(...top15.map(place => place.englishReviews));
        let topPlace = top15.find(place => place.englishReviews === maxEnglishReviews);
        let leastPlace = top15.find(place => place.englishReviews === minEnglishReviews);

        let tableBodyHtml = '';
        top15.forEach(place => {
            let emoji = '';
            if (place === topPlace) {
                emoji = '⭐'; 
            } else if (place === leastPlace) {
                emoji = 'ඞ';
            }

            tableBodyHtml += `<tr>
                                <td>${emoji}</td>
                                <td>${place.name || 'N/A'}</td>
                                <td>${place.address || 'N/A'}</td>
                                <td>${place.lng + ", " + place.lat}</td>
                                <td>${place.polarity !== undefined ? place.polarity.toFixed(2) : 'N/A'}</td>
                                <td>${place.numReviews}</td>
                              </tr>`;
        });

        document.getElementById('results-body').innerHTML = tableBodyHtml;

        document.querySelector('#results h2').textContent = `Top 15 Results for ${city} - ${category}`;

        displayGraph(top15, city, category);

    } catch (error) {
        console.error('Error fetching data:', error);
        document.getElementById('results').innerHTML = `<p>Error fetching data: ${error.message}</p>`;
    }
}

// Function to count the number of English reviews with retry logic
async function countEnglishReviewsWithRetry(reviewsUrl, retries) {
    while (retries > 0) {
        try {
            return await countEnglishReviews(reviewsUrl);
        } catch (error) {
            retries--;
            console.error(`Retrying... (${retries} attempts left)`);
            if (retries === 0) {
                console.error('Max retries reached. Error:', error);
                return 0; // Return 0 if all retries fail
            }
        }
    }
}

// Function to count the number of English reviews
async function countEnglishReviews(reviewsUrl) {
    if (!reviewsUrl) {
        return 0;
    }

    try {
        const response = await fetch(reviewsUrl);
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        const reviews = await response.json();
        
        // Count reviews in English, ensuring each review has a language field
        let englishReviewCount = 0;
        for (let review of reviews) {
            if (review.language && review.language === 'en') {
                englishReviewCount++;
            }
        }
        
        return englishReviewCount;
    } catch (error) {
        throw new Error('Error fetching reviews: ' + error.message);
    }
}

function displayGraph(data, city, category) {
    // Extract relevant data from the input to display in the graph
    const names = data.map(place => place.name || 'N/A');
    const englishReviews = data.map(place => place.englishReviews);

    // Get the context of the canvas to draw the chart
    const ctx = document.getElementById('graph').getContext('2d');

    // Clear any existing chart instance to avoid overlay issues
    if (window.tourismChart) {
        window.tourismChart.destroy();
    }

    // Create the chart
    window.tourismChart = new Chart(ctx, {
        type: 'bar', // Choose the type of chart, e.g., 'line', 'bar', etc.
        data: {
            labels: names,
            datasets: [{
                label: `Number of English Reviews for ${category} in ${city}`,
                data: englishReviews,
                backgroundColor: 'rgba(54, 162, 235, 0.6)',
                borderColor: 'rgba(54, 162, 235, 1)',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}
