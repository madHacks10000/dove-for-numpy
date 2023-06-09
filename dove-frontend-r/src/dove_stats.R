C_0 <- dove.wrap(0)
C_1 <- dove.wrap(1)

pchisq.default = stats::pchisq # assign default as current definition
pchisq = function(x, ...) { # make S3
    UseMethod("pchisq", x)
}

pchisq.dove_matrix <- function(x, df) {
#    df <- dove.wrap(df)
#    match.arg(class(df), c("dove_value", "dove_pointer", "dove_register"))
#    stopifnot(ncol(x) == 1)
#    op_string <- sprintf("%s %s %s", "pchisq", toString(x), toString(df))
#    operated_dove_matrix(c(dim(x)[1],1), op_string)
    tpvals <- c(0.004,0.02,0.06,0.15,0.46,1.07,1.64,2.71,3.84,6.63,10.83,
                                0.10,0.21,0.45,0.71,1.39,2.41,3.22,4.61,5.99,9.21,13.82,
                                0.35,0.58,1.01,1.42,2.37,3.66,4.64,6.25,7.81,11.34,16.27,
                                0.71,1.06,1.65,2.20,3.36,4.88,5.99,7.78,9.49,13.28,18.47,
                                1.14,1.61,2.34,3.00,4.35,6.06,7.29,9.24,11.07,15.09,20.52,
                                1.63,2.20,3.07,3.83,5.35,7.23,8.56,10.64,12.59,16.81,22.46,
                                2.17,2.83,3.82,4.67,6.35,8.38,9.80,12.02,14.07,18.48,24.32,
                                2.73,3.49,4.59,5.53,7.34,9.52,11.03,13.36,15.51,20.09,26.12,
                                3.32,4.17,5.38,6.39,8.34,10.66,12.24,14.68,16.92,21.67,27.88,
                                3.94,4.87,6.18,7.27,9.34,11.78,13.44,15.99,18.31,23.21,29.59)
    tprobs <- c(0.95, 0.90, 0.80, 0.70, 0.50, 0.30,
                                0.20, 0.10, 0.05, 0.01, 0.001)

    pvals <- dove.matrix(tpvals, nrow=length(tpvals))
    probs <- dove.matrix(tprobs, nrow=length(tprobs))
    row <- (df - 1) * 11
    if(!(row < 99)) {
        row <- 0
    }
    retval <- dove.matrix(nrow=nrow(x), ncol=1)
    dove.for(1, nrow(x), 1, function(i) {
        flag <- C_1
        retval[i,] <- probs[1,]
        dove.for(2, 11, 1, function(j) {
            next_stat <- pvals[row+j,]
            flag <- flag & (x[i,] >= next_stat)
            prob <- probs[j,]
            retval[i,] <- ifelse(flag, prob, retval[i,])  
        })
    })
    retval <- C_1 - retval
    retval
}

fisher.test.default = stats::fisher.test # assign default as current definition
fisher.test = function(z, ...) { # make S3
    UseMethod("fisher.test", z)
}

lookupLogFacs <- NULL

finitLogFacs <- function(n) {
    if (is.null(lookupLogFacs)) {
        # ret <- dove.matrix(nrow=(n+1))
        logFacs <- matrix(nrow=(n+1))
        logFacs[1,] <- 0
        # ret[1,] <- C_0
        dove.for(2, n+1, 1, function(i) {
            logFacs[i,] <- logFacs[(i-1),] + log(dove.wrap(i-1))
            # ret[i,] <- dove.wrap(logFacs[i,])
        })
        lookupLogFacs <<- logFacs
    }
    lookupLogFacs
}

flogHypergeometricProb <- function(logFacs, a, b, c, d) {
    n <- nrow(logFacs) - 1
    idxMat <- dove.matrix(c(0,0,0,0,0,0,0,0,0), nrow = 9, ncol = 1)
    ab <- a+b
    cd <- c+d
    ac <- a+c
    bd <- b+d
    abcd <- a+b+c+d

    dove.for(1,n+1,1,function(i) {
            idx <- dove.wrap(i-1)
            idxMat[1,] <- ifelse(ab == idx, logFacs[i,], idxMat[1,])
            idxMat[2,] <- ifelse(cd == idx, logFacs[i,], idxMat[2,])
            idxMat[3,] <- ifelse(ac == idx, logFacs[i,], idxMat[3,])
            idxMat[4,] <- ifelse(bd == idx, logFacs[i,], idxMat[4,])
            idxMat[5,] <- ifelse(a == idx, logFacs[i,], idxMat[5,])
            idxMat[6,] <- ifelse(b == idx, logFacs[i,], idxMat[6,])
            idxMat[7,] <- ifelse(c == idx, logFacs[i,], idxMat[7,])
            idxMat[8,] <- ifelse(d == idx, logFacs[i,], idxMat[8,])
            idxMat[9,] <- ifelse(abcd == idx, logFacs[i,], idxMat[9,])

#        dove.for(1,9,1,function(j) {
#            idxMat[j,] <- ifelse(to_check[j,] == dove.wrap(i-1), logFacs[i,], idxMat[j,])
#        })
    })

    result <- idxMat[1,] + idxMat[2,] + idxMat[3,] + idxMat[4,] - idxMat[5,] - idxMat[6,] - idxMat[7,] - idxMat[8,] - idxMat[9,]
    result
}

ffet <- function(logFacs, a, b, c, d) {
    n <- nrow(logFacs) - 1
    logpCutoff <- flogHypergeometricProb(logFacs,a,b,c,d)
    pFraction <- dove.matrix(c(0),nrow=1,ncol=1)
    dove.for(0, n, 1, function(i) {
        x <- dove.wrap(i)
        process_flag <- (a+b-x >= C_0) & (a+c-x >= C_0) & (d-a+x >= C_0)
        l <- flogHypergeometricProb(logFacs, x, a+b-x, a+c-x, d-a+x)
        cutoff_flag <- (l <= logpCutoff)
        cutoff_flag <- cutoff_flag & process_flag
        new_value <- pFraction[,] + exp(l - logpCutoff)
        pFraction[,] <- ifelse(cutoff_flag, new_value, pFraction[,])
    })
    logpValue <- logpCutoff + log(pFraction)
    pval <- exp(logpValue)
    pval
}

fisher.test.dove_matrix <- function(z, n=60) {
    # This assumes a certain format for the operation.
    stopifnot(ncol(z) == 4)
    ret <- dove.matrix(nrow=nrow(z), ncol=2)
    flogFacs <- finitLogFacs(n)
    dove.for(1, nrow(z), 1, function(i) {
        # default fill: by column
        a <- z[[i,1]]
        b <- z[[i,3]]
        c <- z[[i,2]]
        d <- z[[i,4]]
        pval <- ffet(flogFacs,a,b,c,d)
        or <- (a * d)/(b * c)
        #TODO: need more stats other than p-value and odd's ratio
        ret[i,1] <- or
        ret[i,2] <- pval
    })
    colnames(ret) <- c("estimate", "p.value")
    ret

    # a <- z[1,1]
    # b <- z[1,2]
    # c <- z[2,1]
    # d <- z[2,2]
    # pval <- ffet(flogFacs,a,b,c,d)
    # or <- (a * d)/(b * c)
    # #TODO: need more stats other than p-value and odd's ratio
    # ret <- dove.matrix(nrow=2, ncol=1, dimnames=list(c("estimate", "p.value")))
    # ret[1,1] <- or
    # ret[2,1] <- pval
    # ret
}
