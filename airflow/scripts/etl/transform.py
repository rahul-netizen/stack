
from pathlib import Path
import requests
import typer
from typing_extensions import Annotated
from pydantic import BaseModel
from utility.helpers import timeit

from zipfile import ZipFile
from utility.logger import logger

@timeit
def transform(file_path: Annotated[Path, typer.Option(help="File path to zip file from which survey data is to be extracted")]):
    logger.info(f'Unzipping data for stackoverflow survey at {file_path}.. ')
    zip = ZipFile(file_path)
    
    with typer.progressbar(
        length=len(zip.infolist()),
        label='Unzipping archive',
    ) as bar:
        for file in zip.infolist():
            bar.update(file.file_size, file)
            if  Path(file.filename).suffix == '.csv':
                zip.extract(file.filename, path=file_path.parent)
                print()
                logger.info(f"File {file_path} loaded & stored at {(file_path.parent / file.filename).as_posix()}")
                return Path(file_path.parent / file.filename )
        
        
if __name__ == "__main__":
    typer.run(transform)