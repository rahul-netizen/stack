from pathlib import Path
from utility.utils import timing
import great_expectations as gx
import json

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
