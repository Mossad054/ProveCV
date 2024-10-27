import openai
import os

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
