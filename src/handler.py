from json import dumps
from ast import literal_eval
from dog import get_rand_img, get_breed_img, breed_list

def random(event, context):
    query_params = event.get('queryStringParameters', {})
    image = query_params.get('image', 'false').lower() if query_params else 'false'
    return respond(
        return_image=literal_eval(image.capitalize()),
        response=get_rand_img()
    )

def breed(event, context):
    response = get_rand_img()
    breed = event['pathParameters']['breed']
    query_params = event.get('queryStringParameters', {})
    image = query_params.get('image', 'false').lower() if query_params else 'false'
    
    breed = get_breed_img(breed)
    if breed:
        return respond(
            return_image=literal_eval(image.capitalize()),
            response=breed
        )
    else:
        return {
            "statusCode": 400,
            "body": "not a valid breed"
        } 

def breeds(event, context):
    return {
        "statusCode": 200,
        "body": dumps({"breeds": breed_list})
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