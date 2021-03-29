from schema import Schema, And, Use, Optional, SchemaError
from flask import request
from .status_responses import bad_request
from functools import wraps
from typing import Callable

#Prevent redundancy and improve readibility
str_lower_strip = str, Use(str.lower), Use(str.strip)


supported_metrics = ('g','ml')
def metric_is_supported(metric:str) -> bool: 
   return metric in supported_metrics

IngredientsSchema = Schema([{'name': And(*str_lower_strip),
                             'amount': Use(int),
                             'metric': And(*str_lower_strip, metric_is_supported,
                                           error=f"'ingredients' key 'metric' value '{{}}' should be one of the following strings: {supported_metrics}")}])
                                           
CreateRecipeSchema = Schema({'name': And(*str_lower_strip),
                             'ingredients': IngredientsSchema,
                              Optional('steps'): {Use(int):str}})

EditRecipeSchema = Schema({'name': And(*str_lower_strip),
                           Optional('ingredients'): IngredientsSchema,
                           Optional('steps'): {Use(int):str}})

def validate_schema(schema:Schema) -> Callable:
   def func_wrapper(f:Callable) -> Callable:
      @wraps(f)
      def wrapper(*args, **kwargs) -> Callable:
         try:
            schema.validate(request.json)

            # The following validations/transformations could not be expressed using the schema library
            if 'ingredients' in request.json:
               # Validate length of ingredients is not 0
               if len(request.json['ingredients'])==0:
                  raise SchemaError('The number of ingredients can not be 0.')
               # Cast ingredients into a string after validating
               request.json['ingredients'] = str(request.json['ingredients'])


         except SchemaError as e:
            return bad_request(request.path, additional_message=("The JSON data sent does not conform to the expected schema.\n" 
                                                               f"Please review documentation and see the following exception: {e}"))
         else:
            return f(*args, **kwargs)
      return wrapper
   return func_wrapper
