import json
import os

# Placeholder for LLM API call
# You can use libraries like `google-generativeai` or `openai` here.
# For this script, I will simulate the generation process or provide the structure 
# where you can plug in your API key.

def generate_synthetic_data():
    """
    Generates synthetic User Story -> Gherkin pairs.
    In a real scenario, this would call an LLM API.
    """
    
    print("Generating synthetic data using LLM (Simulated)...")
    
    # Prompt that would be sent to the LLM:
    prompt = """
    Generate 50 diverse Agile User Stories and their corresponding Gherkin Test Cases.
    Format the output as a JSON list of objects with 'input_text' (User Story) and 'target_text' (Gherkin).
    """
    
    # Simulated response from LLM
    synthetic_data = [
        {
            "input_text": "As a user, I want to login with my email and password so that I can access my account.",
            "target_text": "Feature: User Login\n\n  Scenario: Successful Login\n    Given the user is on the login page\n    When the user enters valid email and password\n    And clicks the login button\n    Then the user should be redirected to the dashboard"
        },
        {
            "input_text": "As a shopper, I want to add items to my cart so that I can purchase them later.",
            "target_text": "Feature: Shopping Cart\n\n  Scenario: Add item to cart\n    Given the user is viewing a product\n    When the user clicks 'Add to Cart'\n    Then the item count in the cart should increase by 1"
        },
        # ... In a real run, this list would be populated by the LLM API response
    ]
    
    # Instructions for the user to actually use an API
    print("\nNOTE: This script currently uses a hardcoded sample.")
    print("To actually generate 50+ examples, you need to integrate an LLM SDK.")
    print("Example integration (commented out in code):")
    
    # Example Gemini Integration (Conceptual)
    # import google.generativeai as genai
    # genai.configure(api_key="YOUR_API_KEY")
    # model = genai.GenerativeModel('gemini-pro')
    # response = model.generate_content(prompt)
    # synthetic_data = json.loads(response.text)
    
    return synthetic_data

if __name__ == "__main__":
    data = generate_synthetic_data()
    
    output_file = "data.json"
    with open(output_file, "w") as f:
        json.dump(data, f, indent=4)
        
    print(f"Data saved to {output_file}")
