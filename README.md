# Indian Election Data Visualization Dashboard

## Overview
This project is an interactive data visualization dashboard to analyze Indian General Election data using the Trivedi Centre for Political Data (TCPD) – Lok Dhaba dataset (1991-2019). The dashboard provides insights into voting trends, party performance, and participation patterns over time.

## Project Structure
```
D2/
├── app.py                 # Flask backend API
├── requirements.txt       # Python dependencies
├── election_data2.db     # SQLite database with cleaned election data
├── templates/
│   └── index.html        # Frontend dashboard HTML
├── static/
│   ├── style.css         # Dashboard styling
│   └── dashboard.js      # Dashboard JavaScript and visualizations
├── API_DOCUMENTATION.md   # API documentation
├── SCHEMA_DOCUMENTATION.md # Database schema documentation
└── PRESENTATION.md        # Key findings presentation
```

## Installation

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Ensure the database file `election_data2.db` is in the project root directory.

## Running the Application

1. Start the Flask server:
```bash
python app.py
```

2. Open your browser and navigate to:
```
http://localhost:5000
```

## Features

### Visualizations
- **Party-wise Seat Share**: Bar chart showing seats won by each party per year
- **State-wise Turnout Analysis**: Interactive map showing voter turnout by state
- **Gender Representation Over Time**: Line chart tracking male/female candidate percentages
- **Top Parties by Vote Share**: Donut chart showing vote share percentages
- **Margin of Victory Distribution**: Histogram showing victory margins across constituencies
- **National vs Regional Parties**: Trend analysis of vote share over time

### Filters
- Year filter: Analyze data for specific election years
- State filter: Focus on specific states
- Party filter: Analyze specific parties

### Search Functionality
- Search by candidate name
- Search by constituency name
- Filter by multiple criteria simultaneously

### Analytics Dashboard
- Highest voter turnout state (latest election)
- Women candidates percentage
- Seat changes between elections
- Narrowest victory margins

## API Endpoints

See `API_DOCUMENTATION.md` for complete API documentation.

## Database Schema

See `SCHEMA_DOCUMENTATION.md` for database schema details.

## Key Findings

See `PRESENTATION.md` for key insights and findings.

## Technologies Used
- **Backend**: Flask (Python)
- **Frontend**: HTML, CSS, JavaScript
- **Visualizations**: Chart.js, Leaflet.js
- **Database**: SQLite

## Author
Engineering Talent Program Assignment

