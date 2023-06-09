#include "plusminus.hpp"

#ifdef LIB_FTFP
void NoOp::call(fixed scalar, fixed *result)
#else
void NoOp::call(double scalar, double *result)
#endif
{
  *result = scalar;
  UnaryOp::call(scalar, result);
}
#ifdef LIB_FTFP
void NegationOp::call(fixed scalar, fixed *result)
{
  *result = fix_neg(scalar);
#else
void NegationOp::call(double scalar, double *result)
{
  *result = -scalar;
#endif
  UnaryOp::call(scalar, result);
}

#ifdef LIB_FTFP
void BitwiseNotOp::call(fixed scalar, fixed *result)
{
    Primitives::place_bool_in_fixed(!fix_convert_to_int64(scalar),
            result);
#else
void BitwiseNotOp::call(double scalar, double *result)
{
  *result = (double) (!((int) scalar));
#endif /* LIB_FTFP */
  UnaryOp::call(scalar, result);
}
