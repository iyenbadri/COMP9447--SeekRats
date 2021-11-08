
import boto3
import json
from modifyTables import allowlist_modifyTables

dynamodb = boto3.resource('dynamodb')


# /allowlist/get_list/{org_id}/{repo_id}:
def get_list(event, context):
    org_id = event['pathParameters']['org_id']
    repo_id = event['pathParameters']['repo_id']
    query_params = event["queryStringParameters"]

    try: 
        list_of_terms = None
        if "with_info" in query_params.keys():
            if query_params["with_info"]:
                list_of_terms = allowlist_modifyTables.read_repo_with_info(org_id, repo_id, dynamodb=dynamodb)
        if list_of_terms == None:
            list_of_terms = allowlist_modifyTables.read_repo(org_id, repo_id, dynamodb=dynamodb)
        
        return {
            'statusCode': 200,
            'description': "OK",
            'body': json.dumps(list_of_terms)
        }
    except Exception as e:
        if str(e)=="An error occurred (ResourceNotFoundException) when calling the Query operation: Cannot do operations on a non-existent table":
            return {
                'statusCode': 400,
                'description': "The organization id was not found"
            }
        elif str(e)=="ValueError: Repo has not been initialized":
            return {
                'statusCode': 401,
                'description': "The repo id was not correct"
            }
        elif str(e)=="An error occurred (ResourceNotFoundException) when calling the Query operation: Requested resource not found":
            return {
                'statusCode': 410,
                'description': "An unknown error occurred on DynamoDB. Please try again later"
            }
        else:
            return {
                'statusCode': 409,
                'description': "Bad Key"
            }