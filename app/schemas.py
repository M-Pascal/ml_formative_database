# from pydantic import BaseModel

# class Patient(BaseModel):
#     id: str
#     diagnosis: str


# from pydantic import BaseModel
# from typing import Dict

# class PatientDetails(BaseModel):
#     id: str
#     diagnosis: str
#     tumor_mean: Dict[str, float]
#     tumor_se: Dict[str, float]
#     tumor_worst: Dict[str, float]

from pydantic import BaseModel
from typing import Optional


class TumorMean(BaseModel):
    radius_mean: float
    texture_mean: float
    perimeter_mean: float
    area_mean: float
    smoothness_mean: float
    compactness_mean: float
    concavity_mean: float
    concave_points_mean: float
    symmetry_mean: float
    fractal_dimension_mean: float


class TumorSE(BaseModel):
    radius_se: float
    texture_se: float
    perimeter_se: float
    area_se: float
    smoothness_se: float
    compactness_se: float
    concavity_se: float
    concave_points_se: float
    symmetry_se: float
    fractal_dimension_se: float


class TumorWorst(BaseModel):
    radius_worst: float
    texture_worst: float
    perimeter_worst: float
    area_worst: float
    smoothness_worst: float
    compactness_worst: float
    concavity_worst: float
    concave_points_worst: float
    symmetry_worst: float
    fractal_dimension_worst: float


class Patient(BaseModel):
    id: str
    diagnosis: str
    tumor_mean: TumorMean
    tumor_se: TumorSE
    tumor_worst: TumorWorst
