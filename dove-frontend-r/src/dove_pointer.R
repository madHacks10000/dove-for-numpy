# Create S3 class dove_pointer position (row, col) in dataset name.
# TODO: change interface
new_dove_pointer <- function(name, row, col) {
    structure(list("name"=name, "row"=row, "col"=col), class = "dove_pointer")
}

print.dove_pointer <- function(x, ...) {
    cat(toString(x), sep='\n')
    invisible(x)
}

toString.dove_pointer <- function(x, ...) {
    sprintf("$%d@(%s,%s)", x$name, toString(x$row), toString(x$col))
}

