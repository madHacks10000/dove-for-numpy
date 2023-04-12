#ifndef _MATMUL_HPP
#define _MATMUL_HPP
#include "../binary_op.hpp"
#include "../primitives.hpp"

#include <vector>
#include <stdexcept>

class MatMultOp: public BinaryOp {
public:
#ifdef LIB_FTFP
  void call(p_block* matrix1, p_block* matrix2, fixed *result);
#else
  void call(p_block* matrix1, p_block* matrix2, double *result);
#endif /* LIB_FTFP */
};

#endif /* _MATMUL_HPP */
