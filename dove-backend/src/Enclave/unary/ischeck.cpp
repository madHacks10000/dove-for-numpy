#include "ischeck.hpp"

#ifdef LIB_FTFP
void IsNaOp::call(fixed scalar, fixed *result)
{
  Primitives::place_bool_in_fixed(Primitives::is_na(scalar), result);
}
#else
void IsNaOp::call(double scalar, double *result)
{
  *result = (double) (Primitives::is_na(scalar));
}
#endif /* LIB_FTFP */
#ifdef LIB_FTFP
void IsNanOp::call(fixed scalar, fixed *result)
{
  Primitives::place_bool_in_fixed(Primitives::is_nan(scalar), result);
}
#else
void IsNanOp::call(double scalar, double *result)
{
  *result = (double) (Primitives::is_nan(scalar));
}
#endif /* LIB_FTFP */
#ifdef LIB_FTFP
void IsInfiniteOp::call(fixed scalar, fixed *result)
{
  int8_t ret = fix_is_inf_pos(scalar) | fix_is_inf_neg(scalar);
  Primitives::place_bool_in_fixed(ret, result);
}
#else
void IsInfiniteOp::call(double scalar, double *result)
{
  *result = (double) (std::isinf(scalar));
}
#endif /* LIB_FTFP */
