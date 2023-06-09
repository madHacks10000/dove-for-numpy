operated_dove_matrix <- function(dims, op_string, dimnames = NULL) {
    matrix_id <- dove_matrix_counter
    cat(sprintf("def $%d [1:%d] [1:%d]", matrix_id, dims[1],
                dims[2]), file=INSTR_FILE, append=TRUE, sep='\n') 
    cat(sprintf("\t%s", op_string), file=INSTR_FILE, append=TRUE, sep='\n') 
    cat(sprintf("end $%d", matrix_id), file=INSTR_FILE, append=TRUE, sep='\n') 
    dove_matrix_counter <<- dove_matrix_counter + 1
    structure(list(nrow=dims[1], ncol=dims[2], dimnames = dimnames), id=matrix_id, const=FALSE, class = "dove_matrix")
}

Math.dove_matrix <- function(x, ...) {
    var_params <- list(...)
    match.arg(class(x), c("dove_matrix", "dove_pointer", "dove_value", "dove_register"))
    if (length(var_params) == 0) { #unary math
        op_string <- sprintf("%s %s", .Generic, toString(x))
    } else if (length(var_params) == 1) { #binary math
        y <- var_params[[1]]
        match.arg(class(y), c("dove_matrix", "dove_pointer", "dove_value", "dove_register"))
        op_string <- sprintf("%s %s %s", .Generic, toString(x), toString(y))
    } else {
        stop("cannot pass more than 2 arguments")
    }
    # TODO: For the math operations, we may have to create a new variable with
    # the result of the operation. We also need to keep track of updates to
    # variables somehow. Note that we can safely ignore the addition of two
    # scalar values if they don't go into a variable. This will probably
    # involve some manual messing around with reference values for each of the
    # Secret objects -- one calculation is one modification!

    if (inherits(x, "dove_matrix")) {
        operated_dove_matrix(dim(x), op_string, dimnames = x$dimnames)
    } else {
        cat(op_string, file=INSTR_FILE, append=TRUE, sep='\n') 
        cat(sprintf("set %%%d", dove_register_counter), file=INSTR_FILE, append=TRUE, sep='\n')
        new_dove_register()
    }
}

Math.dove_pointer <- Math.dove_matrix
Math.dove_register <- Math.dove_matrix
Math.dove_value <- Math.dove_matrix

Summary.dove_matrix <- function(..., na.rm = FALSE) {
    va_list <- list(...)
    op_string <- sprintf("%s%s %s", .Generic, if (na.rm) "|NA" else "",
        paste(sapply(va_list, toString), collapse = ' ') )

    if (.Generic == "range") {
        operated_dove_matrix(c(2,1), op_string)
    } else {
        cat(op_string, file=INSTR_FILE, append=TRUE, sep='\n')
        cat(sprintf("set %%%d", dove_register_counter), file=INSTR_FILE, append=TRUE, sep='\n')
        new_dove_register()
    }
}

Summary.dove_pointer <- Summary.dove_matrix
Summary.dove_register <- Summary.dove_matrix
Summary.dove_value <- Summary.dove_matrix

pmin.default = base::pmin # assign default as current definition
pmin = function(..., na.rm = FALSE) { # make S3
    UseMethod("pmin")
}

pmin.dove_matrix <- function(..., na.rm = FALSE) {
    va_list <- list(...)
    stopifnot(length(va_list) > 0)
    dims <- dim(va_list[[1]])
    for (item in va_list) {
         stopifnot(identical(dim(item), dims))
    }
    
    ret <- +va_list[[1]]
    nrow <- nrow(ret)
    ncol <- ncol(ret)
    dove.for(1,nrow,1,function(j) {
        dove.for(1,ncol,1,function(k) {
            tmp <- dove.matrix(nrow=length(va_list))
            for(i in 1:length(va_list)) {
                curr <- va_list[[i]]
                tmp[i,1] <- curr[[j,k]]
            }
            ret[j,k] <- min(tmp, na.rm=na.rm)
        })
    })
    
    ret
}

pmax.default = base::pmax # assign default as current definition
pmax = function(..., na.rm = FALSE) { # make S3
    UseMethod("pmax")
}

pmax.dove_matrix <- function(..., na.rm = FALSE) {
    va_list <- list(...)
    stopifnot(length(va_list) > 0)
    dims <- dim(va_list[[1]])
    for (item in va_list) {
        stopifnot(identical(dim(item), dims))
    }

    ret <- +va_list[[1]]
    nrow <- nrow(ret)
    ncol <- ncol(ret)
    dove.for(1,nrow,1,function(j) {
        dove.for(1,ncol,1,function(k) {
            tmp <- dove.matrix(nrow=length(va_list))
            for(i in 1:length(va_list)) {
                curr <- va_list[[i]]
                tmp[i,1] <- curr[[j,k]]
            }
            ret[j,k] <- max(tmp, na.rm=na.rm)
        })
    })
    ret
}

Ops.dove_matrix <- function(e1, e2) {
    # TODO: Allow more types of ops.
    .Generic <- match.arg(.Generic, c("+", "-", "*", "/", "^", "==", ">", "<", "<=", ">=", "!=", "!", "&", "|", "%%", "%/%", "%*%"))
    if (missing(e2)) {
        op_string <- sprintf("%s %s", .Generic, toString(e1))
        if (inherits(e1, "dove_matrix")) {
            new_op_matrix <- operated_dove_matrix(dim(e1), op_string, dimnames = e1$dimnames)
            if (!is.null(attr(e1, "which"))) {
                attr(new_op_matrix, "which") <- TRUE
            }
            new_op_matrix
        } else {
            cat(op_string, file=INSTR_FILE, append=TRUE, sep='\n') 
            cat(sprintf("set %%%d", dove_register_counter), file=INSTR_FILE, append=TRUE, sep='\n')
            new_dove_register()
        }
    } else {
        e1 <- dove.wrap(e1)
        e2 <- dove.wrap(e2)
        match.arg(class(e1), c("dove_matrix", "dove_pointer", "dove_value", "dove_register"))
        match.arg(class(e2), c("dove_matrix", "dove_pointer", "dove_value", "dove_register"))
        op_string <- sprintf("%s %s %s", .Generic, toString(e1), toString(e2))
        if (inherits(e1, "dove_matrix") || inherits(e2, "dove_matrix")) {
            is_same_class <- inherits(e1, "dove_matrix") == inherits(e2, "dove_matrix")
            is_diff_dim <- !identical(dim(e1), dim(e2))
            is_not_multiple <- if (length(dim(e1)) > length(dim(e2)))
                length(dim(e1)) %% length(dim(e2))
                else length(dim(e2)) %% length(dim(e1))
            if (is_same_class && is_diff_dim && is_not_multiple) {
                stop("non-conformble dove matrices")
            }
            operated_dove_matrix(if (inherits(e1, "dove_matrix")) dim(e1) else dim(e2), op_string, if (inherits(e1, "dove_matrix")) dimnames(e1) else dimnames(e2))
        } else {
            cat(op_string, file=INSTR_FILE, append=TRUE, sep='\n') 
            cat(sprintf("set %%%d", dove_register_counter), file=INSTR_FILE, append=TRUE, sep='\n')
            new_dove_register()
        }
    }
}

Ops.dove_pointer <- Ops.dove_matrix
Ops.dove_register <- Ops.dove_matrix
Ops.dove_value <- Ops.dove_matrix

is.na.dove_matrix <- function(x) {
    op_string <- sprintf("NA? %s", toString(x))
    if (class(x) == "dove_matrix") {
        operated_dove_matrix(dim(x), op_string)
    } else {
        cat(op_string, file=INSTR_FILE, append=TRUE, sep='\n') 
        cat(sprintf("set %%%d", dove_register_counter), file=INSTR_FILE, append=TRUE, sep='\n')
        new_dove_register()
    }
}

is.na.dove_pointer <- is.na.dove_matrix
is.na.dove_register <- is.na.dove_matrix
is.na.dove_value <- is.na.dove_matrix



is.nan.dove_matrix <- function(x) {
    op_string <- sprintf("NAN? %s", toString(x))
    if (class(x) == "dove_matrix") {
        operated_dove_matrix(dim(x), op_string)
    } else {
        cat(op_string, file=INSTR_FILE, append=TRUE, sep='\n') 
        cat(sprintf("set %%%d", dove_register_counter), file=INSTR_FILE, append=TRUE, sep='\n')
        new_dove_register()
    }
}
is.nan.dove_pointer <- is.nan.dove_matrix
is.nan.dove_register <- is.nan.dove_matrix
is.nan.dove_value <- is.nan.dove_matrix


is.infinite.dove_matrix <- function(x) {
    op_string <- sprintf("INF? %s", toString(x))
    if (class(x) == "dove_matrix") {
        operated_dove_matrix(dim(x), op_string)
    } else {
        cat(op_string, file=INSTR_FILE, append=TRUE, sep='\n') 
        cat(sprintf("set %%%d", dove_register_counter), file=INSTR_FILE, append=TRUE, sep='\n')
        new_dove_register()
    }
#    (x == Inf) | (x == -Inf)
}
is.infinite.dove_pointer <- is.infinite.dove_matrix
is.infinite.dove_register <- is.infinite.dove_matrix
is.infinite.dove_value <- is.infinite.dove_matrix

is.finite.default = base::is.finite # assign default as current definition
is.finite = function(x) { # make S3
    UseMethod("is.finite")
}
is.finite.dove_matrix <- function(x) {
    !is.infinite(x) & !is.na(x) & !is.nan(x)
}
is.finite.dove_pointer <- is.finite.dove_matrix
is.finite.dove_register <- is.finite.dove_matrix
is.finite.dove_value <- is.finite.dove_matrix

# TODO: Could do this better
as.numeric.default = base::as.numeric # assign default as current definition
as.numeric = function(x, ...) { # make S3
    UseMethod("as.numeric")
}
as.numeric.dove_matrix <- function(x, ...) {
    x
}

cat.default = base::cat # assign default as current definition
cat = function (..., file = "", sep = " ", fill = FALSE, labels = NULL, append = FALSE) { # make S3
    UseMethod("cat")
}
cat.dove_matrix <- function(..., file = "", sep = " ", fill = FALSE, labels = NULL, append = FALSE) {
    if (identical(INSTR_FILE, nullfile())) {
        # don't print when we're in the dry run
        return()
    }
    var_params <- list(...)
    var_params[[1]] <- toString(var_params[[1]])
    base::cat(var_params[[1]], file = file, sep = sep, fill = fill, labels = labels, append = append)
}
cat.dove_pointer <- cat.dove_matrix
cat.dove_register <- cat.dove_matrix
cat.dove_value <- cat.dove_matrix

print.dove_matrix <- function(x) {
    if (identical(INSTR_FILE, nullfile())) {
        # don't print when we're in the dry run
        return()
    }
    cat(sprintf("print %s", toString(x)), file=INSTR_FILE, append=TRUE, sep='\n')
    if (inherits(x,"dove_matrix")) {
        cat(sprintf("%s%s [1:%d] [1:%d]", toString(x), 
                    `if`(attr(x, "const"), "const", ""), nrow(x), ncol(x)), sep='\n')
    } else {
        cat(toString(x), sep='\n')
    }
}

print.dove_pointer <- print.dove_matrix
print.dove_register <- print.dove_matrix
print.dove_value <- print.dove_matrix

# List things

# TODO actually find out how split works to resolve edge cases 
split.dove_matrix <- function(x, f, drop = FALSE) {
    if (drop) {
        stop("drop parameter not supported")
    }

    # this almost certainly isn't how factors work in R...
    l <- list()
    for (i in f) {
        l[[i]] <- x[i,]
    }

    class(l) <- "dove_list"  # special marker for when it's unlisted
    l
}

lapply.default = base::lapply # assign default as current definition
lapply = function(X, FUN, ...) { # make S3
    UseMethod("lapply")
}
lapply.dove_list <- function(X, FUN, ...) {
    l <- NextMethod()
    class(l) <- "dove_list"  # propagate dove_list marker
    l
}

unlist.dove_matrix <- function (x, recursive = TRUE, use.names = TRUE) {
    x
}

unlist.dove_list <- function (x, recursive = TRUE, use.names = TRUE) {
    ## TODO parameters
    stopifnot(length(x) > 0)

    nrow <- length(x)
    ncol <- length(x[1])
    unlisted <- dove.matrix(nrow = nrow, ncol = ncol)
    for (i in 1:nrow) {
        unlisted[i,] <- x[[i]]
    }
    unlisted
}

## TODO support data frame in general
data.frame <- function (..., row.names = NULL, check.rows = FALSE, check.names = TRUE,
                        fix.empty.names = TRUE, stringsAsFactors = default.stringsAsFactors()) {
    list(...)
}
