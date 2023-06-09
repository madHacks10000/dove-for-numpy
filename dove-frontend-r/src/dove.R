# dove.R
# A wrapped representation of a secret value in DOVE.

# Initalize register tracking.
source('dove_register.R')

# Allow pointers to datasets.
source('dove_pointer.R')

# Enable the creation of scalar values.
source('dove_value.R')

# Handle matrix-related operations.
source('dove_matrix.R')

# Load statistcal methods for pseudonyms.
source('dove_stats.R')

# Provide basic support for conditionals.
source('dove_if.R')

# Provide basic support for iteration.
source('dove_for.R')

# Emulate apply functionality.
source('dove_apply.R')

# Create pseudonyms from configuration.
source('dove_config.R')

# Allow dataset exporting (requires Rcpp)
source('dove_export.R')

# Summary Generic Functions
# commented out atm due to performance concerns
#source('dove_summary.R')

# HACK for R 3.4.4
nullfile <- function() {
    return("/dev/null")
}
