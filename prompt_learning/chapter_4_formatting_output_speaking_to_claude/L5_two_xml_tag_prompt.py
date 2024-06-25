import boto3
import json
import logging

def generate_message( user_prompt1,user_prompt2 ):
   
    
    prompt_template=f"""please write atwo poems one about {user_input1} and one about {user_input2} . put each in <poem> tags """

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
    user_input1 = input("Enter first animal name (or type 'exit' to quit): ")
    print("*"*40)
    user_input2 = input("Enter second animal name (or type 'exit' to quit): ")
    if user_input1.lower() == "exit":
        break
    else:
        print("*" * 40)
        generate_message(user_input1,user_input2)


