from schema import Schema, And, Use, Optional, SchemaError
from flask import request
from errors import bad_request
from functools import wraps
from typing import Callable

#Prevent redundancy and improve readibility
str_lower_strip = str, Use(str.lower), Use(str.strip)


supported_metrics = ('g','ml')
def metric_is_supported(metric:str) -> bool: 
    return metric in supported_metrics

IngredientsSchema = Schema([{'Name': And(*str_lower_strip),
                             'Amount': Use(int),
                             'Metric': And(*str_lower_strip, metric_is_supported,
                                           error=f"'Ingredients' key 'Metric' value '{{}}' should be one of the following strings: {supported_metrics}")}])
                                           
CreateRecipeSchema = Schema({'Name': And(*str_lower_strip),
                             'Ingredients': IngredientsSchema,
                              Optional('Steps'): {Use(int):str}})

EditRecipeSchema = Schema({'Name': And(*str_lower_strip),
                           Optional('Ingredients'): IngredientsSchema,
                           Optional('Steps'): {Use(int):str}})

GetRecipeSchema = Schema(Use(int))
DeleteRecipeSchema = Schema(Use(int))


def validate_schema(schema:Schema) -> Callable:
   def func_wrapper(f:Callable) -> Callable:
      @wraps(f)
      def wrapper(*args, **kwargs) -> Callable:
         try:
            schema.validate(request.form)
         except SchemaError as e:
            return bad_request(request.path, additional_message=("The JSON data sent does not conform to the expected schema.\n" 
                                                               f"Please review documentation and see the following exception: {e}."))
         else:
            return f(*args, **kwargs)
      return wrapper
   return func_wrapper

print('Hello')

d = {'Name':'Hello','Ingredients':[{'Name':'flour','Amount':'200','Metric':'g'}]}
CreateRecipeSchema.validate(d)
