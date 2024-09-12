import requests

def answer_question(question):
    url = "http://localhost:11434/api/generate"
    
    payload = {
        "model": "gemma2:2b",
        "prompt": question,
        "stream": False
    }
    
    response = requests.post(url, json=payload)
    
    if response.status_code == 200:
        return response.json()['response']
    else:
        return "Sorry, I couldn't generate an answer."
    
if __name__ == "__main__":
    answer = answer_question('Hello, what are you?')
    print(answer)