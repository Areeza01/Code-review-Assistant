
const API = "http://127.0.0.1:8000";

async function uploadCode() {

    const fileInput = document.getElementById("fileInput");
    const button = document.getElementById("analyzeButton");
    const report = document.getElementById("report");
    const score = document.getElementById("qualityScore");

    // Check file
    if (!fileInput.files || fileInput.files.length === 0) {
        alert("Please select a file first.");
        return;
    }

    const file = fileInput.files[0];

    // Change button immediately
    button.innerText = "Analyzing...";
    button.disabled = true;

    report.innerText = "Analyzing code... Please wait.";

    try {

        // =========================
        // Upload File
        // =========================

        const formData = new FormData();

        formData.append("file", file);

        const uploadResponse = await fetch(
            `${API}/upload`,
            {
                method: "POST",
                body: formData
            }
        );

        if (!uploadResponse.ok) {
            throw new Error("File upload failed.");
        }

        const uploadData = await uploadResponse.json();


        // =========================
        // Analyze Code
        // =========================

        const reviewResponse = await fetch(
            `${API}/review?filename=${encodeURIComponent(uploadData.filename)}`,
            {
                method: "POST"
            }
        );

        if (!reviewResponse.ok) {
            throw new Error("Code analysis failed.");
        }

        const result = await reviewResponse.json();


        // =========================
        // Display Results
        // =========================

        report.innerText =
            result.report || "No report available.";

        if (result.score !== undefined) {
            score.innerText = result.score;
        }

    }

    catch (error) {

        console.error(error);

        report.innerText =
            "Error: " + error.message;

    }

    finally {

        // Change button back
        button.innerText = "Analyze Code";
        button.disabled = false;
    }
}

