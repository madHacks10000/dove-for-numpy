#include "log_bin.hpp"

#ifdef LIB_FTFP
void LogBinOp::call(fixed scalar1, fixed scalar2, fixed *result)
{
  fixed x = scalar1;
  fixed y = scalar2;
  fixed ln_x = fix_ln(x);
  fixed ln_y = fix_ln(y);
  *result = fix_div(ln_x, ln_y);
#else
void LogBinOp::call(double scalar1, double scalar2, double *result)
{
  *result = log(scalar1)/log(scalar2);
#endif
  BinaryOp::call(scalar1, scalar2, result);
}
