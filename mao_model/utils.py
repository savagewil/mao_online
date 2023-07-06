def table_lookup(table: dict, lookup: str):
    variables = lookup.split(".")
    for var in variables:
        table = table[var]
    return table
