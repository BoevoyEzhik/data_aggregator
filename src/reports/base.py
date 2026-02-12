from abc import ABC, abstractmethod
from typing import Dict, List, Union


class BaseReport(ABC):

    @abstractmethod
    def generate(
        self, data: Dict[str, Dict[str, Union[float, int]]]
    ) -> List[Dict[str, Union[float, str]]]:
        pass
