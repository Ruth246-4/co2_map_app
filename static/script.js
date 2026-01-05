// ---------- MAP ----------
const map = L.map("map").setView([20, 0], 2);

L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    attribution: "© OpenStreetMap"
}).addTo(map);

let marker = null;
let selectedPlace = null;

// ---------- DATA HELPERS ----------
function randomCO2() {
    return Math.floor(370 + Math.random() * 130); // ppm
}

function zoneFromPPM(ppm) {
    if (ppm >= 450) return "Red";
    if (ppm >= 400) return "Orange";
    return "Green";
}

function emissionCause(lat) {
    if (Math.abs(lat) < 10)
        return "Coastal influence, humidity and sea–land breeze variations.";
    if (lat > 20 && lat < 50)
        return "Urbanisation, traffic congestion and industrial emissions.";
    return "Mixed natural and anthropogenic sources.";
}

// ---------- PANEL ----------
function showPanel(html) {
    document.getElementById("panelContent").innerHTML = html;
    document.getElementById("infoPanel").classList.remove("hidden");
}

// ---------- SEARCH ----------
async function performSearch() {
    const query = searchInput.value.trim();
    if (!query) return alert("Enter a location");

    const res = await fetch(
        `https://nominatim.openstreetmap.org/search?format=json&q=${query}`
    );
    const data = await res.json();
    if (!data.length) return alert("Location not found");

    const p = data[0];
    const lat = parseFloat(p.lat);
    const lon = parseFloat(p.lon);

    // Generate emission history (inefficiency fixed)
    const history = [];
    for (let i = 0; i < 12; i++) {
        history.push({
            ppm: randomCO2(),
            time: new Date(Date.now() - i * 86400000).toLocaleString()
        });
    }

    selectedPlace = {
        name: p.display_name,
        lat, lon,
        history,
        population: Math.floor(500000 + Math.random() * 5000000),
        cause: emissionCause(lat)
    };

    map.setView([lat, lon], 8);

    if (marker) map.removeLayer(marker);

    const current = history[0];
    marker = L.marker([lat, lon]).addTo(map)
        .bindPopup(`
            <b>${p.display_name}</b><br>
            CO₂: ${current.ppm} ppm<br>
            Zone: ${zoneFromPPM(current.ppm)}
        `)
        .openPopup();
}

// ---------- ELEMENTS ----------
const searchInput = document.getElementById("searchInput");

document.getElementById("searchBtn").onclick = performSearch;
searchInput.addEventListener("keydown", e => {
    if (e.key === "Enter") performSearch();
});
document.getElementById("clearBtn").onclick = () => searchInput.value = "";

// ---------- KNOW ----------
document.getElementById("knowBtn").onclick = () => {
    showPanel(`
        <h3>CO₂ Levels</h3>
        <p>🟥 <b>Red:</b> ≥ 450 ppm (Severe)</p>
        <p>🟧 <b>Orange:</b> 400–449 ppm (Moderate)</p>
        <p>🟩 <b>Green:</b> &lt; 400 ppm (Safe)</p>
    `);
};

// ---------- INSTRUCTIONS ----------
document.getElementById("instructionBtn").onclick = () => {
    if (!selectedPlace) return alert("Search first");

    const current = selectedPlace.history[0];
    const zone = zoneFromPPM(current.ppm);

    showPanel(`
        <h3>Instructions</h3>
        <p><b>Cause:</b> ${selectedPlace.cause}</p>
        <p><b>Zone:</b> ${zone}</p>
        <p><b>Preventive Measures:</b></p>
        <ul>
            <li>Reduce vehicle usage</li>
            <li>Control industrial emissions</li>
            <li>Increase green cover</li>
        </ul>
        <p><b>Adaptive Measures:</b></p>
        <ul>
            <li>Limit outdoor exposure</li>
            <li>Use masks in high-risk zones</li>
            <li>Monitor air quality regularly</li>
        </ul>
        ${zone !== "Green" ? "<p><b>India Emergency Helpline:</b> 108</p>" : ""}
    `);
};

// ---------- HISTORY ----------
document.getElementById("historyBtn").onclick = () => {
    if (!selectedPlace) return alert("Search first");

    const values = selectedPlace.history.map(h => h.ppm);
    const max = Math.max(...values);
    const min = Math.min(...values);

    const maxObj = selectedPlace.history.find(h => h.ppm === max);
    const minObj = selectedPlace.history.find(h => h.ppm === min);

    showPanel(`
        <h3>Emission History</h3>
        <p>Latitude: ${selectedPlace.lat}</p>
        <p>Longitude: ${selectedPlace.lon}</p>
        <p>Current CO₂: ${values[0]} ppm</p>
        <p><b>Highest:</b> ${max} ppm (${maxObj.time})</p>
        <p><b>Lowest:</b> ${min} ppm (${minObj.time})</p>
        <p>Population: ${selectedPlace.population}</p>
    `);
};

// ---------- CLOSE ----------
document.getElementById("closePanel").onclick = () =>
    document.getElementById("infoPanel").classList.add("hidden");
