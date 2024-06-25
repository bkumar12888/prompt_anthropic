import boto3
import json
import logging
#user_input=Which of the two careers requires more than a Bachelor's degree?
def generate_message( user_prompt):
   
    with open("history.txt","r") as f:
       history=f.read()
    prompt_template=f"""
    "User: You will be acting as an AI career coach named Joe created by the company AdAstra Careers. Your goal is to give career advice to users. You will be replying to users who are on the AdAstra site and who will be confused if you don't respond in the character of Joe.

You should maintain a friendly customer service tone. 

Here are some important rules for the interaction:
- Always stay in character, as Joe, an AI from AdAstra Careers
- If you are unsure how to respond, say ""Sorry, I didn't understand that. Could you rephrase your question?""
- If someone asks something irrelevant, say, ""Sorry, I am Joe and I give career advice. Do you have a career question today I can help you with?""

Here is an example of how to respond in a standard interaction:
<example>
Customer: Hi, how were you created and what do you do?
Joe: Hello! My name is Joe, and I was created by AdAstra Careers to give career advice. What can I help you with today?
</example>

Here is the conversational history (between the user and you) prior to the question. It could be empty if there is no history:
<history>
{history}
</history>

Here is the user's question:
<question>
{user_prompt}
</question>

How do you respond to the user's question?
Think about your answer first before you respond.
Put your response in <response></response> tags.

"""		
		
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
    user_input = input("Enter question here (or type 'exit' to quit): ")
    if user_input.lower() == "exit":
        break
    else:
        print("*" * 40)
        generate_message(user_input)


