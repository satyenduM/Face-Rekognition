import boto3
import json

def call_lambda_function(function_name, payload):
    client = boto3.client('lambda')
    try:
        response = client.invoke(
            FunctionName=function_name,
            InvocationType='RequestResponse',
            Payload=json.dumps(payload)
        )
        response_payload = json.loads(response['Payload'].read().decode('utf-8'))
        
        if 'body' in response_payload:
            body = response_payload['body']
            if isinstance(body, str):
                body = json.loads(body)
            if 'presignedUrl' in body:
                return body['presignedUrl']
        
        return response_payload
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
