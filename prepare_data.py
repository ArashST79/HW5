"""Keep 311 complaints created in 2024 that have a ZIP code."""

import argparse
import csv
import io
import json
import tarfile
from datetime import datetime
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-i', '--input', type=Path, required=True, help='Original TAR archive')
    parser.add_argument('-o', '--output', type=Path, required=True, help='Filtered CSV')
    args = parser.parse_args()
    counts = dict(total=0, outside_2024=0, invalid_created_date=0,
                  missing_zip_in_2024=0, kept=0)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    temporary = args.output.with_suffix('.csv.partial')
    with tarfile.open(args.input, 'r:*') as archive:
        for member in archive:
            if (not member.isfile() or Path(member.name).name.startswith('._')
                    or not member.name.lower().endswith('.csv')):
                continue
            source = io.TextIOWrapper(archive.extractfile(member), encoding='utf-8-sig', newline='')
            reader = csv.DictReader(source)
            required = {'Created Date', 'Incident Zip'}
            if not required.issubset(reader.fieldnames or []):
                raise ValueError('Required columns are missing')
            with temporary.open('w', encoding='utf-8', newline='') as destination:
                writer = csv.DictWriter(destination, fieldnames=reader.fieldnames)
                writer.writeheader()
                for row in reader:
                    counts['total'] += 1
                    if None in row or any(value is None for value in row.values()):
                        raise ValueError(f'Malformed CSV row {counts["total"]}')
                    try:
                        created = datetime.strptime(row['Created Date'].strip(), '%m/%d/%Y %I:%M:%S %p')
                    except ValueError:
                        counts['invalid_created_date'] += 1
                        continue
                    if created.year != 2024:
                        counts['outside_2024'] += 1
                    elif row['Incident Zip'].strip().lower() in {'', 'nan', 'null', 'none', 'n/a'}:
                        counts['missing_zip_in_2024'] += 1
                    else:
                        writer.writerow(row)
                        counts['kept'] += 1
                    if counts['total'] % 1_000_000 == 0:
                        print(f'Read {counts["total"]:,} rows; kept {counts["kept"]:,}', flush=True)
            break
        else:
            raise ValueError('No CSV found in archive')
    temporary.replace(args.output)
    report = {'input': str(args.input), 'output': str(args.output), 'counts': counts}
    args.output.with_suffix('.summary.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
