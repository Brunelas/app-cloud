import boto3
import uuid

# Configurando o DynamoDB
dynamodb = boto3.resource('dynamodb', region_name='us-east-2')
table = dynamodb.Table('MyDynamoDBTable')

def create_user(name):
    user_id = str(uuid.uuid4())
    table.put_item(Item={'id': user_id, 'name': name})
    return user_id

def get_user(user_id):
    response = table.get_item(Key={'id': user_id})
    return response.get('Item')

def update_user(user_id, name):
    table.update_item(
        Key={'id': user_id},
        UpdateExpression='SET #name = :val1',
        ExpressionAttributeNames={'#name': 'name'},
        ExpressionAttributeValues={':val1': name}
    )

def delete_user(user_id):
    table.delete_item(Key={'id': user_id})

def list_users():
    response = table.scan()
    return response['Items']
