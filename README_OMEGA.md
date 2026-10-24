# Information requirements for fossil-fuel retirement decisions

This package contains the analysis code, data, tests and figure inputs for the
accompanying paper. The complete analysis is in
`Retirement_information_analysis.zip`; the other files provide its run entry,
dependencies, citation information and checksums.

## Run the analysis

Download these files into one local directory. Use Python 3.12 in an isolated
environment, then run:

```sh
python -m pip install -r requirements_omega.txt
python reproduce_omega.py --mode check
python reproduce_omega.py --mode tests
python reproduce_omega.py --mode verify
python reproduce_omega.py --mode rerun
```

The launcher checks the archive checksum and extracts it into `_omega_analysis`
on your computer. It forwards the selected mode to the original analysis entry
point. No manual extraction is needed. GitHub stores the ZIP as a file; running
the launcher locally creates the analysis directories.

`check` validates the analysis inputs. `tests` runs the 228 scientific and
packaging tests. `verify` checks the existing results, and `rerun` recomputes
the 21 scientific products and compares them with the supplied expected results.
Reports are written under
`_omega_analysis/retirement-information/run_results/`.

The reference environment is Python 3.12.4, NumPy 2.2.6, SciPy 1.18.0 and
HiGHS 1.12.0. Solver/platform changes can affect tied selections; the recorded
environment supports the exact-result comparison.

## Data and scope

The annual calculations start from the documented processed panels, including
152 paired observations for 65 generators from the larger 296-generator cohort.
The case calculations use daily operating records and documented conditions
for Campbell, Brandon Shores and Rush Island. The package includes source URLs,
page locators, input specifications, expected outputs and six figure PDFs.
It does not repeat the upstream national EIA and CEMS data reconstruction.

The original source code and directory structure are retained inside the ZIP.
Its README describes the inputs, numerical checks, provenance and source terms.
No commercial solver or account is required to run the supplied analyses.

## Files

- `reproduce_omega.py`: archive check, local extraction and analysis launcher.
- `Retirement_information_analysis.zip`: complete analysis code and inputs.
- `requirements_omega.txt`: recorded Python dependencies.
- `CITATION_OMEGA.cff`: author and citation metadata for this analysis.
- `OMEGA_MANIFEST.json`: file sizes and SHA256 checksums.

The Omega-specific file names allow this package to coexist with the earlier
analyses in the same repository. Use this entry point for the accompanying
retirement-information paper.
