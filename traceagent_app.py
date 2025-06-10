import streamlit as st
import pandas as pd
import random
from traceagent_dashboard import show_audit_dashboard
from remediation_policy import remediation_policy
from dotenv import load_dotenv
import os
import openai

# Load environment variables
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

# Initialize logs in session state if not present
if 'logs' not in st.session_state:
    st.session_state['logs'] = []

# App title and sidebar navigation
st.title("AgentIQ – Transparency & Explainability in Agentic AI")
st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Go to",
   # ["Home", "Agent Actions", "Logs", "Explanations", "Audit Dashboard", "Feedback"]
    ["Home", "Agent Actions", "Logs", "Audit Dashboard", "Feedback"]
)

# Home page
if page == "Home":
    st.header("Welcome to AgentIQ")
    st.write("""
        AgentIQ is an innovative agentic AI framework designed to ensure transparency and explainability in autonomous decision-making.
        It empowers multi-agent systems to perform complex tasks while maintaining a transparent, auditable trail of decisions and actions.
    """)

# Agent Actions page
elif page == "Agent Actions":
    st.header("Agent Actions")
    st.write("Simulate agentic tasks like document decision maker, risk scoring, and fraud detection.")

    actions = ["Release Artefacts Decision Maker", "Risk Scoring", "Fraud Detection"]
    action = st.selectbox("Select an action", actions)

    confidence = round(random.uniform(0.7, 1.0), 2)
    response_time = round(random.uniform(0.5, 2.5), 2)
    error = random.choice([False, False, False, True])
    sla_breach = response_time > 2.0
    explanation = "This action was chosen based on the agent's confidence level and response time."
    policy_name = "Default Remediation Policy"

    if st.button("Perform Action"):
        if error:
            remediation = "Restart service or notify support team"
        elif sla_breach:
            remediation = remediation_policy(action, error, sla_breach)
        else:
            remediation = None

        st.write(f"Agent performed: {action}")
        st.session_state['logs'].append({
            "Action": action,
            "Timestamp": pd.Timestamp.now(),
            "Details": f"Performed {action}",
            "Confidence": confidence,
            "ResponseTime": response_time,
            "Error": error,
            "SLA_Breach": sla_breach,
            "Remediation": remediation,
            "Remediation_Executed": False,
            "Rationale": explanation,
            "Policy": policy_name
        })

# Logs page
elif page == "Logs":
    st.header("Logs")
    st.write("View a table of agent actions with timestamps and details.")

    logs_df = pd.DataFrame(st.session_state['logs'])
    st.table(logs_df)

# Explanations page
#elif page == "Explanations":
 #   st.header("Explanations")
  #  st.write("Generate natural language justifications for agent decisions.")

   # if not openai_api_key:
    #    st.warning("OpenAI API key not found. Set the OPENAI_API_KEY environment variable.")
    #else:
     #   openai.api_key = openai_api_key
#        if st.button("Generate Explanations"):
 #           explanations = []
  #          for log in st.session_state['logs']:
   #             prompt = (
    #                f"Explain why an AI agent performed the following action:\n"
     #               f"Action: {log['Action']}\n"
      #              f"Timestamp: {log['Timestamp']}\n"
       #             f"Details: {log['Details']}\n"
        #            f"Confidence: {log['Confidence']}\n"
         #           f"Response Time: {log['ResponseTime']} seconds\n"
          #          f"Error: {log['Error']}\n"
           #         f"Provide a concise, clear explanation."
            #    )
             #   try:
              #      response = openai.chat.completions.create(
               #         model="gpt-3.5-turbo",
                #        messages=[
                 #           {"role": "system", "content": "You are an expert AI auditor."},
                  #          {"role": "user", "content": prompt}
                   #     ],
                    #    max_tokens=60,
                     #   temperature=0.5,
                    #)
                    #explanation = response.choices[0].message.content.strip()
                #except Exception as e:
                 #   explanation = f"Error generating explanation: {e}"
                #explanations.append(f"**{log['Action']}**: {explanation}")
            #st.markdown("\n\n".join(explanations))

# Audit Dashboard page
elif page == "Audit Dashboard":
    if st.session_state['logs']:
        df = pd.DataFrame(st.session_state['logs'])
        show_audit_dashboard(df)       
    else:
        st.info("No agent actions to display. Perform some actions first.")

# Feedback page
elif page == "Feedback":
    st.header("Human-in-the-Loop Feedback")
    st.write("Submit feedback to improve agent behavior.")

    feedback = st.text_area("Enter your feedback")
    if st.button("Submit Feedback"):
        st.write("Thank you for your feedback!")
        st.session_state['feedback'] = feedback
