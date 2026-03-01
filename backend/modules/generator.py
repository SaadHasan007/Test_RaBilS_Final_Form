from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# Placeholder for the fine-tuned model path
# TODO: Update this path after training the model
MODEL_PATH = "t5-small" # Later: "./my_fine_tuned_model"

try:
    tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
    model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_PATH)
except Exception as e:
    print(f"Error loading model: {e}")
    tokenizer = None
    model = None

def generate_test_cases(user_story):
    """
    Generates Gherkin test cases from a User Story.
    Currently mocks the output until the fine-tuned model is ready.
    """
    
    # Mock output logic for Phase 1
    # In Phase 2/3, we will use:
    # inputs = tokenizer("generate test case: " + user_story, return_tensors="pt")
    # outputs = model.generate(inputs.input_ids, max_length=512)
    # return tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    mock_gherkin = f"""Feature: User Story Implementation

  Scenario: Successful execution of the user story
    Given the user is on the application page
    And the system is in a valid state
    When the user performs the action described as "{user_story[:20]}..."
    Then the system should respond correctly
    And the user goal should be achieved
"""
    return mock_gherkin
