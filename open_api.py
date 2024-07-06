import os
from openai import OpenAI

def get_gpt_response(input, old_resume):
    api_key = os.getenv('OPENAI_API_KEY')

    if not api_key:
        raise ValueError("API key not found. Please set the OPENAI_API_KEY environment variable.")

    client = OpenAI(api_key=api_key)
    
    input = "Modify my resume to match this job description: " + input + " and this resume: " + old_resume + " Do not add a header"
  
    stream = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": input}],
        stream=True,
    )
    result = ""

    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            result += chunk.choices[0].delta.content

    return result