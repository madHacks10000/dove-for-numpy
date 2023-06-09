#ifndef _MATHGEN_HPP
#define _MATHGEN_HPP
#include "../unary_op.hpp"

#ifdef LIB_FTFP
class AbsOp: public UnaryOp {
  void call(fixed scalar, fixed *result);
};

class SignOp: public UnaryOp {
  void call(fixed scalar, fixed *result);
};

class SqrtOp: public UnaryOp {
  void call(fixed scalar, fixed *result);
};

class FloorOp: public UnaryOp {
  void call(fixed scalar, fixed *result);
};

class CeilingOp: public UnaryOp {
  void call(fixed scalar, fixed *result);
};
#else
class AbsOp: public UnaryOp {
  void call(double scalar, double *result);
};

class SignOp: public UnaryOp {
  void call(double scalar, double *result);
};

class SqrtOp: public UnaryOp {
  void call(double scalar, double *result);
};

class FloorOp: public UnaryOp {
  void call(double scalar, double *result);
};

class CeilingOp: public UnaryOp {
  void call(double scalar, double *result);
};
#endif /* LIB_FTFP */
#endif
