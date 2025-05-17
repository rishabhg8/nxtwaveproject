# INSTRUCTION: Create a file named ".env" in the backend directory and add your GroqCloud API key as:
# GROQCLOUD_API_KEY=your_actual_api_key_here

# INSTRUCTION: The GroqCloud chat completions endpoint is now https://api.groq.com/openai/v1/chat/completions

from dotenv import load_dotenv
import os
from groq import Groq
from typing import Dict

load_dotenv()

def build_prompt(user_data: dict) -> str:
    """
    Build the prompt for the LLM based on user data.
    """
    return f"""
    You are an expert career and salary advisor for IT students in India. Given the following user profile, generate a minimal report with:
    1. A concise summary of the user's input (education, experience, skills, interests, goal, companies, learning style, time commitment, constraints) in a minimal, readable format.
    2. A section titled 'Dream Job' that returns ONLY the most suitable job title (e.g., 'Full Stack Developer', 'Data Analyst', etc.) for the user based on their goal and background. Do NOT include any explanation or extra text.
    3. A section titled 'Salary Potential' that returns ONLY the median annual salary number (in INR, e.g., '1200000') for that job in India, based on their background and skillset. Do NOT include any currency symbol, explanation, or extra text.
    
    Format your response as:
    ---
    User Summary:
    <minimal summary here>
    
    Dream Job:
    <job title only>
    
    Salary Potential:
    <salary number only>
    ---
    
    User Profile:
    Education: {user_data['education']}
    Experience: {user_data['experience']}
    Technical Knowledge: {', '.join(user_data['tech_knowledge'])}
    Interests: {user_data['interests']}
    Career Goal: {user_data['goal']}
    Dream Companies/Industries: {user_data['companies']}
    Learning Style: {user_data['learning_style']}
    Time Commitment: {user_data['time_commitment']} hours/week
    Other Constraints: {user_data['other_constraints']}
    """

def get_llm_recommendation(user_data: dict) -> Dict[str, str]:
    """
    Calls GroqCloud LLM API with user data and returns the structured recommendation.
    Returns a dict with a 'report' key containing the LLM's reply or an error message.
    """
    api_key = os.getenv("GROQCLOUD_API_KEY")
    if not api_key:
        return {"report": "Error: GROQCLOUD_API_KEY not set in environment."}
    client = Groq(api_key=api_key)
    prompt = build_prompt(user_data)
    try:
        completion = client.chat.completions.create(
            model="meta-llama/llama-4-scout-17b-16e-instruct",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_completion_tokens=800,
            top_p=1,
            stream=False,
            stop=None,
        )
        llm_reply = completion.choices[0].message.content
        return {"report": llm_reply}
    except Exception as e:
        # More specific error handling for debugging and user feedback
        import traceback
        error_msg = f"Error communicating with GroqCloud API: {str(e)}\n{traceback.format_exc()}"
        return {"report": error_msg} 