from pipelines.query import ask_question

# Test dataset (simulate real enterprise queries)

test_cases = [
     {
        "question": "How many leave days do employees get?",
        "expected": "20 days"
    },
    {
        "question": "Can employees work remotely?",
        "expected": "3 days per week"
    },
    {
        "question": "How to reset password?",
        "expected": "it-support@company.com"
    }
]

def evaluate():
    correct = 0

    for test in test_cases:
        question = test["question"]
        expected = test["expected"]

        answer =  ask_question(question)
        print(f"Q: {question}")
        print(f"Expected: {expected}")
        print(f"Answer: {answer}")

        if expected.lower() in answer.lower():
            correct +=1
    
    accuracy = correct/ len(test_cases)
    print("\n======================")
    print(f"✅ Accuracy: {accuracy * 100:.2f}%")

if __name__ =="__main__":
    evaluate()