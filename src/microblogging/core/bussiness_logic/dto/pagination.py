from dataclasses import dataclass
from typing import Iterable, Union

@dataclass
class PaginationPageDTO:
    data: Iterable
    next_page: Union[int, None]
    prev_page: Union[int, None]
    navigation_num: Iterable
