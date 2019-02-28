# Hashcode 2019
import sys
from pathlib import Path
from typing import Any, List


def read(path: Path) -> List[str]:
    with open(str(path), 'r') as f:
        content = map(lambda x: x.replace('\n', ''), f.readlines())
    return list(content)


def write(data: str, path: Path):
    with open(str(path), 'w') as f:
        f.write(data)


def run(input_data: Any) -> Any:
    return '\n'.join(input_data)


def main():
    if len(sys.argv) != 2:
        exit(-1)

    input_file = Path(sys.argv[1])
    output_file = input_file.parent / f'{input_file.stem}_output{input_file.suffix}'

    input_data = read(input_file)

    output_data = run(input_data)

    write(output_data, output_file)


if __name__ == '__main__':
    main()
