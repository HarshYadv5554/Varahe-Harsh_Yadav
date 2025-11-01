# Database Schema Documentation

## Database: election_data2.db

### Table: election_results

The main table containing Indian General Election data from 1991 to 2019.

#### Columns

| Column Name | Data Type | Description |
|-------------|-----------|-------------|
| State_Name | TEXT | Name of the state |
| Assembly_No | INTEGER | Assembly number |
| Constituency_No | INTEGER | Constituency number |
| Year | INTEGER | Election year |
| month | REAL | Election month |
| Poll_No | INTEGER | Poll number |
| DelimID | INTEGER | Delimitation ID |
| Position | INTEGER | Candidate position (1 = winner) |
| Candidate | TEXT | Candidate name |
| Sex | TEXT | Gender (M/F) |
| Party | TEXT | Political party name |
| Votes | REAL | Number of votes received |
| Valid_Votes | INTEGER | Total valid votes in constituency |
| Electors | REAL | Total number of electors |
| Constituency_Name | TEXT | Name of the constituency |
| Constituency_Type | TEXT | Type of constituency (GEN/SC/ST) |
| N_Cand | INTEGER | Number of candidates |
| Turnout_Percentage | REAL | Voter turnout percentage |
| Vote_Share_Percentage | REAL | Vote share percentage of candidate |
| Deposit_Lost | TEXT | Whether deposit was lost (yes/no) |
| Margin | REAL | Victory margin (vote difference) |
| Margin_Percentage | REAL | Victory margin as percentage |
| ENOP | REAL | Effective Number of Parties |
| pid | TEXT | Party identifier |
| Party_Type_TCPD | TEXT | Party type (National Party/Regional Party/Independents) |
| Party_ID | REAL | Party ID |
| last_poll | INTEGER | Last poll number |
| Contested | REAL | Number of times contested |
| No_Terms | REAL | Number of terms |
| Turncoat | INTEGER | Turncoat indicator (0/1) |
| Incumbent | INTEGER | Incumbent indicator (0/1) |
| Recontest | INTEGER | Recontest indicator (0/1) |
| Election_Type | TEXT | Type of election (e.g., "Lok Sabha Election (GE)") |

#### Key Relationships

- **Primary Identifier**: Combination of `Year`, `State_Name`, `Constituency_Name`, `Position`
- **Winner Identification**: Records where `Position = 1` represent winning candidates
- **Party Classification**: `Party_Type_TCPD` categorizes parties as National, Regional, or Independents

#### Key Metrics

1. **Turnout**: Calculated from `Turnout_Percentage`
2. **Seat Share**: Count of records with `Position = 1` grouped by `Party` and `Year`
3. **Vote Share**: Sum of `Votes` or use `Vote_Share_Percentage`
4. **Victory Margin**: Use `Margin_Percentage` for percentage-based margins
5. **Gender Representation**: Filter by `Sex` field (M/F)

#### Sample Queries

```sql
-- Get seat share by party for 2019
SELECT Party, COUNT(*) as seats
FROM election_results
WHERE Year = 2019 AND Position = 1
GROUP BY Party
ORDER BY seats DESC;

-- Get state-wise average turnout
SELECT State_Name, AVG(Turnout_Percentage) as avg_turnout
FROM election_results
WHERE Year = 2019
GROUP BY State_Name
ORDER BY avg_turnout DESC;

-- Get gender representation
SELECT Year, Sex, COUNT(*) as count
FROM election_results
WHERE Sex IN ('M', 'F')
GROUP BY Year, Sex
ORDER BY Year, Sex;
```

#### Data Coverage

- **Years**: 1991 to 2019
- **States**: All Indian states and union territories
- **Election Type**: Lok Sabha General Elections
- **Total Records**: Varies by election year (typically thousands per election)

#### Notes

- Some fields may contain NULL values - handled in application logic
- `Position = 1` identifies winners
- `Margin_Percentage` is calculated as percentage of valid votes
- State names use underscores instead of spaces (e.g., "Andaman_&_Nicobar_Islands")

