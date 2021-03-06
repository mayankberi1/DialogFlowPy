from typing import List


class Entity(dict):

    def __init__(self, entity_value: str, synonyms: List[str]) -> None:
        super().__init__()

        self['value'] = entity_value
        self['synonyms'] = synonyms
