from pathlib import Path
from utility.utils import timing
from zipfile import ZipFile

@timing
def transform(file_path: Path):
    print(f'Unzipping data for stackoverflow survey at {file_path}.. ')
    zip = ZipFile(file_path)
    for file in zip.infolist():
        if  Path(file.filename).suffix == '.csv':
            zip.extract(file.filename, path=file_path.parent)
            return Path(file_path.parent / file.filename )