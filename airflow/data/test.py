from functools import wraps
from time import time

def timing(f):
    @wraps(f)
    def wrap(*args, **kw):
        ts = time()
        result = f(*args, **kw)
        te = time()
        # print('Function :%r with args:[%r, %r] took: %2.4f sec' % (f.__name__, args, kw, te-ts))
        print('Function :%r with args:[ %r] took: %2.4f sec' % (f.__name__, kw, te-ts))
        return result
    return wrap

@timing
def extract(year):
    print(f'Extractiing data for the {year} year.. ')
    resp = requests.get(f"https://survey.stackoverflow.co/datasets/stack-overflow-developer-survey-{year}.zip")
    data_dir = Path(f'./stack_data/{year}')
    data_dir.mkdir(exist_ok=True, parents=True)
    with open(data_dir / f'stack-overflow-developer-survey-{year}.zip', 'wb') as f:
        f.write(resp.content)
    return data_dir / f'stack-overflow-developer-survey-{year}.zip'

@timing
def transform(file_path: Path):
    print(f'Unzipping data for stackoverflow survey at {file_path}.. ')
    zip = ZipFile(file_path)
    for file in zip.infolist():
        if  Path(file.filename).suffix == '.csv':
            zip.extract(file.filename, path=file_path.parent)
            return Path(file_path.parent / file.filename )
@timing
def dq_checks(file_path: Path, validation_config_filepath: str = 'stackoverflow_survey_data_expectations_suite.json' ):
    print(f'Performing data quality checks using validation config from {validation_config_filepath}..')
    data = gx.read_csv(file_path,  encoding='latin-1')
    gx_data = gx.from_pandas(data)
    results = gx_data.validate(expectation_suite=validation_config_filepath)

    # save results for inspection 
    with open( file_path.parent / f'{file_path.stem}_dq_results.json', 'w') as f:
        json.dump(results.to_json_dict(), fp=f, indent=4)

    return results

@timing
def summerise_expectation_results(exp_results: dict):
    print('DQ result summary..')
    for result in exp_results.get('results'):
        print(f"\t * Success on {result['expectation_config']['expectation_type']} : {result['success']}")

def load(file_path: Path, year: int, db_path: Path = Path('.')):
    try:
        import duckdb
        db_path = str((db_path / 'stack_data_db.db').resolve())
        print(f"Loading data for the year {year} from {file_path} at {db_path}..")
        db_client = duckdb.connect(database = db_path)
        db_client.execute(f"create or replace table stack_{year} as select * from read_csv_auto('{str(file_path.absolute())}')")
        db_client.commit()
        db_client.close()
    except BaseException as e:
        print(f'Error occured while loading data..{str(e)}')

@timing
def orchestrate(start_year, end_year):
    print(f'Starting stackoverflow survey ETL from {start_year} till {end_year}..\n', end='')
    for year in range(start_year, end_year + 1):
        file_path = extract(year)
        data_file_path = transform(file_path)
        results = dq_checks(data_file_path)
        print(f'DQ results : {results.get("success")}')
        summerise_expectation_results(results)
        if results.get("success"):
            load(data_file_path, year)
        print('\n')

if __name__ == '__main__':
    # 2011 to 2021 after that url changed
    orchestrate(2017, 2017)