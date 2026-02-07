/* ---------- Load Logs Table ---------- */
async function loadDashboard() {
    const res = await fetch("/api/logs");
    const data = await res.json();

    const tbody = document.getElementById("log-body");
    tbody.innerHTML = "";

    data.forEach(log => {

        const row = `
        <tr>
            <td>${log.time}</td>
            <td>${log.query}</td>
            <td>${log.status}</td>
            <td>
                <button class="view-btn"
                    onclick="showIncident('${log.query}','${log.status}')">
                    View
                </button>
            </td>
        </tr>
        `;

        tbody.innerHTML += row;
    });
}


/* ---------- Incident Explanation ---------- */
function showIncident(query,status){

    document.getElementById("incident-query").innerText = query;
    document.getElementById("incident-status").innerText = status;

    if(status === "Blocked"){
        document.getElementById("incident-ai").innerText =
        "This query was detected as potentially destructive and blocked automatically.";
    }else{
        document.getElementById("incident-ai").innerText =
        "This query is safe and does not pose a database risk.";
    }

    document.getElementById("incident-section")
        .scrollIntoView({behavior:"smooth"});
}


/* ---------- Load Stats ---------- */
async function loadStats() {
    const res = await fetch("/api/stats");
    const data = await res.json();

    document.getElementById("total-count").innerText = data.total;
    document.getElementById("blocked-count").innerText = data.blocked;
    document.getElementById("snapshot-count").innerText = data.snapshots;
}


/* ---------- Realtime Refresh ---------- */
setInterval(() => {
    loadDashboard();
    loadStats();
}, 5000);

loadDashboard();
loadStats();
