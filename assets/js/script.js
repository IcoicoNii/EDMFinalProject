document.addEventListener('DOMContentLoaded', () => {
    const carouselContainer = document.getElementById('carousel-container');
    const carouselSlides = document.getElementById('carousel-slides');
    const prevButton = document.getElementById('prev-button');
    const nextButton = document.getElementById('next-button');
    const slides = carouselSlides.children;
    let currentIndex = 0;
    const totalSlides = slides.length;
    let autoScrollInterval;
    const autoScrollDelay = 3000; // 3 seconds

    // Function to update slide position
    const updateCarousel = () => {
        const slideWidth = slides[0].offsetWidth; // Get the actual width of a slide
        carouselSlides.style.transform = `translateX(${-currentIndex * slideWidth}px)`;
    };

    // Function to start auto-scrolling
    const startAutoScroll = () => {
        stopAutoScroll(); // Clear any existing interval first
        autoScrollInterval = setInterval(() => {
            currentIndex = (currentIndex + 1) % totalSlides;
            updateCarousel();
        }, autoScrollDelay);
    };

    // Function to stop auto-scrolling
    const stopAutoScroll = () => {
        clearInterval(autoScrollInterval);
    };

    // Event listener for next button
    nextButton.addEventListener('click', () => {
        stopAutoScroll(); // Pause auto-scroll on manual interaction
        currentIndex = (currentIndex + 1) % totalSlides;
        updateCarousel();
        startAutoScroll(); // Resume after a brief moment (or immediately if you prefer)
    });

    // Event listener for previous button
    prevButton.addEventListener('click', () => {
        stopAutoScroll(); // Pause auto-scroll on manual interaction
        currentIndex = (currentIndex - 1 + totalSlides) % totalSlides;
        updateCarousel();
        startAutoScroll(); // Resume
    });

    // Pause auto-scroll on hover
    carouselContainer.addEventListener('mouseenter', stopAutoScroll);
    carouselContainer.addEventListener('mouseleave', startAutoScroll);

    // Initial update and start auto-scrolling
    updateCarousel();
    startAutoScroll();

    // Optional: Add a resize observer to update carousel on container resize
    const resizeObserver = new ResizeObserver(entries => {
        for (let entry of entries) {
            if (entry.target === carouselContainer) {
                stopAutoScroll(); // Pause during resize to prevent visual glitches
                updateCarousel();
                startAutoScroll(); // Resume after resize
            }
        }
    });
    resizeObserver.observe(carouselContainer);
});

        document.addEventListener('DOMContentLoaded', function() {
            fetch('/kpi_data')
                .then(response => response.json())
                .then(data => {
                    if (data.error) {
                        console.error('Error fetching KPI data:', data.error);
                        document.getElementById('kpi-total-revenue').innerText = 'N/A';
                        document.getElementById('kpi-average-revenue').innerText = 'N/A';
                        document.getElementById('kpi-total-products').innerText = 'N/A';
                        document.getElementById('kpi-total-sales').innerText = 'N/A';
                    } else {
                        document.getElementById('kpi-total-revenue').innerText = data.total_revenue;
                        document.getElementById('kpi-average-revenue').innerText = data.average_revenue;
                        document.getElementById('kpi-total-products').innerText = data.total_unique_products;
                        document.getElementById('kpi-total-sales').innerText = data.total_sales_count;
                    }
                })
                .catch(error => {
                    console.error('Network or parsing error:', error);
                    document.getElementById('kpi-total-revenue').innerText = 'Error';
                    document.getElementById('kpi-average-revenue').innerText = 'Error';
                    document.getElementById('kpi-total-products').innerText = 'Error';
                    document.getElementById('kpi-total-sales').innerText = 'Error';
                });
        });