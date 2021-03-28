from flask import Response, jsonify

def to_resp(output, code:int) -> Response:
    resp = jsonify(output)
    resp.status_code = code
    return resp

def invalid_route() -> Response:
    code = 404
    output = {"error":
              {"msg": f"{code} error: This route is currently not supported. See API documentation."}
              }
    return to_resp(output, code)

def not_found(endpoint:str, identifier:str, additional_message='') -> Response:
    code = 404
    output = {"error":
              {"msg": f"{code} error: Resource with identifier '{identifier}' not found for endpoint {endpoint}. {additional_message}"}
              }
    return to_resp(output, code)


def resource_exists(endpoint:str, identifier:str, additional_message='') -> Response:
    code = 409
    output = {"error":
              {"msg": f"{code} error: Resource with identifier '{identifier}' already exists for endpoint {endpoint}. {additional_message}"}
              }
    return to_resp(output, code)

def bad_request(endpoint:str, additional_message='') -> Response:
    code = 400
    output = {"error":
              {"msg": f"{code} error: Bad requed request for endpoint '{endpoint}'. {additional_message}"}
              }
    return to_resp(output, code)

def resource_success(collection, name, verb, code=200) -> Response:
    output = f"Successfully {verb} resource '{name}'. Collection affected: {collection}"
    return to_resp(output, code)
