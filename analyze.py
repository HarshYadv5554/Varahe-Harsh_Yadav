"""
Analytical Scenarios - Answer Questions from the Dashboard
This script queries the database to answer all analytical questions.
"""

import sqlite3
import json
from datetime import datetime

DB_PATH = 'election_data2.db'

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def question_a():
    """a. Which state had the highest voter turnout in the latest general election?"""
    print("\n" + "="*80)
    print("a. Which state had the highest voter turnout in the latest general election?")
    print("="*80)
    
    conn = get_db_connection()
    
    # Get latest year within 1991-2019 range
    cursor = conn.execute("SELECT MAX(Year) as latest_year FROM election_results WHERE Year >= 1991 AND Year <= 2019")
    latest_year = cursor.fetchone()['latest_year']
    print(f"\nLatest election year (1991-2019): {latest_year}")
    
    query = """
    SELECT 
        State_Name,
        AVG(Turnout_Percentage) as avg_turnout,
        MAX(Turnout_Percentage) as max_turnout,
        MIN(Turnout_Percentage) as min_turnout,
        COUNT(DISTINCT Constituency_Name) as constituencies
    FROM election_results
    WHERE Year = ? AND Year >= 1991 AND Year <= 2019
    GROUP BY State_Name
    ORDER BY avg_turnout DESC
    LIMIT 5
    """
    
    cursor = conn.execute(query, (latest_year,))
    results = [dict(row) for row in cursor.fetchall()]
    
    print("\nTop 5 States by Average Voter Turnout:")
    print("-" * 80)
    for i, state in enumerate(results, 1):
        print(f"{i}. {state['State_Name'].replace('_', ' '):<30} "
              f"Average Turnout: {state['avg_turnout']:.2f}% "
              f"(Max: {state['max_turnout']:.2f}%, Min: {state['min_turnout']:.2f}%) "
              f"[{state['constituencies']} constituencies]")
    
    answer = results[0]
    print(f"\n✓ ANSWER: {answer['State_Name'].replace('_', ' ')} had the highest voter turnout "
          f"({answer['avg_turnout']:.2f}%) in {latest_year}")
    
    conn.close()
    return answer

def question_b():
    """b. Which party gained or lost the most seats between two consecutive elections?"""
    print("\n" + "="*80)
    print("b. Which party gained or lost the most seats between two consecutive elections?")
    print("="*80)
    
    conn = get_db_connection()
    
    # Get last two years within 1991-2019 range
    cursor = conn.execute("""
        SELECT DISTINCT Year 
        FROM election_results 
        WHERE Year >= 1991 AND Year <= 2019 
        ORDER BY Year DESC 
        LIMIT 2
    """)
    years = [row['Year'] for row in cursor.fetchall()]
    
    if len(years) < 2:
        print("Error: Need at least 2 years of data")
        return None
    
    year2, year1 = years[0], years[1]
    print(f"\nComparing elections: {year1} → {year2}")
    
    query = """
    SELECT Party, COUNT(*) as seats
    FROM election_results
    WHERE Year = ? AND Year >= 1991 AND Year <= 2019 AND Position = 1
    GROUP BY Party
    """
    
    seats_year1 = {row['Party']: row['seats'] for row in conn.execute(query, (year1,)).fetchall()}
    seats_year2 = {row['Party']: row['seats'] for row in conn.execute(query, (year2,)).fetchall()}
    
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
    
    print("\nTop 10 Party Seat Changes:")
    print("-" * 80)
    print(f"{'Party':<25} {'Seats ' + str(year1):<15} {'Seats ' + str(year2):<15} {'Change':<10}")
    print("-" * 80)
    
    for change in changes[:10]:
        change_sign = "+" if change['change'] > 0 else ""
        print(f"{change['party']:<25} {change['year1_seats']:<15} {change['year2_seats']:<15} {change_sign}{change['change']:<10}")
    
    # Biggest gain
    biggest_gain = max(changes, key=lambda x: x['change'])
    # Biggest loss
    biggest_loss = min(changes, key=lambda x: x['change'])
    
    print(f"\n✓ ANSWER: ")
    print(f"  • Biggest Gain: {biggest_gain['party']} gained {biggest_gain['change']} seats "
          f"({biggest_gain['year1_seats']} → {biggest_gain['year2_seats']} seats)")
    print(f"  • Biggest Loss: {biggest_loss['party']} lost {abs(biggest_loss['change'])} seats "
          f"({biggest_loss['year1_seats']} → {biggest_loss['year2_seats']} seats)")
    print(f"  • Largest Absolute Change: {changes[0]['party']} "
          f"({'+' if changes[0]['change'] > 0 else ''}{changes[0]['change']} seats)")
    
    conn.close()
    return {
        'year1': year1,
        'year2': year2,
        'biggest_gain': biggest_gain,
        'biggest_loss': biggest_loss,
        'largest_change': changes[0]
    }

def question_c():
    """c. What is the percentage of women candidates across all elections?"""
    print("\n" + "="*80)
    print("c. What is the percentage of women candidates across all elections?")
    print("="*80)
    
    conn = get_db_connection()
    
    query = """
    SELECT 
        COUNT(*) as total_candidates,
        SUM(CASE WHEN Sex = 'F' THEN 1 ELSE 0 END) as women_candidates,
        SUM(CASE WHEN Sex = 'M' THEN 1 ELSE 0 END) as men_candidates,
        SUM(CASE WHEN Sex = 'F' THEN 1 ELSE 0 END) * 100.0 / COUNT(*) as women_percentage,
        SUM(CASE WHEN Sex = 'M' THEN 1 ELSE 0 END) * 100.0 / COUNT(*) as men_percentage
    FROM election_results
    WHERE Year >= 1991 AND Year <= 2019
    """
    
    cursor = conn.execute(query)
    result = dict(cursor.fetchone())
    
    # Year-wise breakdown
    query_yearly = """
    SELECT 
        Year,
        COUNT(*) as total_candidates,
        SUM(CASE WHEN Sex = 'F' THEN 1 ELSE 0 END) as women_candidates,
        SUM(CASE WHEN Sex = 'F' THEN 1 ELSE 0 END) * 100.0 / COUNT(*) as women_percentage
    FROM election_results
    WHERE Year >= 1991 AND Year <= 2019
    GROUP BY Year
    ORDER BY Year
    """
    
    cursor = conn.execute(query_yearly)
    yearly_results = [dict(row) for row in cursor.fetchall()]
    
    print("\nOverall Statistics (1991-2019):")
    print("-" * 80)
    print(f"Total Candidates: {result['total_candidates']:,}")
    print(f"Women Candidates: {result['women_candidates']:,} ({result['women_percentage']:.2f}%)")
    print(f"Men Candidates:   {result['men_candidates']:,} ({result['men_percentage']:.2f}%)")
    
    print("\nYear-wise Breakdown:")
    print("-" * 80)
    print(f"{'Year':<8} {'Total':<12} {'Women':<12} {'Women %':<12} {'Trend':<10}")
    print("-" * 80)
    
    prev_percentage = None
    for year_data in yearly_results:
        trend = ""
        if prev_percentage is not None:
            if year_data['women_percentage'] > prev_percentage:
                trend = "↑"
            elif year_data['women_percentage'] < prev_percentage:
                trend = "↓"
            else:
                trend = "→"
        print(f"{year_data['Year']:<8} {year_data['total_candidates']:<12} "
              f"{year_data['women_candidates']:<12} {year_data['women_percentage']:.2f}%{'':<7} {trend}")
        prev_percentage = year_data['women_percentage']
    
    print(f"\n✓ ANSWER: Across all elections (1991-2019), women candidates represent "
          f"{result['women_percentage']:.2f}% of total candidates "
          f"({result['women_candidates']:,} out of {result['total_candidates']:,} candidates)")
    
    conn.close()
    return result

def question_d():
    """d. Which constituencies had the narrowest victory margins?"""
    print("\n" + "="*80)
    print("d. Which constituencies had the narrowest victory margins?")
    print("="*80)
    
    conn = get_db_connection()
    
    query = """
    SELECT 
        Year,
        State_Name,
        Constituency_Name,
        Candidate,
        Party,
        Margin_Percentage,
        Margin,
        Votes,
        Valid_Votes
    FROM election_results
    WHERE Year >= 1991 AND Year <= 2019 AND Position = 1 AND Margin_Percentage IS NOT NULL
    ORDER BY Margin_Percentage ASC
    LIMIT 20
    """
    
    cursor = conn.execute(query)
    results = [dict(row) for row in cursor.fetchall()]
    
    print("\nTop 20 Constituencies with Narrowest Victory Margins:")
    print("-" * 80)
    print(f"{'Rank':<6} {'Year':<6} {'State':<20} {'Constituency':<30} {'Margin %':<12} {'Margin Votes':<12}")
    print("-" * 80)
    
    for i, result in enumerate(results, 1):
        state_short = result['State_Name'].replace('_', ' ')[:18]
        constituency_short = result['Constituency_Name'][:28]
        print(f"{i:<6} {result['Year']:<6} {state_short:<20} {constituency_short:<30} "
              f"{result['Margin_Percentage']:.4f}%{'':<6} {int(result['Margin']) if result['Margin'] else 'N/A':<12}")
    
    # Detailed info for top 5
    print("\nDetailed Information (Top 5):")
    print("-" * 80)
    for i, result in enumerate(results[:5], 1):
        print(f"\n{i}. {result['Constituency_Name']} ({result['Year']})")
        print(f"   State: {result['State_Name'].replace('_', ' ')}")
        print(f"   Winner: {result['Candidate']} ({result['Party']})")
        print(f"   Margin: {result['Margin_Percentage']:.4f}% ({int(result['Margin']) if result['Margin'] else 'N/A'} votes)")
        print(f"   Winner Votes: {int(result['Votes']) if result['Votes'] else 'N/A'}")
        print(f"   Total Valid Votes: {result['Valid_Votes']:,}")
    
    narrowest = results[0]
    print(f"\n✓ ANSWER: The constituency with the narrowest victory margin is "
          f"{narrowest['Constituency_Name']} ({narrowest['Year']}) in "
          f"{narrowest['State_Name'].replace('_', ' ')} with a margin of "
          f"{narrowest['Margin_Percentage']:.4f}% ({int(narrowest['Margin']) if narrowest['Margin'] else 'N/A'} votes)")
    
    conn.close()
    return results[:10]

def question_e():
    """e. How has the vote share of national vs regional parties changed over time?"""
    print("\n" + "="*80)
    print("e. How has the vote share of national vs regional parties changed over time?")
    print("="*80)
    
    conn = get_db_connection()
    
    query = """
    SELECT 
        Year,
        Party_Type_TCPD,
        SUM(Votes) as total_votes,
        SUM(Votes) * 100.0 / (SELECT SUM(Votes) FROM election_results e2 WHERE e2.Year = election_results.Year AND e2.Year >= 1991 AND e2.Year <= 2019) as vote_share_percentage,
        COUNT(CASE WHEN Position = 1 THEN 1 END) as seats_won
    FROM election_results
    WHERE Year >= 1991 AND Year <= 2019 AND Party_Type_TCPD IN ('National Party', 'Regional Party')
    GROUP BY Year, Party_Type_TCPD
    ORDER BY Year, Party_Type_TCPD
    """
    
    cursor = conn.execute(query)
    results = [dict(row) for row in cursor.fetchall()]
    
    # Organize by year
    yearly_data = {}
    for row in results:
        year = row['Year']
        if year not in yearly_data:
            yearly_data[year] = {}
        yearly_data[year][row['Party_Type_TCPD']] = row
    
    print("\nVote Share Trends (1991-2019):")
    print("-" * 80)
    print(f"{'Year':<8} {'National Parties':<25} {'Regional Parties':<25} {'Difference':<15}")
    print(f"{'':<8} {'% Vote':<12} {'Seats':<12} {'% Vote':<12} {'Seats':<12} {'(Nat-Reg)':<15}")
    print("-" * 80)
    
    first_year = None
    last_year = None
    
    for year in sorted(yearly_data.keys()):
        national = yearly_data[year].get('National Party', {})
        regional = yearly_data[year].get('Regional Party', {})
        
        nat_vote = national.get('vote_share_percentage', 0) or 0
        reg_vote = regional.get('vote_share_percentage', 0) or 0
        nat_seats = national.get('seats_won', 0) or 0
        reg_seats = regional.get('seats_won', 0) or 0
        
        if first_year is None:
            first_year = {
                'year': year,
                'national': nat_vote,
                'regional': reg_vote
            }
        
        last_year = {
            'year': year,
            'national': nat_vote,
            'regional': reg_vote
        }
        
        print(f"{year:<8} {nat_vote:>10.2f}% {nat_seats:>10} {reg_vote:>10.2f}% {reg_seats:>10} "
              f"{nat_vote - reg_vote:>12.2f}%")
    
    # Calculate trend
    nat_change = last_year['national'] - first_year['national']
    reg_change = last_year['regional'] - first_year['regional']
    
    print("\nTrend Analysis:")
    print("-" * 80)
    print(f"Period: {first_year['year']} → {last_year['year']}")
    print(f"National Parties: {first_year['national']:.2f}% → {last_year['national']:.2f}% "
          f"({'+' if nat_change > 0 else ''}{nat_change:.2f}% change)")
    print(f"Regional Parties: {first_year['regional']:.2f}% → {last_year['regional']:.2f}% "
          f"({'+' if reg_change > 0 else ''}{reg_change:.2f}% change)")
    
    print(f"\n✓ ANSWER: ")
    print(f"  • National parties vote share changed from {first_year['national']:.2f}% "
          f"({first_year['year']}) to {last_year['national']:.2f}% ({last_year['year']}), "
          f"a change of {'+' if nat_change > 0 else ''}{nat_change:.2f} percentage points")
    print(f"  • Regional parties vote share changed from {first_year['regional']:.2f}% "
          f"({first_year['year']}) to {last_year['regional']:.2f}% ({last_year['year']}), "
          f"a change of {'+' if reg_change > 0 else ''}{reg_change:.2f} percentage points")
    
    if abs(nat_change) > abs(reg_change):
        dominant = "National" if nat_change > 0 else "Regional"
        print(f"  • The trend shows a stronger change in National parties' vote share")
    
    conn.close()
    return {
        'first_year': first_year,
        'last_year': last_year,
        'national_change': nat_change,
        'regional_change': reg_change
    }

def question_f():
    """f. What correlation exists between education level and the winning chances of candidates?"""
    print("\n" + "="*80)
    print("f. What correlation exists between education level and the winning chances of candidates?")
    print("="*80)
    
    conn = get_db_connection()
    
    # Check if education column exists
    cursor = conn.execute("PRAGMA table_info(election_results)")
    columns = [row[1] for row in cursor.fetchall()]
    
    education_columns = [col for col in columns if 'education' in col.lower() or 'edu' in col.lower()]
    
    if not education_columns:
        print("\n❌ Education data is NOT available in the dataset.")
        print("   The dataset does not contain education level information for candidates.")
        print("\n✓ ANSWER: Cannot determine correlation as education data is not available in the dataset.")
        conn.close()
        return {'available': False}
    
    # If education data exists
    education_col = education_columns[0]
    
    query = """
    SELECT 
        """ + education_col + """ as Education,
        COUNT(*) as total_candidates,
        SUM(CASE WHEN Position = 1 THEN 1 ELSE 0 END) as winners,
        SUM(CASE WHEN Position = 1 THEN 1 ELSE 0 END) * 100.0 / COUNT(*) as win_percentage,
        AVG(Vote_Share_Percentage) as avg_vote_share
    FROM election_results
    WHERE Year >= 1991 AND Year <= 2019 AND """ + education_col + """ IS NOT NULL
    GROUP BY """ + education_col + """
    ORDER BY win_percentage DESC
    """
    
    cursor = conn.execute(query)
    results = [dict(row) for row in cursor.fetchall()]
    
    print(f"\nWin Rate by Education Level ({education_col}):")
    print("-" * 80)
    print(f"{'Education Level':<30} {'Total':<12} {'Winners':<12} {'Win Rate %':<15} {'Avg Vote Share %':<15}")
    print("-" * 80)
    
    for result in results:
        print(f"{str(result['Education']):<30} {result['total_candidates']:<12} "
              f"{result['winners']:<12} {result['win_percentage']:>12.2f}% "
              f"{result['avg_vote_share']:>14.2f}%")
    
    # Calculate correlation
    highest_win = max(results, key=lambda x: x['win_percentage'])
    lowest_win = min(results, key=lambda x: x['win_percentage'])
    
    print("\nAnalysis:")
    print("-" * 80)
    print(f"Highest Win Rate: {highest_win['Education']} ({highest_win['win_percentage']:.2f}%)")
    print(f"Lowest Win Rate:  {lowest_win['Education']} ({lowest_win['win_percentage']:.2f}%)")
    
    # Calculate overall correlation
    total_winners = sum(r['winners'] for r in results)
    total_candidates = sum(r['total_candidates'] for r in results)
    overall_win_rate = (total_winners / total_candidates) * 100
    
    print(f"\nOverall Win Rate (across all education levels): {overall_win_rate:.2f}%")
    
    print(f"\n✓ ANSWER: ")
    print(f"  • Education level data is available: {education_col}")
    print(f"  • Highest win rate: {highest_win['Education']} ({highest_win['win_percentage']:.2f}%)")
    print(f"  • Lowest win rate: {lowest_win['Education']} ({lowest_win['win_percentage']:.2f}%)")
    print(f"  • Correlation: {'Positive' if highest_win['win_percentage'] > overall_win_rate else 'Negative'} correlation "
          f"between education level and winning chances (range: {lowest_win['win_percentage']:.2f}% - {highest_win['win_percentage']:.2f}%)")
    
    conn.close()
    return {
        'available': True,
        'education_column': education_col,
        'results': results,
        'highest': highest_win,
        'lowest': lowest_win
    }

def main():
    print("\n" + "="*80)
    print("ANALYTICAL SCENARIOS - DASHBOARD QUESTIONS")
    print("Indian General Election Data Analysis (1991-2019)")
    print("="*80)
    
    try:
        a_result = question_a()
        b_result = question_b()
        c_result = question_c()
        d_result = question_d()
        e_result = question_e()
        f_result = question_f()
        
        print("\n" + "="*80)
        print("ANALYSIS COMPLETE")
        print("="*80)
        print("\nAll questions have been answered using the dashboard data.")
        print("You can also view these answers in the dashboard's Analytics section.")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()

