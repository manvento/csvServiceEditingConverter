import json
import os
import sys

from typing import Optional

import pandas as pd


def load_data(filepath: str) -> pd.DataFrame:
    """ Load CSV data into a DataFrame. """
    return pd.read_csv(filepath, delimiter=';')


def generate_json_configuration(group: pd.DataFrame):
    """
    Generates the json configuration.
    :param group:
    :return:
    """
    result = []
    for index, row in group.iterrows():
        result.append({
            "name": row['name'],
            "editable": row['editable'],
            "hidden": row['hidden'],
            "mandatory": row['mandatory'],
            "order": index
        })

    return json.dumps(result)


def generate_sql_statements(data: pd.DataFrame, group_id: Optional[int]):
    """ Generate SQL INSERT statements from CSV data with merged JSON configurations. """
    grouped: pd.DataFrameGroupBy = data.groupby(['layer_id', 'service_item_id'])
    sql_statements = []

    group_id_value = 'null' if group_id is None else f"'{group_id}'"

    for (layer_id, service_item_id), group in grouped:

        json_config_str = generate_json_configuration(group)

        # Prepare DELETE statement
        delete_statement = f"DELETE FROM gw_service_editing WHERE layer_id = '{layer_id}' AND " \
                           f"service_item_id = '{service_item_id}' AND group_id = {group_id_value};"
        sql_statements.append(delete_statement)

        # Prepare INSERT statement
        insert_statement = f"INSERT INTO gw_service_editing (group_id, layer_id, \"configuration\", service_item_id) " \
                           f"VALUES ({group_id_value}, '{layer_id}', '{json_config_str}', '{service_item_id}');"
        sql_statements.append(insert_statement)

    return sql_statements


def process_directory(directory: str, group_id: Optional[int]):
    """ Process each CSV file in the directory recursively and generate SQL statements. """
    sql_statements = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".csv"):
                filepath = os.path.join(root, file)
                data = load_data(filepath)
                statements = generate_sql_statements(data, group_id)
                sql_statements.extend(statements)
    return sql_statements


def main():
    """ Main function to process the CSV file or directory and write SQL statements to a file. """
    if len(sys.argv) < 2:
        print("Usage: python script.py <file_or_directory_path> [group_id]")
        return

    path = sys.argv[1]
    group_id = sys.argv[2] if len(sys.argv) > 2 else None

    # Check if the path is a directory or a single file
    if os.path.isdir(path):
        sql_statements = process_directory(path, group_id)
    else:
        data = load_data(path)
        sql_statements = generate_sql_statements(data, group_id)

    # Write SQL statements to the output file
    with open("insert_script.sql", 'w') as f:
        for statement in sql_statements:
            f.write(statement + '\n')

    print(f"SQL statements have been saved to insert_script.sql")


if __name__ == "__main__":
    main()
