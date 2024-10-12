from pathlib import Path
import requests
import typer
from typing_extensions import Annotated
from pydantic import BaseModel
from helpers import timeit

STACKOVERFLOW_SURVEY_URL = f"https://survey.stackoverflow.co/datasets/stack-overflow-developer-survey-{0}.zip"
RAW_DATA_DIR = "./stack_data/"


@timeit
def extract(
        year: Annotated[int, typer.Option(help="Year to extract the stackoverflow survey data")],
        dir:  Annotated[Path, typer.Option(help="Dir to store raw data to")] = RAW_DATA_DIR
    ):
    print(f'Starting data extraction for the {year} year.. ')
    resp = requests.get(STACKOVERFLOW_SURVEY_URL.format(year))
    
    if resp.ok:
        data_dir = Path(f'{dir}/{year}')
        data_dir.mkdir(exist_ok=True, parents=True)
        with open(data_dir / f'stack-overflow-developer-survey-{year}.zip', 'wb') as f:
            f.write(resp.content)
        
        print(f"Sucessfully extracted & stored at {data_dir.as_posix()}/stack-overflow-developer-survey-{year}.zip..")
        return data_dir / f'stack-overflow-developer-survey-{year}.zip'
    
    else:
        print(f"Could not download data for the {year} year due to {resp.reason} and {resp.content}..")


if __name__ == "__main__":
    typer.run(extract)