#include "unary_op.hpp"

#ifdef LIB_FTFP
void UnaryOp::call(fixed scalar, fixed *result)
{
    fixed na = Primitives::na_value();
#else
void UnaryOp::call(double scalar, double *result)
{
  // Check for NA
  double na = Primitives::na_value();
#endif
  int is_na = Primitives::is_na(scalar);
  Primitives::cmov64(is_na, &na, result);
}

#ifdef LIB_FTFP
void UnaryOp::call(p_block *matrix, fixed *result)
#else
void UnaryOp::call(p_block *matrix, double *result)
#endif
{
  if (matrix == NULL || result == NULL) {
    throw std::invalid_argument("both pointers must be valid");
  }
  size_t m_sz = matrix->num_rows * matrix->num_cols;
  for (size_t i = 0; i < m_sz; i++) {
    call(*(matrix->get(i)), result+i);
  }
}
