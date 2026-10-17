# NYC 311 learning project

Explore complaint counts and compare monthly average complaint closure times across NYC ZIP codes.

## Data preparation

Run with Python 3 from this project folder:

```sh
python3 prepare_data.py -i /path/to/311_records.csv.tar -o data/311_2024.csv
```

The script retains complaints created in 2024 with a nonmissing ZIP code and preserves the original columns. It reads records one at a time to limit memory usage. Unclosed complaints remain available for counting; they will be excluded from closure-time calculations later.

The prepared dataset contains 3,423,953 complaints. Data files are excluded from Git through `.gitignore`.

## Planned work

- Build a command-line complaint-counting tool.
- Compare complaint frequency in a Jupyter notebook.
- Precompute monthly closure-time averages.
- Build an interactive Bokeh dashboard.
