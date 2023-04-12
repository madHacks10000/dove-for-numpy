dove-backend 🕊️
================================================

This repository provides a prototype implementation of the Data-Oblivious Virtual Environment (DOVE) backend. You can read more about this in our academic research paper, [DOVE: A Data-Oblivious Virtual Environment](https://www.ndss-symposium.org/ndss-paper/dove-a-data-oblivious-virtual-environment/), which appeared in NDSS 2021.

This is **research code**, and has not been certified for production use. That being said, if you see something, [say something](https://github.com/dove-project/dove-backend/issues)!

Building the DOVE backend
----------------------------------
### Prerequisites
Our current backend prototype assumes that a frontend generated a DOT that is stored at ``../dove-frontend-r/src/instr.asm``.
If DOT is stored in a different directory, please edit the global variable ``ASSEMBLY_PATH`` in ``src/App/App.cpp``. 
Likewise, the current implementation assumes that the secret data is stored in plaintext at ``examples/``. To ensure confidentiality and authenticity of the data, please employ TLS (or similar) to transfer data.

We built and tested the backend on following specs:
- Intel Skylake Core i3-6100 CPU
- 1 TB HDD
- 24 GB of RAM
- Ubuntu 18.04.4 LTS
- Intel SGX Linux Driver 2.9.1
- g++ compiler

Also, the following tools/packages are required to build the backend:
- `python2` and package `mpmath`
  - Our version of [`libfixedtimefixedpoint`](https://github.com/kmowery/libfixedtimefixedpoint) uses an old version of Python. We plan on moving to the more recent Python 3 version in a future release.

### Build instructions
We provide two makefiles to build our backend (1) with or (2) without running inside of an Intel SGX enclave. 

To build the backend without SGX, use the following:
```sh
cd src
make -f Makefile.base all
```

To build the backend with SGX, you first need to ensure whether your system has the Linux Intel SGX software stack. Please refer to the [Intel SGX GitHub repository](https://github.com/intel/linux-sgx) for more details.

To build the backend with SGX, use the following:
```sh
cd src
make -f Makefile.sgx all
```

Running the backend
------------------------------
Assuming that the DOT is already generated from the frontend, use the following to run the backend without SGX.
```sh
cd src
./splitapp
```
Likewise, to run the backend with SGX, use the following:
```sh
cd src
./app
```

If a DOT contains a `print` instruction, then our current prototype outputs the argument of print as plaintext named ``result_X.data`` (where ``X`` is a counter that begins with 0) in ``examples/``. To ensure confidentiality and authenticity of the data, please employ TLS (or similar) to transfer data.

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
