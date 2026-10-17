#!/usr/bin/env python3
"""Count complaint types by borough within an inclusive creation-date range."""

import argparse
import csv
import sys
from collections import Counter
from datetime import datetime
from pathlib import Path


def parse_date(value):
    """Convert a command-line date into a date Python can compare."""
    try:
        return datetime.strptime(value, '%Y-%m-%d').date()
    except ValueError as error:
        raise argparse.ArgumentTypeError('Use a valid date in YYYY-MM-DD format') from error


def count_complaints(input_path, start, end):
    counts = Counter()
    with input_path.open(encoding='utf-8-sig', newline='') as source:
        reader = csv.DictReader(source)
        required = {'Created Date', 'Complaint Type', 'Borough'}
        if not required.issubset(reader.fieldnames or []):
            raise ValueError('CSV must contain Created Date, Complaint Type, and Borough')
        for row in reader:
            if None in row or any(value is None for value in row.values()):
                raise ValueError(f'Malformed CSV record ending on line {reader.line_num}')
            try:
                created = datetime.strptime(row['Created Date'].strip(), '%m/%d/%Y %I:%M:%S %p').date()
            except ValueError as error:
                raise ValueError(f'Invalid Created Date near line {reader.line_num}') from error
            # Include the entire start day and entire end day.
            if start <= created <= end:
                key = (row['Complaint Type'].strip(), row['Borough'].strip())
                counts[key] += 1
    return counts


def write_counts(counts, destination):
    writer = csv.writer(destination)
    writer.writerow(['complaint type', 'borough', 'count'])
    for (complaint, borough), count in sorted(counts.items()):
        writer.writerow([complaint, borough, count])


def main():
    parser = argparse.ArgumentParser(description=__doc__, epilog='Example: python3 borough_complaints.py -i data/311_2024.csv -s 2024-01-01 -e 2024-01-31')
    parser.add_argument('-i', '--input', type=Path, required=True, help='Input complaint CSV')
    parser.add_argument('-s', '--start', type=parse_date, required=True, help='First creation date, YYYY-MM-DD (inclusive)')
    parser.add_argument('-e', '--end', type=parse_date, required=True, help='Last creation date, YYYY-MM-DD (inclusive)')
    parser.add_argument('-o', '--output', type=Path, help='Output CSV; omit to print to the terminal')
    args = parser.parse_args()
    if args.start > args.end:
        parser.error('Start date must be on or before end date')
    if args.output and args.input.resolve() == args.output.resolve():
        parser.error('Output must be different from the input file')
    try:
        counts = count_complaints(args.input, args.start, args.end)
        if args.output:
            with args.output.open('w', encoding='utf-8', newline='') as destination:
                write_counts(counts, destination)
        else:
            write_counts(counts, sys.stdout)
    except (OSError, ValueError, csv.Error) as error:
        parser.exit(1, f'Error: {error}\n')


if __name__ == '__main__':
    main()
