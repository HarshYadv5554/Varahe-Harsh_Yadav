// Auto-detect API base URL - use relative path for production, absolute for local dev
const API_BASE = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1' 
    ? 'http://localhost:5000/api' 
    : '/api';

let charts = {};
let turnoutMap = null;
let currentYear = '';

// Initialize dashboard
document.addEventListener('DOMContentLoaded', async () => {
    await loadFilters();
    await initializeMap();
    await updateAllCharts();
    await loadAnalytics();
});

// Load filter options
async function loadFilters() {
    try {
        const [years, states, parties] = await Promise.all([
            fetch(`${API_BASE}/filters/years`).then(r => r.json()),
            fetch(`${API_BASE}/filters/states`).then(r => r.json()),
            fetch(`${API_BASE}/filters/parties`).then(r => r.json())
        ]);

        const yearFilter = document.getElementById('yearFilter');
        const stateFilter = document.getElementById('stateFilter');
        const partyFilter = document.getElementById('partyFilter');

        years.forEach(year => {
            const option = document.createElement('option');
            option.value = year;
            option.textContent = year;
            yearFilter.appendChild(option);
        });

        states.forEach(state => {
            const option = document.createElement('option');
            option.value = state;
            option.textContent = state.replace(/_/g, ' ');
            stateFilter.appendChild(option);
        });

        parties.forEach(party => {
            const option = document.createElement('option');
            option.value = party;
            option.textContent = party;
            partyFilter.appendChild(option);
        });
    } catch (error) {
        console.error('Error loading filters:', error);
    }
}

// Update all charts
async function updateAllCharts() {
    currentYear = document.getElementById('yearFilter').value || '';
    await Promise.all([
        loadSeatShareChart(),
        loadTurnoutMap(),
        loadGenderChart(),
        loadVoteShareChart(),
        loadMarginChart(),
        loadNationalVsRegionalChart()
    ]);
}

// Party-wise Seat Share Chart
async function loadSeatShareChart() {
    try {
        const url = currentYear ? `${API_BASE}/party-seat-share?year=${currentYear}` : `${API_BASE}/party-seat-share`;
        const data = await fetch(url).then(r => r.json());

        const ctx = document.getElementById('seatShareChart').getContext('2d');
        
        if (charts.seatShare) {
            charts.seatShare.destroy();
        }

        // Group by year if multiple years
        if (!currentYear && data.length > 0 && data[0].Year) {
            const years = [...new Set(data.map(d => d.Year))];
            const parties = [...new Set(data.map(d => d.Party))];
            
            const datasets = parties.slice(0, 10).map(party => ({
                label: party,
                data: years.map(year => {
                    const entry = data.find(d => d.Year === year && d.Party === party);
                    return entry ? entry.seats : 0;
                }),
                backgroundColor: getRandomColor()
            }));

            charts.seatShare = new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: years,
                    datasets: datasets
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: true,
                    scales: {
                        y: { beginAtZero: true }
                    },
                    plugins: {
                        legend: { display: true, position: 'right' }
                    }
                }
            });
        } else {
            // Single year or no year selected
            const sortedData = currentYear 
                ? data.sort((a, b) => b.seats - a.seats).slice(0, 15)
                : data.sort((a, b) => b.seats - a.seats).slice(0, 15);

            charts.seatShare = new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: sortedData.map(d => d.Party || 'Unknown'),
                    datasets: [{
                        label: 'Seats Won',
                        data: sortedData.map(d => d.seats),
                        backgroundColor: 'rgba(102, 126, 234, 0.8)'
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: true,
                    scales: {
                        y: { beginAtZero: true }
                    },
                    plugins: {
                        legend: { display: false }
                    }
                }
            });
        }
    } catch (error) {
        console.error('Error loading seat share chart:', error);
    }
}

// State-wise Turnout Map
let turnoutMarkers = [];

async function loadTurnoutMap() {
    try {
        const url = currentYear ? `${API_BASE}/state-turnout?year=${currentYear}` : `${API_BASE}/state-turnout`;
        const data = await fetch(url).then(r => r.json());

        if (!turnoutMap) {
            turnoutMap = L.map('turnoutMap').setView([23.0225, 77.5], 5.5);
            L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                attribution: '© OpenStreetMap contributors',
                maxZoom: 10,
                minZoom: 4
            }).addTo(turnoutMap);
        }

        // Clear previous markers
        turnoutMarkers.forEach(marker => turnoutMap.removeLayer(marker));
        turnoutMarkers = [];

        // Sort data by turnout for better visualization
        const sortedData = data
            .filter(state => state.avg_turnout && state.avg_turnout > 0)
            .sort((a, b) => b.avg_turnout - a.avg_turnout);

        // Create custom styled markers with state labels
        sortedData.forEach(state => {
            const coords = getStateCoordinates(state.State_Name);
            if (coords && state.avg_turnout) {
                const turnout = parseFloat(state.avg_turnout);
                const color = getColorForTurnout(turnout);
                
                // Calculate marker size based on turnout (larger for higher turnout)
                const size = Math.max(30, Math.min(60, turnout * 0.8));
                
                // Create custom HTML icon with state name and turnout percentage
                const stateNameShort = getShortStateName(state.State_Name);
                const iconHtml = `
                    <div style="
                        background: ${color};
                        border: 3px solid white;
                        border-radius: 8px;
                        padding: 6px 10px;
                        box-shadow: 0 2px 8px rgba(0,0,0,0.3);
                        font-weight: bold;
                        font-size: 11px;
                        color: white;
                        text-align: center;
                        min-width: ${size}px;
                        white-space: nowrap;
                        cursor: pointer;
                        transition: transform 0.2s;
                    " onmouseover="this.style.transform='scale(1.15)'" onmouseout="this.style.transform='scale(1)'">
                        ${stateNameShort}<br/>
                        <span style="font-size: 9px; opacity: 0.95;">${turnout.toFixed(1)}%</span>
                    </div>
                `;

                const customIcon = L.divIcon({
                    html: iconHtml,
                    className: 'custom-state-marker',
                    iconSize: [null, null],
                    iconAnchor: [0, 0]
                });

                const marker = L.marker(coords, { icon: customIcon })
                    .addTo(turnoutMap)
                    .bindPopup(
                        `<div style="text-align: center; padding: 5px;">
                            <strong style="font-size: 14px;">${state.State_Name.replace(/_/g, ' ')}</strong><br/>
                            <div style="margin-top: 8px;">
                                <span style="font-weight: bold; color: ${color}; font-size: 18px;">${turnout.toFixed(2)}%</span><br/>
                                <span style="font-size: 11px; color: #666;">Average Turnout</span>
                            </div>
                            ${state.max_turnout ? `<div style="margin-top: 5px; font-size: 11px; color: #888;">Max: ${parseFloat(state.max_turnout).toFixed(2)}%</div>` : ''}
                            ${state.min_turnout ? `<div style="font-size: 11px; color: #888;">Min: ${parseFloat(state.min_turnout).toFixed(2)}%</div>` : ''}
                        </div>`,
                        {
                            className: 'custom-popup',
                            maxWidth: 200
                        }
                    );

                turnoutMarkers.push(marker);
            }
        });
    } catch (error) {
        console.error('Error loading turnout map:', error);
    }
}

function initializeMap() {
    // Map initialization happens in loadTurnoutMap
}

function getStateCoordinates(stateName) {
    // Simplified state coordinates - in production, use proper GeoJSON
    const stateCoords = {
        'Andhra_Pradesh': [15.9129, 79.7400],
        'Assam': [26.2006, 92.9376],
        'Bihar': [25.0961, 85.3131],
        'Gujarat': [23.0225, 72.5714],
        'Haryana': [29.0588, 76.0856],
        'Karnataka': [15.3173, 75.7139],
        'Kerala': [10.8505, 76.2711],
        'Madhya_Pradesh': [22.9734, 78.6569],
        'Maharashtra': [19.7515, 75.7139],
        'Odisha': [20.9517, 85.0985],
        'Punjab': [31.1471, 75.3412],
        'Rajasthan': [27.0238, 74.2179],
        'Tamil_Nadu': [11.1271, 78.6569],
        'Uttar_Pradesh': [26.8467, 80.9462],
        'West_Bengal': [22.9868, 87.8550],
        'Andaman_&_Nicobar_Islands': [11.6670, 92.7380],
        'Arunachal_Pradesh': [28.2180, 94.7278],
        'Chhattisgarh': [21.2787, 81.8661],
        'Goa': [15.2993, 74.1240],
        'Himachal_Pradesh': [31.1048, 77.1734],
        'Jammu_&_Kashmir': [34.0837, 74.7973],
        'Jharkhand': [23.6102, 85.2799],
        'Manipur': [24.6637, 93.9063],
        'Meghalaya': [25.4670, 91.3662],
        'Mizoram': [23.1645, 92.9376],
        'Nagaland': [26.1584, 94.5624],
        'Sikkim': [27.5330, 88.5122],
        'Tripura': [23.9408, 91.9882],
        'Uttarakhand': [30.0668, 79.0193],
        'Telangana': [18.1124, 79.0193],
        'Delhi': [28.6139, 77.2090],
        'Puducherry': [11.9416, 79.8083],
        'Chandigarh': [30.7333, 76.7794],
        'Dadra_&_Nagar_Haveli': [20.1809, 73.0169],
        'Daman_&_Diu': [20.4283, 72.8397],
        'Lakshadweep': [10.5667, 72.6417]
    };
    return stateCoords[stateName] || null;
}

function getColorForTurnout(turnout) {
    // Enhanced color gradient for better visualization
    if (turnout >= 75) return '#27ae60';      // Dark green - excellent
    if (turnout >= 70) return '#2ecc71';      // Green - very good
    if (turnout >= 65) return '#52c6a3';      // Teal - good
    if (turnout >= 60) return '#3498db';      // Blue - above average
    if (turnout >= 55) return '#5dade2';      // Light blue - average
    if (turnout >= 50) return '#f39c12';      // Orange - below average
    if (turnout >= 45) return '#e67e22';      // Dark orange - low
    return '#e74c3c';                          // Red - very low
}

function getShortStateName(fullName) {
    // Abbreviate state names for cleaner map display
    const abbreviations = {
        'Andhra_Pradesh': 'AP',
        'Arunachal_Pradesh': 'AR',
        'Assam': 'AS',
        'Bihar': 'BR',
        'Chhattisgarh': 'CG',
        'Goa': 'GO',
        'Gujarat': 'GJ',
        'Haryana': 'HR',
        'Himachal_Pradesh': 'HP',
        'Jammu_&_Kashmir': 'JK',
        'Jharkhand': 'JH',
        'Karnataka': 'KA',
        'Kerala': 'KL',
        'Madhya_Pradesh': 'MP',
        'Maharashtra': 'MH',
        'Manipur': 'MN',
        'Meghalaya': 'ML',
        'Mizoram': 'MZ',
        'Nagaland': 'NL',
        'Odisha': 'OR',
        'Punjab': 'PB',
        'Rajasthan': 'RJ',
        'Sikkim': 'SK',
        'Tamil_Nadu': 'TN',
        'Telangana': 'TG',
        'Tripura': 'TR',
        'Uttar_Pradesh': 'UP',
        'Uttarakhand': 'UT',
        'West_Bengal': 'WB',
        'Delhi': 'DL',
        'Puducherry': 'PY',
        'Chandigarh': 'CH',
        'Andaman_&_Nicobar_Islands': 'AN',
        'Dadra_&_Nagar_Haveli': 'DN',
        'Daman_&_Diu': 'DD',
        'Lakshadweep': 'LD'
    };
    
    // If abbreviation exists, use it; otherwise use first 3-4 words
    if (abbreviations[fullName]) {
        return abbreviations[fullName];
    }
    
    // For union territories and states without abbreviations
    const words = fullName.replace(/_/g, ' ').split(' ');
    if (words.length <= 2) {
        return words.join(' ').substring(0, 8);
    }
    return words[0] + ' ' + words[1];
}

// Gender Representation Chart
async function loadGenderChart() {
    try {
        const data = await fetch(`${API_BASE}/gender-representation`).then(r => r.json());
        const ctx = document.getElementById('genderChart').getContext('2d');

        if (charts.gender) {
            charts.gender.destroy();
        }

        const years = [...new Set(data.map(d => d.Year))].sort();
        const maleData = years.map(year => {
            const entry = data.find(d => d.Year === year && d.Sex === 'M');
            return entry ? entry.percentage : 0;
        });
        const femaleData = years.map(year => {
            const entry = data.find(d => d.Year === year && d.Sex === 'F');
            return entry ? entry.percentage : 0;
        });

        charts.gender = new Chart(ctx, {
            type: 'line',
            data: {
                labels: years,
                datasets: [
                    {
                        label: 'Male (%)',
                        data: maleData,
                        borderColor: 'rgba(54, 162, 235, 1)',
                        backgroundColor: 'rgba(54, 162, 235, 0.1)',
                        tension: 0.4
                    },
                    {
                        label: 'Female (%)',
                        data: femaleData,
                        borderColor: 'rgba(255, 99, 132, 1)',
                        backgroundColor: 'rgba(255, 99, 132, 0.1)',
                        tension: 0.4
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                scales: {
                    y: { beginAtZero: true, max: 100 }
                },
                plugins: {
                    legend: { display: true }
                }
            }
        });
    } catch (error) {
        console.error('Error loading gender chart:', error);
    }
}

// Top Parties by Vote Share (Donut Chart)
async function loadVoteShareChart() {
    try {
        const url = currentYear ? `${API_BASE}/top-parties-vote-share?year=${currentYear}&limit=10` : `${API_BASE}/top-parties-vote-share?limit=10`;
        const data = await fetch(url).then(r => r.json());
        const ctx = document.getElementById('voteShareChart').getContext('2d');

        if (charts.voteShare) {
            charts.voteShare.destroy();
        }

        charts.voteShare = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: data.map(d => d.Party || 'Unknown'),
                datasets: [{
                    data: data.map(d => parseFloat(d.vote_share_percentage || 0)),
                    backgroundColor: [
                        '#667eea', '#764ba2', '#f093fb', '#4facfe',
                        '#00f2fe', '#43e97b', '#fa709a', '#fee140',
                        '#30cfd0', '#330867'
                    ]
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                plugins: {
                    legend: { display: true, position: 'right' },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                return context.label + ': ' + context.parsed.toFixed(2) + '%';
                            }
                        }
                    }
                }
            }
        });
    } catch (error) {
        console.error('Error loading vote share chart:', error);
    }
}

// Margin of Victory Distribution (Histogram)
async function loadMarginChart() {
    try {
        const url = currentYear ? `${API_BASE}/margin-distribution?year=${currentYear}` : `${API_BASE}/margin-distribution`;
        const data = await fetch(url).then(r => r.json());
        const ctx = document.getElementById('marginChart').getContext('2d');

        if (charts.margin) {
            charts.margin.destroy();
        }

        // Create histogram bins
        const bins = [0, 5, 10, 15, 20, 25, 30, 35, 40, 50, 100];
        const binCounts = new Array(bins.length - 1).fill(0);
        
        data.forEach(value => {
            for (let i = 0; i < bins.length - 1; i++) {
                if (value >= bins[i] && value < bins[i + 1]) {
                    binCounts[i]++;
                    break;
                }
            }
            if (value >= bins[bins.length - 1]) {
                binCounts[binCounts.length - 1]++;
            }
        });

        const binLabels = bins.slice(0, -1).map((bin, i) => `${bin}-${bins[i + 1]}%`);

        charts.margin = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: binLabels,
                datasets: [{
                    label: 'Number of Constituencies',
                    data: binCounts,
                    backgroundColor: 'rgba(102, 126, 234, 0.8)'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                scales: {
                    y: { beginAtZero: true }
                },
                plugins: {
                    legend: { display: false }
                }
            }
        });
    } catch (error) {
        console.error('Error loading margin chart:', error);
    }
}

// National vs Regional Parties
async function loadNationalVsRegionalChart() {
    try {
        const data = await fetch(`${API_BASE}/analytics/national-vs-regional`).then(r => r.json());
        const ctx = document.getElementById('nationalVsRegionalChart').getContext('2d');

        if (charts.nationalVsRegional) {
            charts.nationalVsRegional.destroy();
        }

        const years = [...new Set(data.map(d => d.Year))].sort();
        const nationalData = years.map(year => {
            const entry = data.find(d => d.Year === year && d.Party_Type_TCPD === 'National Party');
            return entry ? parseFloat(entry.vote_share_percentage || 0) : 0;
        });
        const regionalData = years.map(year => {
            const entry = data.find(d => d.Year === year && d.Party_Type_TCPD === 'Regional Party');
            return entry ? parseFloat(entry.vote_share_percentage || 0) : 0;
        });

        charts.nationalVsRegional = new Chart(ctx, {
            type: 'line',
            data: {
                labels: years,
                datasets: [
                    {
                        label: 'National Parties (%)',
                        data: nationalData,
                        borderColor: 'rgba(102, 126, 234, 1)',
                        backgroundColor: 'rgba(102, 126, 234, 0.1)',
                        tension: 0.4
                    },
                    {
                        label: 'Regional Parties (%)',
                        data: regionalData,
                        borderColor: 'rgba(118, 75, 162, 1)',
                        backgroundColor: 'rgba(118, 75, 162, 0.1)',
                        tension: 0.4
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                scales: {
                    y: { beginAtZero: true }
                },
                plugins: {
                    legend: { display: true }
                }
            }
        });
    } catch (error) {
        console.error('Error loading national vs regional chart:', error);
    }
}

// Search functionality
async function searchCandidates() {
    try {
        const candidate = document.getElementById('candidateSearch').value;
        const constituency = document.getElementById('constituencySearch').value;
        const year = document.getElementById('yearFilter').value;
        const state = document.getElementById('stateFilter').value;
        const party = document.getElementById('partyFilter').value;

        let url = `${API_BASE}/search?`;
        const params = [];
        
        if (candidate) params.push(`candidate=${encodeURIComponent(candidate)}`);
        if (constituency) params.push(`constituency=${encodeURIComponent(constituency)}`);
        if (year) params.push(`year=${year}`);
        if (state) params.push(`state=${encodeURIComponent(state)}`);
        if (party) params.push(`party=${encodeURIComponent(party)}`);

        url += params.join('&');

        const data = await fetch(url).then(r => r.json());
        const tbody = document.getElementById('searchTableBody');
        
        tbody.innerHTML = data.map(row => `
            <tr>
                <td>${row.Year || ''}</td>
                <td>${(row.State_Name || '').replace(/_/g, ' ')}</td>
                <td>${row.Constituency_Name || ''}</td>
                <td>${row.Candidate || ''}</td>
                <td>${row.Party || ''}</td>
                <td>${row.Sex === 'M' ? 'Male' : row.Sex === 'F' ? 'Female' : ''}</td>
                <td>${row.Votes ? parseInt(row.Votes).toLocaleString() : ''}</td>
                <td>${row.Position || ''}</td>
            </tr>
        `).join('');
    } catch (error) {
        console.error('Error searching:', error);
    }
}

// Load analytics insights
async function loadAnalytics() {
    try {
        // Highest turnout state
        const turnoutData = await fetch(`${API_BASE}/analytics/highest-turnout-state`).then(r => r.json());
        document.getElementById('highestTurnout').innerHTML = 
            `<strong>${(turnoutData.State_Name || '').replace(/_/g, ' ')}</strong><br/>` +
            `Turnout: ${parseFloat(turnoutData.avg_turnout || 0).toFixed(2)}% (${turnoutData.year})`;

        // Women percentage
        const womenData = await fetch(`${API_BASE}/analytics/women-percentage`).then(r => r.json());
        document.getElementById('womenPercentage').innerHTML = 
            `<strong>${parseFloat(womenData.women_percentage || 0).toFixed(2)}%</strong><br/>` +
            `${parseInt(womenData.women_candidates || 0).toLocaleString()} out of ${parseInt(womenData.total_candidates || 0).toLocaleString()} candidates`;

        // Seat changes
        const seatChangeData = await fetch(`${API_BASE}/analytics/seat-change`).then(r => r.json());
        const topGainers = seatChangeData.changes.slice(0, 3).map(c => 
            `<div>${c.party}: ${c.change > 0 ? '+' : ''}${c.change} seats</div>`
        ).join('');
        document.getElementById('seatChanges').innerHTML = 
            `<div><strong>${seatChangeData.year1} → ${seatChangeData.year2}</strong></div>` + topGainers;

        // Narrowest margins
        const marginData = await fetch(`${API_BASE}/analytics/narrowest-margins?limit=5`).then(r => r.json());
        const margins = marginData.slice(0, 5).map(m => 
            `<div>${m.Constituency_Name}: ${parseFloat(m.Margin_Percentage || 0).toFixed(2)}%</div>`
        ).join('');
        document.getElementById('narrowMargins').innerHTML = margins;
    } catch (error) {
        console.error('Error loading analytics:', error);
    }
}

function getRandomColor() {
    const colors = [
        'rgba(102, 126, 234, 0.8)',
        'rgba(118, 75, 162, 0.8)',
        'rgba(240, 147, 251, 0.8)',
        'rgba(79, 172, 254, 0.8)',
        'rgba(0, 242, 254, 0.8)',
        'rgba(67, 233, 123, 0.8)',
        'rgba(250, 112, 154, 0.8)',
        'rgba(254, 225, 64, 0.8)'
    ];
    return colors[Math.floor(Math.random() * colors.length)];
}

