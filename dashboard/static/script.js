async function loadDashboard(){

    const res = await fetch("/api/logs");
    const data = await res.json();

    const tbody = document.getElementById("log-body");
    tbody.innerHTML = "";

    let blockedCount = 0;

    data.logs.forEach(log => {

        const tr = document.createElement("tr");

        if(log.status === "Blocked") blockedCount++;

        tr.innerHTML = `
            <td>${log.time}</td>
            <td>${log.query}</td>
            <td class="${log.status === "Blocked" ? "blocked" : "safe"}">${log.status}</td>
            <td>
                <button class="view-btn"
                    onclick="showIncident('${log.query}','${log.status}','${log.explanation}')">
                    View
                </button>
            </td>
        `;

        tbody.appendChild(tr);
    });

    document.getElementById("total-count").innerText = data.logs.length;
    document.getElementById("blocked-count").innerText = blockedCount;
    document.getElementById("snapshot-count").innerText = data.snapshots;

    if(blockedCount > 0){
        showToast("⚠ Dangerous query detected and snapshot created");
    }
}


function showIncident(query,status,explanation){

    document.getElementById("incident-query").innerText = query;
    document.getElementById("incident-status").innerText = status;
    document.getElementById("incident-ai").innerText = explanation;

    document.getElementById("incident-section")
        .scrollIntoView({behavior:"smooth"});
}



function showToast(message){

    const toast = document.getElementById("toast");
    const text = document.getElementById("toast-text");

    text.innerText = message;

    toast.classList.remove("hidden");
    toast.classList.add("show");

    setTimeout(()=>{
        toast.classList.remove("show");
        toast.classList.add("hidden");
    },4000);
}


/* realtime refresh every 5 seconds */
setInterval(() => {
    fetch('/live_logs')
        .then(res => res.json())
        .then(data => {
            updateDashboard(data);
        });
}, 5000);
