import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from streamlit_option_menu import option_menu

API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="AI Recruitment Resume Analyzer",
    page_icon="📄",
    layout="wide"
)

# ==========================
# HEADER
# ==========================

st.title("🚀 AI Recruitment Resume Analyzer")

st.markdown(
    "Upload resumes, analyze candidates, rank applicants and generate reports."
)

# ==========================
# NAVIGATION
# ==========================

menu = option_menu(
    menu_title=None,
    options=[
        "Dashboard",
        "Job Description",
        "Upload Resume",
        "Rankings",
        "Reports"
    ],
    icons=[
        "speedometer",
        "file-earmark-text",
        "cloud-upload",
        "trophy",
        "bar-chart"
    ],
    orientation="horizontal"
)

# ==========================
# DASHBOARD
# ==========================

if menu == "Dashboard":

    st.header("📊 Recruitment Analytics Dashboard")

    try:

        rankings_response = requests.get(
            f"{API_URL}/rankings"
        )

        report_response = requests.get(
            f"{API_URL}/report"
        )

        rankings = rankings_response.json()
        report = report_response.json()

        # KPI Cards

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "Total Candidates",
                report.get(
                    "total_candidates",
                    0
                )
            )

        with col2:
            st.metric(
                "Highest Score",
                report.get(
                    "highest_score",
                    0
                )
            )

        with col3:
            st.metric(
                "Top Candidate",
                report.get(
                    "top_candidate",
                    "N/A"
                )
            )

        if rankings:

            df = pd.DataFrame(rankings)

            df["score"] = pd.to_numeric(
            df["score"],
            errors="coerce"
             ).fillna(0)

            average_score = round(
                float(df["score"].mean()),
                2
            )

        else:

            average_score = 0

        with col4:
            st.metric(
                "Average Score",
                average_score
            )

        st.divider()

        if rankings:

            df = pd.DataFrame(rankings)

            df["score"] = pd.to_numeric(
                df["score"],
                errors="coerce"
            ).fillna(0)

            # Candidate Score Chart

            st.subheader(
                "📈 Candidate Scores"
            )

            score_chart = px.bar(
                df,
                x="filename",
                y="score",
                color="score",
                text="score",
                title="Candidate Ranking Scores"
            )

            st.plotly_chart(
                score_chart,
                use_container_width=True
            )

            # Score Distribution

            st.subheader(
                "📊 Score Distribution"
            )

            distribution_chart = px.histogram(
                df,
                x="score",
                nbins=10,
                color="score",
                title="Candidate Score Distribution"
            )

            st.plotly_chart(
                distribution_chart,
                use_container_width=True
            )

           
            # Leaderboard

            st.subheader(
                "🏆 Candidate Leaderboard"
            )

            leaderboard = df.sort_values(
                by="score",
                ascending=False
            )

            st.dataframe(
                leaderboard,
                use_container_width=True
            )

        else:

            st.info(
                "No candidate data available."
            )

    except Exception as e:

        st.error(
            f"Dashboard Error: {e}"
        )

# ==========================
# JOB DESCRIPTION
# ==========================

elif menu == "Job Description":

    st.header("📝 Job Description")

    try:

        current_jd = requests.get(
            f"{API_URL}/job-description"
        ).json()

        st.info(
            f"Current JD:\n\n{current_jd.get('job_description', '')}"
        )

    except Exception:
        pass

    jd = st.text_area(
        "Enter Job Description",
        height=250,
        placeholder="Looking for a Python Developer with Azure, SQL, FastAPI and Docker experience..."
    )

    if st.button(
        "Save Job Description"
    ):

        response = requests.post(
            f"{API_URL}/job-description",
            json={
                "description": jd
            }
        )

        if response.status_code == 200:

            st.success(
                "Job Description Saved Successfully"
            )

        else:

            st.error(
                "Failed to save Job Description"
            )

# ==========================
# UPLOAD RESUME
# ==========================

elif menu == "Upload Resume":

    st.header("📂 Upload Resume")

    uploaded_file = st.file_uploader(
        "Upload PDF or DOCX Resume",
        type=[
            "pdf",
            "docx"
        ]
    )

    if uploaded_file:

        if st.button(
            "Analyze Resume"
        ):

            with st.spinner(
                "Analyzing Resume..."
            ):

                files = {
                    "file": (
                        uploaded_file.name,
                        uploaded_file,
                        uploaded_file.type
                    )
                }

                response = requests.post(
                    f"{API_URL}/upload",
                    files=files
                )

                if response.status_code != 200:
                    st.error(
                        f"Backend Error ({response.status_code})"
                    )

                    st.text(response.text)
                    st.stop()

                try:
                    result = response.json()

                except Exception:
                    st.error("Backend did not return valid JSON")
                    st.text(response.text)
                    st.stop()

                st.success(
                    "Resume Processed Successfully"
                )

                st.subheader(
                    "Candidate Information"
                )

                st.write(
                    f"**Filename:** {result.get('filename', '')}"
                )

                st.write(
                    f"**Score:** {result.get('score', 0)}"
                )

                st.write(
                    f"**Recommendation:** {result.get('recommendation', '')}"
                )

                st.write(
                    f"**Blob URL:** {result.get('blob_url', '')}"
                )

                st.subheader(
                    "Skills"
                )

                st.write(
                    result.get(
                        "skills",
                        []
                    )
                )

                st.subheader(
                    "Strengths"
                )

                for strength in result.get(
                    "strengths",
                    []
                ):

                    st.success(
                        strength
                    )

                st.subheader(
                    "Weaknesses"
                )

                for weakness in result.get(
                    "weaknesses",
                    []
                ):

                    st.warning(
                        weakness
                    )

# ==========================
# RANKINGS
# ==========================

elif menu == "Rankings":

    st.header(
        "🏆 Candidate Rankings"
    )

    response = requests.get(
        f"{API_URL}/rankings"
    )

    data = response.json()

    if len(data) > 0:

        df = pd.DataFrame(data)

        df["score"] = pd.to_numeric(
            df["score"],
            errors="coerce"
        ).fillna(0)

        df = df.sort_values(
            by="score",
            ascending=False
        )

        st.dataframe(
            df,
            use_container_width=True
        )

    else:

        st.info(
            "No candidates found."
        )

# ==========================
# REPORTS
# ==========================

elif menu == "Reports":

    st.header(
        "📈 Summary Report"
    )

    response = requests.get(
        f"{API_URL}/report"
    )

    report_data = response.json()

    st.json(
        report_data
    )

    st.subheader(
        "Report Summary"
    )

    st.write(
        f"**Total Candidates:** "
        f"{report_data.get('total_candidates', 0)}"
    )

    st.write(
        f"**Top Candidate:** "
        f"{report_data.get('top_candidate', 'N/A')}"
    )

    st.write(
        f"**Highest Score:** "
        f"{report_data.get('highest_score', 0)}"
    )