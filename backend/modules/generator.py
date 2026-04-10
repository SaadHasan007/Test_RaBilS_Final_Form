from transformers import T5Tokenizer, T5ForConditionalGeneration
import torch 
from . import nlp

MODEL_PATH = "./models" 

try:
    tokenizer = T5Tokenizer.from_pretrained(MODEL_PATH)
    model = T5ForConditionalGeneration.from_pretrained(MODEL_PATH)

except Exception as e:
    print(f"Error loading model: {e}")
    tokenizer = None
    model = None

def generate_ac(user_story):

    input_text = "convert user story to acceptance criteria: " + user_story

    inputs = tokenizer(
        input_text,
        return_tensors="pt",
        truncation=True,
        padding=True,
        max_length=128
    )

    with torch.no_grad():
        outputs = model.generate(
            inputs["input_ids"],
            max_length=128,
            num_beams=4,
            early_stopping=True
        )

    result = tokenizer.decode(outputs[0], skip_special_tokens=True)

    return result


def generate_test_cases(user_story): 
    ac = generate_ac(user_story)
    result= [user_story,ac]
    return nlp.nlp_processor(result)
    
