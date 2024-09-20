from pydantic import BaseModel, Field
from typing import List, Optional, Union

class EnvironmentVariable(BaseModel):
    name: str
    value: Optional[Union[str, bool]] = None
    linkTo: Optional[str] = None

class DatabaseInputSchema(BaseModel):
    name: str
    username: str
    password: str

class ApplicationInputSchema(BaseModel):
    name: str
    dockerFilePath: Optional[str] = None
    environmentVariables: Optional[List[Optional[EnvironmentVariable]]] = None
    gitUrl: Optional[str] = None
    gitBranch: Optional[str] = None
    dockerBuildContext: Optional[str] = None
    image: Optional[str] = None
    database: Optional[DatabaseInputSchema] = None
    cloudStorage: Optional[bool] = False

class PlanSchema(BaseModel):
    action: str = Field(..., pattern='^(create|update|delete)$')
    resourceType: str = Field(..., pattern='^(Stack|Application)$')
    changes: List[dict]
    metadata: Optional[dict] = None

class StackPlanSchema(BaseModel):
    stack: dict
    applications: List[dict]

class ApplicationSchema(ApplicationInputSchema):
    plan: PlanSchema
    databasePlan: Optional[PlanSchema] = None

class StackSchema(BaseModel):
    name: str
    previewEnabled: bool
    applications: List[ApplicationSchema]
    plan: PlanSchema

class CreateStackPayloadSchema(BaseModel):
    id: str
    name: str
    previewEnabled: bool

class StackInputSchema(BaseModel):
    name: str
    previewEnabled: bool
    applications: List[ApplicationInputSchema]

class StackPlanResponseSchema(BaseModel):
    stack: StackSchema
    applications: List[ApplicationSchema]

class DeployedApplicationSchema(BaseModel):
    name: Optional[str] = None
    error: Optional[str] = None
    type: Optional[str] = None
    details: Optional[List[dict]] = None

class DeployedStackSchema(BaseModel):
    name: str
    error: Optional[str] = None
    applications: List[DeployedApplicationSchema]

class DeployResponseSchema(BaseModel):
    stacks: List[DeployedStackSchema]
    stacksUrl: str

# Export types for compatibility
ApplicationInput = ApplicationInputSchema
Plan = PlanSchema
Application = ApplicationSchema
Stack = StackSchema
CreateStackPayload = CreateStackPayloadSchema
StackInput = StackInputSchema
StackPlanResponse = StackPlanResponseSchema
DeployedApplication = DeployedApplicationSchema
DeployedStack = DeployedStackSchema
DeployResponse = DeployResponseSchema
