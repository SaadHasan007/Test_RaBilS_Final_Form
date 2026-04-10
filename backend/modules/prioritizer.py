# def calculate_priority(test_case_text, user_story_text):
#     """
#     Calculates priority based on risk keywords and complexity of the test case.
#     Returns: "High", "Medium", or "Low"
#     """
    
#     # 1. Risk Analysis
#     high_risk_keywords = ["payment", "security", "database", "auth", "authentication", "login", "money", "transaction", "sensitive"]
    
#     risk_score = 0
#     combined_text = (test_case_text + " " + user_story_text).lower()
    
#     for keyword in high_risk_keywords:
#         if keyword in combined_text:
#             risk_score += 1
            
#     # 2. Complexity Analysis (Count steps in Gherkin)
#     # Assuming Gherkin steps start with Given, When, Then, And, But
#     steps = 0
#     lines = test_case_text.split('\n')
#     step_keywords = ["Given", "When", "Then", "And", "But"]
    
#     for line in lines:
#         stripped_line = line.strip()
#         for keyword in step_keywords:
#             if stripped_line.startswith(keyword):
#                 steps += 1
#                 break
    
#     # Decision Logic
#     if risk_score > 0:
#         return "High"
#     elif steps > 5:
#         return "Medium"
#     else:
#         return "Low"

#def calculate_priority(test_case_text, user_story_text):
def calculate_priority(user_story_text):

    return "high"
    """
    Calculates priority based on risk keywords and complexity of the test case.
    Returns: "High", "Medium", or "Low"
    
    Now supports structured test cases (list of dicts).
    """
    high_risk_keywords = [
        "payment", "security", "database", "auth", "authentication",
        "login", "money", "transaction", "sensitive"
    ]
    
    risk_score = 0
    
    # Convert list of test cases into a single string
    if isinstance(test_case_text, list):
        # Join all testCase + steps text into one string
        test_case_text_str = " ".join(
            tc.get("testCase", "") + " " + " ".join(tc.get("steps", []))
            for tc in test_case_text
        )
    else:
        # Fallback if it's still a string
        test_case_text_str = test_case_text
    
    combined_text = (test_case_text_str + " " + user_story_text).lower()
    
    # 1. Risk Analysis
    for keyword in high_risk_keywords:
        if keyword in combined_text:
            risk_score += 1
    
    # 2. Complexity Analysis (Count steps)
    steps = 0
    if isinstance(test_case_text, list):
        for tc in test_case_text:
            steps += len(tc.get("steps", []))
    else:
        # old string-based logic
        lines = test_case_text.split('\n')
        step_keywords = ["Given", "When", "Then", "And", "But"]
        for line in lines:
            stripped_line = line.strip()
            for keyword in step_keywords:
                if stripped_line.startswith(keyword):
                    steps += 1
                    break
    
    # 3. Decision Logic
    if risk_score > 0:
        return "High"
    elif steps > 5:
        return "Medium"
    else:
        return "Low"