import os
from openai import OpenAI

def get_gpt_response(input, old_resume):
    # Replace 'your-api-key' with your actual OpenAI API key
    api_key = os.getenv('OPENAI_API_KEY')

    if not api_key:
        raise ValueError("API key not found. Please set the OPENAI_API_KEY environment variable.")

    client = OpenAI(api_key=api_key)
    
    # input = "Build me a 2 page resume using this job description: " + input + " and this resume: " + old_resume + " and no header"
    input = "Modify my resume to match this job description: " + input + " and this resume: " + old_resume + " Do not add a header"
    # # Prompt the user for content
    # user_prompt = input("Enter your prompt: ")

    # Call the API with the user's prompt
    stream = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": input}],
        stream=True,
    )
    # Initialize an empty string to store the result
    result = ""

    # Collect the response from the API into the result variable
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            result += chunk.choices[0].delta.content

    # # Print the result
    # print("\nGPT-3 Response:")
    # print(result)
    return result