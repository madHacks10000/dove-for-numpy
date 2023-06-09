#include <limits>
#include "summary.hpp"

#ifdef LIB_FTFP
void SumFunc::call(p_block *matrix, fixed *result)
{
  fixed sum = FIX_ZERO;
  int has_na = 0;

  size_t m_sz = matrix->num_cols * matrix->num_rows;
  for (size_t i = 0; i < m_sz; i++) {
    fixed* ptr = matrix->get(i);
    fixed current_val = *ptr;
    fixed dummy_val = FIX_ZERO;
    check_na_flag(&current_val, &dummy_val, &has_na);
    sum = fix_add(sum,dummy_val);
  }

  *result = Primitives::na_value();
  Primitives::cmov64(na_rm | !has_na, &sum, result);
}

void ProdFunc::call(p_block *matrix, fixed *result)
{
  fixed prod = fix_convert_from_double(1);
  int has_na = 0;

  size_t m_sz = matrix->num_cols * matrix->num_rows;
  for (size_t i = 0; i < m_sz; i++) {
    fixed* ptr = matrix->get(i);
    fixed current_val = *ptr;
    fixed dummy_val = fix_convert_from_double(1);
    check_na_flag(&current_val, &dummy_val, &has_na);
    prod = fix_mul(prod,dummy_val);
  }

  *result = Primitives::na_value();
  Primitives::cmov64(na_rm | !has_na, &prod, result);
}

void MeanFunc::call(p_block *matrix, fixed *result)
{
  fixed mean = FIX_ZERO;
  size_t len = matrix->num_cols * matrix->num_rows;
  int has_na = 0;

  SumFunc::call(matrix, result);
  mean = fix_div(*result, fix_convert_from_int64(len));

  *result = Primitives::na_value();
  Primitives::cmov64(na_rm | !has_na, &mean, result);
}

void AnyFunc::call(p_block *matrix, fixed *result)
{
  int has_na = 0;
  int ret = 0;
  fixed output = FIX_ZERO;

  size_t m_sz = matrix->num_cols * matrix->num_rows;
  for (size_t i = 0; i < m_sz; i++) {
    fixed* ptr = matrix->get(i);
    fixed current_val = *ptr;
    fixed dummy_val = FIX_ZERO;
    check_na_flag(&current_val, &dummy_val, &has_na);
    ret = ret | Primitives::fixed_to_int(dummy_val);
  }

  output = fix_convert_from_int64(ret);
  *result = Primitives::na_value();
  Primitives::cmov64(na_rm | !has_na, &output, result);
}

void AllFunc::call(p_block *matrix, fixed *result)
{
  int has_na = 0;
  int ret = 1;
  fixed output = FIX_ZERO;

  size_t m_sz = matrix->num_cols * matrix->num_rows;
  for (size_t i = 0; i < m_sz; i++) {
    fixed* ptr = matrix->get(i);
    fixed current_val = *ptr;
    fixed dummy_val = fix_convert_from_double(1);
    check_na_flag(&current_val, &dummy_val, &has_na);
    ret = ret & Primitives::fixed_to_int(dummy_val);
  }

  output = fix_convert_from_int64(ret);
  *result = Primitives::na_value();
  Primitives::cmov64(na_rm | !has_na, &output, result);
}

void MinFunc::call(p_block *matrix, fixed *result) {
  int finite = 0; //TODO allow finite to be one of arguments
  int has_na = 0;
  fixed ret = FIX_INF_POS;

  size_t m_sz = matrix->num_cols * matrix->num_rows;
  for (size_t i = 0; i < m_sz; i++) {
    fixed* ptr = matrix->get(i);
    fixed current_val = *ptr;
    fixed dummy_val = FIX_INF_POS;
    check_na_flag(&current_val, &dummy_val, &has_na);
    int fflag, is_new_min;

    fflag = ((int) !fix_is_inf_neg(dummy_val)) | !finite;
    is_new_min = ((int) fix_gt(ret, dummy_val)) & fflag;
    Primitives::cmov64(is_new_min, &dummy_val, &ret);
  }

  *result = Primitives::na_value();
  Primitives::cmov64(na_rm | !has_na, &ret, result);
}

void MaxFunc::call(p_block *matrix, fixed *result)
{  
  int finite = 0;// TODO: allow finite to be one of arguments
  int has_na = 0;
  fixed ret = FIX_INF_NEG;

  size_t m_sz = matrix->num_cols * matrix->num_rows;
  for (size_t i = 0; i < m_sz; i++) {
    fixed* ptr = matrix->get(i);
    fixed current_val = *ptr;
    fixed dummy_val = FIX_INF_NEG;
    check_na_flag(&current_val, &dummy_val, &has_na);
    int fflag, is_new_max;

    fflag = ((int) !fix_is_inf_pos(dummy_val)) | !finite;
    is_new_max = ((int) fix_lt(ret, dummy_val)) & fflag;
    Primitives::cmov64(is_new_max, &dummy_val, &ret);
  }

  *result = Primitives::na_value();
  Primitives::cmov64(na_rm | !has_na, &ret, result);
}

void RangeFunc::call(p_block *matrix, fixed *result)
{
  MinFunc::call(matrix, &result[0]);
  MaxFunc::call(matrix, &result[1]);
}

#else /* ELSE */

void SumFunc::call(p_block *matrix, double *result)
{
  double sum = 0;
  int has_na = 0;

  size_t m_sz = matrix->num_cols * matrix->num_rows;
  for(size_t i = 0; i < m_sz; i++) {
    double* ptr = matrix->get(i);
    double current_val = *ptr;
    double dummy_val = 0;
    check_na_flag(&current_val, &dummy_val, &has_na);
    sum += dummy_val;
  }

  *result = Primitives::na_value();
  Primitives::cmov64(na_rm | !has_na, &sum, result);
}

void ProdFunc::call(p_block *matrix, double *result)
{
  double prod = 1;
  int has_na = 0;

  size_t m_sz = matrix->num_cols * matrix->num_rows;
  for(size_t i = 0; i < m_sz; i++) {
    double* ptr = matrix->get(i);
    double current_val = *ptr;
    double dummy_val = 1;
    check_na_flag(&current_val, &dummy_val, &has_na);
    prod *= dummy_val;
  }

  *result = Primitives::na_value();
  Primitives::cmov64(na_rm | !has_na, &prod, result);
}

void AnyFunc::call(p_block *matrix, double *result)
{
  int has_na = 0;
  int ret = 0;
  double output = 0;

  size_t m_sz = matrix->num_cols * matrix->num_rows;
  for(size_t i = 0; i < m_sz; i++) {
    double* ptr = matrix->get(i);
    double current_val = *ptr;
    double dummy_val = 0;
    check_na_flag(&current_val, &dummy_val, &has_na);
    ret = ret | (int)dummy_val;
  }

  output = ret;
  *result = Primitives::na_value();
  Primitives::cmov64(na_rm | !has_na, &output, result);
}

void AllFunc::call(p_block *matrix, double *result)
{
  int has_na = 0;
  int ret = 1;
  double output = 0;

  size_t m_sz = matrix->num_cols * matrix->num_rows;
  for(size_t i = 0; i < m_sz; i++) {
    double* ptr = matrix->get(i);
    double current_val = *ptr;
    double dummy_val = 1;
    check_na_flag(&current_val, &dummy_val, &has_na);
    ret = ret & (int)dummy_val;
  }

  output = ret;
  *result = Primitives::na_value();
  Primitives::cmov64(na_rm | !has_na, &output, result);
}

void MinFunc::call(p_block *matrix, double *result) {
  int finite = 0; //TODO: allow finite to be one of arguments
  int has_na = 0;
  double ret = std::numeric_limits<double>::infinity();
  double lowest = std::numeric_limits<double>::lowest();

  size_t m_sz = matrix->num_cols * matrix->num_rows;
  for(size_t i = 0; i < m_sz; i++) {
    double* ptr = matrix->get(i);
    double current_val = *ptr;
    double dummy_val = std::numeric_limits<double>::infinity();
    check_na_flag(&current_val, &dummy_val, &has_na);
    int fflag, is_new_min;

    fflag = (lowest <= dummy_val) | !finite;
    is_new_min = (ret > dummy_val) & fflag;
    Primitives::cmov64(is_new_min, &dummy_val, &ret);
  }

  *result = Primitives::na_value();
  Primitives::cmov64(na_rm | !has_na, &ret, result);
}

void MaxFunc::call(p_block *matrix, double *result)
{  
  int finite = 0;// TODO: allow finite to be one of arguments
  int has_na = 0;
  double ret = -std::numeric_limits<double>::infinity();
  double highest = std::numeric_limits<double>::max();

  size_t m_sz = matrix->num_cols * matrix->num_rows;
  for(size_t i = 0; i < m_sz; i++) {
    double* ptr = matrix->get(i);
    double current_val = *ptr;
    double dummy_val = -std::numeric_limits<double>::infinity();
    check_na_flag(&current_val, &dummy_val, &has_na);
    int fflag, is_new_max;

    fflag = (highest >= dummy_val) | !finite;
    is_new_max = (ret < dummy_val) & fflag;
    Primitives::cmov64(is_new_max, &dummy_val, &ret);
  }

  *result = Primitives::na_value();
  Primitives::cmov64(na_rm | !has_na, &ret, result);
}

void RangeFunc::call(p_block *matrix, double *result)
{
  MinFunc::call(matrix, &result[0]);
  MaxFunc::call(matrix, &result[1]);
}
#endif /* LIB_FTFP */
