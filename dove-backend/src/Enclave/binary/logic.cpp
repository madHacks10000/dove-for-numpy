#include "logic.hpp"

#ifdef LIB_FTFP
void BitwiseAndOp::call(fixed scalar1, fixed scalar2, fixed *result)
{
  int64_t s1 = Primitives::fixed_to_int(scalar1);
  int64_t s2 = Primitives::fixed_to_int(scalar2);
  Primitives::place_bool_in_fixed(s1 & s2, result);
#else
void BitwiseAndOp::call(double scalar1, double scalar2, double *result)
{
  *result = (double)((int) scalar1 & (int) scalar2);
#endif /* LIB_FTFP */
  BinaryOp::call(scalar1, scalar2, result);
}

#ifdef LIB_FTFP
void BitwiseOrOp::call(fixed scalar1, fixed scalar2, fixed *result)
{
  int64_t s1 = Primitives::fixed_to_int(scalar1);
  int64_t s2 = Primitives::fixed_to_int(scalar2);
  Primitives::place_bool_in_fixed(s1 | s2, result);
#else
void BitwiseOrOp::call(double scalar1, double scalar2, double *result)
{
  *result = (double)((int) scalar1 | (int) scalar2);
#endif /* LIB_FTFP */
  BinaryOp::call(scalar1, scalar2, result);
}
