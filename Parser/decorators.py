from typing import final
from functools import wraps


@final
class ProjectDecorators:
    @classmethod
    def result_processing(self, function_to_decorate):
        @wraps(function_to_decorate)
        def wrapper(self):
            return list(set(function_to_decorate(self)))

        return wrapper
