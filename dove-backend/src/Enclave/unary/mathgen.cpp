#include "mathgen.hpp"

#ifdef LIB_FTFP
void AbsOp::call(fixed scalar, fixed *result)
{
  *result = fix_abs(scalar);
#else
void AbsOp::call(double scalar, double *result)
{
  *result = std::abs(scalar);
#endif
  UnaryOp::call(scalar, result);
}

#ifdef LIB_FTFP
void SignOp::call(fixed scalar, fixed *result)
{
  fixed zero = FIX_ZERO;
  int8_t f = fix_cmp(scalar, zero);
  *result = fix_convert_from_int64(f);
#else
void SignOp::call(double scalar, double *result)
{
  *result = 0; //assumed to be zero
  int is_neg = (scalar < 0);
  int is_pos = (scalar > 0);
  double negsign = -1;
  double possign = 1;
  Primitives::cmov64(is_neg, &negsign, result);
  Primitives::cmov64(is_pos, &possign, result);
#endif
  UnaryOp::call(scalar, result);
}

#ifdef LIB_FTFP
void SqrtOp::call(fixed scalar, fixed *result)
{
  *result = fix_sqrt(scalar);
#else
void SqrtOp::call(double scalar, double *result)
{
  *result = std::sqrt(scalar);
#endif
  UnaryOp::call(scalar, result);  
}

#ifdef LIB_FTFP
void FloorOp::call(fixed scalar, fixed *result)
{
  *result = fix_floor(scalar);
#else
void FloorOp::call(double scalar, double *result)
{
  *result = std::floor(scalar);
#endif
  UnaryOp::call(scalar, result);
}

#ifdef LIB_FTFP
void CeilingOp::call(fixed scalar, fixed *result)
{
  *result = fix_ceil(scalar);
#else
void CeilingOp::call(double scalar, double *result)
{
  *result = std::ceil(scalar);
#endif
  UnaryOp::call(scalar, result);
}
