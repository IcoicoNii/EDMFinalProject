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


