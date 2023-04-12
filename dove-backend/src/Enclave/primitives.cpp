#include <cmath>

#include "primitives.hpp"

#ifdef LIB_FTFP
void Primitives::place_bool_in_fixed(int8_t b, fixed* addr)
{
  fixed one = fix_convert_from_double(1);
  *addr = FIX_ZERO;
  Primitives::cmov64(b, &one, addr);
}

int Primitives::fixed_to_int(fixed x)
{
  return (int) fix_convert_to_int64(x);
}

fixed Primitives::na_value()
{
  return 0x1 + fix_convert_from_double(1954);
}

double Primitives::na_r_value()
{
  static volatile _ieee_double x;
  x.word[_HW] = 0x7ff00000;
  x.word[_LW] = 1954;
  return x.value;
}

int Primitives::is_na(fixed x)
{
  return (x == Primitives::na_value());
}

int Primitives::is_nan(fixed x)
{
  return (fix_is_nan(x)) & !(Primitives::is_na(x));
}

#else
double Primitives::na_value()
{
  static volatile _ieee_double x;
  x.word[_HW] = 0x7ff00000;
  x.word[_LW] = 1954;
  return x.value;
}

int Primitives::is_na(double x)
{
  _ieee_double y;
  y.value = x;
  return ((y.word[_LW] == 1954) & (y.word[_HW] == 0x7ff00000));
}

int Primitives::is_nan(double x)
{
  _ieee_double y;
  y.value = x;
  return ((y.word[_LW] != 1954) & (y.word[_HW] == 0x7ff00000));
}

#endif /* LIB_FTFP */

void Primitives::cmov64(int cond, void* src_ptr, void* dst_ptr)
{
  __asm__ __volatile__ (  "mov (%2), %%rax\n\t"

                          "test %0, %0\n\t"

                          "cmovne (%1), %%rax\n\t"

                          "mov %%rax, (%2)"

                          :

                          : "b"(cond), "c"(src_ptr), "d"(dst_ptr)

                          : "cc", "%rax", "memory"

                          );
}
