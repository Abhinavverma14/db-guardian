async function loadDashboard() {
    try {
        const response = await fetch("/live_logs");
        const data = await response.json();

        const logTable = document.getElementById("log-body");

        logTable.innerHTML = "";

        data.forEach(log => {
            const row = `
                <tr>
                    <td>${log.time}</td>
                    <td>${log.query}</td>
                    <td>${log.status}</td>
                    <td><button class="btn-view">View</button></td>
                </tr>
            `;
            logTable.innerHTML += row;
        });

    } catch (error) {
        console.error("Error loading dashboard:", error);
    }
}

/* realtime refresh every 5 seconds */
setInterval(loadDashboard, 5000);

/* first load immediately */
loadDashboard();
