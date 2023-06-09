dove_matrix_counter <- 1

# Override the standard R Matrix class
matrix <- function(data = NA, nrow = 1, ncol = 1, byrow = FALSE, dimnames = NULL, rand = FALSE) {
    dove.matrix(data, nrow, ncol, byrow, dimnames, rand)
}

# Create S3 class dove_matrix with specific dove_secret data.
# new_dove_matrix <- function(data_list, dims, dataset_name = character()) {
dove.matrix <- function(data = NA, nrow = 1, ncol = 1, byrow = FALSE, dimnames = NULL, rand = FALSE) {
    matrix_id <- dove_matrix_counter
    dims <- c(nrow,ncol)

    dataset_name <- NULL
    data_list <- NULL

    if (byrow) {
        # TODO: fill by row
        stop("filling by row not supported")
    }

    # TODO ?
    # if (!is.na(data) && rand) {
    #     stop("cannot mix data and random values")
    # }

    if (is.character(data)) {
        dataset_name <- data
    # TODO: vectors unwrap dove_values
    } else if (is.list(data)|| (is.vector(data) && !is.na(data))) {
        data_list <- data
        for (item in data_list) {
            # Make sure everything is printed before matrix definition.
            force(item)
        }
    } else if (!(class(data) == "logical" && is.na(data))) {
        stop(paste("unknown data type", class(data)))
    }

    if (!rand && length(dataset_name) == 0 && length(data_list) != 0) {
        if (!is.vector(data_list) && !identical(dim(data_list), dims)) {
            if (nrow == 1 && ncol > 1) {
                dims[[1]] <- (dim(data_list)[[1]] * dim(data_list)[[2]]) / ncol
            } else if (ncol == 1 && nrow > 1) {
                dims[[2]] <- (dim(data_list)[[1]] * dim(data_list)[[2]]) / nrow
            } else {
                stop("cannot coerce dims")
            }
        }

        dim(data_list) <- dims
    }

    cat(sprintf("def $%d [1:%d] [1:%d]", matrix_id, dims[1],
                dims[2]), file=INSTR_FILE, append=TRUE, sep='\n') 
    new_mtx <- structure(list(nrow=dims[1], ncol=dims[2], dimnames=dimnames), id=matrix_id, class = "dove_matrix")

    # TODO do something more interesting with dimnames

    if (rand) {
        cat(sprintf("\trand"), file=INSTR_FILE, append=TRUE,
                sep='\n') 
        attr(new_mtx, "const") <- FALSE
    } else if (length(dataset_name) > 0) {
        cat(sprintf("\tdataset %s", dataset_name), file=INSTR_FILE, append=TRUE,
                sep='\n') 
        attr(new_mtx, "const") <- TRUE
    } else {
        if (length(data_list) == 0) {
            cat(sprintf("\tempty"), file=INSTR_FILE, append=TRUE, sep='\n')
        } else {
            for (i in 1:dims[1]) {
                row_i <- NULL
                row_len <- 0
                for (j in 1:dims[2]) {
                    item <- data_list[[i,j]]
                    item <- dove.wrap(item)
                    c_type <- as.character(class(item))
                    if (!(c_type %in% c("dove_matrix", "dove_pointer", "dove_register", "dove_value"))) {
                        stop(sprintf("incorrect data type %s for item %s\n", c_type, item))
                            break
                    }
                    row_i <- c(row_i, toString(item))
                    row_len <- row_len + (if (c_type == "dove_matrix") ncol(item) else 1)
                }
                # TODO: Consistent indexing
                if (row_len != dims[[2]]) {
                    stop("number of columns does not match provided dimensions")
                }
                cat(sprintf("\trow %d ", i), file=INSTR_FILE, append=TRUE, sep='')
                cat(row_i, file=INSTR_FILE, append=TRUE)
                cat('\n', file=INSTR_FILE, append=TRUE, sep='')
            }
        }
        attr(new_mtx, "const") <- FALSE
    }

    cat(sprintf("end $%d", matrix_id), file=INSTR_FILE, append=TRUE, sep='\n') 
    dove_matrix_counter <<- dove_matrix_counter + 1

    new_mtx
}

# Get and set dimension names
dimnames.default = .Primitive("dimnames") # assign default as current definition
dimnames = function(x) { # make S3
    UseMethod("dimnames", x)
}
dimnames.dove_matrix <- function(x) {
    x$dimnames
}

`dimnames<-.default` = .Primitive("dimnames<-") # assign default as current definition
`dimnames<-` = function(x, value) { # make S3
    UseMethod("dimnames<-", x)
}

`dimnames<-.dove_matrix` <- function(x, value) {
    stopifnot(is.list(x)) # dimnames must be lists
    stopifnot(length(value) == 2) # the list must be of size 2 (number of dims)
    stopifnot(is.null(value[[1]]) || length(value[[1]]) == nrow(x)) # the first set of dimnames (rows)
    stopifnot(is.null(value[[2]]) || length(value[[2]]) == ncol(x)) # the second set of dimnames (cols)
    x$dimnames <- value
    x
}

# String Representation
toString.dove_matrix <- function(mtx) {
    sprintf("$%d", attr(mtx, "id"))
}

# Slices/Elements of a Matrix
source('dove_slices.R')

# S3 Group Generics
source('dove_generics.R')

# Operations from <http://philender.com/courses/multivariate/notes/matr.html>
# Multiplication by a Scalar and Matrix Addition & Subtraction handled in Ops group
# Matrix Multiplication
`%*%.default` = .Primitive("%*%") # assign default as current definition
`%*%` = function(x, ...) { # make S3
    UseMethod("%*%", x)
}

`%*%.dove_matrix` <- function(e1, e2) {
    if (length(dim(e1)) != length(dim(e2)) || length(dim(e1)) > 2) {
        stop("cannot operate on non-2D matrices")
    }
    if (dim(e1)[2] != dim(e2)[1]) {
        stop("non-conformble teer matrices")
    }

    op_string <- sprintf("%s $%d $%d", "%*%", attr(e1, "id"), attr(e2, "id"))
    operated_dove_matrix(c(dim(e1)[1],dim(e2)[2]), op_string)
}

# Transpose of a Matrix
t.dove_matrix <- function(mtx) {
    # Horribly inefficient for transcript size, but shows how we can compose
    # elementary operations to provide new ones.
    t_mtx <- dove.matrix(NA, nrow=ncol(mtx), ncol=nrow(mtx))
    for (i in 1:nrow(mtx)) {
        for (j in 1:ncol(mtx)) {
            t_mtx[j,i] <- mtx[i,j]
        }
    }
    t_mtx
}

# Shadow function for rep, in the case that we're building a matrix of NA
rep <- function(x, ...) {
    var_params <- list(...)
    if (length(x) == 1 && is.na(x)) {
        dove.matrix(nrow=var_params[[1]])
    } else {
        base::rep(x, ...)
    }
}

# Conversion to a Matrix
as.matrix.dove_matrix <- function(x, ...) {
    # This does nothing but confirm that this is a matrix -- no changes here!
    return(x)
}


# TODO: Common Vectors: Unit, Zero
# TODO: Common Matrices: Unit, Zero, Diagonal, Identity, Symmetric
# TODO: Inverse & Determinant of a Matrix
# TODO: Rank of a Matrix

# Number of Rows & Columns
dim.dove_matrix <- function(mtx) {
    c(mtx$nrow, mtx$ncol)
}

`dim<-.dove_matrix` <- function(mtx, value) {
    val <- value
    stopifnot(length(val) == 2)
    stopifnot(!attr(mtx, "const"))
    stopifnot(val[[1]] * val[[2]] == nrow(mtx) * ncol(mtx))
    mtx$nrow <- val[[1]]
    mtx$ncol <- val[[2]]
    cat(sprintf("dim $%d [1:%d] [1:%d]", attr(mtx, "id"), val[[1]], val[[2]]), file=INSTR_FILE, append=TRUE, sep='\n')
    mtx
}

length.dove_matrix <- function(mtx) {
    if (!is.null(attr(mtx, "which"))) {
        return(sum(mtx))
    }
    mtx$nrow * mtx$ncol
}

# Computing Column & Row Sums
rowSums.default = base::rowSums # assign default as current definition
rowSums = function(x, ...) { # make S3
    UseMethod("rowSums", x)
}
rowSums.dove_matrix <- function(x, na.rm = FALSE) {
#    op_string <- sprintf("%s%s %s", "rowSums", if (na.rm) "|NA" else "",
#         toString(x))
#    operated_dove_matrix(c(dim(x)[1],1), op_string)
  nrow <- nrow(x)
  ret <- dove.matrix(NA, nrow=nrow, ncol=1)
  dove.for(1,nrow,1,function(i) {
    tmp <- x[i,]
    ret[i,] <- sum(tmp, na.rm=na.rm)
  })
  ret
}

colSums.default = base::colSums # assign default as current definition
colSums = function(x, ...) { # make S3
    UseMethod("colSums", x)
}
colSums.dove_matrix <- function(x, na.rm = FALSE) {
    # op_string <- sprintf("%s%s %s", "colSums", if (na.rm) "|NA" else "",
    #      toString(x))
    # operated_dove_matrix(c(dim(x)[2],1), op_string)
  ncol <- ncol(x)
  ret <- dove.matrix(NA, nrow=1, ncol=ncol)
  dove.for(1,ncol,1, function(i) {
    tmp <- x[,i]
    ret[,i] <- sum(tmp, na.rm=na.rm)  
  })
  ret
}
 
mean.default = base::mean # assign default as current definition
mean = function(x, ...) { # make S3
    UseMethod("mean", x)
}

# Computing Column & Row Means
mean.dove_matrix <- function(x, na.rm = FALSE) {
#    va_list <- list(...)
#    op_string <- sprintf("%s%s %s", "mean", if (na.rm) "|NA" else "",
#        paste(sapply(va_list, toString), collapse = ' ') )
#    cat(op_string, file=INSTR_FILE, append=TRUE, sep='\n')
#    cat(sprintf("set %%%d", dove_register_counter), file=INSTR_FILE, append=TRUE, sep='\n')
#    new_dove_register()
  sz <- nrow(x) * ncol(x)
  tot <- sum(x, na.rm=na.rm)
  ret <- tot/dove.wrap(sz)
  ret
}

rowMeans.default = base::rowMeans # assign default as current definition
rowMeans = function(x, ...) { # make S3
    UseMethod("rowMeans", x)
}
rowMeans.dove_matrix <- function(x, na.rm = FALSE) {
#     op_string <- sprintf("%s%s %s", "rowMeans", if (na.rm) "|NA" else "",
#          toString(x))
#     operated_dove_matrix(c(dim(x)[1],1), op_string)
  nrow <- nrow(x)
  ncol <- ncol(x)
  sz <- nrow * ncol
  ret <- dove.matrix(NA, nrow=nrow, ncol=1)
  dove.for(1,nrow,1,function(i) {
    tmp <- x[i,]
    ret[i,] <- sum(tmp, na.rm=na.rm)/dove.wrap(ncol)
  })
  ret
}

colMeans.default = base::colMeans # assign default as current definition
colMeans = function(x, ...) { # make S3
    UseMethod("colMeans", x)
}
colMeans.dove_matrix <- function(x, na.rm = FALSE) {
    # op_string <- sprintf("%s%s %s", "colMeans", if (na.rm) "|NA" else "",
    #      toString(x))
    # operated_dove_matrix(c(dim(x)[2],1), op_string)
  ncol <- ncol(x)
  nrow <- nrow(x)
  sz <- ncol * nrow
  ret <- dove.matrix(NA, nrow=1, ncol=ncol)
  dove.for(1,ncol,1, function(i) {
    tmp <- x[,i]
    ret[,i] <- sum(tmp,na.rm=na.rm)/dove.wrap(nrow)  
  })
  ret
}

# Horizontal Concatenation
cbind.dove_matrix <- function(...) {
  var_params = list(...)
  op_string <- "cbind"
  new_colnames <- c()
  stopifnot(length(var_params) > 0);
  num_rows <- 0
  num_cols <- 0
  for (idx in 1:length(var_params)) {
    item <- var_params[[idx]]
    match.arg(class(item), c("dove_matrix", "dove_pointer", "dove_value", "dove_register"))
    if (class(item) == "dove_matrix") {
      if (num_rows == 0) {
        num_rows <- nrow(item)
      }
      if (num_rows != nrow(item)) {
        stop("number of rows of matrices must match")
      }
      if (ncol(item) > 1) {
        # TODO: avoid this
        for (j in 1:ncol(item)) {
            op_string <- paste(op_string, toString(item[,j]))
            num_cols <- num_cols + 1
            if (!is.null(colnames(item))) {
                new_colnames <- append(new_colnames, colnames(item)[[j]])
            } else {
                new_colnames <- append(new_colnames, names(var_params[idx]))
            }
        }
      } else {
          num_cols <- num_cols + ncol(item)
          op_string <- paste(op_string, toString(item))
          if (!is.null(colnames(item))) {
              new_colnames <- append(new_colnames, colnames(item))
          } else {
              new_colnames <- append(new_colnames, names(var_params[idx]))
          }
      }
    } else {
      num_cols <- num_cols + 1
      op_string <- paste(op_string, toString(item))
      new_colnames <- append(new_colnames, names(var_params[idx]))
    }
  }
  if (num_rows == 0) {
    num_rows <- 1
  }

  # TODO loss of rownames
  operated_dove_matrix(c(num_rows,num_cols), op_string, dimnames = list(NULL, new_colnames))
}

# cbind.dove_matrix <- function(...) {
#   var_params = list(...)
#   stopifnot(length(var_params) > 0);
#   num_rows <- 0
#   num_cols <- 0
#   new_colnames <- c()
# 
#   #forloop to pre-compute size of combined matrix
#   for (idx in 1:length(var_params)) {
#     item <- var_params[[idx]]
#     match.arg(class(item), c("dove_matrix", "dove_pointer", "dove_value", "dove_register"))
#     if (class(item) == "dove_matrix") {
#       if (num_rows == 0) {
#         num_rows <- nrow(item)
#       }
#       if (num_rows != nrow(item)) {
#         stop("number of rows of matrices must match")
#       }
#       num_cols <- num_cols + ncol(item)
#     } else {
#       num_cols <- num_cols + 1
#     }
#   }
#   if (num_rows == 0) {
#     num_rows <- 1
#   }
# 
#   ret <- dove.matrix(nrow=num_rows, ncol=num_cols)
# 
#   ccol_idx <- 0
#   for (idx in 1:length(var_params)) {
#     item <- var_params[[idx]]
#     if (class(item) == "dove_matrix") {
#       dove.for (1,num_rows,1,function(i) {
#         dove.for (1,ncol(item),1,function(j) {
#            ret[i,j+ccol_idx] <- item[[i,j]]
#         })
#       })
#       ccol_idx <- ccol_idx + ncol(item)
#     } else {
#       ret[1,ccol_idx+1] <- item
#       ccol_idx <- ccol_idx + 1
#     }
#   }
# 
#   ret
# }

#Vertical Concatenation (Appending)
rbind.dove_matrix <- function(...) {
  var_params = list(...)
  op_string <- "rbind"
  stopifnot(length(var_params) > 0);
  # TODO dimnames for rbind
  num_cols <- 0
  num_rows <- 0
  for (item in var_params) {
    match.arg(class(item), c("dove_matrix", "dove_pointer", "dove_value", "dove_register"))
    if (class(item) == "dove_matrix") {
      if (num_cols == 0) {
        num_cols <- ncol(item)
      }
      if (num_cols != ncol(item)) {
        stop("number of rows of matrices must match")
      }
      if (nrow(item) > 1) {
        # TODO: avoid this
        for (i in 1:nrow(item)) {
            op_string <- paste(op_string, toString(item[i,]))
            num_rows <- num_rows + 1
        }
      } else {
        num_rows <- num_rows + nrow(item)
        op_string <- paste(op_string, toString(item))
      }
    } else {
      num_rows <- num_rows + 1
      op_string <- paste(op_string, toString(item))
    }
  }
  if (num_cols == 0) {
    num_cols <- 1
  }
  operated_dove_matrix(c(num_rows,num_cols), op_string)
}

# rbind.dove_matrix <- function(...) {
#   var_params = list(...)
#   op_string <- "rbind"
#   stopifnot(length(var_params) > 0);
#   # TODO dimnames for rbind
#   num_cols <- 0
#   num_rows <- 0
#   
#   #forloop to pre-compute size of combined matrix
#   for (item in var_params) {
#     match.arg(class(item), c("dove_matrix", "dove_pointer", "dove_value", "dove_register"))
#     if (class(item) == "dove_matrix") {
#       if (num_cols == 0) {
#         num_cols <- ncol(item)
#       }
#       if (num_cols != ncol(item)) {
#         stop("number of rows of matrices must match")
#       }
#       num_rows <- num_rows + nrow(item)
#     } else {
#       num_rows <- num_rows + 1
#     }
#   }
#   if (num_cols == 0) {
#     num_cols <- 1
#   }
# 
#   ret <- dove.matrix(nrow=num_rows, ncol=num_cols)
# 
#   crow_idx <- 0
#   for (item in var_params) {
#     if (class(item) == "dove_matrix") {
#       dove.for (1,nrow(item),1,function(i) {
#         dove.for (1,num_cols,1,function(j) {
#             ret[i+crow_idx,j] <- item[[i,j]]
#           })
#         })
#       crow_idx <- crow_idx + nrow(item)
#     } else {
#       ret[crow_idx,1] <- item
#       crow_idx <- crow_idx + 1
#     }
#   }
# 
#   ret
# }

## `which` and friends
source('dove_which.R')
