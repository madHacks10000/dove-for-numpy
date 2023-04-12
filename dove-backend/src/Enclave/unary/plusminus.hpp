#ifndef _PLUSMINUS_HPP
#define _PLUSMINUS_HPP
#include "../unary_op.hpp"

#ifdef LIB_FTFP
class NoOp: public UnaryOp {
  void call(fixed scalar, fixed *result);
};

class NegationOp: public UnaryOp {
  void call(fixed scalar, fixed *result);
};

class BitwiseNotOp: public UnaryOp {
  void call(fixed scalar, fixed *result);
};
#else
class NoOp: public UnaryOp {
  void call(double scalar, double *result);
};

class NegationOp: public UnaryOp {
  void call(double scalar, double *result);
};

class BitwiseNotOp: public UnaryOp {
  void call(double scalar, double *result);
};
#endif /* LIB_FTFP */
#endif /* _PLUSMINUS_HPP */
