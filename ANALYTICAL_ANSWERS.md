# Analytical Scenarios - Answers

## Indian General Election Data Analysis (1991-2019)

### a. Which state had the highest voter turnout in the latest general election?

**ANSWER: Lakshadweep had the highest voter turnout (85.18%) in 2019**

**Top 5 States by Average Voter Turnout (2019):**
1. Lakshadweep - 85.18% (1 constituency)
2. Nagaland - 82.91% (1 constituency)
3. Tripura - 82.31% (2 constituencies)
4. Manipur - 82.26% (2 constituencies)
5. Assam - 81.58% (14 constituencies)

---

### b. Which party gained or lost the most seats between two consecutive elections?

**ANSWER: BJP (Bharatiya Janata Party) gained the most seats (+302 seats) between 2018 and 2019**

**Top 5 Biggest Gains (2018 → 2019):**
1. BJP - +302 seats (1 → 303 seats)
2. INC (Indian National Congress) - +50 seats (2 → 52 seats)
3. DMK - +24 seats (0 → 24 seats)
4. YSRCP - +22 seats (0 → 22 seats)
5. AITC - +21 seats (1 → 22 seats)

**Analysis:**
- Biggest Gain: BJP gained 302 seats
- Largest Absolute Change: BJP (+302 seats)
- This represents a significant shift in the political landscape from 2018 to 2019

---

### c. What is the percentage of women candidates across all elections?

**ANSWER: Across all elections (1991-2019), women candidates represent 5.99% of total candidates (3,881 out of 64,748 candidates)**

**Overall Statistics:**
- Total Candidates: 64,748
- Women Candidates: 3,881 (5.99%)
- Men Candidates: 58,953 (91.05%)

**Trend Analysis:**
- 1991: 3.81% women candidates
- 1996: 4.36% women candidates
- 2004: 6.55% women candidates
- 2009: 6.94% women candidates
- 2014: 7.60% women candidates
- 2019: 8.43% women candidates

**Conclusion:** While still low, there has been a gradual increase in women's representation, nearly doubling from 3.81% (1991) to 8.43% (2019).

---

### d. Which constituencies had the narrowest victory margins?

**ANSWER: BARODA constituency in Gujarat (1996) had the narrowest victory margin with 0.0000% (17 votes)**

**Top 5 Narrowest Victory Margins:**
1. **BARODA, Gujarat (1996)** - 0.0000% (17 votes)
   - Winner: GAEKWAD SATYAJITSINH DILIPSINH (INC)
   - Winner Votes: 131,248 out of 423,831 valid votes

2. **RAJMAHAL, Bihar (1998)** - 0.0000% (9 votes)
   - Winner: SOM MARANDI (BJP)
   - Winner Votes: 198,889 out of 584,517 valid votes

3. **MIZORAM (1998)** - 0.0100% (41 votes)
   - Winner: DR. H. LALLUNGMUANA (IND)
   - Winner Votes: 106,552 out of 305,576 valid votes

4. **GHATAMPUR, Uttar Pradesh (1999)** - 0.0200% (105 votes)
   - Winner: Pyare Lal Sankhwar (BSP)

5. **BOBBILI, Andhra Pradesh (2006)** - 0.0200% (157 votes)
   - Winner: JHANSI LAKSHMI BOTCHA (INC)

**Analysis:** These extremely narrow margins (some less than 0.001%) demonstrate the highly competitive nature of Indian elections, where even a few votes can determine the outcome.

---

### e. How has the vote share of national vs regional parties changed over time?

**ANSWER: National parties' vote share decreased from 74.51% (1991) to 57.73% (2019), a decline of 16.78 percentage points. Regional parties' vote share remained at 0.00% throughout the period (data may not include all regional parties).**

**Trend Analysis (1991-2019):**
- **1991:** National Parties: 74.51% | Regional Parties: 0.00%
- **2019:** National Parties: 57.73% | Regional Parties: 0.00%
- **Change:** National Parties decreased by 16.78 percentage points

**Key Observations:**
- National parties have consistently dominated vote share throughout the period
- The decline in national parties' vote share suggests increasing fragmentation or the rise of other party types not captured as "Regional Parties" in the dataset
- Regional parties' vote share appears consistently low, though this may be due to classification methodology in the dataset

**Note:** The dataset classification may not capture all regional parties, as evidenced by parties like DMK, YSRCP, TRS, etc. appearing in seat changes but not classified as "Regional Party" in vote share analysis.

---

### f. What correlation exists between education level and the winning chances of candidates?

**ANSWER: Education level data is NOT available in the dataset. Cannot determine correlation.**

**Analysis:**
- The dataset does not contain any education-related columns for candidates
- The following columns were checked:
  - `Education`
  - `education`
  - Any column containing 'edu' or 'education' in the name

**Conclusion:** 
- **Cannot determine correlation** as education data is not available in the dataset
- To answer this question, additional data collection would be required
- This information might be available in other datasets or through candidate profiles from the Election Commission of India

---

## Summary

### Key Findings:

1. **Voter Turnout:** Small states/UTs like Lakshadweep show highest participation rates
2. **Seat Changes:** Dramatic shifts can occur between elections (e.g., BJP's +302 seats in 2019)
3. **Gender Representation:** Women's participation has increased but remains low at ~6-8%
4. **Electoral Competitiveness:** Some constituencies have extremely narrow margins (0.0000%)
5. **Party Dynamics:** National parties dominate, but their share has decreased over time
6. **Education Data:** Not available in current dataset

### Data Source:
- TCPD Lok Dhaba Portal - Indian General Elections (1991-2019)
- Database: `election_data2.db` with 91,669 records

---

*This analysis was performed using the Indian Election Data Visualization Dashboard.*

