from dataclasses import dataclass, field
from typing import List, Dict

@dataclass
class Group:
    id: str
    name: str
    members: List[str]
    expenses: List[Dict] = field(default_factory=list)
