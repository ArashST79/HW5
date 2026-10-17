"""Summarize closure hours by closure month and ZIP; never load all rows."""
import argparse
import csv
import json
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path


def summarize(source, output):
    totals = defaultdict(lambda: [0.0, 0])
    audit = Counter()
    fmt = '%m/%d/%Y %I:%M:%S %p'
    with source.open(encoding='utf-8-sig', newline='') as f:
        reader = csv.DictReader(f)
        required = {'Created Date', 'Closed Date', 'Incident Zip'}
        if not required.issubset(reader.fieldnames or []):
            raise ValueError('Missing required date or ZIP columns')
        for row in reader:
            audit['rows_read'] += 1
            zipcode = row['Incident Zip'].strip()
            if zipcode.lower() in {'', 'nan', 'none', 'null', 'n/a'}:
                audit['missing_zip'] += 1
                continue
            if not row['Closed Date'].strip():
                audit['missing_closed_date'] += 1
                continue
            try:
                created = datetime.strptime(row['Created Date'].strip(), fmt)
                closed = datetime.strptime(row['Closed Date'].strip(), fmt)
            except ValueError:
                audit['invalid_date'] += 1
                continue
            if created.year != 2024:
                audit['outside_2024'] += 1
                continue
            seconds = (closed - created).total_seconds()
            if seconds < 0:
                audit['negative_duration'] += 1
                continue
            month = closed.strftime('%Y-%m')
            hours = seconds / 3600
            # Citywide averages use all incidents, not an average of ZIP averages.
            for area in (zipcode, 'ALL'):
                totals[(month, area)][0] += hours
                totals[(month, area)][1] += 1
            audit['included'] += 1
            if closed.year > 2024:
                audit['closed_after_2024'] += 1
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open('w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['month', 'zipcode', 'count', 'total_hours', 'average_hours'])
        for (month, zipcode), (hours, count) in sorted(totals.items()):
            writer.writerow([month, zipcode, count, hours, hours / count])
    output.with_suffix('.audit.json').write_text(json.dumps(dict(audit), indent=2) + '\n')
    return dict(audit)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-i', type=Path, required=True, help='Filtered 2024 CSV')
    parser.add_argument('-o', type=Path, default=Path('data/monthly_response_times.csv'))
    args = parser.parse_args()
    print(json.dumps(summarize(args.i, args.o), indent=2))
