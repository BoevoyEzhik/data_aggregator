from abc import ABC, abstractmethod
from typing import Dict, List, TypedDict, Union


class EconomicRecord(TypedDict):
    year: int
    gdp: Union[float, None]
    gdp_growth: Union[float, None]
    inflation: Union[float, None]
    unemployment: Union[float, None]
    population: Union[int, None]
    continent: str


EconomicData = Dict[str, List[EconomicRecord]]


class BaseReport(ABC):

    @abstractmethod
    def generate(self, data: EconomicData) -> List[Dict[str, Union[str, float]]]:
        pass
