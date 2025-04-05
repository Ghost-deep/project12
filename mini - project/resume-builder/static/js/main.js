function updatePreview() {
    const name = document.getElementById("name")?.value || "";
    const email = document.getElementById("email")?.value || "";
    const phone = document.getElementById("phone")?.value || "";
    const summary = document.getElementById("summary")?.value || "";
    const degree = document.getElementById("degree")?.value || "";
    const institution = document.getElementById("institution")?.value || "";
    const eduYear = document.getElementById("eduYear")?.value || "";
    const jobTitle = document.getElementById("jobTitle")?.value || "";
    const company = document.getElementById("company")?.value || "";
    const expYears = document.getElementById("expYears")?.value || "";
    const jobDescription = document.getElementById("jobDescription")?.value || "";
    const skills = document.getElementById("skills")?.value || "";

    const data = {
        name, email, phone, summary,
        degree, institution, eduYear,
        jobTitle, company, expYears,
        jobDescription, skills
    };

    // Store in localStorage to access in preview.html
    localStorage.setItem("resumeData", JSON.stringify(data));
}

// Load preview data in preview.html
function loadPreview() {
    const data = JSON.parse(localStorage.getItem("resumeData") || "{}");
    if (!data) return;

    document.getElementById("previewName").textContent = data.name || "";
    document.getElementById("previewEmail").textContent = data.email || "";
    document.getElementById("previewPhone").textContent = data.phone || "";
    document.getElementById("previewSummary").textContent = data.summary || "";

    document.getElementById("previewDegree").textContent = data.degree || "";
    document.getElementById("previewInstitution").textContent = data.institution || "";
    document.getElementById("previewEduYear").textContent = data.eduYear || "";

    document.getElementById("previewJobTitle").textContent = data.jobTitle || "";
    document.getElementById("previewCompany").textContent = data.company || "";
    document.getElementById("previewExpYears").textContent = data.expYears || "";
    document.getElementById("previewJobDescription").textContent = data.jobDescription || "";
    document.getElementById("previewSkills").textContent = data.skills || "";
}

function exportAsPDF() {
    alert("🔧 PDF export feature coming soon!");
}

function exportAsDOCX() {
    alert("🔧 DOCX export feature coming soon!");
}

// Event Bindings
document.addEventListener("DOMContentLoaded", () => {
    const inputs = document.querySelectorAll("input, textarea");
    inputs.forEach(input => {
        input.addEventListener("input", updatePreview);
    });

    const form = document.getElementById("resumeForm");
    if (form) {
        form.addEventListener("submit", function(e) {
            e.preventDefault();
            updatePreview();
            alert("✅ Resume data saved! Click 'Go to Preview' to view.");
        });
    }

    // Auto-load preview data on preview.html
    if (document.getElementById("resumePreview")) {
        loadPreview();
    }
});
