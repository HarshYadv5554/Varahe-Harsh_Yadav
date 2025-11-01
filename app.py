from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import sqlite3
import json

app = Flask(__name__, template_folder='templates', static_folder='static')
CORS(app)

DB_PATH = 'election_data2.db'

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'})

@app.route('/api/party-seat-share', methods=['GET'])
def party_seat_share():
    """Get party-wise seat share per year (1991-2019 per requirements)"""
    year = request.args.get('year', type=int)
    
    conn = get_db_connection()
    
    if year:
        query = """
        SELECT Party, COUNT(*) as seats
        FROM election_results
        WHERE Year = ? AND Year >= 1991 AND Year <= 2019 AND Position = 1
        GROUP BY Party
        ORDER BY seats DESC
        """
        cursor = conn.execute(query, (year,))
    else:
        query = """
        SELECT Year, Party, COUNT(*) as seats
        FROM election_results
        WHERE Year >= 1991 AND Year <= 2019 AND Position = 1
        GROUP BY Year, Party
        ORDER BY Year, seats DESC
        """
        cursor = conn.execute(query)
    
    results = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return jsonify(results)

@app.route('/api/state-turnout', methods=['GET'])
def state_turnout():
    """Get state-wise turnout analysis (1991-2019 per requirements)"""
    year = request.args.get('year', type=int)
    
    conn = get_db_connection()
    
    if year:
        query = """
        SELECT 
            State_Name,
            AVG(Turnout_Percentage) as avg_turnout,
            MAX(Turnout_Percentage) as max_turnout,
            MIN(Turnout_Percentage) as min_turnout
        FROM election_results
        WHERE Year = ? AND Year >= 1991 AND Year <= 2019
        GROUP BY State_Name
        ORDER BY avg_turnout DESC
        """
        cursor = conn.execute(query, (year,))
    else:
        query = """
        SELECT 
            Year,
            State_Name,
            AVG(Turnout_Percentage) as avg_turnout,
            MAX(Turnout_Percentage) as max_turnout,
            MIN(Turnout_Percentage) as min_turnout
        FROM election_results
        WHERE Year >= 1991 AND Year <= 2019
        GROUP BY Year, State_Name
        ORDER BY Year, avg_turnout DESC
        """
        cursor = conn.execute(query)
    
    results = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return jsonify(results)

@app.route('/api/gender-representation', methods=['GET'])
def gender_representation():
    """Get gender representation over time (1991-2019 per requirements)"""
    conn = get_db_connection()
    
    query = """
    SELECT 
        Year,
        Sex,
        COUNT(*) as count,
        COUNT(*) * 100.0 / (SELECT COUNT(*) FROM election_results e2 WHERE e2.Year = election_results.Year AND e2.Year >= 1991 AND e2.Year <= 2019) as percentage
    FROM election_results
    WHERE Year >= 1991 AND Year <= 2019 AND Sex IN ('M', 'F')
    GROUP BY Year, Sex
    ORDER BY Year, Sex
    """
    
    cursor = conn.execute(query)
    results = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return jsonify(results)

@app.route('/api/top-parties-vote-share', methods=['GET'])
def top_parties_vote_share():
    """Get top parties by vote share percentage (1991-2019 per requirements)"""
    year = request.args.get('year', type=int)
    limit = request.args.get('limit', default=10, type=int)
    
    conn = get_db_connection()
    
    if year:
        query = """
        SELECT 
            Party,
            SUM(Votes) as total_votes,
            SUM(Votes) * 100.0 / (SELECT SUM(Votes) FROM election_results WHERE Year = ? AND Year >= 1991 AND Year <= 2019) as vote_share_percentage,
            COUNT(CASE WHEN Position = 1 THEN 1 END) as seats_won
        FROM election_results
        WHERE Year = ? AND Year >= 1991 AND Year <= 2019
        GROUP BY Party
        ORDER BY vote_share_percentage DESC
        LIMIT ?
        """
        cursor = conn.execute(query, (year, year, limit))
    else:
        query = """
        SELECT 
            Party,
            SUM(Votes) as total_votes,
            SUM(Votes) * 100.0 / (SELECT SUM(Votes) FROM election_results WHERE Year >= 1991 AND Year <= 2019) as vote_share_percentage,
            COUNT(CASE WHEN Position = 1 THEN 1 END) as seats_won
        FROM election_results
        WHERE Year >= 1991 AND Year <= 2019
        GROUP BY Party
        ORDER BY vote_share_percentage DESC
        LIMIT ?
        """
        cursor = conn.execute(query, (limit,))
    
    results = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return jsonify(results)

@app.route('/api/margin-distribution', methods=['GET'])
def margin_distribution():
    """Get margin of victory distribution (1991-2019 per requirements)"""
    year = request.args.get('year', type=int)
    
    conn = get_db_connection()
    
    if year:
        query = """
        SELECT Margin_Percentage
        FROM election_results
        WHERE Year = ? AND Year >= 1991 AND Year <= 2019 AND Position = 1 AND Margin_Percentage IS NOT NULL
        ORDER BY Margin_Percentage
        """
        cursor = conn.execute(query, (year,))
    else:
        query = """
        SELECT Margin_Percentage
        FROM election_results
        WHERE Year >= 1991 AND Year <= 2019 AND Position = 1 AND Margin_Percentage IS NOT NULL
        ORDER BY Margin_Percentage
        """
        cursor = conn.execute(query)
    
    results = [row['Margin_Percentage'] for row in cursor.fetchall()]
    conn.close()
    return jsonify(results)

@app.route('/api/search', methods=['GET'])
def search():
    """Search by candidate or constituency (1991-2019 per requirements)"""
    candidate = request.args.get('candidate', '')
    constituency = request.args.get('constituency', '')
    year = request.args.get('year', type=int)
    state = request.args.get('state', '')
    party = request.args.get('party', '')
    gender = request.args.get('gender', '')
    
    conn = get_db_connection()
    
    query = "SELECT * FROM election_results WHERE Year >= 1991 AND Year <= 2019"
    params = []
    
    if candidate:
        query += " AND Candidate LIKE ?"
        params.append(f'%{candidate}%')
    
    if constituency:
        query += " AND Constituency_Name LIKE ?"
        params.append(f'%{constituency}%')
    
    if year:
        query += " AND Year = ?"
        params.append(year)
    
    if state:
        query += " AND State_Name = ?"
        params.append(state)
    
    if party:
        query += " AND Party = ?"
        params.append(party)
    
    if gender:
        query += " AND Sex = ?"
        params.append(gender)
    
    query += " ORDER BY Year DESC, Position LIMIT 100"
    
    cursor = conn.execute(query, params)
    results = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return jsonify(results)

@app.route('/api/filters/years', methods=['GET'])
def get_years():
    """Get list of available years (1991-2019 per requirements)"""
    conn = get_db_connection()
    cursor = conn.execute("SELECT DISTINCT Year FROM election_results WHERE Year >= 1991 AND Year <= 2019 ORDER BY Year")
    years = [row['Year'] for row in cursor.fetchall()]
    conn.close()
    return jsonify(years)

@app.route('/api/filters/states', methods=['GET'])
def get_states():
    """Get list of available states (1991-2019 per requirements)"""
    conn = get_db_connection()
    cursor = conn.execute("SELECT DISTINCT State_Name FROM election_results WHERE Year >= 1991 AND Year <= 2019 ORDER BY State_Name")
    states = [row['State_Name'] for row in cursor.fetchall()]
    conn.close()
    return jsonify(states)

@app.route('/api/filters/parties', methods=['GET'])
def get_parties():
    """Get list of available parties (1991-2019 per requirements)"""
    conn = get_db_connection()
    cursor = conn.execute("SELECT DISTINCT Party FROM election_results WHERE Year >= 1991 AND Year <= 2019 AND Party IS NOT NULL ORDER BY Party")
    parties = [row['Party'] for row in cursor.fetchall()]
    conn.close()
    return jsonify(parties)

@app.route('/api/analytics/highest-turnout-state', methods=['GET'])
def highest_turnout_state():
    """Which state had the highest voter turnout in the latest general election (1991-2019)?"""
    conn = get_db_connection()
    
    # Get latest year within 1991-2019 range
    cursor = conn.execute("SELECT MAX(Year) as latest_year FROM election_results WHERE Year >= 1991 AND Year <= 2019")
    latest_year = cursor.fetchone()['latest_year']
    
    query = """
    SELECT 
        State_Name,
        AVG(Turnout_Percentage) as avg_turnout
    FROM election_results
    WHERE Year = ? AND Year >= 1991 AND Year <= 2019
    GROUP BY State_Name
    ORDER BY avg_turnout DESC
    LIMIT 1
    """
    cursor = conn.execute(query, (latest_year,))
    result = dict(cursor.fetchone())
    result['year'] = latest_year
    conn.close()
    return jsonify(result)

@app.route('/api/analytics/seat-change', methods=['GET'])
def seat_change():
    """Which party gained or lost the most seats between two consecutive elections (1991-2019)?"""
    year1 = request.args.get('year1', type=int)
    year2 = request.args.get('year2', type=int)
    
    conn = get_db_connection()
    
    if not year1 or not year2:
        # Get last two years within 1991-2019 range
        cursor = conn.execute("SELECT DISTINCT Year FROM election_results WHERE Year >= 1991 AND Year <= 2019 ORDER BY Year DESC LIMIT 2")
        years = [row['Year'] for row in cursor.fetchall()]
        if len(years) >= 2:
            year2, year1 = years[0], years[1]
        else:
            return jsonify({'error': 'Need at least 2 years of data'})
    
    query1 = """
    SELECT Party, COUNT(*) as seats
    FROM election_results
    WHERE Year = ? AND Year >= 1991 AND Year <= 2019 AND Position = 1
    GROUP BY Party
    """
    
    seats_year1 = {row['Party']: row['seats'] for row in conn.execute(query1, (year1,)).fetchall()}
    seats_year2 = {row['Party']: row['seats'] for row in conn.execute(query1, (year2,)).fetchall()}
    
    changes = []
    all_parties = set(list(seats_year1.keys()) + list(seats_year2.keys()))
    
    for party in all_parties:
        seats1 = seats_year1.get(party, 0)
        seats2 = seats_year2.get(party, 0)
        change = seats2 - seats1
        changes.append({
            'party': party,
            'year1_seats': seats1,
            'year2_seats': seats2,
            'change': change
        })
    
    changes.sort(key=lambda x: abs(x['change']), reverse=True)
    conn.close()
    
    return jsonify({
        'year1': year1,
        'year2': year2,
        'changes': changes[:10]  # Top 10
    })

@app.route('/api/analytics/women-percentage', methods=['GET'])
def women_percentage():
    """What is the percentage of women candidates across all elections (1991-2019)?"""
    conn = get_db_connection()
    
    query = """
    SELECT 
        COUNT(*) as total_candidates,
        SUM(CASE WHEN Sex = 'F' THEN 1 ELSE 0 END) as women_candidates,
        SUM(CASE WHEN Sex = 'F' THEN 1 ELSE 0 END) * 100.0 / COUNT(*) as women_percentage
    FROM election_results
    WHERE Year >= 1991 AND Year <= 2019
    """
    
    cursor = conn.execute(query)
    result = dict(cursor.fetchone())
    conn.close()
    return jsonify(result)

@app.route('/api/analytics/narrowest-margins', methods=['GET'])
def narrowest_margins():
    """Which constituencies had the narrowest victory margins (1991-2019)?"""
    limit = request.args.get('limit', default=20, type=int)
    year = request.args.get('year', type=int)
    
    conn = get_db_connection()
    
    if year:
        query = """
        SELECT 
            Year,
            State_Name,
            Constituency_Name,
            Candidate,
            Party,
            Margin_Percentage,
            Margin
        FROM election_results
        WHERE Year = ? AND Year >= 1991 AND Year <= 2019 AND Position = 1 AND Margin_Percentage IS NOT NULL
        ORDER BY Margin_Percentage ASC
        LIMIT ?
        """
        cursor = conn.execute(query, (year, limit))
    else:
        query = """
        SELECT 
            Year,
            State_Name,
            Constituency_Name,
            Candidate,
            Party,
            Margin_Percentage,
            Margin
        FROM election_results
        WHERE Year >= 1991 AND Year <= 2019 AND Position = 1 AND Margin_Percentage IS NOT NULL
        ORDER BY Margin_Percentage ASC
        LIMIT ?
        """
        cursor = conn.execute(query, (limit,))
    
    results = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return jsonify(results)

@app.route('/api/analytics/national-vs-regional', methods=['GET'])
def national_vs_regional():
    """How has the vote share of national vs regional parties changed over time (1991-2019)?"""
    conn = get_db_connection()
    
    query = """
    SELECT 
        Year,
        Party_Type_TCPD,
        SUM(Votes) as total_votes,
        SUM(Votes) * 100.0 / (SELECT SUM(Votes) FROM election_results e2 WHERE e2.Year = election_results.Year AND e2.Year >= 1991 AND e2.Year <= 2019) as vote_share_percentage
    FROM election_results
    WHERE Year >= 1991 AND Year <= 2019 AND Party_Type_TCPD IN ('National Party', 'Regional Party')
    GROUP BY Year, Party_Type_TCPD
    ORDER BY Year, Party_Type_TCPD
    """
    
    cursor = conn.execute(query)
    results = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return jsonify(results)

@app.route('/api/analytics/education-correlation', methods=['GET'])
def education_correlation():
    """What correlation exists between education level and winning chances (1991-2019)?"""
    # Note: This dataset may not have education data, so we'll check if it exists
    conn = get_db_connection()
    
    # Check if education column exists
    cursor = conn.execute("PRAGMA table_info(election_results)")
    columns = [row[1] for row in cursor.fetchall()]
    
    if 'Education' in columns or 'education' in columns:
        query = """
        SELECT 
            Education,
            COUNT(*) as total_candidates,
            SUM(CASE WHEN Position = 1 THEN 1 ELSE 0 END) as winners,
            SUM(CASE WHEN Position = 1 THEN 1 ELSE 0 END) * 100.0 / COUNT(*) as win_percentage
        FROM election_results
        WHERE Year >= 1991 AND Year <= 2019 AND Education IS NOT NULL
        GROUP BY Education
        ORDER BY win_percentage DESC
        """
        cursor = conn.execute(query)
        results = [dict(row) for row in cursor.fetchall()]
    else:
        # Return a message indicating education data is not available
        results = {'message': 'Education data not available in dataset'}
    
    conn.close()
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True, port=5000)

