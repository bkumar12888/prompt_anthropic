import boto3
import json
import logging

def generate_message( user_prompt):
   
    
    prompt_template=f"""Please classify emails into the following categories, and do not include explanations: 
<categories>
(A) Pre-sale question
(B) Broken or defective item
(C) Billing question
(D) Other (please explain)
</categories>

Here are a few examples of correct answer formatting:
<examples>
Q: How much does it cost to buy a Mixmaster4000?
A: The correct category is: A

Q: My Mixmaster won't turn on.
A: The correct category is: B

Q: Please remove me from your mailing list.
A: The correct category is: D
</examples>

Here is the email for you to categorize: {user_prompt}
"""
    assistance_template=f"""The correct category is:"""

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
                            
                              { "role": "user","content":prompt_template},
                            
                              { "role": "assistant","content":assistance_template}, 
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


