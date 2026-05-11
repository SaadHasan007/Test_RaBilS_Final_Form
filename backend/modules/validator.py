import re
import spacy
from nltk.corpus import wordnet as wn ,stopwords
import numpy as np
import torch
from sentence_transformers import SentenceTransformer, util
import pickle
from modules.nlp import parse_user_story

# rule based ambiguity detection using framework suggested in research papers
nlp = spacy.load("en_core_web_sm") #English nlp model
embedding_model = SentenceTransformer('models/all-MiniLM-L6-v2') #pre-trained AI model that understands sentence meaning
dataset_embeddings = torch.load("models/userstory_dataset_embeddings.pt") # Embed all stories (text,text,..) to [[0.3 ,0.34, 0.67],[0.3 ,0.34, 0.67]..]

VAGUE_WORDS = [
    "fast", "efficient", "secure", "easy",
    "good", "better", "bad",
    "many", "some", "several",
    "user-friendly", "appropriate", "quick"
]
SAFE_WORDS = {
    "user", "system", "dashboard", "data", "account",
    "login", "logout", "access", "track","delivery"
}


STOPWORDS = set(stopwords.words('english'))

def is_polysemous(userStory):
    doc = nlp(userStory.lower())

    poly_words = []

    for token in doc:
        word = token.text

        # Skip stopwords
        if word in STOPWORDS:
            continue

        # Skip safe words
        if word in SAFE_WORDS:
            continue

        # Only important POS
        if token.pos_ not in ["NOUN", "VERB", "ADJ"]:
            continue

        synsets = wn.synsets(word)

        # Strict threshold
        if len(synsets) >= 3:
            poly_words.append(word)

    return poly_words
def detect_missing_structure(userStory):
    issues = []

    # Pattern checks
    as_actor = re.search(r"\bas (a|an|the)\b", userStory, re.IGNORECASE)
    i_want = re.search(r"\bi want\b", userStory,re.IGNORECASE)
    so_that = re.search(r"\bso that\b", userStory, re.IGNORECASE)
    has_comma_after_actor = bool(re.search(r"\bas\s+(a|an|the)\s+[^,]+,\s*", userStory, re.IGNORECASE))
    ends_with_full_stop = userStory.strip().endswith(".")

    if not as_actor:
        issues.append("Missing 'As a' section")

    if not i_want:
        issues.append("Missing 'I want' section")

    if not so_that:
        issues.append("Missing 'So that' section")
        
    if not has_comma_after_actor:
        issues.append("Missing 'Comma'  after actor section")

    if not ends_with_full_stop:
        issues.append("Missing 'full stop' at end")
    return {
        "missing_structure": len(issues) > 0,
        "issues": issues
    }
def detect_grammar_issues(userStory):
    doc = nlp(userStory)
    issues = []

    has_verb = any(token.dep_ == "ROOT" and token.pos_ == "VERB" for token in doc)
    has_subject = any(token.dep_ in ["nsubj", "nsubjpass"] for token in doc)
    has_object = any(token.dep_ in ["dobj", "pobj"] for token in doc)

    if not has_verb:
        issues.append("Missing main verb")

    if not has_subject:
        issues.append("Missing subject")

    if not has_object:
        issues.append("Missing object or target")

    if len(doc) < 5:
        issues.append("Sentence too short")

    return {
        "grammar_issues": len(issues) > 0,
        "issues": issues
    }

# level 1 : Lexical Level
def detect_vagueness(userStory):
    result = parse_user_story(userStory)
    goal = result["goal"] or " "
    benefit = result["benefit"] or " "
    words = goal +" "+ benefit
    words = words.lower().split()


    vague_found = [w for w in words if w in VAGUE_WORDS]
    poly_found = [w for w in words if is_polysemous(w)]

    detected = len(vague_found) > 0 or len(poly_found) > 0
    notes = ""
    # Confidence logic
    if vague_found and not poly_found:
        confidence = 0.95
        notes = f"Vague word(s) found: {vague_found} | Confidence :{confidence*100}%"
    elif poly_found and not vague_found:
        confidence = 0.55
        notes = f"Vague word(s) found: {poly_found} | Confidence :{confidence*100}%"
    elif vague_found and poly_found:
        confidence = 0.99
        notes = f"Vague word(s) found: {vague_found} {poly_found} | Confidence :{confidence*100}%"
    else:
        confidence = 0.00
        notes = ""

    return {
        "type": "vagueness",
        "detected": detected,
        "confidence": confidence,
        "details": {
            "vague_words": vague_found,
            "polysemous_words": poly_found
        },
        "notes" : notes
    }
# level 2 : Syntactic Level
def syntactic_inconsistency_detector(userStory):
    structure = detect_missing_structure(userStory)
    grammar = detect_grammar_issues(userStory)

    notes = ""
    if(structure["missing_structure"]):
        s_confidence = 0.99
        notes = f"Syntactic Ambiguity | Syntax error(s) found in UserStory | Confidence :{s_confidence*100}%"
    if(grammar["grammar_issues"]):
        g_confidence  = 0.80
        notes = f"Syntactic Ambiguity | Grammer issues(s) found in UserStory | Confidence :{g_confidence*100}%"

    detected = structure["missing_structure"] or grammar["grammar_issues"]
    return {
        "type": "syntax",
        "detected": detected,
        "confidence": 0.8 if detected else 0.0,
        "details": {
            "structure": structure,
            "grammar": grammar
        },
        "notes": notes 
    }
# level 3 : Semantic Level
def detect_insufficiency(target_story, threshold=0.35):
    target_emb = embedding_model.encode(target_story, convert_to_tensor=True)
    similarities = util.cos_sim(target_emb, dataset_embeddings)[0].cpu().numpy()

    max_sim = float(np.max(similarities))
    detected = False
    confidence = 0.3
    notes = ""
    if(max_sim < threshold):
        detected = True
        confidence = 0.75
        notes = f"Semantic Ambiguity | UserStory is out of context | Confidence :{confidence*100}%"

    return {
        "type": "insufficiency",
        "detected": detected,
        "confidence": confidence,
        "details": {
            "max_similarity": max_sim
        },
        "notes" : notes
    }
# level 4 : Pragmatic Level
def detect_duplication(target_story, all_stories):
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
# fusion level
def rule_based_ambiguity_detection(target_story, all_stories=[]):
    notes = []
    results = [
        detect_vagueness(target_story),
        syntactic_inconsistency_detector(target_story),
        detect_insufficiency(target_story)
    ]

    if all_stories:
        results.append(detect_duplication(target_story, all_stories))
    for r in results:
        notes.append(r["notes"])

    return {
        "type": "rule_based",
        "confidence": 0.8,
        "results": results,
        "notes" : notes
    }





# ML based ambuguity detection----------------

# Load model and vectorizer
with open("models/logistic_regression_model_ambiguty_detection/model.pkl", "rb") as f:
    model = pickle.load(f)
with open("models/logistic_regression_model_ambiguty_detection/vectorizer.pkl", "rb") as f:
    vectorizer = pickle.load(f)
    
label_columns = [
    "ActorAmbiguity",
    "SemanticAmbiguity",
    "ScopeAmbiguity",
    "AcceptanceAmbiguity",
    "DependencyAmbiguity",
    "PriorityAmbiguity"
]

#prediction using logistic regression
def ml_based_ambiguity_prediction(userStory):
    vec = vectorizer.transform([userStory.lower()])
    probs = model.predict_proba(vec)

    threshold = 0.3

    predictions = {
        label: int(p[0][1] > threshold)
        for label, p in zip(label_columns, probs)
    }

    detected = any(predictions.values())

    return {
        "type": "ml_based",
        "detected": detected,
        "confidence": 0.65 if detected else 0.3,
        "details": predictions
    }

#fusion layer, combine all report
def generate_final_ambiguity_report(userStory, all_stories=[]):

    rule_report = rule_based_ambiguity_detection(userStory, all_stories)
    ml_report = ml_based_ambiguity_prediction(userStory)

    # Combine detections
    combined_detected = (
        any(r["detected"] for r in rule_report["results"]) 
        or ml_report["detected"]
    )

    # Weighted confidence
    final_confidence = (
        0.6 * rule_report["confidence"] +
        0.4 * ml_report["confidence"]
    )

    return {
        "user_story": userStory,
        "ambiguity_detected": combined_detected,
        "confidence": round(final_confidence, 2),
        "analysis": {
            "rule_based": rule_report,
            "ml_based": ml_report
        }
    }



#remove code below, it was for testing only
def print_ambiguity_report(report):
    print("\n" + "="*60)
    print("USER STORY:")
    print(report["user_story"])
    print("="*60)

    print(f"\nAmbiguity Detected: {report['ambiguity_detected']}")
    print(f"Overall Confidence: {report['confidence']}")
    print("-"*60)

    # 🔵 RULE-BASED
    print("\n[ RULE-BASED ANALYSIS ]")
    rb = report["analysis"]["rule_based"]

    for r in rb["results"]:
        print(f"\n→ Type: {r['type']}")
        print(f"  Detected: {r['detected']}")
        print(f"  Confidence: {r['confidence']}")

        # Details (dynamic)
        for key, value in r["details"].items():
            print(f"  {key}: {value}")

    print("-"*60)

    # 🟣 ML-BASED
    print("\n[ ML-BASED ANALYSIS ]")
    ml = report["analysis"]["ml_based"]

    print(f"Detected: {ml['detected']}")
    print(f"Confidence: {ml['confidence']}")

    print("\nPredicted Ambiguities:")
    for key, value in ml["details"].items():
        print(f"  {key}: {value}")

    print("="*60 + "\n")

# ts="As a user, I would like to access dashboard to track delivery."
# ats=["As a store owner, I need to track order so that I have better find desired items",
#      "As a user, I want to open dashboard to track delivery.",
#      "As a seller, I want to handle orders so that I can complete purchase"]
# print_ambiguity_report(generate_final_ambiguity_report(ts,ats))


#----------------------------------------------------------------------------------------------------------

