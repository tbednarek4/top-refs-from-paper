# top-refs-from-paper
Quick and simple Python script processing the most cited `length` references from the `depth` generation of the citation tree of a given paper (via `DOI`) using the Crossref API.

# Usage of the Google Colab notebook
Just click the following badge [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/tbednarek4/top-refs-from-paper/blob/main/example.ipynb) linking to the `example.ipynb` notebook showing the functionality.

# Usage on the local machine
Download the `ranking.py` script and run it via the below command (tested on the Windows Powershell terminal):
<pre>
python ranking.py --doi {<i>string</i> DOI} --depth {<i>integer</i> depth} --length {<i>integer</i> length}
</pre>
For example:
<pre>
python ranking.py --doi https://doi.org/10.1016/j.susc.2005.05.030 --depth 3 --length 100
</pre>

# Errors printed in the code output
Sometimes the Crossref does not have the further reference or there is some error within their data, so it is printed while the code is working for the manual check (i.e. one can grab those "failed" DOI-s and check their validity oneself).
