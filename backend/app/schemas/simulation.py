from pydantic import BaseModel


class SimulationRunRequest(BaseModel):
    scenario_id: str


class SimulationScenario(BaseModel):
    scenario_id: str
    name: str
    description: str
