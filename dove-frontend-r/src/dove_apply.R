apply.default = base::apply # assign default as current definition
apply = function(X, MARGIN, FUN, ...) {
    UseMethod("apply")
}

apply.dove_matrix <- function(X, MARGIN, FUN, ...) {
    dove.apply(X, MARGIN, FUN, ...)  # don't want to break existing API
}

dove.apply <- function(X, MARGIN, FUN, ...) {
    stopifnot(inherits(X, "dove_matrix"))
    # op_string <- "mapply"
    if (MARGIN == 1) {
        # op_string <- "rapply"
        # applied_mtx <- new_dove_matrix(list(), c(nrow(X), 1))
        applied_mtx <- dove.matrix(nrow=nrow(X), ncol=1)
        dove.for(1, nrow(X), 1, function(i) {
            to_append <- FUN(X[i,], ...)
            applied_mtx[i] <- to_append
        })
        applied_mtx
    } else if (MARGIN == 2) {
        # op_string <- "capply"
        # applied_mtx <- new_dove_matrix(list(), c(ncol(X), 1))
        applied_mtx <- dove.matrix(nrow=ncol(X), ncol=1)
        dove.for(1, ncol(X), 1, function (j) {
            to_append <- FUN(X[,j], ...)
            applied_mtx[j] <- to_append
        })
        applied_mtx
    } else {
        stop("undefined margin")
    }
}
