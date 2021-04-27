import os
import xml.etree.ElementTree as ET
from pathlib import Path
from shutil import copyfile


def my_copy_funk(file_name: str) -> None:
    if not Path(file_name).suffix == ".xml":
        raise TypeError("Wrong file extension")
    root = ET.parse(file_name).getroot()
    for file in root:
        try:
            destination_path = Path(file.attrib["destination_path"])
            source_path = Path(file.attrib["source_path"])

            if not source_path.is_absolute():
                source_path = Path(str(os.getcwd()) + str(source_path))
            if not destination_path.is_absolute():
                destination_path = Path(str(os.getcwd()) + str(destination_path))

            destination_path.mkdir(parents=True, exist_ok=True)
            copyfile(
                Path(source_path, file.attrib["file_name"]),
                Path(destination_path, file.attrib["file_name"]),
            )
        except Exception as e:
            print(e)


if __name__ == "__main__":

    FILENAME = "config.xml"

    my_copy_funk(FILENAME)
