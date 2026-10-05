const API = "http://127.0.0.1:8000";


// Load dashboard when page opens
loadDashboard();


async function loadDashboard() {

    const totalReviews = document.getElementById("totalReviews");
    const totalIssues = document.getElementById("totalIssues");
    const historyTable = document.getElementById("historyTable");


    // Default values
    totalReviews.textContent = "0";
    totalIssues.textContent = "0";


    try {

        const response = await fetch(`${API}/dashboard`);


        if (!response.ok) {
            throw new Error("Failed to load dashboard");
        }


        const data = await response.json();


        // =====================================
        // Total Reviews
        // =====================================

        totalReviews.textContent =
            data.total_reviews ?? 0;


        // =====================================
        // Total Issues
        // =====================================
        // If backend returns null or nothing,
        // display 0 instead.

        totalIssues.textContent =
            data.total_issues ?? 0;


        // =====================================
        // Review History
        // =====================================

        historyTable.innerHTML = "";


        const reviews = Array.isArray(data.reviews)
            ? data.reviews
            : [];


        // No reviews
        if (reviews.length === 0) {

            historyTable.innerHTML = `
                <tr>
                    <td colspan="4">
                        No reviews yet.
                    </td>
                </tr>
            `;

            return;
        }


        // Display reviews
        reviews.forEach(review => {

            const row = document.createElement("tr");


            const id = review.id ?? "-";

            const filename =
                review.filename ?? "-";

            const language =
                review.language ?? "-";

            const issues =
                review.issues_found ?? 0;


            row.innerHTML = `
                <td>${id}</td>
                <td>${filename}</td>
                <td>${language}</td>
                <td>${issues}</td>
            `;


            historyTable.appendChild(row);

        });


    } catch (error) {

        console.error(
            "Dashboard error:",
            error
        );


        // Keep statistics at zero
        totalReviews.textContent = "0";
        totalIssues.textContent = "0";


        historyTable.innerHTML = `
            <tr>
                <td colspan="4">
                    Unable to load review history.
                </td>
            </tr>
        `;

    }
}