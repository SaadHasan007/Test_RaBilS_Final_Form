import re

#main list of all the test cases 

#counter used to generate IDs 
req_id_count= 0
test_id_count= 0

#extract entities from userstory 
def parse_user_story(user_story):
    us = clean_text(user_story)
    result = {"actor" : extract_actor(us),
              "goal" : extract_goal(us),
              "benefit" : extract_benefit(us)}
    return result

#extract entities from acceptance_criteria
def parse_acceptance_criteria(acceptance_criteria):

    cases = str(acceptance_criteria).split("|")
    result = []
    for case in cases:
        case = clean_text(case)
        pattern = r"Given\s+(.*?)\s+when\s+(.*?)\s+then\s+(.*)"
        match = re.search(pattern, case, re.IGNORECASE)

        if match:
            result.append({
                "given" : match.group(1).strip(),
                "when" : match.group(2).strip(),
                "then" : match.group(3).strip()
            })
            
    return result

#generate requirement id
def get_req_id():
    global req_id_count
    req_id_count = req_id_count+1
    id= "REQ-00"+str(req_id_count)
    return id

#generate test case id
def get_test_id():
    global test_id_count
    test_id_count = test_id_count+1
    id= "TC-00"+str(test_id_count)
    return id

#reset id counter values to 0 
def reset_ids():
    global req_id_count
    req_id_count=0
    global test_id_count
    test_id_count=0

#remove extra spaces from given text
def clean_text(text):
    text = str(text) #convert text to string 
    text = text.strip() # remove space from start and end of the sentence 
    text = re.sub(r'\s+',' ', text) # remove extra spaces from with in the sentence
    return text

def extract_actor(story):

    match = re.search(r"As\s+(?:a|an|the)\s+(.*?)(?:,|\s+I\s+want)", story, re.IGNORECASE)

    if match:
        return match.group(1).strip()

    return None    

def extract_goal(story):

    #extract goal 
    match = re.search(r"I want\s+(.*?)(?:,| so that)", story, re.IGNORECASE) 

    if match:
        goal = match.group(1).strip()
        #remove helping words
        goal = re.sub(r"^(to|a|an|the|my)\s+","", goal, flags=re.IGNORECASE)

        return goal

    return None

def extract_benefit(text):
    #extract text after "so that"
    match = re.search(r"so that\s+(.*)", text, re.IGNORECASE)
    if match:
        return match.group(1).strip()
    return None

#combine everything in required format to send it to fornt end
def nlp_processor(us,ac,priority):
    user_story = us
    acceptance_criteria = ac

    result1 = parse_user_story(user_story)
    result2 = parse_acceptance_criteria(acceptance_criteria) 

    req_id =get_req_id()

    testcase =[{ 
        "testCaseId": get_test_id(),
        "requirementId": req_id,
        "testCase": result1["goal"],
        "precondition": result2[0]["given"],
        "steps": [
        result2[0]["when"]
        ],
        "expectedResult": result2[0]["then"],
        "priority": priority 
    },
    {"testCaseId": get_test_id(),
        "requirementId": req_id,
        "testCase": result1["goal"],
        "precondition": result2[1]["given"],
        "steps": [
        result2[1]["when"],
        "...",
        "work in progess in nlp module nlp_Processor"
        ],
        "expectedResult": result2[1]["then"],
        "priority": priority
    }
    ]
    return testcase