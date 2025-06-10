# AgentIQ – Transparency & Explainability in Agentic AI

This repository contains prototypes for **AgentIQ**, a next-generation framework focused on ensuring transparency, explainability, and auditability in agentic AI systems. The apps are built using [Streamlit](https://streamlit.io/) and demonstrate features such as agent action simulation, logging, explanations, audit dashboards, and human-in-the-loop feedback.

## Project Structure

- [`traceagent_app`](AgentIQ):  
  The main prototype app. Provides navigation for simulating agent actions, viewing logs, generating explanations, visualizing audit dashboards, and collecting feedback. Uses Streamlit session state to manage logs and feedback.

- `traceagent_dashboard.py`:  
  The interactive audit dashboard for AgentIQ, including performance metrics, error detection, SLA breach analysis, and export options (CSV, PDF).

- `pdf_utils.py`:  
  Utility for exporting filtered data to PDF.

- Other supporting modules for remediation policy, environment variables, and sample agent logic.

## Features

- **Agent Action Simulation:**  
  Simulate tasks such as document classification, risk scoring, fraud detection, and workflow automation.

- **Logging:**  
  View and manage logs of agent actions with timestamps, details, and confidence scores.

- **Explanations:**  
  Generate natural language justifications for agent decisions using LLMs.

- **Audit Dashboard:**  
  Visualize agent workflows, decision distributions, SLA breaches, and error metrics. Includes clickable links for remediation tickets (JIRA integration).

- **Data Export:**  
  Export filtered agent action data as CSV or PDF.

- **Human-in-the-Loop Feedback:**  
  Submit feedback to improve agent behavior and auditability.

## Deployment on Streamlit Cloud

To deploy this app on [Streamlit Cloud](https://streamlit.io/cloud):

1. Push your code (including `requirements.txt`) to a public GitHub repository.
2. Go to [Streamlit Cloud](https://streamlit.io/cloud) and sign in.
3. Click **"New app"** and connect your GitHub repo.
4. Set the main file path (e.g., `AgentIQ`).
5. Click **"Deploy"**.

Streamlit Cloud will automatically install dependencies from `requirements.txt` and launch your app.

## Getting Started

1. **Install dependencies:**
   ```sh
   pip install streamlit pandas matplotlib fpdf
   ```

2. **Run the main app:**
   ```sh
   streamlit run traceagent_app
   ```
  

## Notes

- These are prototype/demo apps using mock data for demonstration purposes.
- You can extend the apps to connect to real agentic AI systems or datasets.
- For PDF export, ensure you have the `fpdf` package installed.

## License

This project is provided for demonstration and prototyping purposes.