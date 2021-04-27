import argparse
import hashlib
from os.path import exists
from pathlib import Path


def my_hash_checker(file_name: str, dir_to_check: str) -> None:

    if not exists(file_name):
        raise FileNotFoundError(f"File {file_name} not found")
    if not exists(dir_to_check):
        raise FileNotFoundError(f"Directory  {dir_to_check} not found")

    hashes_funcs = {"md5": hashlib.md5, "sha1": hashlib.sha1, "sha256": hashlib.sha256}

    with open(file_name, "r") as file:
        all_rows = [i.split() for i in file]

    for row in all_rows:
        if not exists(Path(dir_to_check, row[0])):
            print(f"{row[0]} NOT FOUND")
            continue

        if (
            row[1] in hashes_funcs
            and hashes_funcs[row[1]](
                open(Path(dir_to_check, row[0]), "rb").read()
            ).hexdigest()
            == row[2]
        ):
            print(f"{row[0]} OK")
            continue

        print(f"{row[0]} FAIL")


if __name__ == "__main__":

    # Use "python task_2.py all_hash.txt ." to run the program

    parser = argparse.ArgumentParser(
        description="This program checks hash sums of the files"
    )

    parser.add_argument("input_file", type=str, help="path to the input file")

    parser.add_argument(
        "dir_to_check",
        type=str,
        help="path to the directory containing the files to check",
    )

    args = parser.parse_args()

    my_hash_checker(args.input_file, args.dir_to_check)
