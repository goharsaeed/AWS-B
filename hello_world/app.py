import boto3
import json
dynamodb = boto3.resource('dynamodb', endpoint_url='http://localhost:8000', region_name='us-east-1')
table = dynamodb.Table('phone-Data-table')

def lambda_handler(event, context):
    caller_number = event['CallerNumber']

    vanity_possibilities = generate_vanity_numbers(caller_number)

    save_vanity_numbers(caller_number, vanity_possibilities)

    last_5_callers_vanity = get_last_5_callers_vanity()
    print("Vanity numbers for last 5 callers:", last_5_callers_vanity)

    
    return {
        'statusCode': 200,
        'body': json.dumps('Vanity numbers saved to DynamoDB and displayed successfully')
    }

def generate_vanity_numbers(phone_number):
    digit_to_letter = {
        '2': 'ABC',
        '3': 'DEF',
        '4': 'GHI',
        '5': 'JKL',
        '6': 'MNO',
        '7': 'PQRS',
        '8': 'TUV',
        '9': 'WXYZ',
        '0': '0'  
    }

    vanity_numbers = []

    for digit in phone_number:
        letters = digit_to_letter.get(digit, '')  
        if letters:
            vanity_numbers.append(letters)  

    return vanity_numbers

def save_vanity_numbers(caller_number, vanity_possibilities):
    response = table.put_item(
        Item={
            'CallerNumber': caller_number,
            'VanityPossibilities': json.dumps(vanity_possibilities)
        }
    )
    print(response)

def get_last_5_callers_vanity():
    return ['vanity1', 'vanity2', 'vanity3', 'vanity4', 'vanity5']

if __name__ == '__main__':
    event_data = {
        'CallerNumber': '1234567890' 
    }
    lambda_handler(event_data, None)
