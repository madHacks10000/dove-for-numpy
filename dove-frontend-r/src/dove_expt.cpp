#include <Rcpp.h>
#include <iostream>
#include <fstream>
#include <string>

using namespace Rcpp;

// [[Rcpp::export]]
void exportData(std::string fname, NumericVector m) {
    int len = m.size();
    size_t bufsize = sizeof(double) * len;
    double* buf = (double*)malloc(bufsize);
    for(int i = 0; i < len; i++) {
        buf[i] = m[i];
    }
    std::ofstream outfile(fname.c_str(), std::ios::binary | std::ios::out);
    outfile.write((char*) buf, bufsize);
    outfile.close();
    free(buf);
}
