from functools import wraps
import inspect

from flask import request

"""
Modified version of https://github.com/fayebutler/flask_required_args/blob/master/flask_required_args/decorators.py to allow for a 
more customised error message.
"""

def required_data(f, message="Did not receive data for", expected_in='url'):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        """ Decorator that makes sure the view arguments are in the request json data, otherwise 400 error """

        expected_in_supp = ('url','data')
        if expected_in not in expected_in_supp:
            raise ValueError(f"The parameter 'expected_in' is not one of the supported values:{expected_in_supp}")

        sig = inspect.signature(f)
        data = request.get_json()

        for arg in sig.parameters.values():
            # Check if the argument is passed from the url
            if expected_in=='url' and arg.name in kwargs:
                continue
            # check if the argument is in the json data
            if expected_in=='data' and data and data.get(arg.name) is not None:
                kwargs[arg.name] = data.get(arg.name)
            # else check if it has been given a default
            elif arg.default is not arg.empty:
                kwargs[arg.name] = arg.default

        missing_args = [arg for arg in sig.parameters.keys() if arg not in kwargs.keys()]
        if missing_args:
            return '{}: {}'.format(message,', '.join(missing_args)), 400

        return f(*args, **kwargs)
    return decorated_function