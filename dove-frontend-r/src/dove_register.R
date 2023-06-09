dove_register_counter <- 1

new_dove_register <- function() {
    reg <- structure(list(dove_register_counter), class = "dove_register")
    # We want to update the parent scope.
    dove_register_counter <<- dove_register_counter + 1
    # We make no distinction between matrix references and scalar references. 
    reg
}

toString.dove_register <- function(x) {
    sprintf("%%%d", x[[1]])
}

