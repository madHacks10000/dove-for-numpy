#ifndef _LOGIC_HPP
#define _LOGIC_HPP
#include "../binary_op.hpp"

#ifdef LIB_FTFP
class BitwiseAndOp: public BinaryOp {
  void call(fixed scalar1, fixed scalar2, fixed *result);
};

class BitwiseOrOp: public BinaryOp {
  void call(fixed scalar1, fixed scalar2, fixed *result);
};
#else
class BitwiseAndOp: public BinaryOp {
  void call(double scalar1, double scalar2, double *result);
};

class BitwiseOrOp: public BinaryOp {
  void call(double scalar1, double scalar2, double *result);
};
#endif /* LIB_FTFP */
#endif /* _LOGIC_HPP */
