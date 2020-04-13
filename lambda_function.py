#from __future__ import print_function

import boto3
import json

#print('Loading function')


def lambda_handler(event, context):
    '''Provide an event that contains the following keys:

      - operation: one of the operations in the operations dict below
      - tableName: required for operations that interact with DynamoDB
      - payload: a parameter to pass to the operation being performed
    '''
    #print("Received event: " + json.dumps(event, indent=2))
    operation = event['operation']

    if 'tableName' in event:
        dynamo = boto3.resource('dynamodb').Table(event['tableName'])

    operations = {
        'create': lambda x: dynamo.put_item(**x),
        'read': lambda x: dynamo.scan(**x),
        'update': lambda x: dynamo.update_item(**x),
        'delete': lambda x: dynamo.delete_item(**x),
        
    }

    if operation in operations:
        output =  operations[operation](event.get('payload'))
        try:
            return output["Items"]
        except KeyError:
            return 'No output for this action to display here'
            
    else:
        return {
            'statusCode': 400
        }
        raise ValueError('Unrecognized operation "{}"'.format(operation))