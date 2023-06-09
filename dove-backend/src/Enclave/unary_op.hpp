#ifndef _UNARY_OP_HPP
#define _UNARY_OP_HPP

#include <stdexcept>
#include <string>
#include <cstdarg>

#include "p_block.hpp"
#include "primitives.hpp"

#ifdef LIB_FTFP
extern "C" {
#include "ftfp.h"
}
#else
#include <cmath>
#endif

class UnaryOp {
public:
  UnaryOp() {}
  virtual ~UnaryOp() {};

#ifdef LIB_FTFP
  virtual void call(fixed scalar, fixed *result);
  virtual void call(p_block *matrix, fixed *result);
#else
  virtual void call(double scalar, double *result);
  virtual void call(p_block *matrix, double *result);
#endif
};

#endif /* _UNARY_OP_HPP */
