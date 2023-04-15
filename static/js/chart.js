// Function to fetch data of the number of open positions in each city in Bulgaria
async function fetchOpenPositionsCount() {
    const response = await fetch('/count_open_positions');
    const data = await response.json();
    return data.city_counts;
    }
    
    // Function to create the chart using the fetched data
    async function createChart() {
    // Fetch data of the number of open positions in each city in Bulgaria
    const cityCounts = await fetchOpenPositionsCount();
    // Extract the city labels and the corresponding number of open positions
    const cityLabels = cityCounts.map(cityCount => cityCount.city);
    const openPositionsData = cityCounts.map(cityCount => cityCount.count);

    // Get the context of the canvas element to render the chart
    const ctx = document.getElementById('openPositionsChart').getContext('2d');
    // Create the chart object using Chart.js library
    const chart = new Chart(ctx, {
        type: 'pie',
        // Set the data for the chart
        data: {
            labels: cityLabels,
            datasets: [{
                data: openPositionsData,
                // Set the background colors for the chart
                backgroundColor: ['#4e73df', '#1cc88a', '#36b9cc', '#f6c23e', '#e74a3b', '#858796']
            }]
        },
        // Set the options for the chart
        options: {
            responsive: true,
            plugins: {
                // Set the position and the title for the legend
                legend: {
                    position: 'top',
                },
                title: {
                    display: true,
                    text: 'Open Positions by City in Bulgaria'
                }
            }
        }
    });
}

// Call the function to create the chart on page load
createChart();