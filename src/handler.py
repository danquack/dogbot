from json import dumps
from os import environ
from ast import literal_eval
from dog import get_rand_img, get_breed_img, get_breed_list


def index(event, context):
    return {
            "statusCode": 301,
            "headers": {
                "Location": "//" + environ['domain'] + "/random?image=true",
                "Cache-Control": "max-age=0"
            }
    }
    

def random(event, context):
    query_params = event.get('queryStringParameters', {})
    image = query_params.get('image', 'false').lower() if query_params else 'false'
    
    dog = get_rand_img()
    if dog:
        return respond(
            return_image=literal_eval(image.capitalize()),
            response=dog
        )
    else:
        return random(event, context)

def breed(event, context):
    response = get_rand_img()
    breed = event['pathParameters']['breed']
    query_params = event.get('queryStringParameters', {})
    image = query_params.get('image', 'false').lower() if query_params else 'false'
    
    dog = get_breed_img(breed)
    if breed:
        return respond(
            return_image=literal_eval(image.capitalize()),
            response=dog
        )
    else:
        return {
            "statusCode": 400,
            "body": "not a valid breed"
        } 

def breeds(event, context):
    return {
        "statusCode": 200,
        "body": dumps({"breeds": get_breed_list()})
    }

def respond(response, return_image):
    if return_image :
        return {
            "statusCode": 302,
            "headers": {
                "Location": response,
                "Cache-Control": "max-age=0"
            }
        }

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
            "Accept": "application/json"
        },
        "body": dumps({
            "url": response
        })
    }
        

    return response