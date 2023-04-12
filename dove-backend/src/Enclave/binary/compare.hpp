#ifndef _COMPARE_HPP
#define _COMPARE_HPP
#include "../binary_op.hpp"

#ifdef LIB_FTFP
class EqualOp: public BinaryOp {
  void call(fixed scalar1, fixed scalar2, fixed *result);
};

class GreaterThanOp: public BinaryOp {
  void call(fixed scalar1, fixed scalar2, fixed *result);
};

class LessThanOp: public BinaryOp {
  void call(fixed scalar1, fixed scalar2, fixed *result);
};

class NotEqualOp: public BinaryOp {
  void call(fixed scalar1, fixed scalar2, fixed *result);
};

class GreaterThanEqualOp: public BinaryOp {
  void call(fixed scalar1, fixed scalar2, fixed *result);
};

class LessThanEqualOp: public BinaryOp {
  void call(fixed scalar1, fixed scalar2, fixed *result);
};
#else
class EqualOp: public BinaryOp {
  void call(double scalar1, double scalar2, double *result);
};

class GreaterThanOp: public BinaryOp {
  void call(double scalar1, double scalar2, double *result);
};

class LessThanOp: public BinaryOp {
  void call(double scalar1, double scalar2, double *result);
};

class NotEqualOp: public BinaryOp {
  void call(double scalar1, double scalar2, double *result);
};

class GreaterThanEqualOp: public BinaryOp {
  void call(double scalar1, double scalar2, double *result);
};

class LessThanEqualOp: public BinaryOp {
  void call(double scalar1, double scalar2, double *result);
};
#endif /* LIB_FTFP */
#endif /* _COMPARE_HPP */
