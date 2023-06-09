ifelse.default = base::ifelse # assign default as current definition
ifelse = function(test, yes, no) { # make S3
    UseMethod("ifelse")
}

ifelse.dove_matrix <- function (cond, if_true, if_false) {
    stopifnot(!inherits(if_true, "logical") || is.na(if_true)) 
    stopifnot(!inherits(if_false, "logical") || is.na(if_false))

    if_true <- dove.wrap(if_true)
    if_false <- dove.wrap(if_false)

    match.arg(class(cond), c("dove_matrix", "dove_pointer", "dove_value", "dove_register"))
    # We need the "logical" class for NA
    match.arg(class(if_true), c("dove_matrix", "dove_pointer", "dove_value", "dove_register", "logical", "dove_for_index"))
    match.arg(class(if_false), c("dove_matrix", "dove_pointer", "dove_value", "dove_register", "logical", "dove_for_index"))

    if (class(cond) == "dove_matrix") {
        stopifnot(class(cond) == class(if_false))
        stopifnot(identical(dim(cond), dim(if_false)))
    }

    if (class(if_false) == "dove_matrix") {
        stopifnot(class(if_true) == class(if_false))
        stopifnot(identical(dim(if_true), dim(if_false)))
    }

    if ((class(if_true) == "logical") && is.na(if_true)) {
        if_true <- dove.wrap(NaN)
    }

    if ((class(if_false) == "logical") && is.na(if_false)) {
        if_false <- dove.wrap(NaN)
    }

    result <- +if_false
    cat(sprintf("ifelse %s %s %s", toString(cond), toString(if_true), toString(result)), file=INSTR_FILE, append=TRUE, sep='\n') 
    if (class(if_false) == "dove_matrix") {
        result
    } else {
        cat(sprintf("set %%%d", dove_register_counter), file=INSTR_FILE, append=TRUE, sep='\n')
        new_dove_register()
    }
}

ifelse.dove_pointer <- ifelse.dove_matrix
ifelse.dove_register <- ifelse.dove_matrix
ifelse.dove_value <- ifelse.dove_matrix

# TODO: dove_if_matrix -- takes in a logical matrix, and then checks to
# see where that matrix is 1/0. For 1 (true), place the corresponding
# index value from the if_true part; else for 0 (false) place the
# corresponding index value from the if_false part. Necessarily, if_true
# and if_false must have the same dimensions as each other and the
# destination (checked in `[<-`). They can be scalars -- the matrix is
# just filled with them instead. This is another way we can reduce the
# load on the transcript. 
