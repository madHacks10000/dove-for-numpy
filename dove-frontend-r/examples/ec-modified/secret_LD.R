calc_LD <- function( geno, inds=1:nrow(geno), get.D=T, get.Dprime=F, get.rsq=T, get.chisq=T, get.chisq_prime=F ) {
### Eva KF Chan 
### 23 Feb 2009
### Last Modified: 29 Nov 2013
###
### Calculates D, D', r, chisq, chisq'
### Given locus A with allele frequencies pA & pa and locus B with allele frequencies pB and pb
### Let pAB be the allele frequencies of allele A/B.  As the AB/ab is indistinguishable from Ab/aB, we assume equal probability for either assortment; i.e. For individuals with Aa at locus A and Bb at locus b, we assume p(AB/ab)=p(Ab/aB)=0.5.  NOTE that this is assumption is part of the reason why this function is relatively fast, compare to, for example, the LD() function in R/genetics which estimates p(AB) using a maximum likelihood approach. 
### D = pAB - pApB
### D' = { D/Dmax for D>=0 , where Dmax = min( pApb, papB )
###    = { D/Dmin for D<0  , where Dmin = max(-pApB,-papb )
### r = D / sqrt( pApapBpb )
### chi2 = (2ND^2) / (pApapBpb)
### chi2'= chisq / ( 2N(l-1) ) where l=min(k,m) 
###                                  N = # individuals
###                                  k & m = # alelles in locus A & B
###
### Arguments:
### 	geno:            m x n matrix of genotypes {0,1,2,NA} where m=number of markers, n=number of individuals
###	inds:            integer vector of marker indices (rows of geno) for subseting markers for LD calculation
###	get.D:           {T,F} Boolean value to indicate whether the D measure is to be calculated
###	get.Dprime:      {T,F} Boolean value to indicate whether the D' measure is to be calculated
###	get.rsq:         {T,F} Boolean value to indicate whether the r^2 measure is to be calculated
###	get.chisq:       {T,F} Boolean value to indicate whether the chi2 measure is to be calculated
###	get.chisq_prime: {T,F} Boolean value to indicate whether the chi2' measure is to be calculated


	if( all(!get.D, !get.Dprime, !get.rsq, !get.chisq, !get.chisq_prime) ) { stop('Must request at least one LD statistic.\n') }
	D_prime <- NULL
    rsq <- NULL
    chisq <- NULL
    chisq_prime <- NULL
    df <- NULL
	D <- dove.matrix(NA, nrow=nrow(geno), ncol=length(inds))
	if( get.Dprime ) { D_prime <- dove.matrix(NA, nrow=nrow(geno), ncol=length(inds)) }
	if( get.rsq ) { rsq <- dove.matrix(NA, nrow=nrow(geno), ncol=length(inds))}
	if( get.chisq | get.chisq_prime ) { 
		chisq <- dove.matrix(NA, nrow=nrow(geno), ncol=length(inds))
		df <- dove.matrix(NA, nrow=nrow(geno), ncol=length(inds))
		if( get.chisq_prime ) { chisq_prime <- dove.matrix(NA, nrow=nrow(geno), ncol=length(inds)) }
	}
	
    # TODO: for now, only works with not-missing data
	# if( all(as.logical(!is.na(geno))) ) {	#no missing data
    tmp.geno <- +geno	## genotypes at locus A
    N <- dove.wrap(ncol(tmp.geno))	#number of individuals (diploid is assumed)
    pA <- ((C_2*rowSums(tmp.geno==C_0,na.rm=T))+rowSums(tmp.geno==C_1,na.rm=T)) / (C_2*N)
    pa <- C_1-pA
    dove.for(1, length(inds), 1, function(i) {
    #    print(sprintf("iteration %d of %d", i, length(inds)))
        # tmp.Bgeno <- matrix(tmp.geno[inds[i],],nrow=nrow(tmp.geno),ncol=ncol(tmp.geno),byrow=T)	
        ## genotypes at locus B
        tmp.Bgeno <- dove.matrix(NA, nrow=nrow(tmp.geno), ncol=ncol(tmp.geno))
        # index_row <- tmp.geno[inds[i],]  # TODO: somehow we need to support this style of code
        index_row <- tmp.geno[i,]
        dove.for(1, ncol(tmp.geno), 1, function(k) {
            tmp.Bgeno[k,] <- index_row
        })
        pB <- ((C_2*rowSums(tmp.Bgeno==C_0,na.rm=T))+rowSums(tmp.Bgeno==C_1,na.rm=T)) / (C_2*N)
        pb <- C_1-pB
        pAB <- ((rowSums(tmp.geno==C_0 & tmp.Bgeno==C_0, na.rm=T)*C_2) + (rowSums(tmp.geno==C_1 & tmp.Bgeno==C_0, na.rm=T)) + (rowSums(tmp.geno==C_0 & tmp.Bgeno==C_1, na.rm=T)) + (rowSums(tmp.geno==C_1 & tmp.Bgeno==C_1, na.rm=T)*(C_1/C_2))) / (C_2*N) 
        D[,i] <- pAB-(pA*pB)
        if( get.Dprime ) { 
            Dmax <- pmin(pA*pb, pa*pB)
            Dmin <- pmax(-pA*pB, -pa*pb)
            pos <- (D[,i]>=C_0)
            # D_prime[which(pos),i] <- D[which(pos),i] / Dmax[which(pos)]
            # D_prime[which(!pos),i] <- D[which(!pos),i] / Dmin[which(!pos)]

            D_prime[,i] <- ifelse(pos, D[,i]/Dmax, D[,i]/Dmin)
            # for (idx in 1:nrow(pos)) {
            #     D_prime[idx,i] <- ifelse(pos[[idx]] == C_1, D[idx,i]/Dmax[idx], D[idx,i]/Dmin[idx])
            # }
        }
        if( get.rsq ) {
            rsq[,i] <- (D[,i]*D[,i]) / (pA*pa*pB*pb)
        }
        if( get.chisq | get.chisq_prime ) {
            chisq[,i] <- (C_2*N*D[,i]*D[,i]) / (pA*pa*pB*pb)
            if( get.chisq_prime ) {
                k=C_2-(pA==C_0|pa==C_0)
                m=C_2-(pB==C_0|pb==C_0)
                #df[,i] <- (k-1)*(m-1)
                chisq_prime[,i] <- chisq[,i] / (C_2*N*pmin(k,m))
            }
        }

    })	
	# } else {	#at least one missing data point in geno
    # for(i in 1:length(inds)) {
    #     tmp.geno <- geno[,!is.na(geno[inds[i],])]	## genotypes at locus A; i.e. all loci, but excluding samples with missing data at lcous B (i)
    #     tmp.Bgeno <- matrix(tmp.geno[inds[i],],nrow=nrow(tmp.geno),ncol=ncol(tmp.geno),byrow=T)	## genotypes at locus B (i.e. i-th locus); pulling from tmp.geno, so samples with missing data at i-th locus (B) will also be excluded
    #     tmp.Bgeno[is.na(tmp.geno)] <- NA 	#anytime where locus A (i.e. all non i-th locus) is missing, set as missing 
    #     N <- rowSums(!is.na(tmp.geno))
    #     pA <- ((2*apply(tmp.geno==0,1,sum,na.rm=T))+apply(tmp.geno==1,1,sum,na.rm=T)) / (2*N) 
    #     pB <- ((2*apply(tmp.Bgeno==0,1,sum,na.rm=T))+apply(tmp.Bgeno==1,1,sum,na.rm=T)) / (2*N)
    #     pa <- 1-pA
    #     pb <- 1-pB
    #     pAB <- ((apply(tmp.geno==0 & tmp.Bgeno==0, 1, sum,na.rm=T)*2) + (apply(tmp.geno==1 & tmp.Bgeno==0, 1, sum,na.rm=T)) + (apply(tmp.geno==0 & tmp.Bgeno==1, 1, sum,na.rm=T)) + (apply(tmp.geno==1 & tmp.Bgeno==1, 1, sum,na.rm=T)*0.5)) / (2*N) 
    #     D[,i] <- pAB-(pA*pB)
    #     if( get.Dprime ) { 
    #         Dmax <- pmin(pA*pb, pa*pB)
    #         Dmin <- pmax(-pA*pB, -pa*pb)
    #         pos <- (D[,i]>=0)
    #         D_prime[which(pos),i] <- D[which(pos),i] / Dmax[which(pos)]
    #         D_prime[which(!pos),i] <- D[which(!pos),i] / Dmin[which(!pos)]
    #     }
    #     if( get.rsq ) {
    #         rsq[,i] <- (D[,i]*D[,i]) / (pA*pa*pB*pb)
    #     }
    #     if( get.chisq | get.chisq_prime ) {
    #         chisq[,i] <- (2*N*D[,i]*D[,i]) / (pA*pa*pB*pb)
    #         k=2-as.integer(pA==0|pa==0)
    #         m=2-as.integer(pB==0|pb==0)
    #         df[,i] <- (k-1)*(m-1)
    #         if( get.chisq_prime ) {
    #             chisq_prime[,i] <- chisq[,i] / (2*N*pmin(k,m))
    #         }
    #     }
    # }
	# }
	if( !get.D ) { D <- NULL }
	if( !get.chisq ) { chisq <- NULL }
	return(list(D=D, Dprime=D_prime, rsq=rsq, chisq=chisq, chisq_prime=chisq_prime, chisq_df=df))
}

source('../examples/ec-modified/init_data.R')
LDrsq.allpops.SNPs <- calc_LD( geno, get.D=T, get.Dprime=T, get.rsq=T, get.chisq=T, get.chisq_prime=T )
#print(LDrsq.allpops.SNPs$rsq[1:10,2])
#print("LDrsq.popA.SNPs1to50")
#popAgeno <- geno[,which(subpop=='A')]
#LDrsq.popA.SNPs1to50 <- calc_LD(popAgeno, inds=1:50, get.D=T, get.Dprime=T, get.rsq=T, get.chisq=T, get.chisq_prime=T )
#print(LDrsq.popA.SNPs1to50$Dprime)
