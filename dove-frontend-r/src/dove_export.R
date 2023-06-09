library(Rcpp)
sourceCpp("dove_expt.cpp")

dove.export_data <- function(fname, m) {
    exportData(fname, m)
}
