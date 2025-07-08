from flask import Flask, render_template_string, render_template # Ensure render_template is here
import pandas as pd
import os
import plotly.graph_objects as go
import plotly.express as px
import altair as alt


app = Flask(__name__, static_folder='assets') # <--- ADD static_folder='assets'

# --- Configuration for Data File ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
EXCEL_FILE_PATH = os.path.join(BASE_DIR, 'assets', 'data', 'nestle_sales_data.xlsx')

df = None

def load_data():
    """Loads data from the Excel file into a Pandas DataFrame."""
    global df
    try:
        df = pd.read_excel(EXCEL_FILE_PATH, engine='openpyxl')
        df['Date'] = pd.to_datetime(df['Date'])
        df['Month'] = df['Date'].dt.month_name()
        df['Year'] = df['Date'].dt.year

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

with app.app_context():
    load_data()

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
                body {
                    margin: 0;
                    padding: 0;
                    overflow: hidden;
                    background-color: #f9f9f9; /* Match grid-item bg */
                    height: 100vh; /* Ensure body takes full iframe height */
                    width: 100vw;  /* Ensure body takes full iframe width */
                    display: flex; /* Use flexbox to center chart if needed */
                    justify-content: center;
                    align-items: center;
                }
                .plotly-container {
                    width: 100%;
                    height: 100%;
                    /* Ensure this container also takes full available space */
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
    value_text = base.mark_text(align='center', baseline='bottom').encode(
        text=alt.Text('Total Revenue', format='.2s'),  # Format the text as well
        order='Year:O',
        color=alt.value('black')  # Set text color to black for visibility
    )

    # Layer the bar chart and value labels
    # Removed .interactive() method
    layered_chart = alt.layer(bars, value_text).properties(
        width=alt.Step(14), # Use alt.Step for width in faceted charts to control individual facet width
        height='container'  # Use 'container' to make it responsive
    )

    # Facet the layered chart by Product Name
    final_chart = layered_chart.facet(
        column=alt.Column('Product Name:N', header=alt.Header(titleOrient="bottom", labelOrient="bottom"))
    ).properties(
        # Title of the chart
        title='Three Year Sales Trend for Each Product',
    )

    # Convert the Altair chart to HTML.
    # Set 'actions': False to hide the default menu for save/zoom.
    chart_html = final_chart.to_html(embed_options={'actions': False}) # <--- Changed to False

    return render_chart_template(chart_html, "Three Year Sales Trend for Each Product")

if __name__ == '__main__':
    app.run(debug=True, port=5000)