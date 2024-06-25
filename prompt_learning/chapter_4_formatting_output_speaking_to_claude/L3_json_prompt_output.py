import boto3
import json
import logging

def generate_message( user_prompt):
    
    prompt_template=f"""please write a poem about {user_input} . use JSON format with the keys as "first_line","second_line",and "third_line" """
     
    client = boto3.client(service_name="bedrock-runtime", region_name="us-west-2")
    model_id = "anthropic.claude-3-sonnet-20240229-v1:0"
    #model_id ="anthropic.claude-3-haiku-20240307-v1:0"

    try:
         response = client.invoke_model_with_response_stream(
                modelId=model_id,
                body=json.dumps(
                    {
                        "anthropic_version": "bedrock-2023-05-31",
                        "max_tokens": 1024,
                        "messages": [
                        {"role": "user", "content": prompt_template},
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


