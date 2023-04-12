#ifndef _PRIMITIVES_HPP
#define _PRIMITIVES_HPP

#ifdef LIB_FTFP
extern "C" {
#include "ftfp.h"
}
#endif /* LIB_FTFP */

class Primitives {
public:
#ifdef LIB_FTFP
  static fixed na_value();
  static double na_r_value();
  static int is_na(fixed x);
  static int is_nan(fixed x);
  static int fixed_to_int(fixed x);
  static void place_bool_in_fixed(int8_t b, fixed* addr);
#else
  static double na_value();
  static int is_na(double x);
  static int is_nan(double x);
#endif /* LIB_FTFP */

  static void cmov64(int cond, void* src_ptr, void* dst_ptr);
  Primitives(Primitives const&) = delete;
  void operator=(Primitives const&) = delete;

  typedef union
  {
    double value;
    unsigned int word[2];
  } _ieee_double;

  static const int _HW = 1;
  static const int _LW = 0;
};

#endif /* _PRIMITIVES_H */
