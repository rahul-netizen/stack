from utility.helpers import timeit
from etl.extraction import extract
from etl.transform import transform
import typer

@timeit
def orchestrate(start_year: int, end_year: int):
    print(f'Starting stackoverflow survey ETL from {start_year} till {end_year}..\n', end='')
    for year in range(start_year, end_year + 1):
        file_path = extract(year)
        if file_path:
            data_file_path = transform(file_path)
        # results = dq_checks(data_file_path)
        # print(f'DQ results : {results.get("success")}')
        # summerise_expectation_results(results)

        # skipping dq checks
        # if results.get("success"):
        #     load(data_file_path, year)
        # load(data_file_path, year)
        print('\n')

if __name__ == "__main__":
    # typer.run(orchestrate)
    orchestrate(2014, 2014)