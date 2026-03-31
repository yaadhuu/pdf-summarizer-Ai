from groq import Groq
from dotenv import load_dotenv
import os

# load the .env file
load_dotenv()

# connect to Groq using API key from .env file
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def get_answer(question: str, relevant_chunks: list, mode: str = "chat") -> str:
    
    # join all chunks into one big text
    context = "\n\n".join(relevant_chunks)
    
    if mode == "chat":
        prompt = f"""You are a helpful study assistant. 
Use ONLY the context below to answer the question.
If the answer is not in the context, say 'I could not find that in the document.'

Context:
{context}

Question: {question}

Answer:"""

    elif mode == "quiz":
        prompt = f"""Generate exactly 5 multiple choice questions with 4 options each based on the context.
You MUST format your entire response exactly like the template below. Do not add any conversational text.

Q1: [Question text]
A) [Option A]
B) [Option B]
C) [Option C]
D) [Option D]
ANSWER: [Correct Option Letter]
EXPLANATION: [Brief explanation]

Q2: [Question text]
... and so on up to Q5.

Context:
{context}

Response:"""

    elif mode == "summary":
        prompt = f"""You are a study assistant.
Summarize the following content in clear bullet points.
Keep it simple and easy to understand.

Content:
{context}

Summary:"""

    elif mode == "eli5":
        prompt = f"""You are a teacher explaining to a student for the first time.
Explain the following content in very simple language like the student is hearing it for the first time.

Content:
{context}

Simple Explanation:"""

    else:
        prompt = f"Answer this question: {question}\n\nContext: {context}"

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=1024
    )
    
    return response.choices[0].message.content