import boto3
import json
import logging

def generate_message( user_prompt):
   
    
    prompt_template=f"""Please classify this email into the following categories: {{user_input}}

Do not include any extra words except the category. Think step by step before you answer.

<categories>
(A) Pre-sale question
(B) Broken or defective item
(C) Billing question
(D) Other (please explain)
</categories>

Answer with only the letter of the answer wrapped in <answer> tags, such as <answer>B</answer>"""


    client = boto3.client(service_name="bedrock-runtime", region_name="us-west-2")
    #model_id = "anthropic.claude-3-sonnet-20240229-v1:0"
    model_id ="anthropic.claude-3-haiku-20240307-v1:0"

    try:
         response = client.invoke_model_with_response_stream(
                modelId=model_id,
                body=json.dumps(
                    {
                        "anthropic_version": "bedrock-2023-05-31",
                        "max_tokens": 1024,
                        "messages": [
                            {
                                "role": "user",
                                "content": [{"type": "text", "text": prompt_template}],
                            }
                        ],
                    }
                ),
            )

         for event in response.get("body"):
             chunk = json.loads(event["chunk"]["bytes"])
             if chunk['type'] == 'content_block_delta':
                 if chunk['delta']['type'] == 'text_delta':
                     print(chunk['delta']['text'], end="")


    except:
         print("Hello")
         raise

    print("\n")
    print("*"*40)

print("-" * 88)
print("Welcome to the genAI workshop")
print("-" * 88)

while True:
    user_input = input("Enter animals name (or type 'exit' to quit): ")
    if user_input.lower() == "exit":
        break
    else:
        print("*" * 40)
        generate_message(user_input)


