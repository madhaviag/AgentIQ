import streamlit as st
import matplotlib.pyplot as plt
import webbrowser
import pandas as pd




def show_audit_dashboard(df):
    st.title("🕵️ Audit Dashboard")

    # Action filter
    action_filter = st.multiselect(
        "Filter by Agents Action",
        options=df["Action"].unique(),
        default=df["Action"].unique()
    )
    filtered_data = df[df["Action"].isin(action_filter)]

    # --- Export options at top right ---
    export_col1, export_col2, spacer = st.columns([8,1,1])
    with export_col2:
        st.write("")  # For alignment
        st.download_button(
            label="📥 Export as CSV",
            data=filtered_data.to_csv(index=False),
            file_name="filtered_data.csv",
            mime="text/csv",
            help="Download filtered data as CSV"
        )
    #with export_col2:
        # Export to PDF       

       # pdf_data = df_to_pdf(filtered_data)
       # st.download_button(
       #     label="⬇️ Export as PDF",
       #     data=pdf_data,
       #     file_name="filtered_data.pdf",
       #     mime="application/pdf"
       # )

    st.markdown("---")
    # Action frequency and distribution charts side by side
    if not filtered_data.empty:
        st.subheader("📊 Agent Action Metrics")
        chart_col1, chart_col2 = st.columns(2)

        with chart_col1:
            st.markdown("**Action Frequency**")
            st.bar_chart(filtered_data["Action"].value_counts())

        with chart_col2:
            st.markdown("**Action Distribution**")
            fig, ax = plt.subplots()
            decision_counts = filtered_data["Action"].value_counts()
            ax.pie(decision_counts, labels=decision_counts.index, autopct='%1.1f%%')
            ax.set_title("Action Distribution")
            st.pyplot(fig)

    st.markdown("---")

    # Key Metrics in table
    st.subheader("Performance Metrics")
    total_actions = len(filtered_data)
    avg_response = filtered_data["ResponseTime"].mean() if "ResponseTime" in filtered_data.columns else 0
    error_rate = filtered_data["Error"].mean() * 100 if "Error" in filtered_data.columns else 0

    metrics = {
        "**📝 Total Actions**": [total_actions],
        "**⏱️ Avg Response Time (s)**": [f"{avg_response:.2f}"],
        "**❌ Error Rate (%)**": [f"{error_rate:.1f}"],
    }
    if "SLA_Breach" in filtered_data.columns:
        sla_breach_count = filtered_data["SLA_Breach"].sum()
        sla_breach_rate = (sla_breach_count / len(filtered_data)) * 100 if len(filtered_data) > 0 else 0
        metrics["**🚨 SLA Breaches**"] = [int(sla_breach_count)]
        metrics["**⚡ SLA Breach Rate (%)**"] = [f"{sla_breach_rate:.1f}%"]

    metrics_df = pd.DataFrame(metrics).T
    metrics_df.columns = ["Value"]
    st.table(metrics_df)

    st.markdown("---")

    # Ethics & Alignment Checks
    st.subheader("🧭 Ethics & Alignment Checks")
    # Decision Explanations in expander
    if "Rationale" in filtered_data.columns:
        with st.expander("💡Agent Decision Explanations"):
            for idx, row in filtered_data.iterrows():
                st.info(
                    f"**🛠️ Action:** {row['Action']}  \n"
                    f"**📝 Rationale:** {row['Rationale']}  \n"
                    f"**📜 Policy:** {row.get('Policy', 'N/A')}"
                )

    if "Confidence" in filtered_data.columns:
        low_conf = filtered_data[filtered_data["Confidence"] < 0.8]
        if not low_conf.empty:
            st.warning(f"⚠️ {len(low_conf)} agent actions had low confidence (<0.8). Human Review recommended.")

    if "Error" in filtered_data.columns:
        repeated_errors = filtered_data[filtered_data["Error"]].groupby("Action").size()
        for action, count in repeated_errors.items():
            if count > 2:
                st.error(f"🔁 Action '{action}' had {count} errors. Possible feedback loop or misalignment.")

        error_count = filtered_data["Error"].sum()
        if error_count > 0:
            st.error(f"🚨 {int(error_count)} error(s) detected in agent actions!")
             # Create a DataFrame with a JIRA link for each error row
            error_rows = filtered_data[filtered_data["Error"] == True].copy()
            jira_base_url = (
                "https://jira.service.anz/secure/CreateIssueDetails!init.jspa"
                "?pid=84922"
                "&issuetype=20"
                "&summary=Agent%20Error%20Alert%20from%20AgentIQ"
                "&description=Error%20detected%20for%20action%20{action}%20at%20{timestamp}."
                "&labels=AgentIQ,AutoAlert"
            )
            # Add a column with the HTML link
            error_rows["Remediation Ticket"] = error_rows.apply(
               lambda row: f'<a href="{jira_base_url.format(action=row["Action"], timestamp=row["Timestamp"])}" target="_blank">Remediation Ticket</a>',
               axis=1
            )
            display_cols = ["Action", "Timestamp", "Details", "Remediation Ticket"]
            st.markdown("**Errors Detected:**")
            # Render as HTML table
            st.markdown(
                error_rows[display_cols].to_html(escape=False, index=False),
                unsafe_allow_html=True
            )

            # Also show the bulk JIRA button as before
            jira_url = (
                "https://jira.service.anz/secure/CreateIssueDetails!init.jspa"
                "?pid=84922"
                "&issuetype=20"
                "&summary=Agent%20Error%20Alert%20from%20AgentIQ"
                "&description=One%20or%20more%20agent%20actions%20have%20logged%20errors.%20"
                f"Error%20count%3A%20{int(error_count)}.%20Please%20review%20the%20audit%20dashboard%20for%20details."
                "&labels=AgentIQ,AutoAlert"
            )
            if st.button("🪧 Create JIRA Ticket for All Errors"):
                webbrowser.open_new_tab(jira_url)
           

    st.markdown("---")
    st.subheader("🧭 Self Healing and Remediation Actions")
    # Remediation Section in expander
    if "Remediation" in filtered_data.columns:
        pending = filtered_data[
            (filtered_data["Remediation"].notnull()) & (~filtered_data["Remediation_Executed"])
        ]
        if not pending.empty:
            with st.expander("🤖 Autonomous Remediation Proposals", expanded=True):
                for idx, row in pending.iterrows():
                    st.warning(
                        f"🛠️ Issue detected for action '{row['Action']}' at {row['Timestamp']}: {row['Remediation']}"
                    )
                    df.loc[idx, "Remediation_Executed"] = True
                    st.success(f"✅ Remediation executed: {row['Remediation']}")

    st.markdown("---")

    
