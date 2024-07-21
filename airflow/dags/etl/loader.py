from pathlib import Path
from utility.utils import timing


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