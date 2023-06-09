# Create S3 class for use with DOVE, promoting types of base R structure.
dove.wrap <- function(x) {
    # Ignore if the class is already a DOVE value
    if (inherits(x, "dove_matrix") || inherits(x, "dove_pointer") || inherits(x, "dove_value") ||  inherits(x, "dove_register")) {
        return(x)
    }

    # Allow the wrapping of a for_index into a register for computation
    if (inherits(x, "dove_for_index")) {
        cat(sprintf("+ %s", toString(x)), file=INSTR_FILE, append=TRUE, sep='\n') 
        cat(sprintf("set %%%d", dove_register_counter), file=INSTR_FILE, append=TRUE, sep='\n')
        return(new_dove_register())
    }

    # Get this out of the way
    if (is.na(x)) {
        return(structure(NaN, class = "dove_value"))
    }

    # First, find out if it's a matrix
    if (is.matrix(x)) {
        # Use dove.matrix to convert this matrix into a secret matrix
        return(dove.matrix(data = x, nrow = nrow(x), ncol = ncol(x)))
    }

    if (is.logical(x)) {
        x <- if (x) 1 else 0
    }

    # Now we want to see if it's a scalar vector or a single number
    stopifnot(is.numeric(x))
    if (length(x) > 1) {
        return(dove.matrix(data = x, nrow = length(x)))
    }

    # It's a number!
    structure(x, class = "dove_value")
}

toString.dove_value <- function(x) {
    sprintf("#%.17g", x)
}
