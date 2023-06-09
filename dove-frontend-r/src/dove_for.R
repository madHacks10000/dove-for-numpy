dove_for_index_counter <<- 1

new_dove_for_index <- function(min_max) {
    idx <- structure(list(min_max), class = "dove_for_index")
    attr(idx, "id") <- dove_for_index_counter
    # We want to update the parent scope.
    dove_for_index_counter <<- dove_for_index_counter + 1
    idx
}

toString.dove_for_index <- function(x) {
    sprintf("\\%d", attr(x, "id"))
}

length.dove_for_index <- function(x) {
    # TODO: check for correctness here
    1
}

print.dove_for_index <- function(x) {
    cat(sprintf("print %s", toString(x)), file=INSTR_FILE, append=TRUE, sep='\n')
    print(toString(x))
}
cat.dove_for_index <- cat.dove_matrix

# TODO: Overload `seq` and `:` functions for for_index

Ops.dove_for_index <- function(e1, e2) {
    # TODO: Allow more types of ops.
    .Generic <- match.arg(.Generic, c("+", "-", "*", "/", "^", "==", ">", "<", "<=", ">=", "!=", "!", "&", "|", "%%", "%/%", "%*%"))
    if (!(.Generic %in% c("==", ">", "<", "<=", ">=", "!="))) {
        if (missing(e2)) {
            op_string <- sprintf("%s %s", .Generic, toString(e1))
        } else {
            if (inherits(e1, "numeric")) {
                e1 = dove.wrap(e1)
            }
            if (inherits(e2, "numeric")) {
                e2 = dove.wrap(e2)
            }
            op_string <- sprintf("%s %s %s", .Generic, toString(e1), toString(e2))
        }
        cat(op_string, file=INSTR_FILE, append=TRUE, sep='\n')
        if (inherits(e1, "dove_for_index")) {
            e1 <- unlist(e1)  
        }
        if (inherits(e2, "dove_for_index")) {
            e2 <- unlist(e2)  
        }
        cz = NextMethod()
        rtvl = new_dove_for_index(c(cz[[1]], cz[[2]]))
        cat(sprintf("indexvar %s", toString(rtvl)), file=INSTR_FILE, append=TRUE, sep='\n')
        rtvl
    } else {
        if (inherits(e1, "dove_for_index")) {
            e1 <- unlist(e1)  
        }
        if (inherits(e2, "dove_for_index")) {
            e2 <- unlist(e2)  
        }
        NextMethod()
    }
}

# TODO: figure out a way for loop variables to enter the global environment
# TODO: type checks for the from/to/step
# TODO: handle the case where step is also a former loop index
dove.for <- function(from, to, step, loop) {
    idx <- new_dove_for_index(c(from[[1]][[1]], to[[1]][[1]]))  # in case a second index is used
    # TODO inefficient
    push_file <- INSTR_FILE
    INSTR_FILE <<- nullfile()
    
    # Save register values to prevent double incrementation
    tmp_for_idx_ctr <- dove_for_index_counter
    tmp_reg_ctr <- dove_register_counter
    tmp_mtx_ctr <- dove_matrix_counter

    dry_run <- try(loop(idx), TRUE)
    INSTR_FILE <<- push_file

    # Restore registers back
    dove_for_index_counter <<- tmp_for_idx_ctr
    dove_register_counter <<- tmp_reg_ctr
    dove_matrix_counter <<- tmp_mtx_ctr

    if (class(dry_run) == 'try-error') {
        # Dry run failed, run as normal loop
        dove_for_index_counter <<- dove_for_index_counter - 1
        # print(sprintf("[dry run error] %s", dry_run[[1]]))  # DEBUG
        for (i in seq(from, to, step)) {
            loop(i)
        }
    } else {
        # Dry run passed
        cat(sprintf("forloop [%s:%s:%s] %s", toString(from), toString(to), toString(step), toString(idx)), file=INSTR_FILE,
                append=TRUE, sep='\n')
        loop(idx)
        cat(sprintf("endloop %s", toString(idx)), file=INSTR_FILE, append=TRUE, sep='\n') 
    }
}
