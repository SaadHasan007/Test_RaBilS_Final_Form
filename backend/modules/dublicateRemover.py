
# def detect_dublicates():
#     return

import numpy as np
from sentence_transformers import SentenceTransformer, util

embedding_model = SentenceTransformer('models/all-MiniLM-L6-v2')

def detect_dublicates(target_story, all_stories = []):

    if(not all_stories):
        notes= "no dublicates found"
        return {
        "type": "duplication",
        "detected": False,
        "confidence": 1,
        "details": {
            "similarity": 0,
            "matched_index": 0
        },
        "notes": notes
    }
    embeddings = embedding_model.encode(all_stories, convert_to_tensor=True)
    target_emb = embedding_model.encode(target_story, convert_to_tensor=True)

    similarities = util.cos_sim(target_emb, embeddings)[0].cpu().numpy()

    max_sim = float(np.max(similarities))
    index = int(np.argmax(similarities))

    detected = False
    notes = ""
    if(max_sim >= 0.75):
         detected = True
         confidence = 0.85
         notes = f"Pragmatic Ambiguity | Redundant UserStory Detected | Confidence :{confidence*100}%"

    return {
        "type": "duplication",
        "detected": detected,
        "confidence": 0.85 if max_sim >= 0.85 else 0.7 if detected else 0.2,
        "details": {
            "similarity": max_sim,
            "matched_index": index
        },
        "notes": notes
    }


# def remove_dublicates(testcase_ids,testcase_list):

#     #CODE TO CLEAR DUPLICATE FROM LIST
#     testcase_list = []

#     return testcase_list

