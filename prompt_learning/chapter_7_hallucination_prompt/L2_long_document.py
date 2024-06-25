import boto3
import json
import logging

def generate_message():
   
    with open('doc.txt') as f:
        doc=f.read()
     
    prompt_template=f"""<question>What was Matterport's subscriber base on the precise date of May 31, 2020?</question>
    Please read the below document. Then, in <scratchpad> tags, pull the most relevant quote from the document and consider whether it answers the user's question or whether it lacks sufficient detail. Then write a brief numerical answer in <answer> tags.

   <document>
   {doc}
   </document
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


if __name__ == '__main__':
    generate_message()


