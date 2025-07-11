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

document.addEventListener('DOMContentLoaded', function () {
  fetch('/kpi_data')
    .then(response => response.json())
    .then(data => {
      if (data.error) {
        console.error('Error fetching KPI data:', data.error);
        document.getElementById('kpi-total-revenue').innerText = 'N/A';
        document.getElementById('kpi-average-revenue').innerText = 'N/A';
        document.getElementById('kpi-total-products').innerText = 'N/A';
        document.getElementById('kpi-total-sales').innerText = 'N/A';
        document.getElementById('max-revenue').innerText = 'N/A';
        document.getElementById('min-revenue').innerText = 'N/A';
      } else {
        document.getElementById('kpi-total-revenue').innerText = data.total_revenue;
        document.getElementById('kpi-average-revenue').innerText = data.average_revenue;
        document.getElementById('kpi-total-products').innerText = data.total_unique_products;
        document.getElementById('kpi-total-sales').innerText = data.total_sales_count;
        document.getElementById('max-revenue').innerText = data.max_revenue;
        document.getElementById('min-revenue').innerText = data.min_revenue;
      }
    })
    .catch(error => {
      console.error('Network or parsing error:', error);
      document.getElementById('kpi-total-revenue').innerText = 'Error';
      document.getElementById('kpi-average-revenue').innerText = 'Error';
      document.getElementById('kpi-total-products').innerText = 'Error';
      document.getElementById('kpi-total-sales').innerText = 'Error';
      document.getElementById('max-revenue').innerText = 'Error';
      document.getElementById('min-revenue').innerText = 'Error';
    });
});


document.addEventListener('DOMContentLoaded', () => {
  const navToggle = document.getElementById('nav-toggle');
  const navMenu = document.getElementById('nav-menu');
  const navbar = document.getElementById('navbar');

  // Toggle mobile navigation menu
  navToggle.addEventListener('click', () => {
    navMenu.classList.toggle('hidden');
    navMenu.classList.toggle('opacity-0');
    navMenu.classList.toggle('scale-95');
    navMenu.classList.toggle('open'); // Add/remove 'open' class for transition
  });

  // Smooth scroll with offset for all navigation links
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
      e.preventDefault(); // Prevent default anchor click behavior

      const targetId = this.getAttribute('href');
      const targetElement = document.querySelector(targetId);

      if (targetElement) {
        const navbarHeight = navbar.offsetHeight; // Get the current height of the navbar
        // Calculate the position to scroll to, subtracting the navbar height
        const offsetPosition = targetElement.offsetTop - navbarHeight;

        window.scrollTo({
          top: offsetPosition,
          behavior: 'smooth' // Smooth scrolling effect
        });

        // Close mobile menu after clicking a link
        if (!navMenu.classList.contains('hidden')) {
          navMenu.classList.add('hidden');
          navMenu.classList.add('opacity-0');
          navMenu.classList.add('scale-95');
          navMenu.classList.remove('open');
        }
      }
    });
  });
});

function updateContent(index) {
  const data = [
    // Data set 0
    {
      summary: "This is the summary for data set 0. It covers general information and initial findings.",
      keyPoints: [
        "Initial setup complete.",
        "Data collection started.",
        "Basic analysis initiated."
      ],
      iframeSrc: "/chart/sales_by_location_map",
      chartHeading: "Revenue Distribution Across Australia",
      insight: 'Insight 0',
      iframeSize: 'scale(1)'
    },
    // Data set 1
    {
      summary: "This is the summary for data set 1. Focuses on regional sales performance and market trends.",
      keyPoints: [
        "Regional sales increased by 10%.",
        "New market segment identified.",
        "Competitor analysis shows strong performance."
      ],
      iframeSrc: "/chart/three_year_sales_trend",
      chartHeading: "Three Year Sales Trend for Each Product",
      insight: 'Insight 1',
      iframeSize: 'scale(0.95)'
    },
    // Data set 2
    {
      summary: "The monthly sales trend exhibits significant volatility and cyclical patterns between January 2018 and December 2020. Sales generally show mid-year peaks (e.g., July 2018, July 2019, July 2020) and year-end/year-beginning dips. The highest revenue was achieved in July 2019, surpassing $1.2 million. Conversely, the lowest significant point occurred around December 2019, at approximately $0.4 million. A critical observation is the anomalous and sharp decline to near zero revenue in December 2020, which stands out as an extreme outlier and suggests a potential data issue or an extraordinary event impacting sales.",
      keyPoints: [
        "Peak Performance. The highest sales revenue occurred around July 2019, exceeding $1.2M.",
        "Lowest Performance. The lowest significant sales revenue (excluding the final sharp drop) was around December 2019, at approximately $0.4M.",
        "Volatility. The sales show considerable month-to-month volatility, with clear ups and downs.",
        'Potential Seasonality. A pattern of mid-year peaks and year-end/year-beginning dips is observable.',
        'Anomalous December 2020. The almost complete collapse of sales in December 2020 is a critical point that warrants further investigation, as it does not follow the established cyclical pattern and is an extreme outlier.',
      ],
      iframeSrc: "/chart/total_sales_revenue_by_product",
      chartHeading: "Total Sales Revenue by Product",
      insight: 'Given the clear mid-year peaks and end-of-year dips, Nestlé should align its marketing, inventory, and distribution strategies to match these seasonal patterns. Campaigns and product launches should be timed around July to maximize revenue, while the sharp drop in December 2020 should be investigated to prevent future disruptions, whether due to operational, external, or data issues.',
      iframeSize: 'scale(0.95)'
    },
    // Data set 3
    {
      summary: "The data highlights Nestle's strong reliance on direct sales channels for the majority of its products. However, there's a clear differentiation in online sales penetration, with Maggi leading significantly in online sales, while products like Milo, Nescafe Gold, and Nesquik Duo appear to have little to no online sales contribution in this dataset. Nescafe, Nescau, and Smarties show a more balanced distribution between online and direct channels.",
      keyPoints: [
        'Dominance of Direct Sales. For most Nestle products shown, sales through "Direct" channels significantly outweigh "Online" sales, indicating a strong reliance on traditional distribution.',
        'Zero Online Sales for Specific Products. Milo, Nescafe Gold, and Nesquik Duo recorded 100% of their sales via "Direct" channels, implying no or negligible online sales within this dataset for these items',
        'Maggi\'s High Online Sales. Maggi is a notable exception, with a high 81% of sales coming from "Online," significantly higher than any other product and suggesting a strong digital presence or different consumer purchasing patterns.',
        'Varying Degrees of Online Presence. Other products like Nescafe (49% Online), Nescau (47% Online), Smarties (46% Online), and Nestle Drumstick (39% Online) show varying, but generally moderate, contributions from online sales.',
        'Lowest Online Penetration (among those with online sales). Kit Kat had the lowest online sales percentage among products with an online presence, at just 15%.'
      ],
      iframeSrc: "/chart/sales_distribution_by_product_medium",
      chartHeading: "Sales Distribution by Product (Medium)",
      insight: "Nestlé should enhance its online sales strategy, especially for high-performing products like Milo and Nescafe Gold that currently have no online presence. Since Maggi's strong online performance (81%) proves the potential of digital platforms, a similar push through e-commerce promotions or influencer campaigns could unlock new revenue streams for traditionally Direct-only items.",
      iframeSize: 'scale(0.97)'
    },
    // Data set 4
    {
      summary: "The data highlights Nestle's strong reliance on direct sales channels for the majority of its products. However, there's a clear differentiation in online sales penetration, with Maggi leading significantly in online sales, while products like Milo, Nescafe Gold, and Nesquik Duo appear to have little to no online sales contribution in this dataset. Nescafe, Nescau, and Smarties show a more balanced distribution between online and direct channels.",
      keyPoints: [
        'Dominance of Direct Sales. For most Nestle products shown, sales through "Direct" channels significantly outweigh "Online" sales, indicating a strong reliance on traditional distribution.',
        'Zero Online Sales for Specific Products. Milo, Nescafe Gold, and Nesquik Duo recorded 100% of their sales via "Direct" channels, implying no or negligible online sales within this dataset for these items',
        'Maggi\'s High Online Sales. Maggi is a notable exception, with a high 81% of sales coming from "Online," significantly higher than any other product and suggesting a strong digital presence or different consumer purchasing patterns.',
        'Varying Degrees of Online Presence. Other products like Nescafe (49% Online), Nescau (47% Online), Smarties (46% Online), and Nestle Drumstick (39% Online) show varying, but generally moderate, contributions from online sales.',
        'Lowest Online Penetration (among those with online sales). Kit Kat had the lowest online sales percentage among products with an online presence, at just 15%.'
      ],
      iframeSrc: "/chart/sales_transaction_by_channel",
      chartHeading: "Sales Transaction by Channel",
      insight: "Nestlé should enhance its online sales strategy, especially for high-performing products like Milo and Nescafe Gold that currently have no online presence. Since Maggi's strong online performance (81%) proves the potential of digital platforms, a similar push through e-commerce promotions or influencer campaigns could unlock new revenue streams for traditionally Direct-only items.",
      iframeSize: 'scale(1.5)'
    },
    // Data set 5
    {
      summary: "The monthly sales trend exhibits significant volatility and cyclical patterns between January 2018 and December 2020. Sales generally show mid-year peaks (e.g., July 2018, July 2019, July 2020) and year-end/year-beginning dips. The highest revenue was achieved in July 2019, surpassing $1.2 million. Conversely, the lowest significant point occurred around December 2019, at approximately $0.4 million. A critical observation is the anomalous and sharp decline to near zero revenue in December 2020, which stands out as an extreme outlier and suggests a potential data issue or an extraordinary event impacting sales.",
      keyPoints: [
        "Peak Performance. The highest sales revenue occurred around July 2019, exceeding $1.2M.",
        "Lowest Performance. The lowest significant sales revenue (excluding the final sharp drop) was around December 2019, at approximately $0.4M.",
        "Volatility. The sales show considerable month-to-month volatility, with clear ups and downs.",
        'Potential Seasonality. A pattern of mid-year peaks and year-end/year-beginning dips is observable.',
        'Anomalous December 2020. The almost complete collapse of sales in December 2020 is a critical point that warrants further investigation, as it does not follow the established cyclical pattern and is an extreme outlier.',
      ],
      iframeSrc: "/chart/monthly_sales_trend",
      chartHeading: "Monthly Sales Trend",
      insight: 'Given the clear mid-year peaks and end-of-year dips, Nestlé should align its marketing, inventory, and distribution strategies to match these seasonal patterns. Campaigns and product launches should be timed around July to maximize revenue, while the sharp drop in December 2020 should be investigated to prevent future disruptions, whether due to operational, external, or data issues.',
      iframeSize: 'scale(0.95)'
    },
    // Data set 6
    {
      summary: "This is the summary for data set 6. Presents the monthly revenue forecast using SARIMAX model.",
      keyPoints: [
        "SARIMAX model predicts stable revenue growth.",
        "Forecasts indicate potential for sustained performance.",
        "Model provides reliable projections for future revenue."
      ],
      iframeSrc: "/chart/monthly_revenue_forecast_sarimax",
      chartHeading: "Monthly Revenue Forecast (SARIMAX)",
      insight: 'Insight 6',
      iframeSize: 'scale(0.95)'
    },
  ];

  if (index >= 0 && index < data.length) {
    const selectedData = data[index];

    // Update data-summary paragraph
    const dataSummaryElement = document.getElementById('data-summary');
    if (dataSummaryElement) {
      dataSummaryElement.textContent = selectedData.summary;
    } else {
      console.error("Element with id 'data-summary' not found.");
    }

    // Update key-points as an unordered list
    const keyPointsElement = document.getElementById('key-points');
    if (keyPointsElement) {
      // Clear existing content
      keyPointsElement.innerHTML = '';
      const ul = document.createElement('ul');
      ul.classList.add('list-disc', 'pl-5', 'space-y-1','font-medium'); // Add Tailwind CSS classes for styling

      selectedData.keyPoints.forEach(point => {
        const li = document.createElement('li');
        li.textContent = point;
        ul.appendChild(li);
      });
      keyPointsElement.appendChild(ul);
    } else {
      console.error("Element with id 'key-points' not found.");
    }

    // Update chart heading
    const headingElement = document.getElementById('chart-heading');
    if (headingElement) {
      headingElement.textContent = selectedData.chartHeading;
    } else {
      console.error("Element with id 'chart-heading' not found.");
    }

    // Update insights paragraph
    const insightElement = document.getElementById('insights');
    if (insightElement) {
      insightElement.textContent = selectedData.insight;
    } else {
      console.error("Element with id 'insights' not found.");
    }

    // Update iframe src and style
    const iframeElement = document.getElementById('analytics-iframe');
    if (iframeElement) {
      iframeElement.src = selectedData.iframeSrc;
      iframeElement.style.transform = selectedData.iframeSize; // Adjust scale if needed
    } else {
      console.error("Iframe element not found.");
    }

  } else {
    console.error("Invalid index provided. Please ensure the index is within the bounds of the data array.");
  }
}

// Optional: Call updateContent(0) to load initial data when the page loads
document.addEventListener('DOMContentLoaded', () => {
  updateContent(0);
});

// Example usage:
// Call this function with the desired index to update the content.
// For instance, to load data set 1:
// updateContent(1);

// You can attach this function to buttons or other interactive elements.
// For example, if you have buttons to switch between data sets:
// document.addEventListener('DOMContentLoaded', () => {
//   const button0 = document.getElementById('button-for-data0'); // Assuming you add IDs to your buttons
//   if (button0) {
//     button0.addEventListener('click', () => updateContent(0));
//   }
//   const button1 = document.getElementById('button-for-data1');
//   if (button1) {
//     button1.addEventListener('click', () => updateContent(1));
//   }
// });

