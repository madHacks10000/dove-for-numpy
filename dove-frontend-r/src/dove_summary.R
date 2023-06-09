all.default = base::all
all = function(x, ..., na.rm = FALSE) {
    UseMethod("all", x)
}

all.dove_matrix <- function(x, ..., na.rm = FALSE) {
    nrow <- nrow(x)
    ncol <- ncol(x)
    ret <- dove.matrix(c(1),nrow=1,ncol=1)
    dove.for(1,nrow,1,function(i) {
        dove.for(1,ncol,1,function(j) {
            if(na.rm) {
                tmp <- +ret[[1,1]]
                ret[,] <- ret[[1,1]] & x[[i,j]]
                ret[,] <- ifelse(is.na(x[[i,j]]), tmp, ret[[1,1]])
            } else {
                ret[,] <- ret[[1,1]] & x[[i,j]]
            }
        })
    })
    return(+ret[[1,1]])
}

any.default = base::any
any = function(x, ..., na.rm = FALSE) {
    UseMethod("any", x)
}

any.dove_matrix <- function(x, ..., na.rm = FALSE) {
    nrow <- nrow(x)
    ncol <- ncol(x)
    ret <- dove.matrix(c(0),nrow=1,ncol=1)
    dove.for(1,nrow,1,function(i) {
        dove.for(1,ncol,1,function(j) {
            if(na.rm) {
                tmp <- +ret[[1,1]]
                ret[,] <- ret[[1,1]] | x[[i,j]]
                ret[,] <- ifelse(is.na(x[[i,j]]), tmp, ret[[1,1]])
            } else {
                ret[,] <- ret[[1,1]] | x[[i,j]]
            }
        })
    })
    return(+ret[[1,1]])
}

sum.default = base::sum
sum = function(x, ..., na.rm = FALSE) {
    UseMethod("sum", x)
}
sum.dove_matrix <- function(x, ..., na.rm = FALSE) {
    nrow <- nrow(x)
    ncol <- ncol(x)
    ret <- dove.matrix(c(0),nrow=1,ncol=1)
    dove.for(1,nrow,1,function(i) {
        dove.for(1,ncol,1,function(j) {
            if(na.rm) {
                tmp <- +ret[[1,1]]
                ret[,] <- ret[[1,1]] + x[[i,j]]
                ret[,] <- ifelse(is.na(x[[i,j]]), tmp, ret[[1,1]])
            } else {
                ret[,] <- ret[[1,1]] + x[[i,j]]
            }
        })
    })
    return(+ret[[1,1]])
}

prod.default = base::prod
prod = function(x, ..., na.rm = FALSE) {
    UseMethod("prod", x)
}
prod.dove_matrix <- function(x, ..., na.rm = FALSE) {
    nrow <- nrow(x)
    ncol <- ncol(x)
    ret <- dove.matrix(c(1),nrow=1,ncol=1)
    dove.for(1,nrow,1,function(i) {
        dove.for(1,ncol,1,function(j) {
            if(na.rm) {
                tmp <- +ret[[1,1]]
                ret[,] <- ret[[1,1]] * x[[i,j]]
                ret[,] <- ifelse(is.na(x[[i,j]]), tmp, ret[[1,1]])
            } else {
                ret[,] <- ret[[1,1]] * x[[i,j]]
            }
        })
    })
    return(+ret[[1,1]])
}


min.default = base::min
min = function(x, ..., na.rm=FALSE) {
    UseMethod("min", x)
}
min.dove_matrix <- function(x, ..., na.rm=FALSE) {
    nrow <- nrow(x)
    ncol <- ncol(x)
    ret <- dove.matrix(c(Inf),nrow=1,ncol=1)
    dove.for(1,nrow,1,function(i) {
        dove.for(1,ncol,1,function(j) {
            if(na.rm) {
                tmp <- +ret[[1,1]]
                ret[,] <- ifelse(ret[[1,1]] < x[[i,j]], ret[[1,1]], x[[i,j]])
                ret[,] <- ifelse(is.na(x[[i,j]]), tmp, ret[[1,1]])
            } else {
                ret[,] <- ifelse(ret[[1,1]] < x[[i,j]], ret[[1,1]], x[[i,j]])
            }
        })
    })
    return(+ret[[1,1]])
}

max.default = base::max
max = function(x, ..., na.rm = FALSE) {
    UseMethod("max", x)
}
max.dove_matrix <- function(x, ..., na.rm=FALSE) {
    nrow <- nrow(x)
    ncol <- ncol(x)
    ret <- dove.matrix(c(-Inf),nrow=1,ncol=1)
    dove.for(1,nrow,1,function(i) {
        dove.for(1,ncol,1,function(j) {
            if(na.rm) {
                tmp <- +ret[[1,1]]
                ret[,] <- ifelse(ret[[1,1]] > x[[i,j]], ret[[1,1]], x[[i,j]])
                ret[,] <- ifelse(is.na(x[[i,j]]), tmp, ret[[1,1]])
            } else {
                ret[,] <- ifelse(ret[[1,1]] > x[[i,j]], ret[[1,1]], x[[i,j]])
            }
        })
    })
    return(+ret[[1,1]])
}

range.default = base::range
range = function(x, ..., na.rm = FALSE) {
    UseMethod("range", x)
}
range.dove_matrix <- function(x, ..., na.rm = FALSE) {
    ret <- dove.matrix(nrow=2)
    ret[1,1] <- min(x, na.rm=na.rm)
    ret[2,1] <- max(x, na.rm=na.rm)
    ret
}
