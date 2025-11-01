# API Documentation

## Base URL
```
http://localhost:5000/api
```

## Endpoints

### Health Check
- **GET** `/api/health`
- Returns API status
- **Response**: `{"status": "ok"}`

### Data Visualization Endpoints

#### 1. Party-wise Seat Share
- **GET** `/api/party-seat-share`
- Get party-wise seat share per year
- **Query Parameters**:
  - `year` (optional): Filter by specific year
- **Response**: Array of objects with `Party`, `seats`, and optionally `Year`

#### 2. State-wise Turnout
- **GET** `/api/state-turnout`
- Get state-wise voter turnout analysis
- **Query Parameters**:
  - `year` (optional): Filter by specific year
- **Response**: Array of objects with `State_Name`, `avg_turnout`, `max_turnout`, `min_turnout`, and optionally `Year`

#### 3. Gender Representation
- **GET** `/api/gender-representation`
- Get gender representation over time
- **Response**: Array of objects with `Year`, `Sex`, `count`, `percentage`

#### 4. Top Parties by Vote Share
- **GET** `/api/top-parties-vote-share`
- Get top parties by vote share percentage
- **Query Parameters**:
  - `year` (optional): Filter by specific year
  - `limit` (optional, default: 10): Number of top parties to return
- **Response**: Array of objects with `Party`, `total_votes`, `vote_share_percentage`, `seats_won`

#### 5. Margin of Victory Distribution
- **GET** `/api/margin-distribution`
- Get margin of victory distribution for histogram
- **Query Parameters**:
  - `year` (optional): Filter by specific year
- **Response**: Array of margin percentage values

#### 6. Search
- **GET** `/api/search`
- Search by candidate or constituency
- **Query Parameters**:
  - `candidate` (optional): Search candidate name (partial match)
  - `constituency` (optional): Search constituency name (partial match)
  - `year` (optional): Filter by year
  - `state` (optional): Filter by state
  - `party` (optional): Filter by party
  - `gender` (optional): Filter by gender (M/F)
- **Response**: Array of matching election results (limited to 100)

### Filter Options Endpoints

#### 7. Get Available Years
- **GET** `/api/filters/years`
- Get list of all available election years
- **Response**: Array of year integers

#### 8. Get Available States
- **GET** `/api/filters/states`
- Get list of all available states
- **Response**: Array of state name strings

#### 9. Get Available Parties
- **GET** `/api/filters/parties`
- Get list of all available parties
- **Response**: Array of party name strings

### Analytics Endpoints

#### 10. Highest Turnout State
- **GET** `/api/analytics/highest-turnout-state`
- Get state with highest voter turnout in latest election
- **Response**: Object with `State_Name`, `avg_turnout`, `year`

#### 11. Seat Changes
- **GET** `/api/analytics/seat-change`
- Get seat changes between two consecutive elections
- **Query Parameters**:
  - `year1` (optional): First year to compare
  - `year2` (optional): Second year to compare
- **Response**: Object with `year1`, `year2`, and `changes` array (top 10)

#### 12. Women Candidates Percentage
- **GET** `/api/analytics/women-percentage`
- Get percentage of women candidates across all elections
- **Response**: Object with `total_candidates`, `women_candidates`, `women_percentage`

#### 13. Narrowest Victory Margins
- **GET** `/api/analytics/narrowest-margins`
- Get constituencies with narrowest victory margins
- **Query Parameters**:
  - `limit` (optional, default: 20): Number of results to return
  - `year` (optional): Filter by specific year
- **Response**: Array of objects with constituency details and margin information

#### 14. National vs Regional Parties
- **GET** `/api/analytics/national-vs-regional`
- Get vote share trends for national vs regional parties over time
- **Response**: Array of objects with `Year`, `Party_Type_TCPD`, `total_votes`, `vote_share_percentage`

#### 15. Education Correlation
- **GET** `/api/analytics/education-correlation`
- Get correlation between education level and winning chances
- **Response**: Object with education-based statistics or message indicating data not available

## Example Requests

```bash
# Get party seat share for 2019
curl "http://localhost:5000/api/party-seat-share?year=2019"

# Search for candidates named "Gandhi"
curl "http://localhost:5000/api/search?candidate=Gandhi"

# Get top 15 parties by vote share
curl "http://localhost:5000/api/top-parties-vote-share?limit=15"

# Get narrowest victory margins for 2019
curl "http://localhost:5000/api/analytics/narrowest-margins?year=2019&limit=10"
```

## Response Format

All endpoints return JSON responses. Error responses follow this format:
```json
{
  "error": "Error message"
}
```

