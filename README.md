# NYC 311 learning project

Explore complaint counts and compare monthly average complaint closure times across NYC ZIP codes.

## Data preparation

Run with Python 3 from this project folder:

```sh
python3 prepare_data.py -i /path/to/311_records.csv.tar -o data/311_2024.csv
```

The script retains complaints created in 2024 with a nonmissing ZIP code and preserves the original columns. It reads records one at a time to limit memory usage. Unclosed complaints remain available for counting; they will be excluded from closure-time calculations later.

The prepared dataset contains 3,423,953 complaints. Data files are excluded from Git through `.gitignore`.

## Complaint-counting tool

Count complaints by type and borough, using an inclusive creation-date range:

```sh
python3 borough_complaints.py -i data/311_2024.csv -s 2024-01-01 -e 2024-01-31
```

Add `-o data/january_counts.csv` to save the CSV instead of printing it. Use `python3 borough_complaints.py -h` for help. Both endpoint dates include the full day. Unclosed complaints are counted. Results are sorted by complaint type and borough; a range with no matches produces only the CSV header. Invalid dates or missing required columns produce an error.

The assignment uses two different script names; this project follows Task 1's `borough_complaints.py` name.

## Jupyter on your Mac

Task 2 is being completed locally for self-directed learning; the assignment's EC2 setup is deferred.

Create a separate Python environment and install the dependencies (one-time setup):

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

To start Jupyter from the project folder:

```sh
source .venv/bin/activate
jupyter lab --ip=127.0.0.1
```

Open `getting_started.ipynb`. Click a code cell and press **Shift + Enter** to execute it. The kernel is the Python process that runs the cells. Keep the terminal running while using Jupyter; press **Control + C** there to stop the server when finished. The server runs locally with its default token authentication. The `.venv` directory is excluded from Git; `requirements.txt` records the installed versions.

## Planned work

- Compare complaint frequency in a Jupyter notebook.
- Precompute monthly closure-time averages.
- Build an interactive Bokeh dashboard.
