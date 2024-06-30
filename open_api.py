import os
from openai import OpenAI

# Replace 'your-api-key' with your actual OpenAI API key


# Prompt the user for content
user_prompt = input("Enter your prompt: ")

# Call the API with the user's prompt
stream = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": user_prompt}],
    stream=True,
)
# Initialize an empty string to store the result
result = ""

# Collect the response from the API into the result variable
for chunk in stream:
    if chunk.choices[0].delta.content is not None:
        result += chunk.choices[0].delta.content

# Print the result
print("\nGPT-3 Response:")
print(result)