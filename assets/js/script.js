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
      summary: "The map visualizes the total revenue generated across Australia's states and territories, revealing a varied financial landscape. South Australia records the highest revenue at $5.51 million, closely followed by Tasmania with $5.38 million. New South Wales and Queensland exhibit strong performances at $4.25 million and $4.31 million, respectively. The Northern Territory generated $4.14 million, while Victoria reported $3.64 million. The Australian Capital Territory shows a comparatively lower revenue of $3.10 million. Western Australia continues to represent the lowest revenue-generating region, with a total of $485.15K. This distribution highlights distinct regional strengths and areas requiring strategic attention.",
      keyPoints: [
        "<strong>Leading Revenue Contributors:</strong> South Australia and Tasmania are the top-performing regions, with revenues of $5.51 million and $5.38 million, respectively.",
        "<strong>Strong Mid-Tier Performance:</strong> Queensland, New South Wales, and the Northern Territory demonstrate robust revenue contributions, ranging from $4.14 million to $4.31 million.",
        "<strong>Consistent Contribution:</strong> Victoria contributes a solid $3.64 million to the overall revenue.",
        "<strong>Lower-Tier Performance:</strong> The Australian Capital Territory's revenue stands at $3.10 million, placing it in a lower-performing category compared to most states.",
        "<strong>Significant Underperformance:</strong> Western Australia remains the lowest revenue-generating region by a substantial margin, with only $485.15K.",
        "<strong>Revenue Disparity:</strong> A considerable gap exists between the highest-earning regions and Western Australia, indicating varying levels of market penetration or operational success across the country."

      ],
      iframeSrc: "/chart/sales_by_location_map",
      chartHeading: "Revenue Distribution Across Australia",
      insight: "A thorough examination of high-performing markets like South Australia and Tasmania is essential to distill successful strategies for broader application. Western Australia's notably low revenue of $485.15K demands immediate, targeted analysis to address underlying challenges. Strategic interventions within the solid mid-tier regions such as Queensland, New South Wales, Victoria, and the Northern Territory, could also unlock substantial incremental growth, optimizing overall market performance.",
      iframeSize: 'scale(1)'
    },
    // Data set 1
    {
      summary: "The sales data from 2018 to 2020 presents a mixed picture of performance across the product portfolio. While Milo and Nesquik Duo have emerged as resilient and consistent growth drivers, the overarching trend is a significant sales downturn in 2020 that affected most other products. The year 2019 appears to have been a peak for many brands, but this success was not sustained. Moving forward, the focus should be twofold: first, to analyze and reinforce the successful strategies driving the growth of Milo and Nesquik Duo. Second, a thorough investigation is required to understand the root causes of the widespread 2020 decline and the extreme volatility of products like Maggi and Nes Cau to determine if they can be revitalized or if resources should be reallocated.",
      keyPoints: [
        "<strong>Top Performer:</strong> Milo is the leading product in both sales volume and growth trajectory, reaching $2.4M in 2020.",
        "<strong>Consistent Growers:</strong> Milo and Nesquik Duo are the only products with uninterrupted year-over-year sales growth.",
        "<strong>General Trend:</strong> Most products experienced a significant sales decline in 2020 after peaking in 2019.",
        "<strong>Highest Volatility:</strong> Maggi and Nestle Drumstick show the most dramatic fluctuations, with massive growth in 2019 followed by a steep fall.",
        "<strong>Product of Concern:</strong> Nes Cau's sales performance in 2020 indicates a critical issue needing urgent analysis."
      ],
      iframeSrc: "/chart/three_year_sales_trend",
      chartHeading: "Three Year Sales Trend for Each Product",
      insight: "Milo and Nesquik Duo show strong, consistent growth and should be prioritized for increased investment, marketing, and distribution expansion. The sharp decline across most products in 2020 suggests an external disruption, such as a market shift or change in consumer behavior, that should be thoroughly investigated. The company should take immediate corrective action for underperformers like Nes Cau, which saw a near-total sales collapse, and conduct in-depth analysis of Maggi and Nescafe Gold to identify causes of volatility and implement strategies to stabilize and sustain their performance.",
      iframeSize: 'scale(0.95)'
    },
    // Data set 2
    {
      summary: "The \"Total Sales Revenue by Product\" chart illustrates the sales performance of various products, highlighting a clear hierarchy in revenue generation. Milo leads all products with a total revenue of $6.0 million, closely followed by Nescafe at $5.5 million. Nesquik Duo secures the third position with $4.3 million. A mid-tier group includes Nes Cau ($3.3M), Nestle Drumstick ($3.2M), and Smarties ($2.4M). Kit Kat and Maggi both register $2.2 million in revenue, indicating similar performance. Nescafe Gold trails with the lowest revenue at $1.7 million, suggesting it is a comparatively weaker performer. This distribution underscores varying product popularity and market contribution.",
      keyPoints: [
        "<strong>Top Performer:</strong> Milo generates the highest revenue at $6.0 million.",
        "<strong>Close to Top:</strong> Nescafe follows closely behind with $5.5 million in total revenue.",
        "<strong>Significant Third:</strong> Nesquik Duo holds a strong third position, contributing $4.3 million.",
        "<strong>Mid-Tier Product:</strong> Nes Cau ($3.3M), Nestle Drumstick ($3.2M), and Smarties ($2.4M) form a distinct mid-revenue tier.",
        "<strong>Comparable Performance:</strong> Kit Kat and Maggi show similar revenue figures, both at $2.2 million.",
        "<strong>Lowest Revenue:</strong> Nescafe Gold is the lowest-performing product with $1.7 million in revenue.",
        "<strong>Revenue Disparity:</strong> There is a notable difference in revenue across products, with Milo generating over three times the revenue of Nescafe Gold."
      ],
      iframeSrc: "/chart/total_sales_revenue_by_product",
      chartHeading: "Total Sales Revenue by Product",
      insight: 'Strategic emphasis should be placed on amplifying the market penetration and value proposition of Milo and Nescafe, given their leading revenue contributions. A rigorous diagnostic assessment for Nescafe Gold is imperative to identify and mitigate factors contributing to its low revenue. Furthermore, examining the consistent performance of products like Kit Kat and Maggi will inform targeted initiatives aimed at elevating their market standing and revenue generation.',
      iframeSize: 'scale(0.95)'
    },
    // Data set 3
    {
      summary: "The data highlights Nestle's strong reliance on direct sales channels for the majority of its products. However, there's a clear differentiation in online sales penetration, with Maggi leading significantly in online sales, while products like Milo, Nescafe Gold, and Nesquik Duo appear to have little to no online sales contribution in this dataset. Nescafe, Nescau, and Smarties show a more balanced distribution between online and direct channels.",
      keyPoints: [
        '<strong>Dominance of Direct Sales:</strong> For most Nestle products shown, sales through "Direct" channels significantly outweigh "Online" sales, indicating a strong reliance on traditional distribution.',
        '<strong>Zero Online Sales for Specific Products:</strong> Milo, Nestle Drumstick, and Nesquik Duo recorded 100% of their sales via "Direct" channels, implying no or negligible online sales within this dataset for these items',
        '<strong>Maggi\'s Medium Sales:</strong> Maggi with 36% of its sales generated through digital channels. This indicates a significant online presence and consumer preference for Maggi.',
        '<strong>Varying Degrees of Online Presence:</strong> Other products like Nescafe, Nes Cau, Smarties  show varying, but generally moderate, contributions from online sales.',
        '<strong>Lowest Online Penetration (among those with online sales):</strong> Nes Cau had the lowest online sales percentage among products with an online presence.'
      ],
      iframeSrc: "/chart/sales_distribution_by_product_medium",
      chartHeading: "Sales Distribution by Product (Medium)",
      insight: "Nestlé should enhance its online sales strategy, especially for high-performing products like Milo and Nescafe Gold that currently have no online presence. Since Maggi's strong online performance (81%) proves the potential of digital platforms, a similar push through e-commerce promotions or influencer campaigns could unlock new revenue streams for traditionally Direct-only items.",
      iframeSize: 'scale(0.97)'
    },
    // Data set 4
    {
      summary: "The \"Sales Transaction By Channel\" donut chart delineates the distribution of Nestlé's sales transactions across its primary mediums. The Direct channel demonstrably constitutes the majority of transactions, registering 61.56% of the total volume. On the other hand, the Online channel accounts for a substantial, although lesser, proportion at 38.44%. This segmentation underscores a foundational reliance on direct sales methodologies, complemented by a robust and significant contribution from digital sales platforms.",
      keyPoints: [
        "<strong>Dominant Direct Sales:</strong> The Direct channel is the primary medium for Nestlé's sales transactions, representing nearly two-thirds (61.56%) of all sales.",
        '<strong>Significant Online Presence:</strong> The Online channel contributes a substantial 38.44% to total sales transactions, highlighting its importance in the overall sales strategy.',
        '<strong>Channel Disparity:</strong> There is a clear difference in transaction volume between the two channels, with Direct sales significantly outweighing Online sales.'
      ],
      iframeSrc: "/chart/sales_transaction_by_channel",
      chartHeading: "Sales Transaction by Channel",
      insight: "Given the strong performance of the Direct channel, Nestlé should explore strategies to further optimize this channel, perhaps through enhanced direct marketing efforts or by valuing existing customer relationships. Simultaneously, considering the notable contribution of the Online channel, Nestlé could invest in digital marketing campaigns, e-commerce platform improvements, or explore new online partnerships to boost its share.",
      iframeSize: 'scale(1.5)'
    },
    // Data set 5
    {
      summary: "The monthly sales trend exhibits significant volatility and cyclical patterns between January 2018 and December 2020. Sales generally show mid-year peaks (e.g., July 2018, July 2019, July 2020) and year-end/year-beginning dips. The highest revenue was achieved in July 2019, surpassing $1.2 million. Conversely, the lowest significant point occurred around December 2019, at approximately $0.4 million. A critical observation is the anomalous and sharp decline to near zero revenue in December 2020, which stands out as an extreme outlier and suggests a potential data issue or an extraordinary event impacting sales.",
      keyPoints: [
        "<strong>Peak Performance:</strong> The highest sales revenue occurred around July 2019, exceeding $1.2M.",
        "<strong>Lowest Performance:</strong> The lowest significant sales revenue (excluding the final sharp drop) was around December 2019, at approximately $0.4M.",
        "<strong>Volatility:</strong> The sales show considerable month-to-month volatility, with clear ups and downs.",
        "<strong>Potential Seasonality:</strong> A pattern of mid-year peaks and year-end/year-beginning dips is observable.",
        "<strong>Anomalous December 2020:</strong> The almost complete collapse of sales in December 2020 is a critical point that warrants further investigation, as it does not follow the established cyclical pattern and is an extreme outlier.",
      ],
      iframeSrc: "/chart/monthly_sales_trend",
      chartHeading: "Monthly Sales Trend",
      insight: 'Given the clear mid-year peaks and end-of-year dips, Nestlé should align its marketing, inventory, and distribution strategies to match these seasonal patterns. Campaigns and product launches should be timed around July to maximize revenue, while the sharp drop in December 2020 should be investigated to prevent future disruptions, whether due to operational, external, or data issues.',
      iframeSize: 'scale(0.95)'
    },
    // Data set 6
    {
      summary: "The presented chart effectively summarizes the monthly revenue performance and its future outlook. The historical data, processed using Exponential Smoothing, reveals a period of significant revenue fluctuations but with an underlying growth trend. The SARIMAX model's forecast projects a future of stable and sustained revenue growth, albeit with recurring cyclical variations. This indicates that the company anticipates a more predictable financial environment going forward, allowing for better strategic planning and resource allocation. The projections suggest that the company is on track for continued positive financial performance.",
      keyPoints: [
        "<strong>Stable Revenue Growth:</strong> The SARIMAX model predicts stable revenue growth in the coming months. This is evident from the relatively consistent upward trend, albeit with some fluctuations, in the dashed red line representing the forecast.",
        "<strong>Sustained Performance:</strong> The forecasts indicate potential for sustained performance. The projected revenue remains within a reasonable range, suggesting that the company is expected to maintain its financial health.",
        "<strong>Reliable Projections:</strong> The model provides reliable projections for future revenue. While all forecasts have inherent uncertainties, the use of a sophisticated model like SARIMAX suggests an effort to provide robust estimates."
      ],
      iframeSrc: "/chart/monthly_revenue_forecast_sarimax",
      chartHeading: "Monthly Revenue Forecast (SARIMAX)",
      insight: 'Revenue has shown strong but erratic growth from 2018 to early 2021, marked by sharp dips likely caused by seasonality, shifting demand, or internal business factors. The forecast projects a more stable and gradually increasing trend between $300,000 and $500,000, with visible cyclical patterns that suggest recurring seasonal influences. To fully leverage this forecast, the company should align sales campaigns and inventory management with predicted peak periods, implement measures to smooth out past volatility, and enhance resilience to market shocks.',
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
        li.innerHTML = point;
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

