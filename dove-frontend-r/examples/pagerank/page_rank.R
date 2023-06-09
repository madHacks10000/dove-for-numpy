# the number of rows & columns of input matrix
nodes <- 10

page_rank <- function(M) {
    ## Arguments
    ## =========
    ## M: n by n adjacency matrix
    ## 
    ## Output
    ## =========
    ## v: output of page-rank execution engine after 40 iterations
    ##
    
    d <- 0.8
    N <- nrow(M)
    # create a random nodes by 1 matrix from unif[0,1)
    v <- matrix(nrow = nodes, ncol = 1, rand = TRUE)
    norm_one <- sum(abs(v))
    v <- v / norm_one
   
    M_hat <- (M * d) + ((1-d) / N)
    iters <- 40
    for(i in 1:iters) {
        v[,] <- M_hat %*% v
    }

    v
}

M <- matrix("sample", nrow=nodes, ncol=nodes)
r <- page_rank(M)
