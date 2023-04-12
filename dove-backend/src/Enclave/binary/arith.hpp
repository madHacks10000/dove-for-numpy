#ifndef _ARITH_HPP
#define _ARITH_HPP
#include "../binary_op.hpp"

#ifdef LIB_FTFP
class AdditionOp: public BinaryOp {
  void call(fixed scalar1, fixed scalar2, fixed *result);
};

class SubtractionOp: public BinaryOp {
  void call(fixed scalar1, fixed scalar2, fixed *result);
};

class MultiplicationOp: public BinaryOp {
  void call(fixed scalar1, fixed scalar2, fixed *result);
};

class DivisionOp: public BinaryOp {
  void call(fixed scalar1, fixed scalar2, fixed *result);
};

class PowOp: public BinaryOp {
  void call(fixed scalar1, fixed scalar2, fixed *result);
};

class ModOp: public BinaryOp {
  void call(fixed scalar1, fixed scalar2, fixed *result);
};

class IDivOp: public BinaryOp {
  void call(fixed scalar1, fixed scalar2, fixed *result);
};
#else
#include <cmath>
class AdditionOp: public BinaryOp {
  void call(double scalar1, double scalar2, double *result);
};

class SubtractionOp: public BinaryOp {
  void call(double scalar1, double scalar2, double *result);
};

class MultiplicationOp: public BinaryOp {
  void call(double scalar1, double scalar2, double *result);
};

class DivisionOp: public BinaryOp {
  void call(double scalar1, double scalar2, double *result);
};

class PowOp: public BinaryOp {
  void call(double scalar1, double scalar2, double *result);
};

class ModOp: public BinaryOp {
  void call(double scalar1, double scalar2, double *result);
};

class IDivOp: public BinaryOp {
  void call(double scalar1, double scalar2, double *result);
};
#endif /* LIB_FTFP */
#endif /* _ARITH_HPP */
