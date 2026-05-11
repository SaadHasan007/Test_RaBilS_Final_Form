import pickle

# load model 
with open("models/priority_model/randomForestRegressor_model.pkl", "rb") as f:
    model = pickle.load(f)
with open("models/priority_model/vectorizer.pkl", "rb") as f:
    vectorizer = pickle.load(f)



def predict_metrics(userStory):
        
        input = vectorizer.transform([userStory])
        prediction = model.predict(input)[0]

        return {
            "DefectCount": round(float(prediction[0]), 2),
            "DevelopmentTime": round(float(prediction[1]), 2),
            "StoryPoints": round(float(prediction[2]), 2),
            "CustomerSatisfaction": round(float(prediction[3]), 2)
        }

def calculate_story_priority(userStory):

    predicted_metrics=predict_metrics(userStory)
    """
    Calculate final priority score from predicted story metrics.

    Parameters
    ----------
    predicted_metrics : dict
        Output dictionary from predict_story_metrics()

    Returns
    -------
    dict
        Contains:
        - PriorityScore
        - PriorityLabel
    """

    # Extract values
    defect_count = predicted_metrics["DefectCount"]
    development_time = predicted_metrics["DevelopmentTime"]
    story_points = predicted_metrics["StoryPoints"]
    customer_satisfaction = predicted_metrics["CustomerSatisfaction"]

    # =========================
    # Normalize values
    # =========================

    # Adjust max values according to your dataset
    defect_norm = defect_count / 13
    development_norm = development_time / 9
    storypoints_norm = story_points / 13

    # Higher satisfaction means lower priority risk
    satisfaction_norm = 1 - (customer_satisfaction / 5)

    # Keep values inside 0-1 range
    defect_norm = min(max(defect_norm, 0), 1)
    development_norm = min(max(development_norm, 0), 1)
    storypoints_norm = min(max(storypoints_norm, 0), 1)
    satisfaction_norm = min(max(satisfaction_norm, 0), 1)

    # =========================
    # Weighted hybrid formula
    # =========================

    priority_score = (
        0.35 * defect_norm +
        0.25 * development_norm +
        0.25 * storypoints_norm +
        0.15 * satisfaction_norm
    )

    # Convert to percentage
    priority_percentage = round(priority_score * 100, 2)

    # =========================
    # Priority label
    # =========================

    if priority_percentage >= 55:
        label = "Very High"

    elif priority_percentage >= 45:
        label = "High"

    elif priority_percentage >= 40:
        label = "Medium"

    else:
        label = "Low"

    return {
        "PriorityScore": priority_percentage,
        "PriorityLabel": label
    }

def calculate_priority(user_story_text):
    result = calculate_story_priority(user_story_text)
    print(result)
    return result["PriorityLabel"]



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

