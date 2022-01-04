from typing import Union
from mongoengine.queryset.visitor import Q
from functools import reduce
import operator


class DatabaseTransaction:
    
    def __init__(self, model) -> None:
        self._model = model
        self.query_operators = {
            "AND": operator.and_,
            "OR": operator.or_
        }
     
    
    
    def create(self, **kwargs):
        kwargs = self.check_args(kwargs)
        return self._model(**kwargs).save()
    
    def read(self, *, options: dict = {}, **kwargs):
        
        query = self._model.objects(
            reduce(self.query_operators[options.get("query_operator", "AND")],
                   [Q(**{key: val}) for key, val in kwargs.items()]
            )
        )
        
        if options.get("first", False):
            query = query.first()
        
        return query
    
    def update(self, queryset, data: dict):
        data = self.check_args(data)
        queryset.update(
            **data
        )
    
    def delete(self, queryset):
        queryset.delete()
    
    def check_args(self, kwargs: dict) -> dict:
        for arg in kwargs.keys():
            if arg not in self._model._fields.keys():
                kwargs.pop(arg, None)
                
        return kwargs