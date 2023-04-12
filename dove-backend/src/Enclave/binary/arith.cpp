#include "arith.hpp"
#ifdef LIB_FTFP
void AdditionOp::call(fixed scalar1, fixed scalar2, fixed *result)
{
    *result = fix_add(scalar1, scalar2);
#else
void AdditionOp::call(double scalar1, double scalar2, double *result)
{
  *result = scalar1 + scalar2;
#endif
  BinaryOp::call(scalar1, scalar2, result);
}
#ifdef LIB_FTFP
void SubtractionOp::call(fixed scalar1, fixed scalar2, fixed *result)
{
    *result = fix_sub(scalar1, scalar2);
#else
void SubtractionOp::call(double scalar1, double scalar2, double *result)
{
  *result = scalar1 - scalar2;
#endif
  BinaryOp::call(scalar1, scalar2, result);
}

#ifdef LIB_FTFP
void MultiplicationOp::call(fixed scalar1, fixed scalar2, fixed *result)
{
    *result = fix_mul(scalar1, scalar2);
#else
void MultiplicationOp::call(double scalar1, double scalar2, double *result)
{
  *result = scalar1 * scalar2;
#endif
  BinaryOp::call(scalar1, scalar2, result);
}

#ifdef LIB_FTFP
void DivisionOp::call(fixed scalar1, fixed scalar2, fixed *result)
{
    *result = fix_div(scalar1, scalar2);
#else
void DivisionOp::call(double scalar1, double scalar2, double *result)
{
  *result = scalar1 / scalar2;
#endif
  BinaryOp::call(scalar1, scalar2, result);
}

#ifdef LIB_FTFP
void PowOp::call(fixed scalar1, fixed scalar2, fixed *result)
{
    *result = fix_pow(scalar1, scalar2);
#else
void PowOp::call(double scalar1, double scalar2, double *result)
{
  *result = std::pow(scalar1, scalar2);
#endif
  BinaryOp::call(scalar1, scalar2, result);
}

//based on myfmod from r-source
#ifdef LIB_FTFP
void ModOp::call(fixed scalar1, fixed scalar2, fixed *result)
{
  fixed a = scalar1;
  fixed b = scalar2;
  fixed q = fix_div(a, b);
  fixed tmp = fix_floor(q);
  tmp = fix_mul(tmp, b);
  tmp = fix_sub(a, tmp);
  q = fix_floor(fix_div(tmp, b));
  *result = fix_sub(tmp, fix_mul(q, b));
#else
void ModOp::call(double scalar1, double scalar2, double *result)
{
  double q = scalar1/scalar2;
  double tmp = scalar1 - floor(q) * scalar2;
  q = floor(tmp/scalar2);
  *result = tmp - q * scalar2;
#endif
  BinaryOp::call(scalar1, scalar2, result);
}

#ifdef LIB_FTFP
void IDivOp::call(fixed scalar1, fixed scalar2, fixed *result)
{
  *result = fix_floor(fix_div(scalar1,scalar2));
#else
void IDivOp::call(double scalar1, double scalar2, double *result)
{
  *result = floor(scalar1 / scalar2);
#endif
  BinaryOp::call(scalar1, scalar2, result);
}
