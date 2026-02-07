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
            <td><button class="view-btn">View</button></td>
        </tr>`;
        tbody.innerHTML += row;
    });
}

async function loadStats() {
    const res = await fetch("/api/stats");
    const data = await res.json();

    document.getElementById("total-count").innerText = data.total;
    document.getElementById("blocked-count").innerText = data.blocked;
    document.getElementById("snapshot-count").innerText = data.snapshots;
}

/* realtime refresh */
setInterval(() => {
    loadDashboard();
    loadStats();
}, 5000);

loadDashboard();
loadStats();
