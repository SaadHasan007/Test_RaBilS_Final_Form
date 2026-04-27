import json
import torch
from transformers import T5Tokenizer, T5ForConditionalGeneration, Trainer, TrainingArguments
from torch.utils.data import Dataset
 
# 1. Load Data
def load_data(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
    return data

class GherkinDataset(Dataset):
    def __init__(self, data, tokenizer, max_length=512):
        self.data = data
        self.tokenizer = tokenizer
        self.max_length = max_length

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        item = self.data[idx]
        input_text = "generate test case: " + item['input_text']
        target_text = item['target_text']

        input_encoding = self.tokenizer(
            input_text,
            max_length=self.max_length,
            padding="max_length",
            truncation=True,
            return_tensors="pt"
        )
        
        target_encoding = self.tokenizer(
            target_text,
            max_length=self.max_length,
            padding="max_length",
            truncation=True,
            return_tensors="pt"
        )

        labels = target_encoding.input_ids
        labels[labels == self.tokenizer.pad_token_id] = -100 # Ignore padding in loss calculation

        return {
            "input_ids": input_encoding.input_ids.flatten(),
            "attention_mask": input_encoding.attention_mask.flatten(),
            "labels": labels.flatten()
        }

# Main execution block
if __name__ == "__main__":
    # Configuration
    MODEL_NAME = "t5-small"
    OUTPUT_DIR = "./my_fine_tuned_model"
    DATA_FILE = "data.json" # Ensure this file exists before running

    print("Loading tokenizer and model...")
    tokenizer = T5Tokenizer.from_pretrained(MODEL_NAME)
    model = T5ForConditionalGeneration.from_pretrained(MODEL_NAME)

    print("Loading data...")
    try:
        raw_data = load_data(DATA_FILE)
        dataset = GherkinDataset(raw_data, tokenizer)
        
        # Split data (simple split for demo)
        train_size = int(0.8 * len(dataset))
        val_size = len(dataset) - train_size
        train_dataset, val_dataset = torch.utils.data.random_split(dataset, [train_size, val_size])

        training_args = TrainingArguments(
            output_dir=OUTPUT_DIR,
            num_train_epochs=3,
            per_device_train_batch_size=4,
            per_device_eval_batch_size=4,
            warmup_steps=500,
            weight_decay=0.01,
            logging_dir='./logs',
            logging_steps=10,
            evaluation_strategy="steps",
            save_strategy="steps",
            save_steps=500,
            load_best_model_at_end=True,
        )

        trainer = Trainer(
            model=model,
            args=training_args,
            train_dataset=train_dataset,
            eval_dataset=val_dataset,
        )

        print("Starting training...")
        trainer.train()

        print(f"Saving model to {OUTPUT_DIR}...")
        model.save_pretrained(OUTPUT_DIR)
        tokenizer.save_pretrained(OUTPUT_DIR)
        print("Training complete!")

    except FileNotFoundError:
        print(f"Error: {DATA_FILE} not found. Please run data_gen.py first.")
