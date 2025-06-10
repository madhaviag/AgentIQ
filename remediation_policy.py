def remediation_policy(action, error, sla_breach):
    # Example: You can expand this logic or load from config/rules engine
    if error:
        return "Restart service or notify support team"
    if sla_breach:
        return "Scale resources or optimize workflow"
    return None