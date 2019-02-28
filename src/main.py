# Hashcode 2019
import sys
from pathlib import Path
from typing import List

from src.photo_set import PhotoContainer


def read(path: Path) -> List[str]:
    with open(str(path), 'r') as f:
        content = map(lambda x: x.replace('\n', ''), f.readlines())
    content = list(content)
    assert int(content[0]) == len(content) - 1
    return content[1:]


def solution_to_str(data: List[str]) -> str:
    text_data = str()
    text_data += f'{len(data)}\n'
    text_data += '\n'.join(data)
    return text_data


def write(data: str, path: Path):
    with open(str(path), 'w') as f:
        f.write(data)


def main():
    if len(sys.argv) != 2:
        exit(-1)

    input_file = Path(sys.argv[1])
    output_file = input_file.parent / f'{input_file.stem}_output{input_file.suffix}'

    input_data = read(input_file)

    photo_set = PhotoContainer.from_raw(input_data)
    solution = photo_set.solve()

    str_solution = solution_to_str(solution)

    write(str_solution, output_file)


if __name__ == '__main__':
    main()
