import hashlib
from os.path import exists


def my_hash_checker(file_name: str) -> None:

    if not exists(file_name):
        raise FileNotFoundError(f"File {file_name} not found")

    hashes_funcs = {"md5": hashlib.md5, "sha1": hashlib.sha1, "sha256": hashlib.sha256}

    with open(file_name, "r") as file:
        all_rows = [i.split() for i in file]

    for row in all_rows:
        if not exists(row[0]):
            print(f"{row[0]} NOT FOUND")
            continue

        if row[1] in hashes_funcs and hashes_funcs[row[1]](open(row[0], "rb").read()).hexdigest() == row[2]:
            print(f"{row[0]} OK")
            continue

        print(f"{row[0]} FAIL")


if __name__ == "__main__":
    FILENAME = "all_hash.txt"
    my_hash_checker(FILENAME)
