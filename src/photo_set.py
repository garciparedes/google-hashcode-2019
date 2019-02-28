from typing import List

from src.photo import Photo


class PhotoSet(object):

    def __init__(self, photos: List[Photo]):
        self.photos = list(photos)

    @staticmethod
    def from_raw(raw_data: List[str]) -> 'PhotoSet':
        photos = list()

        i = 0
        while i < len(raw_data):
            row = raw_data[i].split(' ')

            if row[0] == 'H':
                photo = Photo(
                    identifier=f'{i}',
                    is_horizontal=True,
                    tags=set(row[2:])
                )
            elif row[0] == 'V':
                i += 1
                if not i < len(raw_data):
                    continue
                row_2 = raw_data[i].split(' ')
                photo = Photo(
                    identifier=f'{i - 1} {i}',
                    is_horizontal=False,
                    tags=set(row[2:]).union(row_2[2:])
                )
            else:
                raise Exception(f'Bad Data input: {row}')
            i += 1
            photos.append(photo)

        return PhotoSet(photos)

    def __str__(self):
        return f'PhotoSet({list(map(str, self.photos))})'

    def generate_solution(self) -> List[str]:
        solution = list()

        for photo in self.photos:
            solution.append(photo.identifier)

        return solution
