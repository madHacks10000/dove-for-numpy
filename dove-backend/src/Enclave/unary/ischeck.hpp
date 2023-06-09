#ifndef _ISCHECK_HPP
#define _ISCHECK_HPP
#include "../unary_op.hpp"

class IsNaOp: public UnaryOp {
#ifdef LIB_FTFP
  void call(fixed scalar, fixed *result);
#else
  void call(double scalar, double *result);
#endif
};

class IsNanOp: public UnaryOp {
#ifdef LIB_FTFP
  void call(fixed scalar, fixed *result);
#else
  void call(double scalar, double *result);
#endif
};

class IsInfiniteOp: public UnaryOp {
#ifdef LIB_FTFP
  void call(fixed scalar, fixed *result);
#else
  void call(double scalar, double *result);
#endif
};

#endif /* _ISNA_HPP */
