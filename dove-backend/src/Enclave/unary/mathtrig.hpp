#ifndef _MATHTRIG_HPP
#define _MATHTRIG_HPP
#include "../unary_op.hpp"

#ifdef LIB_FTFP
class ExpOp: public UnaryOp {
  void call(fixed scalar, fixed *result);
};

class LogOp: public UnaryOp {
  void call(fixed scalar, fixed *result);
};

class CosOp: public UnaryOp {
  void call(fixed scalar, fixed *result);
};

class SinOp: public UnaryOp {
  void call(fixed scalar, fixed *result);
};

class TanOp: public UnaryOp {
  void call(fixed scalar, fixed *result);
};
#else
class ExpOp: public UnaryOp {
  void call(double scalar, double *result);
};

class LogOp: public UnaryOp {
  void call(double scalar, double *result);
};

class CosOp: public UnaryOp {
  void call(double scalar, double *result);
};

class SinOp: public UnaryOp {
  void call(double scalar, double *result);
};

class TanOp: public UnaryOp {
  void call(double scalar, double *result);
};
#endif /* LIB_FTFP */
#endif
