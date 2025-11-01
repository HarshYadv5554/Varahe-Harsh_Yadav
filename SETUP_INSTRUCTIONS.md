# Setup Instructions

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

Or use the provided batch file (Windows):
```bash
run.bat
```

### 2. Verify Database
Ensure `election_data2.db` is in the project root directory.

### 3. Run the Application
```bash
python app.py
```

### 4. Access the Dashboard
Open your web browser and navigate to:
```
http://localhost:5000
```

## Project Structure

```
D2/
├── app.py                      # Flask backend server
├── requirements.txt            # Python dependencies
├── election_data2.db          # SQLite database
├── templates/
│   └── index.html            # Dashboard HTML
├── static/
│   ├── style.css             # Stylesheet
│   └── dashboard.js          # JavaScript logic
├── API_DOCUMENTATION.md       # API endpoint documentation
├── SCHEMA_DOCUMENTATION.md    # Database schema details
├── PRESENTATION.md            # Key findings presentation
└── README.md                  # Project overview
```

## Features Checklist

### ✅ Data Preparation
- [x] Data imported and cleaned in SQLite database
- [x] Database schema documented
- [x] Data models/tables created

### ✅ Backend Development
- [x] Flask API with all required filters
  - [x] Year filter
  - [x] State filter
  - [x] Party filter
  - [x] Gender filter
  - [x] Constituency filter

### ✅ Frontend Dashboard
- [x] Party-wise Seat Share (Bar Chart)
- [x] State-wise Turnout Analysis (Map/Choropleth)
- [x] Gender Representation Over Time (Line Chart)
- [x] Top Parties by Vote Share (Donut Chart)
- [x] Margin of Victory Distribution (Histogram)
- [x] Search by Candidate/Constituency (Table)

### ✅ Analytical Scenarios
- [x] Highest voter turnout state (latest election)
- [x] Party seat gains/losses between elections
- [x] Women candidates percentage
- [x] Narrowest victory margins
- [x] National vs Regional parties vote share trends
- [x] Education correlation (if data available)

### ✅ Deliverables
- [x] Cleaned dataset and schema documentation
- [x] Working dashboard (runs locally)
- [x] API documentation
- [x] Presentation with key findings

## Troubleshooting

### Issue: Port 5000 already in use
**Solution**: Modify `app.py` to use a different port:
```python
app.run(debug=True, port=5001)
```

### Issue: Database not found
**Solution**: Ensure `election_data2.db` is in the same directory as `app.py`

### Issue: Charts not loading
**Solution**: 
1. Check browser console for errors
2. Verify API endpoints are accessible: `http://localhost:5000/api/health`
3. Ensure database connection is working

### Issue: Map not displaying
**Solution**: 
1. Check internet connection (map tiles loaded from OpenStreetMap)
2. Verify Leaflet.js library is loading correctly

## Testing the Dashboard

### Test API Endpoints
```bash
# Health check
curl http://localhost:5000/api/health

# Get party seat share for 2019
curl http://localhost:5000/api/party-seat-share?year=2019

# Search for candidates
curl "http://localhost:5000/api/search?candidate=Gandhi"

# Get analytics
curl http://localhost:5000/api/analytics/highest-turnout-state
```

## Next Steps

1. **Enhance Map Visualization**: Add proper GeoJSON boundaries for Indian states for a true choropleth map
2. **Add More Filters**: Implement additional filtering combinations
3. **Export Functionality**: Add ability to export charts/data as images/CSV
4. **Performance Optimization**: Add caching for frequently accessed queries
5. **Deploy to Cloud**: Deploy to free services like Heroku, Render, or Railway

## Support

For issues or questions, refer to:
- `API_DOCUMENTATION.md` for API usage
- `SCHEMA_DOCUMENTATION.md` for database structure
- `PRESENTATION.md` for insights and findings

