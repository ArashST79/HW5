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


## Complaint frequency analysis (Task 3)

Open `complaint_analysis.ipynb` in Jupyter and run its cells from top to bottom. It calls the command-line tool for the full year and four selected months, ranks complaint types across boroughs, and compares January–February with June–July. Running all cells takes a few minutes because each tool call reads the dataset.

The notebook writes `complaint_type_analysis.md` and `figures/complaint_comparison.png`. It reports both period totals and daily averages to account for unequal period lengths. The saved notebook includes executed results.

## ZIP-code dashboard (Task 4)

First prepare the monthly summary from the filtered data:

```sh
python preprocess_response_times.py -i data/311_2024.csv
```

Then start the dashboard:

```sh
bokeh serve dashboard --address 127.0.0.1 --show
```

The dashboard uses only `data/monthly_response_times.csv`. The original complaint rows are not loaded during dropdown changes. The two dropdowns and chart appear in a single column. Hover over a line for its incident count and average; click legend items to hide/show curves.

Rules: retain complaints created in 2024 with ZIP codes and nonmissing, parseable closure dates; exclude negative durations; include zero-hour closures. Group by closure month, retaining closures after 2024. Citywide means are computed from incident totals, not an unweighted average of ZIP means. Months without eligible incidents show gaps. We treat the dashboard instructions' references to 2020 as a typo because the preparation instructions require 2024.

The audit JSON alongside the summary records exclusions. ZIP values are retained as provided, with surrounding whitespace removed. Naive source timestamps are subtracted directly; the dataset does not supply timezone offsets for resolving daylight-saving ambiguity.

`Bokeh.tgz` contains only the dashboard, preprocessing, and standalone-export Python source. Extract it into the project folder; install dependencies from `requirements.txt` and generate the summary before launching.

### Standalone browser version

Run `python export_dashboard.py` after preprocessing to create `dashboard.html`. Open this file in a browser, or serve it locally. It embeds the small summary and Bokeh assets, so dropdowns work without a live Bokeh server or internet access. This generated file contains summary data and is excluded from Git.

Validation: checked missing/negative dates, zero durations, closure-month grouping, late closures, and incident-weighted citywide means. Both browser dropdowns updated successfully; one measured selection-to-legend update took 63 milliseconds, below the five-second requirement. Performance can vary by computer. Source ZIP labels are not validated against a geographic directory, so the source contains unusual labels (including `NA` and `Unkno`) that should be reviewed before operational use.
