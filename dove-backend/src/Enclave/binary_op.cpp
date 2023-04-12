#include "binary_op.hpp"

#ifdef LIB_FTFP
void BinaryOp::call(fixed scalar1, fixed scalar2, fixed *result)
{
  fixed na = Primitives::na_value();
#else
void BinaryOp::call(double scalar1, double scalar2, double *result)
{
  double na = Primitives::na_value();
#endif
  int is_na = Primitives::is_na(scalar1) | Primitives::is_na(scalar2);
  Primitives::cmov64(is_na, &na, result);
}

#ifdef LIB_FTFP
void BinaryOp::call(p_block *matrix1, p_block *matrix2, fixed *result)
#else
void BinaryOp::call(p_block *matrix1, p_block *matrix2, double *result)
#endif
{
  if (matrix1 == NULL || matrix2 == NULL || result == NULL) {
    throw std::invalid_argument("pointers must be valid");
  }
  size_t m1_sz = matrix1->num_rows * matrix1->num_cols;
  size_t m2_sz = matrix2->num_rows * matrix2->num_cols;
  if (m1_sz != m2_sz) {
    throw std::invalid_argument("mismatched matrices");
  }

  for (size_t i = 0; i < m1_sz; i++) {
    call(*(matrix1->get(i)), *(matrix2->get(i)), result+i);
  }
}

#ifdef LIB_FTFP
void BinaryOp::call(fixed scalar1, p_block *matrix2, fixed *result)
#else
void BinaryOp::call(double scalar1, p_block *matrix2, double *result)
#endif
{
  if (matrix2 == NULL || result == NULL) {
    throw std::invalid_argument("pointers must be valid");
  }
  size_t m_sz = matrix2->num_rows * matrix2->num_cols;
  for (size_t i = 0; i < m_sz; i++) {
    call(scalar1, *(matrix2->get(i)), result+i);
  }
}

#ifdef LIB_FTFP
void BinaryOp::call(p_block *matrix1, fixed scalar2, fixed *result)
#else
void BinaryOp::call(p_block *matrix1, double scalar2, double *result)
#endif
{
  if (matrix1 == NULL || result == NULL) {
    throw std::invalid_argument("pointers must be valid");
  }
  size_t m_sz =matrix1->num_rows * matrix1->num_cols;
  for (size_t i = 0; i < m_sz; i++) {
    call(*(matrix1->get(i)), scalar2, result+i);
  }
}
