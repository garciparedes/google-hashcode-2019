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

    def generate_solution(self, required_size: int = None, breadth_size: int = 2000, **kwargs) -> List[Photo]:

        if not required_size or len(self.photos) < required_size:
            required_size = len(self.photos)

        sorted_photos = list()

        print(len(self.photos))

        shuffle(self.photos)

        target = self.photos.pop()
        sorted_photos.append(target)

        points = 0
        while len(sorted_photos) < required_size:

            if len(sorted_photos) % breadth_size == 0:
                shuffle(self.photos)

            fn = lambda p: (Photo.similarity(sorted_photos[-1], p), p)

            mapping = map(fn, self.photos[:breadth_size])
            maximum = max(mapping, key=itemgetter(0))

            points += maximum[0]

            if len(sorted_photos) % 100 == 0:
                print(f'{len(sorted_photos):5}, {points:2}')

            sorted_photos.append(maximum[1])
            self.photos.remove(maximum[1])

        print(f'FINAL: {len(sorted_photos):5}, {points:2}')

        return sorted_photos

    def optimize_solution(self, sorted_photos: List[Photo], max_optimization_itr: int = 20000, **kwargs) -> List[Photo]:

        saving = 0
        saving_itr = None
        k = 0
        while saving_itr is None or saving_itr > 0 and k < max_optimization_itr:
            saving_itr = 0
            for i in range(0, len(sorted_photos) - 2):

                p1 = sorted_photos[i]
                p2 = sorted_photos[i + 1]
                p3 = sorted_photos[i + 2]

                old = Photo.similarity(p1, p2) + Photo.similarity(p2, p3)
                new = Photo.similarity(p2, p1) + Photo.similarity(p1, p3)

                if new <= old:
                    continue

                saving_itr += new - old

                sorted_photos[i] = p2
                sorted_photos[i + 1] = p1
            if k % 100 == 0:
                print(f'{saving:5}')
            k += 1
            saving += saving_itr
        print(f'FINAL: {saving:5}')

        return sorted_photos

    def solve(self, **kwargs) -> List[str]:
        sorted_photos = self.generate_solution(**kwargs)
        sorted_photos = self.optimize_solution(sorted_photos, **kwargs)
        return list(map(lambda p: p.identifier, sorted_photos))
