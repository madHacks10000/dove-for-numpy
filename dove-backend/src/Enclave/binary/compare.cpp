#include "compare.hpp"

#ifdef LIB_FTFP
void EqualOp::call(fixed scalar1, fixed scalar2, fixed *result)
{
  Primitives::place_bool_in_fixed(fix_eq(scalar1,scalar2), result);
#else
void EqualOp::call(double scalar1, double scalar2, double *result)
{
  *result = (scalar1 == scalar2);
#endif
  BinaryOp::call(scalar1, scalar2, result);
}

#ifdef LIB_FTFP
void GreaterThanOp::call(fixed scalar1, fixed scalar2, fixed *result)
{
  Primitives::place_bool_in_fixed(fix_gt(scalar1,scalar2), result);
#else
void GreaterThanOp::call(double scalar1, double scalar2, double *result)
{
  *result = (scalar1 > scalar2);
#endif
  BinaryOp::call(scalar1, scalar2, result);
}

#ifdef LIB_FTFP
void LessThanOp::call(fixed scalar1, fixed scalar2, fixed *result)
{
  Primitives::place_bool_in_fixed(fix_lt(scalar1,scalar2), result);
#else
void LessThanOp::call(double scalar1, double scalar2, double *result)
{
  *result = (scalar1 < scalar2);
#endif
  BinaryOp::call(scalar1, scalar2, result);
}

#ifdef LIB_FTFP
void NotEqualOp::call(fixed scalar1, fixed scalar2, fixed *result)
{
  Primitives::place_bool_in_fixed(fix_ne(scalar1,scalar2), result);
#else
void NotEqualOp::call(double scalar1, double scalar2, double *result)
{
  *result = (scalar1 != scalar2);
#endif
  BinaryOp::call(scalar1, scalar2, result);
}

#ifdef LIB_FTFP
void GreaterThanEqualOp::call(fixed scalar1, fixed scalar2, fixed *result)
{
  Primitives::place_bool_in_fixed(fix_ge(scalar1,scalar2), result);
#else
void GreaterThanEqualOp::call(double scalar1, double scalar2, double *result)
{
  *result = (scalar1 >= scalar2);
#endif
  BinaryOp::call(scalar1, scalar2, result);
}

#ifdef LIB_FTFP
void LessThanEqualOp::call(fixed scalar1, fixed scalar2, fixed *result)
{
  Primitives::place_bool_in_fixed(fix_le(scalar1,scalar2), result);
#else
void LessThanEqualOp::call(double scalar1, double scalar2, double *result)
{
  *result = (scalar1 <= scalar2);
#endif
  BinaryOp::call(scalar1, scalar2, result);
}
