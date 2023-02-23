# top-refs-from-paper
Quick and simple Python script processing the most cited `length` references from the `depth` generation of the citation tree using the Crossref API.

# Usage
Download the `ranking.py` script and run it in Windows Powershell via the below command:
```
python ranking.py --doi {*str* DOI} --depth {*int* depth} --length {*int* length}
```
For example:
```
python ranking.py --doi https://doi.org/10.1016/j.susc.2005.05.030 --depth 3 --length 100
```
