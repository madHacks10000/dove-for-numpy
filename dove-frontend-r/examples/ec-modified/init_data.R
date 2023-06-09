source('dove.R')

C_0 <- dove.wrap(0)
C_1 <- dove.wrap(1)
C_2 <- dove.wrap(2)
C_4 <- dove.wrap(4)

subpop <- rep(LETTERS[1:3],c(3,3,4))
geno <- dove.matrix("sample", nrow=10, ncol=10)
# geno <- geno[1:100,]
# geno <- dove.matrix("snp.mat", nrow=2808570, ncol=60)
