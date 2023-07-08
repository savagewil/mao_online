def table_lookup(table: dict, lookup: str):
    variables = lookup.split(".")
    for var in variables:
        table = table[var]
    return table


def table_set(table: dict, lookup: str, value: object):
    variables = lookup.split(".")
    for var in variables[:-1]:
        if var in table and isinstance(table[var], dict):
            table = table[var]
        else:
            table[var] = {}
            table = table[var]
    table[variables[-1]] = value
