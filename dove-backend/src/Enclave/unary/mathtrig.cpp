#include "mathtrig.hpp"

#ifdef LIB_FTFP
void ExpOp::call(fixed scalar, fixed *result)
{
  *result = fix_exp(scalar);
#else
void ExpOp::call(double scalar, double *result)
{
  *result = std::exp(scalar);
#endif
  UnaryOp::call(scalar, result);
}

#ifdef LIB_FTFP
void LogOp::call(fixed scalar, fixed *result)
{
  *result = fix_ln(scalar);
#else
void LogOp::call(double scalar, double *result)
{
  *result = std::log(scalar);
#endif
  UnaryOp::call(scalar, result);
}

#ifdef LIB_FTFP
void CosOp::call(fixed scalar, fixed *result)
{
  *result = fix_cos(scalar);
#else
void CosOp::call(double scalar, double *result)
{
  *result = std::cos(scalar);
#endif
  UnaryOp::call(scalar, result);
}

#ifdef LIB_FTFP
void SinOp::call(fixed scalar, fixed *result)
{
  *result = fix_sin(scalar);
#else
void SinOp::call(double scalar, double *result)
{
  *result = std::sin(scalar);
#endif
  UnaryOp::call(scalar, result);
}

#ifdef LIB_FTFP
void TanOp::call(fixed scalar, fixed *result)
{
  *result = fix_tan(scalar);
#else
void TanOp::call(double scalar, double *result)
{
  *result = std::tan(scalar);
#endif
  UnaryOp::call(scalar, result);
}
