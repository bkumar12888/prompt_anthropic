import boto3
import json
import logging

def generate_message( user_prompt):
    user_input=""
    with open("input.txt", "r") as f:
        for line in f:
            user_input=user_input+line
    
    prompt_template=f"""Below is the list of sentences.
                    tell me the second item on the list 
                    each is about an animal ,like rabbits.
                    <sentences>
                    {user_input} 
                    </sentences>"""
    final_prompt=prompt_template
    print(final_prompt)

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
                                "content": [{"type": "text", "text": final_prompt}],
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
    user_input = input("Enter the name of animal (or type 'exit' to quit): ")
    if user_input.lower() == "exit":
        break
    else:
        print("*" * 40)
        generate_message(user_input)


