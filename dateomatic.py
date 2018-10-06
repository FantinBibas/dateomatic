#!/usr/bin/env python3

import sys
import itertools


DayIdentifier = 'd'
MonthIdentifier = 'm'
YearIdentifier = 'y'
SeparatorIdentifier = 's'


default_separators = [
    '/',
    '',
    '-',
    ' ',
    ';',
    ':',
    '.',
]


default_schemas_list = [
    'ysmsd',
    'dsmsy',
    'dsm',
    'msd',
    'msy',
    'ysm',
]


default_months_dictionary = {
    1: ['jan', 'january'],
    2: ['feb', 'february'],
    3: ['mar', 'march'],
    4: ['apr', 'april'],
    5: ['may'],
    6: ['jun', 'june'],
    7: ['jul', 'july'],
    8: ['aug', 'august'],
    9: ['sep', 'sept', 'september'],
    10: ['oct', 'october'],
    11: ['nov', 'november'],
    12: ['dec', 'december'],
}


def get_sized_transformations(number, paddings):
    for padding in paddings:
        yield str(number).zfill(padding)[-padding:]


def get_year_transformations(year):
    yield from get_sized_transformations(year, [2, 4])


def get_month_transformations(month, months_dictionary):
    yield from get_sized_transformations(month, [1, 2] if month < 10 else [2])
    for transformation in months_dictionary[month]:
        yield transformation


def get_day_transformations(day):
    yield from get_sized_transformations(day, [1, 2])


def get_transformation_from_identifier(identifier, day, month, year, months_dictionary, separator):
    if identifier == DayIdentifier:
        yield from get_day_transformations(day)
    elif identifier == MonthIdentifier:
        yield from get_month_transformations(month, months_dictionary)
    elif identifier == YearIdentifier:
        yield from get_year_transformations(year)
    elif identifier == SeparatorIdentifier:
        yield separator


def get_schema_transformations(schema, day, month, year, months_dictionary, separator):
    if len(schema) == 0:
        yield schema
    else:
        transformations = get_transformation_from_identifier(schema[0], day, month, year, months_dictionary, separator)
        if len(schema) == 1:
            yield from transformations
        else:
            for prefix, suffix in itertools.product(transformations, get_schema_transformations(schema[1:], day, month, year, months_dictionary, separator)):
                yield prefix + suffix


def dateomatic(day, month, year, months_dictionary=default_months_dictionary, schemas_list=default_schemas_list, separators=default_separators):
    for separator in separators:
        for schema in schemas_list:
            yield from get_schema_transformations(schema, day, month, year, months_dictionary, separator)


def usage(name):
    print("USAGE:\n\t" + name + " [-h] day month year\n\nDESCRIPTION:")
    print("\t-h\tshow this help and exit")
    print("\tday\tday of the date (ex: 11)")
    print("\tmonth\tmonth of the date (ex: 3)")
    print("\tyear\tyear of the date (ex: 1998)")


def main(argv):
    if '-h' in argv[1:] or len(argv) != 4:
        usage(argv[0])
        return 0 if '-h' in argv[1:] else 1
    try:
        day = int(argv[1])
        month = int(argv[2])
        year = int(argv[3])
    except ValueError:
        return 1
    if day < 1 or day > 31 or month < 1 or month > 12 or year < 0:
        return 1
    for date in dateomatic(day, month, year, default_months_dictionary):
        print(date)
    return 0


if __name__ == '__main__':
    exit(main(sys.argv))
