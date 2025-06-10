import openai

openai.api_key = "YOUR_API_KEY"

def generate_description(product_info: str) -> str:
    messages = [
        {"role": "user", "content": product_info}
    ]
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    return completion.choices[0].message.content

