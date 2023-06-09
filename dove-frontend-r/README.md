dove-frontend-r 🕊️ 
================================================

This repository provides a prototype implementation of the Data-Oblivious Virtual Environment (DOVE) frontend for the R language. You can read more about this in our academic research paper, [DOVE: A Data-Oblivious Virtual Environment](https://www.ndss-symposium.org/ndss-paper/dove-a-data-oblivious-virtual-environment/), which appeared in NDSS 2021.

This is **research code**, and has not been certified for production use. That being said, if you see something, [say something](https://github.com/dove-project/dove-frontend-r/issues)!

Running the frontend
------------------------------

### Prerequisites

[Install the following R packages](https://cran.r-project.org/doc/manuals/r-release/R-admin.html#Installing-packages) to run the DOVE frontend:

- `rlang`
- `readr`
- `Rcpp`

### Running R Benchmarks

The ``examples`` folder contains R benchmark scripts that we used for evaluation. The ``ec-modified`` and ``pagerank`` folders contain scripts that use DOVE primitives directly, so you can simply run them on frontend by entering the following command:

```sh
cd src
R -f PATH_TO_SCRIPT
```

This will create a DOT in the file `instr.asm`. 

Meanwhile, the scripts in the ``ec-original`` folder are benchmarks unmodified from their [source](https://github.com/ekfchan/evachan.org-Rscripts). Thus, they require (automatic) transformation to use DOVE primitives to generate DOTs. For these scripts, run them on frontend by entering the following command:

```sh
cd src
R -f dove_automate.R --args PATH_TO_SCRIPT
```

In general, unmodified R scripts can typically be run with the above R invocation. While we do not claim complete coverage, the frontend transforms a number of functions that perform matrix operations. Please refer to [our paper](https://www.ndss-symposium.org/ndss-paper/dove-a-data-oblivious-virtual-environment/) for more details.

Citation
---------------
If you make any use of this code for academic purposes, please cite as:

```tex
@inproceedings{lee2021dove,
  author = {Hyun Bin Lee and Tushar M. Jois and Christopher W. Fletcher and Carl A. Gunter},
  title = {{DOVE: A Data-Oblivious Virtual Environment}},
  booktitle = {Network and Distributed System Security Symposium (NDSS)},
  year = {2021}
}
```
