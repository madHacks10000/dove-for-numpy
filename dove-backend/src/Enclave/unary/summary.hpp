#ifndef _SUMMARY_HPP
#define _SUMMARY_HPP
#include "../unary_op.hpp"

class SummaryOp: public UnaryOp {
public:
  SummaryOp(int is_na_rm): na_rm(is_na_rm) { }
  virtual ~SummaryOp() { } 
#ifdef LIB_FTFP
  inline void check_na_flag(fixed *scalar, fixed *dummy, int *has_na)
#else
  inline void check_na_flag(double *scalar, double *dummy, int *has_na)
#endif
  {
    int na_flag = Primitives::is_na(*scalar);
    *has_na |= na_flag;
    Primitives::cmov64(!na_flag, scalar, dummy);
  }

#ifdef LIB_FTFP
  void call(fixed scalar, fixed *result)
  {
    fixed *d1 = new fixed[1];  // Freed by p_block's destructor.
#else
  void call(double scalar, double *result)
  {
    double *d1 = new double[1];  // Freed by p_block's destructor.
#endif
    p_block p(1, 1, 0, d1);
    *d1 = scalar;
    p.add(d1);
    call(&p, result);
  };

#ifdef LIB_FTFP
  virtual void call(p_block *matrix, fixed *result) = 0;
#else
  virtual void call(p_block *matrix, double *result) = 0;
#endif

  int na_rm;
};

#ifdef LIB_FTFP
class SumFunc: public SummaryOp {
public:
  SumFunc(int is_na_rm): SummaryOp(is_na_rm) { }
  virtual void call(p_block *matrix, fixed *result);
};

class ProdFunc: public SummaryOp {
public:
  ProdFunc(int is_na_rm): SummaryOp(is_na_rm) { }
  virtual void call(p_block *matrix, fixed *result);
};

class MeanFunc: public SumFunc {
public:
  MeanFunc(int is_na_rm): SumFunc(is_na_rm) { }
  virtual void call(p_block *matrix, fixed *result);
};

class AnyFunc: public SummaryOp {
public:
  AnyFunc(int is_na_rm): SummaryOp(is_na_rm) { }
  void call(p_block *matrix, fixed *result);
};

class AllFunc: public SummaryOp {
public:
  AllFunc(int is_na_rm): SummaryOp(is_na_rm) { }
  void call(p_block *matrix, fixed *result);
};

class RowSumsFunc: public SumFunc {
public:
  RowSumsFunc(int is_na_rm): SumFunc(is_na_rm) { }
  void call(p_block *matrix, fixed *result);
};

class ColSumsFunc: public SumFunc {
public:
  ColSumsFunc(int is_na_rm): SumFunc(is_na_rm) { }
  void call(p_block *matrix, fixed *result);
};

class RowMeansFunc: public MeanFunc {
public:
  RowMeansFunc(int is_na_rm): MeanFunc(is_na_rm) { }
  void call(p_block *matrix, fixed *result);
};

class ColMeansFunc: public MeanFunc {
public:
  ColMeansFunc(int is_na_rm): MeanFunc(is_na_rm) { }
  void call(p_block *matrix, fixed *result);
};

class MinFunc: virtual public SummaryOp {
public:
  MinFunc(int is_na_rm): SummaryOp(is_na_rm) { }
  virtual void call(p_block *matrix, fixed *result);
};

class MaxFunc: virtual public SummaryOp {
public:
  MaxFunc(int is_na_rm): SummaryOp(is_na_rm) { }
  virtual void call(p_block *matrix, fixed *result);
};

class RangeFunc: public MaxFunc, public MinFunc {
public:
  RangeFunc(int is_na_rm): SummaryOp(is_na_rm), MaxFunc(is_na_rm), MinFunc(is_na_rm) { }
  void call(p_block *matrix, fixed *result);
};
#else /* ELSE */
class SumFunc: public SummaryOp {
public:
  SumFunc(int is_na_rm): SummaryOp(is_na_rm) { }
  virtual void call(p_block *matrix, double *result);
};

class ProdFunc: public SummaryOp {
public:
  ProdFunc(int is_na_rm): SummaryOp(is_na_rm) { }
  virtual void call(p_block *matrix, double *result);
};

class MeanFunc: public SumFunc {
public:
  MeanFunc(int is_na_rm): SumFunc(is_na_rm) { }
  virtual void call(p_block *matrix, double *result);
};

class AnyFunc: public SummaryOp {
public:
  AnyFunc(int is_na_rm): SummaryOp(is_na_rm) { }
  void call(p_block *matrix, double *result);
};

class AllFunc: public SummaryOp {
public:
  AllFunc(int is_na_rm): SummaryOp(is_na_rm) { }
  void call(p_block *matrix, double *result);
};

class RowSumsFunc: public SumFunc {
public:
  RowSumsFunc(int is_na_rm): SumFunc(is_na_rm) { }
  void call(p_block *matrix, double *result);
};

class ColSumsFunc: public SumFunc {
public:
  ColSumsFunc(int is_na_rm): SumFunc(is_na_rm) { }
  void call(p_block *matrix, double *result);
};

class RowMeansFunc: public MeanFunc {
public:
  RowMeansFunc(int is_na_rm): MeanFunc(is_na_rm) { }
  void call(p_block *matrix, double *result);
};

class ColMeansFunc: public MeanFunc {
public:
  ColMeansFunc(int is_na_rm): MeanFunc(is_na_rm) { }
  void call(p_block *matrix, double *result);
};

class MinFunc: virtual public SummaryOp {
public:
  MinFunc(int is_na_rm): SummaryOp(is_na_rm) { }
  virtual void call(p_block *matrix, double *result);
};

class MaxFunc: virtual public SummaryOp {
public:
  MaxFunc(int is_na_rm): SummaryOp(is_na_rm) { }
  virtual void call(p_block *matrix, double *result);
};

class RangeFunc: public MaxFunc, public MinFunc {
public:
  RangeFunc(int is_na_rm): SummaryOp(is_na_rm), MaxFunc(is_na_rm), MinFunc(is_na_rm) { }
  void call(p_block *matrix, double *result);
};
#endif /* LIB_FTFP */
#endif /* _SUMMARY_HPP */
