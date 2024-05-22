# CSV to SQL Converter

This script processes CSV files and generates corresponding SQL INSERT statements. The SQL statements are written to an output file named `insert_script.sql`.

## Features

- Load CSV data into a Pandas DataFrame.
- Generate JSON configuration from CSV data.
- Generate SQL INSERT statements from the CSV data.
- Process CSV files in a directory recursively.
- Save generated SQL statements to an output file.

## Requirements

- Python 3.x
- pandas

## Installation

To install the required packages, you can use pip:

```bash
pip install pandas
```

## Usage

To run the script, use the following command:

```bash
python script.py <file_or_directory_path> [group_id]
```

- `<file_or_directory_path>`: Path to the CSV file or directory containing CSV files.
- `[group_id]` (optional): Group ID to be used in the SQL statements.

### Examples

Process a single CSV file:

```bash
python script.py data.csv
```

Process all CSV files in a directory:

```bash
python script.py /path/to/directory
```

Process a single CSV file with a specified group ID:

```bash
python script.py data.csv 123
```

## Functions

### `load_data(filepath: str) -> pd.DataFrame`

Loads CSV data into a DataFrame.

- `filepath`: Path to the CSV file.

### `generate_json_configuration(group: pd.DataFrame) -> str`

Generates the JSON configuration from a DataFrame group.

- `group`: DataFrame group.

Returns a JSON string.

### `generate_sql_statements(data: pd.DataFrame, group_id: Optional[int]) -> list`

Generates SQL INSERT statements from CSV data with merged JSON configurations.

- `data`: DataFrame containing the CSV data.
- `group_id`: Optional group ID.

Returns a list of SQL statements.

### `process_directory(directory: str, group_id: Optional[int]) -> list`

Processes each CSV file in the directory recursively and generates SQL statements.

- `directory`: Path to the directory containing CSV files.
- `group_id`: Optional group ID.

Returns a list of SQL statements.

### `main()`

Main function to process the CSV file or directory and write SQL statements to a file.

## Output

The generated SQL statements are saved to a file named `insert_script.sql` in the current directory.
.
## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
