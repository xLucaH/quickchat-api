from typing import List, Dict, Tuple, Any


def get_placeholder(count: int):
    return ("%s, " * count)[:-2]


def get_insert_formats(inserts: List[Dict]) -> Tuple[str, str, List]:
    """
    Creates insert rows for sql queries from a list of dictionaries with keys as column names.

    :param inserts: List of dictionaries with keys as column names.
    :return:  - col_names: string of column names to insert.
              - values_placeholder: string of format (%s, %s, %s) that represents the rows.
              - values_to_insert: list of values to escape in final db.execute()
    """

    col_names = ", ".join([x for x in inserts[0].keys()])

    values_to_insert = []

    values_placeholder = ""

    for i, item in enumerate(inserts):

        sql_row = "(%s)"  # this is our base row where we insert a placeholder for every value.
        sql_value_row = ""

        for value in item.values():
            values_to_insert.append(value)

            sql_value_row += "%s,"

        sql_value_row = sql_value_row[:-1]
        sql_row = sql_row % sql_value_row

        # Dont append a comma for the last row.
        if i != len(inserts) - 1:
            sql_row += ","

        values_placeholder += sql_row

    return col_names, values_placeholder, values_to_insert

