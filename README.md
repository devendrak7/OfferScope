# OfferScope

A beginner-friendly Python CLI tool that turns raw, unstructured job/internship postings into structured data using Regex, then analyzes them with Pandas and NumPy.

## Problem Statement

Job and internship postings are written as free-form paragraphs. Pay appears in many different formats (`₹15,000/month`, `Rs. 20,000 per month`, `6 LPA`), and comparing dozens of postings by eye to answer questions like "what's the typical stipend?" or "which skills pay more?" is slow and error-prone.

## What OfferScope Does

OfferScope reads postings from `.txt` files, extracts fields (stipend, duration, skills, location, work mode, job type) using Regex, builds a structured table with Pandas, and reports statistics using Pandas and NumPy — all from the terminal.

## Workflow

```text
Raw TXT postings
   → Loader (reads files, splits postings)
   → Regex Extractors (pull structured fields from text)
   → Cleaner (build a Pandas DataFrame, convert numeric columns)
   → Analyzer (Pandas + NumPy statistics)
   → Reports (print to terminal)
   → Exporter (CSV / JSON / TXT)
```

## Features

- Extracts stipend (min/max/midpoint), pay status, duration, work mode, job type, skills and location from raw text
- Handles multiple stipend formats: fixed amount, range, LPA, LPA range
- Ignores unrelated numbers (application fees, course fees, years of experience)
- Stipend statistics: mean, median, standard deviation, 25th/75th/90th percentile, outliers
- Skill demand (count and percentage of postings)
- Skill vs pay (median stipend per skill, with a minimum-sample-size rule)
- Extraction quality report (how many postings had missing/ambiguous fields)
- Search/filter postings by skill, title or location
- Export results to CSV, JSON and TXT
- Reads postings from any number of `.txt` files in `data/raw/`, with bundled sample data as a fallback

## Technologies Used

| Technology | Role |
|---|---|
| Python (`re`, `json`, `pathlib`) | Core logic, file handling, Regex, config loading |
| Pandas | DataFrame, type conversion, filtering, grouping, export |
| NumPy | Mean, median, standard deviation, percentiles |

No frameworks, databases, ML or web scraping are used.

## Project Structure

```text
offerscope/
├── main.py          # CLI menu loop, connects all modules
├── loader.py         # reads .txt files, splits into postings
├── extractors.py      # all Regex extraction logic
├── cleaner.py         # builds the Pandas DataFrame
├── analyzer.py         # Pandas + NumPy analysis
├── reports.py          # prints analysis results
├── exporter.py          # CSV / JSON / TXT export
├── ui.py                 # menu text and input handling
├── config/
│   ├── skills.json        # skill name → list of aliases
│   └── settings.json       # list of recognized cities
├── data/
│   ├── raw/                 # your own postings (not tracked by Git)
│   ├── sample/                # bundled demo postings (tracked)
│   └── output/                  # generated exports (not tracked by Git)
├── tests/
│   ├── test_extractors.py
│   └── test_pipeline.py
├── requirements.txt
└── README.md
```

## Module Responsibilities

- **`loader.py`** — reads a `.txt` file (or every `.txt` file in a folder), splits it on `----------`, removes empty postings.
- **`extractors.py`** — one function per field, using Regex on the raw posting text.
- **`cleaner.py`** — calls the extractors for each posting and builds a Pandas DataFrame with correctly typed numeric columns.
- **`analyzer.py`** — stipend statistics, outlier detection, skill demand, skill vs pay, using Pandas and NumPy.
- **`reports.py`** — only prints results computed elsewhere; no calculation happens here.
- **`exporter.py`** — writes the DataFrame to CSV/JSON/TXT, creating the output folder if needed.
- **`ui.py`** — the menu text and reading the user's choice.
- **`main.py`** — the menu loop that ties everything together.

## How Regex Extraction Works

Each field has its own extractor function that searches the raw posting text for a pattern. For example, work mode checks for the words "hybrid", "remote"/"work from home", or "onsite"/"work from office" (in that priority order), and skills are matched against alias lists in `config/skills.json` using word-boundary matching, so `java` never matches inside `javascript`.

## How Stipend Extraction Works

1. Only lines containing pay-related words are checked (`stipend`, `salary`, `CTC`, `compensation`, `per month`, `monthly`, `LPA`).
2. Lines mentioning fees or funding are skipped, so an application fee is never mistaken for a stipend.
3. On a pay line, patterns are tried in order: LPA range → single LPA → monthly range → single amount with currency → amount with "per month".
4. If nothing reliable is found, the stipend is left empty (`NaN`) rather than guessing.

For a range like `₹15,000 - ₹20,000`, the **midpoint** (₹17,500) is used for analysis — this is an estimate, not the real average pay.

## How LPA Conversion Works

```text
1 LPA = ₹1,00,000 per year → ₹1,00,000 / 12 per month
```

So `2.4 LPA` becomes approximately ₹20,000/month.

## How Duration Conversion Works

```text
1 month ≈ 4.3 weeks
```

So `3 months` becomes `12.9` weeks. All durations are stored in weeks for consistent comparison.

## How Pandas Is Used

Pandas builds the structured table from extracted records, converts stipend columns to numeric (turning missing values into `NaN` with `pd.to_numeric(..., errors="coerce")`), filters rows for search, groups skills with `.explode()` + `.value_counts()`, and exports the final table to CSV/JSON/TXT.

## How NumPy Is Used

NumPy computes the mean, median, standard deviation and percentiles (25th/75th/90th) of the stipend data, converting the cleaned Pandas Series into a NumPy array first.

## Analysis Performed

- **Stipend statistics** — count, min, max, mean, median, standard deviation, percentiles, outliers (IQR method)
- **Skill demand** — count and percentage of postings mentioning each skill
- **Skill vs pay** — median stipend per skill, only shown when at least 3 postings with a valid stipend mention that skill (otherwise `insufficient data`)
- **Extraction quality report** — counts of postings with missing stipend, ambiguous pay status, missing duration, unmentioned work mode, no detected skills, missing location or job type

## CLI Options

```text
1. Load postings
2. Extraction quality report
3. Stipend statistics
4. Skill demand
5. Skill vs pay
6. Search / filter postings
7. Export CSV / JSON / TXT
8. Exit
```

Selecting an analysis option before loading data shows a message instead of crashing. Invalid menu input is handled.

## Installation

```bash
pip install -r requirements.txt
```

## Running the Project

```bash
python main.py
```

Choose option 1 to load data. If `.txt` files exist in `data/raw/`, they are read automatically; otherwise the bundled sample data is used.

## Sample Data

`data/sample/postings.txt` contains 10 synthetic postings written for this project, covering paid/unpaid postings, monthly and LPA pay, ranges, and both remote/hybrid/onsite work modes. Running the stipend report on this sample gives:

```text
Valid stipend postings: 8
Mean: ₹21,562.50 | Median: ₹17,750.00 | Std Dev: ₹17,184.79
25th percentile: ₹11,500.00 | 75th: ₹20,625.00 | 90th: ₹34,500.00
Outliers: [62500.0]
```

Real postings can be added as `.txt` files inside `data/raw/` (see "Providing Real Data" below).

## Providing Real Data

You don't need to combine every posting into one file by hand. Place any number of `.txt` files inside `data/raw/` — for example, one file per website you copied postings from, with individual postings inside each file separated by `----------`. The loader automatically reads every `.txt` file in that folder. If `data/raw/` is empty, the program falls back to the bundled sample data, so the demo always works.

## Output/Export Formats

Exporting (option 7) writes the current DataFrame to:

```text
data/output/postings.csv
data/output/postings.json
data/output/postings.txt
```

The `data/output/` folder is created automatically if it doesn't exist and is not tracked by Git.

## Testing

Tests use Python's built-in `assert` — no extra library.

```bash
python tests/test_extractors.py
python tests/test_pipeline.py
```

`test_extractors.py` checks each Regex extractor individually (stipend formats, unrelated numbers, duration, work mode, job type, pay status, skills, location). `test_pipeline.py` checks the loader, DataFrame construction, outlier detection, skill demand/pay rules, NumPy statistics and export.

## Limitations

OfferScope is a V1 educational project.

- **Small sample size** — results are indicative, not representative of the real job market.
- **Undisclosed stipend bias** — statistics only use postings with a valid extracted stipend.
- **Regex limitations** — unusual wording can be missed; work mode and duration are matched anywhere in the text (no negation handling, e.g. "not remote").
- **No required vs nice-to-have distinction** — all detected skills are treated equally in V1.
- **Midpoint estimation** — a stipend range's midpoint is an estimate, not the true average.
- **LPA conversion assumption** — `1 LPA = ₹1,00,000/year`.
- **Duration approximation** — `1 month ≈ 4.3 weeks`.
- **Internships and jobs analyzed together** — a full-time job's converted LPA can appear as an outlier among internship stipends.
- **Duplicates not removed** — a posting pasted twice is counted twice.

## Future Improvements

- Separate statistics for internships vs full-time jobs
- Duplicate posting detection
- Required vs nice-to-have skill distinction
- More cities and skill aliases in the config files
- Better handling of yearly (non-LPA) rupee amounts

## Author

**Devendra Kumawat**
B.Tech CSE Student, Arya College of Engineering, Jaipur
