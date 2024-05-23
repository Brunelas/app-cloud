from flask import Flask, render_template, request, redirect, url_for
import boto3
from boto3.dynamodb.conditions import Key
import uuid

app = Flask(__name__)

# Configurando o DynamoDB
dynamodb = boto3.resource('dynamodb', region_name='us-east-2')
table = dynamodb.Table('MyDynamoDBTable')

@app.route('/')
def index():
    response = table.scan()
    users = response['Items']
    return render_template('index.html', users=users)

@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        name = request.form['name']
        new_user = {'id': str(uuid.uuid4()), 'name': name}
        table.put_item(Item=new_user)
        return redirect(url_for('index'))
    return render_template('create.html')

@app.route('/update/<string:id>', methods=['GET', 'POST'])
def update(id):
    response = table.get_item(Key={'id': id})
    user = response.get('Item')
    if request.method == 'POST':
        name = request.form['name']
        table.update_item(
            Key={'id': id},
            UpdateExpression='SET #name = :val1',
            ExpressionAttributeNames={'#name': 'name'},
            ExpressionAttributeValues={':val1': name}
        )
        return redirect(url_for('index'))
    return render_template('update.html', user=user)

@app.route('/delete/<string:id>')
def delete(id):
    table.delete_item(Key={'id': id})
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)
