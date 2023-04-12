#ifndef _PRINT_HPP
#define _PRINT_HPP
#include "../unary_op.hpp"

#ifdef NOENCLAVE
#include "../App/App.hpp"

#else
#include "../Enclave_t.h"
#endif /* NOENCLAVE */

#define MAX_LENGTH 1000

class PrintOp: public UnaryOp {
#ifdef LIB_FTFP
  void call(fixed scalar, fixed *result);
  void call(p_block* matrix, fixed *result);
#else
  void call(double scalar, double *result);
  void call(p_block* matrix, double *result);
#endif /* LIB_FTFP */
};

#endif /* _PRINT_HPP */
