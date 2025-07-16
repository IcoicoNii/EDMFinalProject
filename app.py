from flask import Flask, request, render_template_string, render_template, jsonify # Ensure render_template is here
import pandas as pd
import os
import plotly.graph_objects as go
import plotly.express as px
import altair as alt
import folium
import json
from statsmodels.tsa.statespace.sarimax import SARIMAX # New import for SARIMAX
from statsmodels.tsa.holtwinters import ExponentialSmoothing # New import for ExponentialSmoothing



# Define a refined color palette based on the provided dashboard image
nestle_colors = {
    # General Backgrounds
    'dashboard_bg': '#F8F8F8', # Very light grey/off-white for dashboard background
    'chart_area_bg': '#FFFFFF', # Pure white for individual chart plotting areas
    'kpi_box_bg': '#FFFFFF', # White background for KPI boxes
    'kpi_box_border': '#E0E0E0', # Light grey border for KPI boxes

    # KPI Text Colors (matching the vibrant colors in the image)
    'kpi_title_text': '#666666', # Medium grey for KPI titles
    'kpi_value_total_revenue': '#007BFF', # Bright Blue for Total Revenue
    'kpi_value_avg_revenue': '#28A745', # Green for Average Revenue
    'kpi_value_total_products': '#17A2B8', # Light Blue/Cyan for Total Products
    'kpi_value_total_sales': '#FFC107', # Orange for Total Sales
    'kpi_value_max_min_revenue': '#007BFF', # Blue for Max/Min Revenue values

    # Chart Specific Colors (derived from dashboard image)
    'donut_channel_1': '#007BFF', # Blue (primary)
    'donut_channel_2': '#DC3545', # Red (secondary)
    'donut_channel_3': '#28A745', # Green (tertiary, if more slices)
    'donut_channel_4': '#FFC107', # Orange (quaternary)
    'donut_center_text': '#333333', # Dark grey for center text

    'bar_year_2018': '#FFC107', # Orange for 2018 bars
    'bar_year_2019': '#DC3545', # Red for 2019 bars
    'bar_year_2020': '#007BFF', # Blue for 2020 bars

    'product_revenue_gradient_start': '#CCE5FF', # Very light blue (low revenue)
    'product_revenue_gradient_end': '#007BFF', # Darker blue (high revenue)

    'sales_location_gradient_start': '#D4EDDA', # Very light green (low sales)
    'sales_location_gradient_end': '#28A745', # Darker green (high sales)

    'monthly_trend_line_color': '#007BFF', # Bright Blue for monthly trend line
    'monthly_trend_fill_color': 'rgba(0,123,255,0.1)', # Light blue fill with transparency

    'map_color_low': '#BEE5EB', # Light cyan/blue for low map values
    'map_color_mid': '#17A2B8', # Cyan/teal for mid map values
    'map_color_high': '#DC3545', # Red for high map values
    'map_land_fill': '#F5F5F5', # Very light grey for non-data land
    'map_border_color': '#AAAAAA', # Medium grey for map borders

    # Text and Grid Colors for Light Theme
    'title_text_color': '#333333', # Dark grey for main chart titles
    'axis_label_color': '#555555', # Medium dark grey for axis titles
    'tick_label_color': '#777777', # Lighter grey for tick labels
    'grid_line_color': '#EFEFEF', # Very subtle light grey grid lines
    'zero_line_color': '#BBBBBB', # Medium light grey for zero line
    'legend_text_color': '#555555', # Medium dark grey for legend text
    'hover_bg_color': '#333333', # Dark background for hover tooltips
    'hover_text_color': '#FFFFFF', # White text for hover tooltips

    # NEW COLORS FOR FORECAST CHART
    'forecast_historical_line': '#007BFF', # Blue for historical data line
    'forecast_line': '#DC3545', # Red for forecast line
    'forecast_fill': 'rgba(220,53,69,0.1)' # Light red fill for prediction interval
}


app = Flask(__name__, static_folder='assets') # <--- ADD static_folder='assets'

# --- Configuration for Data File ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
EXCEL_FILE_PATH = os.path.join(BASE_DIR, 'assets', 'data', 'nestle_sales_data.xlsx')
GEOJSON_FILE_PATH = os.path.join(BASE_DIR, 'assets', 'data', 'australian-states.geojson') # Path to your NEW GeoJSON file

df = None
geojson_data = None # Initialize geojson_data globally

def load_data():
    """Loads data from the Excel file into a Pandas DataFrame."""
    global df
    try:
        df = pd.read_excel(EXCEL_FILE_PATH, engine='openpyxl')
        df['Date'] = pd.to_datetime(df['Date'])
        df['Month'] = df['Date'].dt.month_name()
        df['Year'] = df['Date'].dt.year
        df['Month_Year'] = df['Date'].dt.to_period('M').astype(str) # For monthly trend plotting


        print(f"Data loaded successfully from: {EXCEL_FILE_PATH}")
        print(df.head())
        print(df.info())
    except FileNotFoundError:
        print(f"Error: Excel file not found at {EXCEL_FILE_PATH}")
        df = pd.DataFrame()
    except KeyError as ke:
        print(f"KeyError: A required column was not found in the Excel file: {ke}")
        print("Please check your Excel column names carefully (case-sensitive) and update app.py if needed.")
        df = pd.DataFrame()
    except Exception as e:
        print(f"An unexpected error occurred while loading data: {e}")
        df = pd.DataFrame()

def load_geojson_data():
    """Loads GeoJSON data for Australian states from a local file."""
    global geojson_data
    try:
        if os.path.exists(GEOJSON_FILE_PATH):
            with open(GEOJSON_FILE_PATH, 'r') as f:
                geojson_data = json.load(f)
            print(f"GeoJSON data loaded successfully from: {GEOJSON_FILE_PATH}")
        else:
            print(f"ERROR: GeoJSON file not found at {GEOJSON_FILE_PATH}.")
            print("Please ensure 'my_australian_states.json' is in your 'assets/data/' folder.")
            geojson_data = {"type": "FeatureCollection", "features": []} # Empty GeoJSON on error
    except Exception as e:
        print(f"An error occurred while loading GeoJSON data: {e}")
        geojson_data = {"type": "FeatureCollection", "features": []} # Empty GeoJSON on error

with app.app_context():
    load_data()
    load_geojson_data()

# --- Helper function for rendering chart HTML ---
def render_chart_template(chart_html, title="Chart"):
    """Helper to render the HTML content for an iframe chart."""
    # The key is that chart_content is passed as a variable to render_template_string
    # which then correctly processes it using Jinja2 within Flask's context.
    return render_template_string("""
        <!DOCTYPE html>
        <html>
        <head>
            <title>{{ title }}</title>
            <style>
                
                

                html, body {
                    margin: 0;
                    padding: 0;
                    overflow: hidden;
                    height: 100%; /* Ensure body takes full iframe height */
                    width: 100%;  /* Ensure body takes full iframe width */
                    display: flex; /* Use flexbox to center chart if needed */
                    justify-content: center;
                    align-items: center;
                }
                .plotly-container {
                                    
                    overflow:hidden;
                    width: 100%;
                    height: 100%;
                    display: flex; /* Makes the chart's container a flex container */
                    justify-content: center; /* Centers content horizontally within the plotly-container */
                    align-items: center; /* Centers content vertically within the plotly-container */
                                        
                }
                                    
                /* Specific styles for Folium maps */
                .folium-map {
                    border-radius: 8px; /* Apply border-radius to the map itself */
                    width: 100%; /* Ensure map fills its container */
                    height: 100%; /* Ensure map fills its container */
                }

            </style>
        </head>
        <body>
            <div class="plotly-container">
                {{ chart_content | safe }}
            </div>
        </body>
        </html>
    """, chart_content=chart_html, title=title)



# --- Flask Routes for your Charts ---

# --- Flask Routes ---

@app.route('/') # <--- ADD THIS BLOCK
def index():
    return render_template('index.html')

# Define the common Plotly config for responsiveness
PLOTLY_CONFIG = {
    'responsive': True,
    'displayModeBar': False # Optional: Hide the Plotly modebar (save, zoom, etc.)
}

# CENTER CHART
@app.route('/chart/three_year_sales_trend')
def three_year_sales_trend_chart():
    """
    Generates an Altair bar chart showing three-year sales trends by product.
    This version is non-interactive but includes tooltips.
    """
    if df.empty:
        return "<h1>Data not loaded or unavailable.</h1>", 500

    # Aggregate total revenue by year and product name
    grouped_df = df.groupby(['Year', 'Product Name'])['Total Revenue'].sum().reset_index()

    # Create the base chart with common encodings
    base = alt.Chart(grouped_df).encode(
        # Y-axis: Total Revenue, formatted to show K and M
        y=alt.Y('Total Revenue', axis=alt.Axis(format='.2s', title='Total Sales')),
        # X-axis: Year, within each Product Name facet
        x=alt.X('Year:O', title=None, axis=alt.Axis(labels=True)),
        tooltip=['Product Name', 'Year', alt.Tooltip('Total Revenue', format='.2s')] # Tooltip for bars
    )

    # Create the bar chart
    bars = base.mark_bar().encode(
        # Updated color scale to use specific hex codes for 2018, 2019, and 2020
        color=alt.Color('Year:N',
                        scale=alt.Scale(domain=[2018, 2019, 2020], range=['#0990FF', '#1069BC', '#064885']),
                        legend=None) # <--- ADDED: legend=None to remove the legend
    )

    # Add text labels for the total revenue at the top of each bar
    value_text = base.mark_text(align='center', baseline='bottom', dy=5, dx=-15).encode(
        text=alt.Text('Total Revenue', format='.2s'),  # Format the text as well
        order='Year:O',
        color=alt.value('white'),  # Set text color to white for visibility
        angle=alt.value(270) # Rotates the text by 270 degrees (equivalent to -90 degrees)

    )

    # Layer the bar chart and value labels
    # Removed .interactive() method
    layered_chart = alt.layer(bars, value_text).properties(
        width=alt.Step(17.5), # Use alt.Step for width in faceted charts to control individual facet width
        height=175
    )

    # Facet the layered chart by Product Name
    final_chart = layered_chart.facet(
        column=alt.Column('Product Name:N', header=alt.Header(titleOrient="bottom", labelOrient="bottom"))
    ).properties(
        # Title of the chart
        title='Three Year Sales Trend for Each Product'
    )

    # Convert the Altair chart to HTML.
    # Set 'actions': False to hide the default menu for save/zoom.
    chart_html = final_chart.to_html(embed_options={'actions': False, 'autosize': 'fit'}) # <--- Changed to False

    return render_chart_template(chart_html, "Three Year Sales Trend for Each Product")

# UPPER RIGHT CHART
@app.route('/chart/total_sales_revenue_by_product')
def total_sales_revenue_by_product_data():
    if df.empty:
        return "<div>Error: Data not loaded or available.</div>", 500

    # Group by 'Product Name' (corrected from 'Product') and sum 'Total Revenue'
    product_revenue = df.groupby('Product Name')['Total Revenue'].sum().reset_index()

    # Sort in descending order of 'Total Revenue'
    product_revenue = product_revenue.sort_values('Total Revenue', ascending=False)

    # Define the custom color scheme
    color_scheme = ['#0A477D', '#0F68BD', '#0E6BB8', '#1068C2', '#0C69BD', '#0D69BD', '#1069B5', '#0B6BC1', '#9ED2FA']

    # Create the bar chart using Plotly Express
    fig = px.bar(product_revenue,
                 x='Product Name', # Corrected from 'Product'
                 y='Total Revenue',
                 title='Total Sales Revenue by Product',
                 labels={'Product Name': 'Product Name', 'Total Revenue': 'Sum of Total Revenue'}, # Corrected label
                 color='Product Name', # Corrected from 'Product'
                 color_discrete_sequence=color_scheme, # Apply custom color scheme
                 text_auto=True, # Automatically add text labels on bars
                 hover_data={'Product Name': True, 'Total Revenue': ':.2f'} # Customize tooltip format
                )

    # Update layout for better aesthetics and specific requirements
    fig.update_layout(
        font_family="Arial",
        title_font_size=20,
        title_font_color="#333",
        xaxis_title_font_size=14,
        yaxis_title_font_size=14,
        plot_bgcolor='rgba(0,0,0,0)', # Transparent background
        paper_bgcolor='rgba(0,0,0,0)', # Transparent paper background
        margin=dict(l=40, r=40, t=60, b=40), # Adjust margins
        showlegend=False # Remove the legend as specified in Altair code
    )

    # Rotate x-axis labels and format y-axis
    fig.update_xaxes(showgrid=False, tickangle=-45)
    fig.update_yaxes(showgrid=True, gridcolor='#e0e0e0', tickformat='$.2s') # Format for millions and dollar sign

    # Set text color to black for better visibility if needed (text_auto usually handles this well)
    fig.update_traces(textfont_color='black')


    return fig.to_html(full_html=False, default_height='100%', default_width='100%')


# PIE CHART UPPER LEFT
from flask import request # Make sure to import request

@app.route('/chart/sales_transaction_by_channel')
def sales_transaction_by_channel_chart():
    print(f"DEBUG: Entering sales_transaction_by_channel_chart.")
    print(f"DEBUG: Type of df at start of function: {type(df)}")
    print(f"DEBUG: Is df empty? {df.empty if isinstance(df, pd.DataFrame) else 'Not a DataFrame'}")
    if isinstance(df, pd.DataFrame) and not df.empty:
        print(f"DEBUG: df columns: {df.columns.tolist()}")

    # Ensure df is a DataFrame and not empty
    if not isinstance(df, pd.DataFrame) or df.empty:
        return "<div>Error: Data not loaded or available for Sales Transaction by Channel.</div>", 500

    try:
        # Check if 'Sales Medium' column exists
        if 'Sales Medium' not in df.columns:
            print("DEBUG: 'Sales Medium' column not found in df. Columns available:", df.columns.tolist())
            return "<div>Error: 'Sales Medium' column not found in data.</div>", 500

        print(f"DEBUG: Type of df['Sales Medium'] before value_counts: {type(df['Sales Medium'])}")
        # Calculate the value counts and reset the index to create a DataFrame
        sales_medium_counts = df['Sales Medium'].value_counts().reset_index()
        print("DEBUG: sales_medium_counts created.")
        print(f"DEBUG: sales_medium_counts head:\n{sales_medium_counts.head()}")
        print(f"DEBUG: Unique Sales Medium values in sales_medium_counts: {sales_medium_counts['Sales Medium'].unique().tolist()}")

        # Rename the columns for clarity
        sales_medium_counts.columns = ['Sales Medium', 'count']
        print("DEBUG: sales_medium_counts columns renamed.")

        # Define the color scale for 'Online' and 'Direct'
        color_map = {
            'Online': '#0990FF',
            'Direct': '#064885'
        }

        # Prepare data for go.Pie, ensuring order
        # Sort by 'Sales Medium' to ensure consistent color mapping and display order
        sales_medium_counts = sales_medium_counts.sort_values(by='Sales Medium', ascending=True)

        labels = sales_medium_counts['Sales Medium'].tolist()
        values = sales_medium_counts['count'].tolist()
        colors = [color_map.get(label, '#CCCCCC') for label in labels] # Fallback color if not in map

        # --- Start of Highlight Logic ---
        highlight_channel = request.args.get('highlight')
        pull_values = [0] * len(labels) # Initialize all pull values to 0 (no pull)

        if highlight_channel and highlight_channel in labels:
            try:
                # Find the index of the channel to highlight
                highlight_index = labels.index(highlight_channel)
                pull_values[highlight_index] = 0.1 # Pull out the slice by 10%
                print(f"DEBUG: Highlighting '{highlight_channel}'. Pull value set for index {highlight_index}.")
            except ValueError:
                # Should not happen if highlight_channel is checked against labels
                print(f"DEBUG: Highlight channel '{highlight_channel}' not found in labels, no pull applied.")
        # --- End of Highlight Logic ---

        # Create the donut chart using plotly.graph_objects
        fig = go.Figure(data=[go.Pie(
            labels=labels,
            values=values,
            hole=0.5, # Creates the donut effect
            marker_colors=colors, # Apply custom colors
            textinfo='label+percent+value', # Show label, percentage, and value on slices
            textposition='inside', # Position text inside slices
            textfont_color='white', # Set text color to white
            marker=dict(line=dict(color='#FFFFFF', width=1)), # Add white border to slices
            hovertemplate='<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}<extra></extra>',
            insidetextorientation='horizontal', # Make labels horizontal (not slanted)
            pull=pull_values # Apply the pull effect here
        )])
        print("DEBUG: Plotly figure created using go.Figure.")

        # Update layout for title and general aesthetics
        fig.update_layout(
            title_text='Sales Transaction By Channel',
            title_x=0.5,  # Center the title
            font_family="Arial",
            title_font_weight="bold",
            title_font_size=10,
            title_font_color="#0A477D",  # Use the specified title color
            margin=dict(l=10, r=10, t=20, b=5),  # Add a small gap above the chart by increasing top margin
            showlegend=False,  # Remove the legend
            plot_bgcolor='rgba(0,0,0,0)',  # Transparent background
            paper_bgcolor='rgba(0,0,0,0)',  # Transparent paper background
            width=300,  # Set width as specified in Altair
            height=180  # Set height as specified in Altair
        )
        print("DEBUG: Plotly layout updated.")

        # Convert Plotly figure to HTML
        chart_html = fig.to_html(full_html=False, config=PLOTLY_CONFIG)
        print("DEBUG: Chart HTML generated successfully.")
        return render_chart_template(chart_html, "Sales Transaction By Channel")
    except Exception as e:
        # Catch any other unexpected errors during chart generation
        print(f"DEBUG: An error occurred during chart generation: {e}")
        return f"<div>Error generating Sales Transaction by Channel chart: {e}</div>", 500

@app.route('/chart/sales_distribution_by_product_medium')
def sales_distribution_by_product_medium_chart():
    """
    Generates a stacked horizontal bar chart showing the percentage distribution
    of sales by product medium for each product.
    """
    if not isinstance(df, pd.DataFrame) or df.empty:
        return "<div>Error: Data not loaded or available for Sales Distribution by Product Medium.</div>", 500

    try:
        # Step 1: Process the data
        # Group by product and sales medium to get the sales count for each.
        product_sales = df.groupby(['Product Name', 'Sales Medium'])['Sales Count'].sum().reset_index()

        # Step 2: Calculate the percentage of sales for each medium within each product
        # We use transform('sum') to get the total sales per product, which allows for a clean percentage calculation.
        product_sales['Percentage'] = 100 * (product_sales['Sales Count'] / product_sales.groupby('Product Name')['Sales Count'].transform('sum'))

        # Fill NaN values with 0 for products that may have sales in only one medium.
        product_sales['Percentage'] = product_sales['Percentage'].fillna(0)

        # Step 3: Set a specific order for products on the Y-axis to match the desired presentation
        product_order = [
            'Smarties', 'Nesquik Duo', 'Nescafe Gold', 'Nes Cau',
            'Maggi', 'Milo', 'Kit Kat', 'Nestle Drumstick', 'Nescafe'
        ]
        product_sales['Product Name'] = pd.Categorical(product_sales['Product Name'], categories=product_order, ordered=True)
        product_sales = product_sales.sort_values('Product Name')

        # Step 4: Define the specific colors for this chart
        medium_colors = {
            'Direct': '#004C99',  # Darker blue
            'Online': '#007BFF'   # Lighter, vibrant blue from your KPI palette
        }

        # Step 5: Create the stacked horizontal bar chart
        fig_product_medium = px.bar(
            product_sales,
            x='Percentage',
            y='Product Name',
            color='Sales Medium',
            orientation='h',
            barmode='stack',
            color_discrete_map=medium_colors,
            text='Percentage' # Display the percentage value on the bar
        )

        # Step 6: Apply the standard theme and customize the chart with explicit width
        # Re-using render_chart_template which handles basic layout, but applying specific plotly updates here
        fig_product_medium.update_layout(
            title=dict(text='% Sales of Product Medium', x=0.5), # Centered title
            xaxis_title='Sales Percentage (%)', # X-axis title
            yaxis_title='',                     # Y-axis title (is clear from labels)
            height=300,                         # Set a fixed height for the chart
            width=400,                          # Set the width
            font_family="Arial",
            title_font_size=15,
            title_font_color="#333",
            xaxis_title_font_size=14,
            yaxis_title_font_size=14,
            plot_bgcolor='rgba(0,0,0,0)', # Transparent background
            paper_bgcolor='rgba(0,0,0,0)', # Transparent paper background
            margin=dict(l=40, r=40, t=60, b=10), # Adjust margins
            legend=dict(
                title_text="Medium",
                orientation="h",
                yanchor="bottom",
                y=1,
                xanchor="right",
                x=1
            ),
            bargap=0.2, # Adjust the gap between bars
        )

        # Step 7: Refine traces for a polished look
        fig_product_medium.update_traces(
            texttemplate='%{x:.0f}%', # Format the text on bars to be a clean percentage
            textposition='inside',
            insidetextfont=dict(color='white', size=14, family='Arial'), # Make inside text bold and clear
            hovertemplate="<b>%{y}</b><br>" +
                          "Medium: %{fullData.name}<br>" + # Use fullData.name to get the legend entry
                          "Sales: %{x:.1f}%<extra></extra>" # Use 'x' for the percentage value
        )

        fig_product_medium.update_layout(
            xaxis=dict(
            range=[0, 100],
            tickvals=[0, 25, 50, 75, 100],
            visible=False  # Hide the x-axis
            ),
            yaxis=dict(showgrid=False),
        )

        # Convert Plotly figure to HTML
        chart_html = fig_product_medium.to_html(full_html=False, config=PLOTLY_CONFIG)
        return render_chart_template(chart_html, "% Sales of Product Medium")

    except Exception as e:
        print(f"DEBUG: An error occurred during sales_distribution_by_product_medium_chart generation: {e}")
        return f"<div>Error generating Sales Distribution by Product Medium chart: {e}</div>", 500

@app.route('/chart/monthly_sales_trend')
def monthly_sales_trend_chart():
    """
    Generates a line chart showing the monthly sales trend.
    """
    print(f"DEBUG: Entering monthly_sales_trend_chart.")
    print(f"DEBUG: Type of df at start of function: {type(df)}")
    print(f"DEBUG: Is df empty? {df.empty if isinstance(df, pd.DataFrame) else 'Not a DataFrame'}")
    if isinstance(df, pd.DataFrame) and not df.empty:
        print(f"DEBUG: df columns: {df.columns.tolist()}")
        if 'Month_Year' in df.columns:
            print(f"DEBUG: First 5 entries of 'Month_Year': {df['Month_Year'].head().tolist()}")
        else:
            print("DEBUG: 'Month_Year' column NOT found in df.")

    if not isinstance(df, pd.DataFrame) or df.empty:
        return "<div>Error: Data not loaded or available for Monthly Sales Trend.</div>", 500

    try:
        # Data processing
        monthly_revenue = df.groupby('Month_Year')['Total Revenue'].sum().reset_index()
        monthly_revenue['Date_Sort'] = pd.to_datetime(monthly_revenue['Month_Year'])
        monthly_revenue = monthly_revenue.sort_values('Date_Sort').drop('Date_Sort', axis=1)

        # Create the line chart
        fig_monthly_line = px.line(monthly_revenue,
                                   x='Month_Year',
                                   y='Total Revenue',
                                   labels={'Total Revenue': 'Total Revenue ($)', 'Month_Year': 'Month-Year'},
                                   markers=True,
                                   line_shape='spline', # Smooth line
                                   color_discrete_sequence=[nestle_colors['monthly_trend_line_color']], # Blue line
                                   hover_data={'Total Revenue':':$,.2f'},
                                   render_mode='svg' # Ensures sharp lines
                                  )

        # Update traces for styling
        fig_monthly_line.update_traces(
            mode='lines+markers', # Ensure both lines and markers are shown
            marker=dict(size=8, line=dict(width=1.5, color=nestle_colors['monthly_trend_line_color'])), # Style markers
            line=dict(width=3), # Thicker line
            fill='tozeroy', # Fill area under the line
            fillcolor=nestle_colors['monthly_trend_fill_color'] # Light blue fill with transparency
        )

        # Apply layout and theme
        fig_monthly_line.update_layout(
            title=dict(text='Monthly Sales Trend', x=0.5), # Centered title
            xaxis_title='Month-Year',
            yaxis_title='Total Revenue ($)',
            showlegend=False,
            height=175,
            font_family="Arial",
            title_font_size=10,
            title_font_color="#333",
            xaxis_title_font_size=10,
            yaxis_title_font_size=14,
            plot_bgcolor='rgba(0,0,0,0)', # Transparent background
            paper_bgcolor='rgba(0,0,0,0)', # Transparent paper background
            margin=dict(l=10, r=10, t=40, b=10), # Adjust margins
            hoverlabel=dict(
                bgcolor='#333333', # Example hover background
                font_color='#FFFFFF', # Example hover text color
                font_family="Arial"
            )
        )

        # Convert Plotly figure to HTML
        chart_html = fig_monthly_line.to_html(full_html=False, config=PLOTLY_CONFIG)
        return render_chart_template(chart_html, "Monthly Sales Trend")

    except Exception as e:
        print(f"DEBUG: An error occurred during monthly_sales_trend_chart generation: {e}")
        return f"<div>Error generating Monthly Sales Trend chart: {e}</div>", 500

@app.route('/kpi_data')
def kpi_data():
    """
    Calculates and returns Key Performance Indicator (KPI) data.
    """
    if df.empty:
        return jsonify({"error": "Data not loaded or available for KPIs."}), 500

    try:
        total_revenue = df['Total Revenue'].sum()
        average_revenue = df['Total Revenue'].mean()
        total_unique_products = df['Product Name'].nunique() # Number of unique product names
        total_sales_count = df['Sales Count'].sum() # Sum of the 'Sales Count' column
        max_revenue = df['Total Revenue'].max()
        min_revenue = df['Total Revenue'].min()

        kpis = {
            "total_revenue": f"${total_revenue:,.2f}",
            "average_revenue": f"${average_revenue:,.2f}",
            "total_unique_products": f"{total_unique_products:,}",
            "total_sales_count": f"{total_sales_count:,}",
            "max_revenue": f"${max_revenue:,.2f}",
            "min_revenue": f"${min_revenue:,.2f}"
        }
        return jsonify(kpis)
    except KeyError as ke:
        return jsonify({"error": f"Missing column for KPI calculation: {ke}"}), 500
    except Exception as e:
        return jsonify({"error": f"An error occurred during KPI calculation: {e}"}), 500

@app.route('/chart/monthly_revenue_forecast_sarimax')
def monthly_revenue_forecast_sarimax_chart():
    """
    Generates a monthly revenue forecast chart using Exponential Smoothing model.
    Includes historical data, forecasted data, and a 95% prediction interval.
    """
    print(f"DEBUG: Entering monthly_revenue_forecast_sarimax_chart (Exponential Smoothing version).")
    print(f"DEBUG: Type of df at start of function: {type(df)}")
    print(f"DEBUG: Is df empty? {df.empty if isinstance(df, pd.DataFrame) else 'Not a DataFrame'}")
    if isinstance(df, pd.DataFrame) and not df.empty:
        print(f"DEBUG: df columns: {df.columns.tolist()}")
        if 'Date' in df.columns:
            print(f"DEBUG: First 5 entries of 'Date': {df['Date'].head().tolist()}")
        else:
            print("DEBUG: 'Date' column NOT found in df.")
    print(f"DEBUG: nestle_colors dictionary: {nestle_colors}")


    if not isinstance(df, pd.DataFrame) or df.empty:
        return "<div>Error: Data not loaded or available for Monthly Revenue Forecast.</div>", 500

    try:
        # Aggregate total revenue by month (start of month)
        monthly_revenue = df.groupby(pd.Grouper(key='Date', freq='MS'))['Total Revenue'].sum().reset_index()
        monthly_revenue.columns = ['Date', 'Total Revenue']
        monthly_revenue = monthly_revenue.set_index('Date') # Set Date as index for time series models

        # Fit an Exponential Smoothing model
        # Using seasonal='add' for additive seasonality and seasonal_periods=12
        model = ExponentialSmoothing(monthly_revenue['Total Revenue'], seasonal='add', seasonal_periods=12)
        results = model.fit()

        # Forecast for the next 36 months (3 years)
        forecast_periods = 36
        forecast_index = pd.date_range(start=monthly_revenue.index[-1] + pd.DateOffset(months=1), periods=forecast_periods, freq='MS')
        forecast_values = results.forecast(steps=forecast_periods)

        # Exponential Smoothing does not directly provide prediction intervals like SARIMAX's conf_int()
        # For simplicity and to match the previous structure, we'll create dummy bounds or skip them if not critical.
        # If prediction intervals are critical, a more complex implementation or a different model might be needed.
        # For now, we'll use a simplified approach to generate bounds for visualization purposes.
        # A common heuristic is to use a fixed percentage of the forecast as bounds, or derive from residuals.
        # For demonstration, let's use a simple +/- 10% for bounds.
        # In a real-world scenario, you'd calculate this more rigorously (e.g., from model residuals).
        forecast_df = pd.DataFrame({
            'Date': forecast_index,
            'Forecasted Revenue': forecast_values,
            'Lower Bound': forecast_values * 0.9, # Simplified lower bound
            'Upper Bound': forecast_values * 1.1  # Simplified upper bound
        }).reset_index(drop=True) # Reset index to avoid duplicate 'Date' column from index

        # Combine historical and forecast data
        historical_df_reset = monthly_revenue.reset_index() # Reset index to make 'Date' a column
        combined_df = pd.concat([historical_df_reset, forecast_df])


        # Create Altair chart
        # Base chart
        base = alt.Chart(combined_df).encode(
            x=alt.X('Date:T', title='Date', axis=alt.Axis(format='%b %Y')) # Format date
        )

        # Historical data line
        print(f"DEBUG: Attempting to access nestle_colors['forecast_historical_line']. Current nestle_colors: {nestle_colors}")
        historical_line = base.mark_line(color=nestle_colors['forecast_historical_line']).encode(
            y=alt.Y('Total Revenue:Q', title='Total Revenue', axis=alt.Axis(format='$,.0s')), # Format Y-axis labels
            tooltip=[alt.Tooltip('Date:T', format='%b %Y'), alt.Tooltip('Total Revenue:Q', title='Historical Revenue', format='$,.2f')]
        )

        # Forecasted data line - now connects to the end of the historical line
        # Use a condition to only show Forecasted Revenue where it's not null
        forecast_line = base.mark_line(color=nestle_colors['forecast_line'], strokeDash=[5, 5]).encode(
            y=alt.Y('Forecasted Revenue:Q', title='Total Revenue'),
            tooltip=[alt.Tooltip('Date:T', format='%b %Y'), alt.Tooltip('Forecasted Revenue:Q', title='Forecasted Revenue', format='$,.2f')]
        )

        # Prediction interval area
        prediction_interval = base.mark_area(opacity=0.2, color=nestle_colors['forecast_fill']).encode(
            y='Lower Bound:Q',
            y2='Upper Bound:Q',
            tooltip=[alt.Tooltip('Date:T', format='%b %Y'), alt.Tooltip('Lower Bound:Q', title='Lower Bound', format='$,.2f'), alt.Tooltip('Upper Bound:Q', title='Upper Bound', format='$,.2f')]
        )
        
        # Combine the layers
        chart = alt.layer(historical_line, forecast_line, prediction_interval).properties(
            title='Monthly Revenue Forecast (Exponential Smoothing)',
            width='container', # Make chart responsive to container width
            height=200
        ).interactive() # Make the chart interactive (zoom, pan)

        # Convert the Altair chart to HTML
        chart_html = chart.to_html(embed_options={'actions': False, 'autosize': 'fit'})
        print("DEBUG: Chart HTML generated successfully.")
        return render_chart_template(chart_html, "Monthly Revenue Forecast")

    except Exception as e:
        print(f"DEBUG: An error occurred during monthly_revenue_forecast_sarimax_chart generation: {e}")
        return f"<div>Error generating Monthly Revenue Forecast chart: {e}</div>", 500

@app.route('/chart/sales_by_location_map')
def sales_by_location_map():
    """
    Generates a choropleth map of Australia showing total revenue by state.
    Includes formatted revenue values in tooltips and popups.
    Allows for dynamic height and width modifications via URL parameters.
    """
    if df.empty or geojson_data is None:
        return "<div>Error: Data or GeoJSON not loaded or available for Sales Location Map.</div>", 500

    # Aggregate total revenue by 'Sales Location'
    # Ensure 'Sales Location' column exists in your DataFrame
    if 'Sales Location' not in df.columns:
        return "<div>Error: 'Sales Location' column not found in data. Cannot generate map.</div>", 500

    sales_by_location = df.groupby('Sales Location')['Total Revenue'].sum().reset_index()

    # Function to format revenue for readability (K for thousands, M for millions)
    def format_revenue_for_map(revenue):
        if pd.isna(revenue):
            return "N/A"
        if revenue >= 1_000_000:
            return f'${revenue/1_000_000:,.2f}M'
        elif revenue >= 1_000:
            return f'${revenue/1_000:,.2f}K'
        else:
            return f'${revenue:,.2f}'

    # Get height and width from query parameters, with default values
    # You can specify units (e.g., '100%', '800px')
    map_height = request.args.get('height', '100%')  # Default height
    map_width = request.args.get('width', '100%')    # Default width

    # Create a base map of Australia
    australia_map = folium.Map(
        location=[-25, 135],
        zoom_start=3,
        control_scale=True,
        height=map_height,  # Apply height
        width=map_width     # Apply width
    )

    # Add the GeoJSON layer with the sales data
    choropleth = folium.Choropleth(
        geo_data=geojson_data,
        name='choropleth',
        data=sales_by_location,
        columns=['Sales Location', 'Total Revenue'],
        key_on='feature.properties.STATE_NAME',
        fill_color='YlGn',
        fill_opacity=0.7,
        line_opacity=0.2,
        # --- MODIFICATION START: Move colorbar to the middle ---
        colorbar_kwargs={
            'position': (0, 0), # (left, bottom) - Adjust these values for bottom-left. 0,0 is typically the bottom-left corner.
            'min_width': 100,
            'max_width': 100,
            'min_height': 300,
            'max_height': 300,
            'relative': True
        }
        # --- MODIFICATION END ---
    ).add_to(australia_map)

    # Add tooltips to display formatted revenue on hover
    choropleth.geojson.add_child(
        folium.features.GeoJsonTooltip(
            fields=['STATE_NAME'],
            aliases=['State:'],
            localize=True,
            labels=True,
            sticky=True,
            style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 6px;")
        )
    )

    # Add popups with formatted revenue on click
    for feature in geojson_data['features']:
        state_name = feature['properties'].get('STATE_NAME')
        if state_name:
            sales_data_row = sales_by_location[sales_by_location['Sales Location'] == state_name]
            if not sales_data_row.empty:
                total_revenue = sales_data_row.iloc[0]['Total Revenue']
                formatted_revenue = format_revenue_for_map(total_revenue)
                popup_text = f"<b>{state_name}</b><br>Total Revenue: {formatted_revenue}"

                folium.GeoJson(
                    feature,
                    tooltip=f"{state_name}",
                    popup=folium.Popup(popup_text)
                ).add_to(australia_map)

    # Add layer control to toggle choropleth (optional)
    folium.LayerControl().add_to(australia_map)

    # Convert the Folium map to HTML
    map_html = australia_map._repr_html_()
    return render_chart_template(map_html, "Sales Distribution by Location")














# MAIN
if __name__ == '__main__':
    # Create the assets/data and assets/charts directories if they don't exist
    os.makedirs('assets/data', exist_ok=True)
    os.makedirs('templates/charts', exist_ok=True)

    # Create dummy chart HTML files if they don't exist
    chart_names = [
        "total_sales_revenue_by_product",
        "sales_transaction_by_channel",
        "three_year_sales_trend", # Added back for completeness if you intend to use it
        "sales_by_state_map" # Added back for completeness if you intend to use it
    ]
    for chart_name in chart_names:
        chart_file_path = os.path.join('templates/charts', f'{chart_name}.html')
        if not os.path.exists(chart_file_path):
            with open(chart_file_path, 'w') as f:
                # For map, we will directly embed the map HTML
                if chart_name == "sales_by_state_map":
                    f.write("""
                    <!DOCTYPE html>
                    <html>
                    <head>
                        <title>Sales by State Map</title>
                        <style>
                            body { margin: 0; overflow: hidden; }
                            iframe { width: 100%; height: 100%; border: none; }
                        </style>
                    </head>
                    <body>
                        <iframe src="/chart/sales_by_state_map" style="width:100%;height:100%;border:none;"></iframe>
                    </body>
                    </html>
                    """)
                else:
                    # For other charts, fetch data from the /data endpoint
                    f.write(f"""
                    <!DOCTYPE html>
                    <html>
                    <head>
                        <title>{chart_name.replace('_', ' ').title()}</title>
                        <style>
                            body {{ margin: 0; overflow: hidden; }}
                            .chart-container {{ width: 100%; height: 100%; }}
                        </style>
                    </head>
                    <body>
                        <div id="chart-container" class="chart-container"></div>
                        <script>
                            fetch('/chart/{chart_name}')
                                .then(response => response.text())
                                .then(html => {{
                                    document.getElementById('chart-container').innerHTML = html;
                                }})
                                .catch(error => console.error('Error loading chart:', error));
                        </script>
                    </body>
                    </html>
                    """)

    app.run(debug=True)
