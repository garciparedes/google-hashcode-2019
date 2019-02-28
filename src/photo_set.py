from operator import itemgetter
from random import shuffle
from typing import List

from src.photo import Photo


class PhotoContainer(object):

    def __init__(self, photos: List[Photo]):
        self.photos = list(photos)

    @staticmethod
    def from_raw(raw_data: List[str]) -> 'PhotoContainer':
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

                if not row_2[0] == 'V':
                    continue

                photo = Photo(
                    identifier=f'{i - 1} {i}',
                    is_horizontal=False,
                    tags=set(row[2:]).union(row_2[2:])
                )
            else:
                raise Exception(f'Bad Data input: {row}')
            i += 1
            photos.append(photo)

        return PhotoContainer(photos)

    def __str__(self):
        return f'PhotoContainer({list(map(str, self.photos))})'

    def generate_solution(self, required_size: int = None, breadth_size: int = 500) -> List[str]:

        if not required_size or len(self.photos) < required_size:
            required_size = len(self.photos)

        sorted_photos = list()

        print(len(self.photos))

        target = self.photos.pop()
        sorted_photos.append(target)

        points = 0
        while len(sorted_photos) < required_size:

            if len(sorted_photos) % breadth_size == 0:
                shuffle(self.photos)

            fn = lambda p: (PhotoContainer.similarity(sorted_photos[-1], p), p)

            mapping = map(fn, self.photos[:breadth_size])
            maximum = max(mapping, key=itemgetter(0))

            points += maximum[0]

            if len(sorted_photos) % 100 == 0:
                print(f'{len(sorted_photos):5}, {points:2}')

            sorted_photos.append(maximum[1])
            self.photos.remove(maximum[1])

        print(f'FINAL: {len(sorted_photos):5}, {points:2}')

        return list(map(lambda p: p.identifier, sorted_photos))

    @staticmethod
    def similarity(p1: Photo, p2: Photo):
        return min(
            len(p1.tags.intersection(p2.tags)),
            len(p1.tags.difference(p2.tags)),
            len(p2.tags.difference(p1.tags))
        )
