
which.default = base::which # assign default as current definition
which = function(x, arr.ind = FALSE, useNames = TRUE) { # make S3
    UseMethod("which")
}

which.dove_matrix <- function(x, arr.ind = FALSE, useNames = TRUE) {
    attr(x, "which") <- TRUE
    x
}

intersect.default = base::intersect # assign default as current definition
intersect = function(x, y) { # make S3
    UseMethod("intersect")
}
intersect.dove_matrix <- function(x, y) {
    z <- (x & y)
    if (attr(x, "which")) {
        attr(z, "which") <- TRUE
    }
    z
}
