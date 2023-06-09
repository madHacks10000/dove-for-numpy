#ifndef _LOG_BIN_HPP
#define _LOG_BIN_HPP
#include "../binary_op.hpp"

class LogBinOp: public BinaryOp {
#ifdef LIB_FTFP
  void call(fixed scalar1, fixed scalar2, fixed *result);
#else
  void call(double scalar1, double scalar2, double *result);
#endif
};

#endif /* _LOG_BIN_HPP */
