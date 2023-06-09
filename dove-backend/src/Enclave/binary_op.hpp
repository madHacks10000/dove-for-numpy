#ifndef _BINARY_OP_HPP
#define _BINARY_OP_HPP

#include <stdexcept>
#include <cstdarg>
#include <cstdlib>

#include "p_block.hpp"
#include "primitives.hpp"

#ifdef LIB_FTFP
extern "C" {
#include "ftfp.h"
}
#else
#include <cmath>
#endif

class BinaryOp {
public:
  BinaryOp() {}
  virtual ~BinaryOp() {};
#ifdef LIB_FTFP
  virtual void call(fixed scalar1, fixed scalar2, fixed *result);
  virtual void call(p_block *matrix1, p_block *matrix2, fixed *result);
  virtual void call(fixed scalar1, p_block *matrix2, fixed *result);
  virtual void call(p_block *matrix1, fixed scalar2, fixed *result);
#else
  virtual void call(double scalar1, double scalar2, double *result);
  virtual void call(p_block *matrix1, p_block *matrix2, double *result);
  virtual void call(double scalar1, p_block *matrix2, double *result);
  virtual void call(p_block *matrix1, double scalar2, double *result);
#endif
};

#endif /* _BINARY_OP_HPP */
