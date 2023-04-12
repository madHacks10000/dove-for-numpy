#include "matmul.hpp"

#ifdef LIB_FTFP
void MatMultOp::call(p_block* matrix1, p_block* matrix2, fixed *result)
{
#else
void MatMultOp::call(p_block* matrix1, p_block* matrix2, double *result)
{
#endif
  if(matrix1->num_cols != matrix2->num_rows)
    throw new std::runtime_error("matrix multiply error due to incorrect shape");
  int len = matrix1->num_cols;
  int rrow = matrix1->num_rows;
  int rcol = matrix2->num_cols;

  for(int i = 0; i < rrow; i++) {
    for(int j = 0; j < rcol; j++) {
#ifdef LIB_FTFP
      fixed tr = 0;
#else
      double tr = 0;
#endif
      int naflag = 0;
      for(int k = 0; k < len; k++) {
        int idx1 = i * len + k;
        int idx2 = k * rcol + j;
#ifdef LIB_FTFP
        fixed ttr = fix_mul(*matrix1->get(idx1), *matrix2->get(idx2));
        tr = fix_add(tr, ttr);
        naflag = naflag | Primitives::is_na(*matrix1->get(idx1)) | 
            Primitives::is_na(*matrix2->get(idx2));
#else
        double a = *matrix1->get(idx1);
        double b = *matrix2->get(idx2);
        tr += a * b;
        naflag = naflag | Primitives::is_na(a) | Primitives::is_na(b);
#endif
      }

      result[i * rcol + j] = tr;
#ifdef LIB_FTFP
      fixed na = Primitives::na_value();
#else
      double na = Primitives::na_value();
#endif
      Primitives::cmov64(naflag, &na, &result[i * rcol + j]);
    }
  }
}
