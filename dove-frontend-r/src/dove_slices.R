sequence_parse <- function(seq_name) {
    if (any(class(seq_name) == "dove_for_index")) {
        # TODO: from:to:step sequences using for indicies
        result_str = sprintf("%s", toString(seq_name))
    } else {
        if (is.na(diff(seq_name)[1])) {
            result_str = sprintf("%d", seq_name[1])
        } else if (all(diff(seq_name) == diff(seq_name)[1])) {
            result_str <- sprintf("%d:%d:%d", seq_name[1], tail(seq_name, n=1), diff(seq_name)[1])
        } else {
            result_str <- cat(seq_name, sep=',') 
        }
    }
    sprintf("[%s]", result_str)
}

`[.dove_matrix` <- function(mtx, i, j, ..., drop = TRUE) {
    var_args <- list(...)
    # TODO: Negative integers exclude
    if (missing(i)) {
        i <- 1:dim(mtx)[1]
    }

    if (missing(j)) {
        j <- 1:dim(mtx)[2]
    }

    if (inherits(i, "dove_matrix") || inherits(j, "dove_matrix")) {
        # Data dependent computation.
        # stop("cannot slice into a pseudonym matrix with another matrix")
        nrow_iter <- nrow(mtx)
        ncol_iter <- ncol(mtx)

        result_mtx <- matrix(nrow = nrow_iter, ncol = ncol_iter)
        dove.for(1, nrow_iter, 1, function(idx_i) {
            dove.for(1, ncol_iter, 1, function(idx_j) {
                if (ncol(i) == 1) {
                    result_mtx[idx_i, idx_j] <- ifelse(i[[idx_i,1]] != 0, mtx[[idx_i,idx_j]], NA)
                } else if (nrow(j) == 1) {
                    result_mtx[idx_i, idx_j] <- ifelse(j[[1,idx_j]] != 0, mtx[[idx_i,idx_j]], NA)
                } else {
                    result_mtx[idx_i, idx_j] <- ifelse(i[[idx_i,idx_j]] != 0, mtx[[idx_i,idx_j]], NA)
                }
            })
        })
        return(result_mtx)
    }

    row_seq <- i
    col_seq <- j

    # HACK?
    if (length(row_seq) == 1 & length(col_seq) == 1) {
        return(mtx[[i,j]])
    }

    # handle dimnames case
    if (is.character(i)) {
        rnames <- rownames(mtx)
        if (is.null(rnames)) {
            stop("matrix does not have rownames")
        }
        row_seq <- NULL
        # TODO inefficient
        for (i_idx in 1:length(i)) {
            for (row_idx in 1:length(rnames)) {
                if (rnames[[row_idx]] == i[[i_idx]]) {
                    row_seq <- append(row_seq, row_idx)
                }
            }
        }
    }
    if (is.character(j)) {
        cnames <- colnames(mtx)
        if (is.null(cnames)) {
            stop("matrix does not have colnames")
        }
        col_seq <- NULL
        # TODO inefficient
        for (j_idx in 1:length(j)) {
            for (col_idx in 1:length(cnames)) {
                if (cnames[[col_idx]] == j[[j_idx]]) {
                    col_seq <- append(col_seq, col_idx)
                }
            }
        }
    }


    if (any(row_seq > dim(mtx)[1]) || any(row_seq < -dim(mtx)[1])) {
        stop("row subscript out of bounds")
    }

    if (any(col_seq > dim(mtx)[2]) || any(col_seq < -dim(mtx)[2])) {
        stop("column subscript out of bounds")
    }

    if (all(row_seq < 0) && all(col_seq < 0)) {
        stop("must select at least one element")
    }

    prev_id <- attr(mtx,"id")
    const <- `if`(attr(mtx, "const"), "const ", "")
    matrix_id <- dove_matrix_counter
    cat(sprintf("slice %s$%d %s %s $%d", const, prev_id, sequence_parse(row_seq), sequence_parse(col_seq), matrix_id), file=INSTR_FILE, append=TRUE, sep='\n') 
    dove_matrix_counter <<- dove_matrix_counter + 1
    structure(list(nrow=length(row_seq), ncol=length(col_seq)), id=matrix_id, const=attr(mtx, "const"), class = "dove_matrix")
    # result
}

`[[.dove_matrix` <- function(mtx, ...) {
    var_args <- list(...)
    # TODO: We don't support > 2D matrices.
    if (length(var_args) > length(dim(mtx)) || length(var_args) > 2) {
        stop("incorrect number of subscripts")
    }
    # TODO: handle this check in the for_index case
    # if (any(var_args < 0)) {
    #     stop("can only select exactly 1 element")
    # }

    i <- var_args[[1]]
    # handle dimnames case
    if (is.character(i)) {
        rnames <- rownames(mtx)
        if (is.null(rnames)) {
            stop("matrix does not have rownames")
        }
                                        # TODO inefficient
        for (row_idx in 1:length(rnames)) {
            if (rnames[[row_idx]] == i) {
                i <- row_idx
                break
            }
        }
    }
    stopifnot(i <= dim(mtx)[1])  # type system prevents us from using secret value

    j <- 0
    if (length(var_args) == 1) {
        if(is.character(var_args[[1]])) {
            j <- 1 #TODO: this is a hack
        } else {
        i <- ((i-1) %/% nrow(mtx)) + 1
        j <- ((i-1) %% nrow(mtx)) + 1
        }
    } else {
        j <- var_args[[2]]
        # handle dimnames case
        if (is.character(j)) {
            cnames <- colnames(mtx)
            if (is.null(cnames)) {
                stop("matrix does not have colnames")
            }
            # TODO inefficient
            for (col_idx in 1:length(cnames)) {
                if (cnames[[col_idx]] == j) {
                    j <- col_idx
                    break
                }
            }
        }
    }

    stopifnot(j <= dim(mtx)[2])

    new_dove_pointer(name=attr(mtx, "id"), row=i, col=j)
}

`[<-.dove_matrix` <- function(mtx, i, j, value, ...) {
    if (missing(i)) {
        i <- 1:dim(mtx)[1]
    }

    if (missing(j)) {
        j <- 1:dim(mtx)[2]
    }

    if ((inherits(value, "logical")) && is.na(value)) {
        value <- dove.wrap(NaN)
    }
    
    # if ((class(value) == "dove_matrix") && (length(i) > 1 || length(j) > 1)) {
    if ((inherits(value, "dove_matrix"))) {
        # TODO: handle updating sequences with `for_index`
        if (inherits(i,"dove_for_index") || inherits(j, "dove_for_index")) {
        } else {
            stopifnot(nrow(value) == length(i), ncol(value) == length(j))
        }
    } else {
        value <- dove.wrap(value)
        match.arg(class(value), c("dove_pointer", "dove_value", "dove_register", "dove_for_index"))
    }


    if (inherits(i, "dove_matrix")) {
        stopifnot(identical(dim(mtx), dim(i)))
        cat(sprintf("update $%d $%d ", attr(mtx, "id"), attr(i, "id")), file=INSTR_FILE, append=TRUE, sep='')
    } else {
        cat(sprintf("update $%d %s %s ", attr(mtx, "id"), sequence_parse(i), sequence_parse(j)), file=INSTR_FILE, append=TRUE, sep='') 
    }
    cat(sprintf("%s", toString(value)), file=INSTR_FILE, append=TRUE, sep='\n')
    invisible(mtx)
}

