from pydantic import BaseModel

class ProjectInput(BaseModel):
    budget: float
    duration: int
    department: str
    project_type: str
    status: str
    region: str
    complexity: str
    completion_percent: float
    days_since_start: int
    benefit_cost_ratio: float
    cost_per_day: float
    project_Benefit: float
    project_Cost: float
