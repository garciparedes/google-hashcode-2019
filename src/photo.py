from typing import Set


class Photo(object):

    def __init__(self, identifier: str, is_horizontal: bool, tags: Set[str]):
        self.identifier = identifier
        self.is_horizontal = is_horizontal
        self.tags = tags

    @property
    def is_vertical(self):
        return not self.is_horizontal

    def __str__(self):
        return f'Photo({self.identifier}, {self.is_horizontal}, {self.tags})'
