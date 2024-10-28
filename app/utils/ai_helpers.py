import openai
import os
import json

# Set your OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")  # Ensure you set this environment variable

def suggest_improvements(resume_content):
    """Use OpenAI GPT to suggest improvements for the given resume content."""
    prompt = (
        f"Please provide suggestions to improve the following resume content:\n\n{resume_content}\n\n"
        "List specific improvements, such as wording changes, formatting tips, or additional sections to include."
    )

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",  # You can change to the model you prefer
            messages=[{"role": "user", "content": prompt}],
            max_tokens=150  # Adjust as needed for longer suggestions
        )
        suggestions = response.choices[0].message['content']
        return suggestions.strip()  # Return the suggestions
    except Exception as e:
        print(f"Error while contacting OpenAI API: {e}")
        return "Could not generate suggestions at this time."

def optimize_for_job(content, job_description):
    """Optimize resume content based on job description."""
    prompt = f"""
    Job Description: {job_description}
    
    Current Resume Content: {content}
    
    Please optimize this resume content to better match the job description while maintaining honesty and accuracy.
    Focus on relevant skills and experiences, and suggest improvements in ATS-friendly format.
    """
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an expert ATS resume optimizer."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500
        )
        return response.choices[0].message['content']
    except Exception as e:
        print(f"Error in AI optimization: {e}")
        return content

def parse_uploaded_resume(text_content):
    """Parse uploaded resume content using AI."""
    prompt = f"""
    Parse the following resume content into structured sections:
    {text_content}
    
    Please return a JSON structure with these sections:
    - professional_summary
    - experience
    - education
    - skills
    """
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an expert resume parser."},
                {"role": "user", "content": prompt}
            ]
        )
        return json.loads(response.choices[0].message['content'])
    except:
        return None
