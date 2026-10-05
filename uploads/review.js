const API = "http://127.0.0.1:8000";

async function uploadCode() {

    const fileInput = document.getElementById("fileInput");
    const report = document.getElementById("report");
    const score = document.getElementById("qualityScore");
    const button = document.getElementById("analyzeButton");

    // Check if a file is selected
    if (!fileInput.files.length) {
        report.textContent = "Please select a Python or JavaScript file.";
        return;
    }

    const file = fileInput.files[0];

    // Check file type
    const allowedExtensions = [".py", ".js"];

    const extension = file.name
        .substring(file.name.lastIndexOf("."))
        .toLowerCase();

    if (!allowedExtensions.includes(extension)) {
        report.textContent =
            "Invalid file type. Please upload a .py or .js file.";
        return;
    }

    // Change button to Analyzing
    button.textContent = "Analyzing...";
    button.disabled = true;

    report.textContent = "Analyzing your code, please wait...";

    try {

        // Upload file
        const formData = new FormData();

        formData.append("file", file);

        const upload = await fetch(`${API}/upload`, {
            method: "POST",
            body: formData
        });

        if (!upload.ok) {
            throw new Error("File upload failed.");
        }

        const uploadData = await upload.json();

        // Request code review
        const review = await fetch(
            `${API}/review?filename=${encodeURIComponent(uploadData.filename)}`,
            {
                method: "POST"
            }
        );

        if (!review.ok) {
            throw new Error("Code analysis failed.");
        }

        const result = await review.json();

        // Display report
        report.textContent =
            result.report || "No review report was returned.";

        // Display score
        if (score && result.score !== undefined) {
            score.textContent = result.score;
        }

    } catch (error) {

        console.error("Review error:", error);

        report.textContent =
            `Error: ${error.message}`;

    } finally {

        // Change button back after analysis
        button.textContent = "Analyze Code";
        button.disabled = false;
    }
}

