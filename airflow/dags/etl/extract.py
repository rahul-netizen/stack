
from pathlib import Path
import requests
from utility.utils import timing

@timing
def extract(year):
    print(f'Extractiing data for the {year} year.. ')
    resp = requests.get(f"https://survey.stackoverflow.co/datasets/stack-overflow-developer-survey-{year}.zip")
    data_dir = Path(f'./stack_data/{year}')
    data_dir.mkdir(exist_ok=True, parents=True)
    with open(data_dir / f'stack-overflow-developer-survey-{year}.zip', 'wb') as f:
        f.write(resp.content)
    return data_dir / f'stack-overflow-developer-survey-{year}.zip'