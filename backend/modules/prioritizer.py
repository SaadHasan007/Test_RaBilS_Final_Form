def calculate_priority(test_case_text, user_story_text):
    """
    Calculates priority based on risk keywords and complexity of the test case.
    Returns: "High", "Medium", or "Low"
    """
    
    # 1. Risk Analysis
    high_risk_keywords = ["payment", "security", "database", "auth", "authentication", "login", "money", "transaction", "sensitive"]
    
    risk_score = 0
    combined_text = (test_case_text + " " + user_story_text).lower()
    
    for keyword in high_risk_keywords:
        if keyword in combined_text:
            risk_score += 1
            
    # 2. Complexity Analysis (Count steps in Gherkin)
    # Assuming Gherkin steps start with Given, When, Then, And, But
    steps = 0
    lines = test_case_text.split('\n')
    step_keywords = ["Given", "When", "Then", "And", "But"]
    
    for line in lines:
        stripped_line = line.strip()
        for keyword in step_keywords:
            if stripped_line.startswith(keyword):
                steps += 1
                break
    
    # Decision Logic
    if risk_score > 0:
        return "High"
    elif steps > 5:
        return "Medium"
    else:
        return "Low"
