from pydantic import BaseModel, ValidationError
from restack_sdk_cloud.sdk_types import StackPlanResponse, StackPlanSchema

def assert_is_stack_plan(config: dict = {}) -> StackPlanResponse:
    try:
        StackPlanSchema(**config)
    except ValidationError as e:
        raise ValueError('Invalid stack modification plan') from e
