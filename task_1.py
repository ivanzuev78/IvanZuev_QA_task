import os
import xml.etree.ElementTree as ET
from shutil import copy
from pathlib import Path

root = ET.parse('config.xml').getroot()
for file in root:
    destination_path = Path(file.attrib['destination_path'])
    source_path = Path(file.attrib['source_path'])
    if not source_path.is_absolute():
        source_path = Path(str(os.getcwd()) + str(source_path))
    if not destination_path.is_absolute():
        destination_path = Path(str(os.getcwd()) + str(destination_path))
    destination_path.mkdir(parents=True, exist_ok=True)

    copy(Path(source_path, file.attrib['file_name']), Path(destination_path, file.attrib['file_name']))
