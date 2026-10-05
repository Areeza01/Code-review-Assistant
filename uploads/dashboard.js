
const API = "http://127.0.0.1:8000";

loadDashboard();

async function loadDashboard() {
    try {
        const response = await fetch(`${API}/dashboard`);

        if (!response.ok) {
            throw new Error("Failed to load dashboard data");
        }

        const data = await response.json();

        // Update statistics
        document.getElementById("totalReviews").textContent =
            data.total_reviews;

        document.getElementById("totalIssues").textContent =
            data.total_issues;

        // Update review history
        const table = document.getElementById("historyTable");

        table.innerHTML = "";

        data.reviews.forEach(review => {

            table.innerHTML += `
                <tr>
                    <td>${review.id ?? "-"}</td>
                    <td>${review.filename ?? "-"}</td>
                    <td>${review.language ?? "-"}</td>
                    <td>${review.issues_found ?? 0}</td>
                </tr>
            `;
        });

    } catch (error) {

        console.error("Dashboard error:", error);

        document.getElementById("totalReviews").textContent = "0";
        document.getElementById("totalIssues").textContent = "0";

        const table = document.getElementById("historyTable");

        table.innerHTML = `
            <tr>
                <td colspan="4">
                    Unable to load review history.
                </td>
            </tr>
        `;
    }
}

