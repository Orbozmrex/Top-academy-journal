from functools import wraps
from top_academy_journal.exceptions import ArgsValidationError
from pydantic import ValidationError, validate_call

def validate_arguments(func):
    pydantic_validated = validate_call(func)
    
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await pydantic_validated(*args, **kwargs)
        except ValidationError as e:
            err_details = "; ".join([f"{err['msg']}" for err in e.errors()])
            raise ArgsValidationError(f"Validation error: {err_details}") from None
            
    return wrapper