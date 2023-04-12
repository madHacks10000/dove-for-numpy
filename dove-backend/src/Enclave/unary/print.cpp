#include "print.hpp"

#ifdef LIB_FTFP
void PrintOp::call(fixed scalar, fixed *result)
{
  size_t len = sizeof(double);
  double* dump_buf = (double*)malloc(len);
  *dump_buf = fix_convert_to_double(scalar);
#else
void PrintOp::call(double scalar, double *result)
{
  size_t len = sizeof(double);
  double* dump_buf = (double*)malloc(len);
  *dump_buf = scalar;
#endif
  ocall_print(std::to_string(*dump_buf).data());
  ocall_dump(dump_buf, len);
  free(dump_buf);
}

#ifdef LIB_FTFP
void PrintOp::call(p_block* matrix, fixed *result)
{
#else
void PrintOp::call(p_block* matrix, double *result)
{
#endif
  size_t count = matrix->num_rows * matrix->num_cols;
  size_t len = count * sizeof(double);
  double* dump_buf = (double*)malloc(len);
  std::string s = "[";
  for (size_t i = 0; i < count; i++) {
#ifdef LIB_FTFP
    fixed val = *matrix->get(i);
    dump_buf[i] = fix_convert_to_double(val);
    double na_val = Primitives::na_r_value();
    Primitives::cmov64(Primitives::is_na(val), &na_val, &dump_buf[i]);
#else
    dump_buf[i] = *matrix->get(i);
#endif
      s += (std::to_string(dump_buf[i]) + ", ");
  }
  s += "]";
  ocall_print(s.c_str());
  ocall_dump(dump_buf, len);
  free(dump_buf);
}
