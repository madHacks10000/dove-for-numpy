#ifndef _INTERNALS_HPP
#define _INTERNALS_HPP

#include <cstddef>
#include <stdexcept>
#include <vector>

#ifdef LIB_FTFP
extern "C" {
#include "ftfp.h"
}
#endif

class p_block
{
public:
#ifdef LIB_FTFP
  p_block(int nrows, int ncols, bool is_const, fixed* chunk);
  p_block(int nrows, int ncols, bool is_const, p_block* p, std::vector<fixed*>& src_ptrs);
  void add(fixed* d);
  fixed *get(int idx);
  void set(int idx, fixed* to_set) { ptrs[idx] = to_set; } ;
#else
  p_block(int nrows, int ncols, bool is_const, double* chunk);
  p_block(int nrows, int ncols, bool is_const, p_block* p, std::vector<double*>& src_ptrs);
  void add(double* d);
  double *get(int idx);
  void set(int idx, double* to_set) { ptrs[idx] = to_set; } ;
#endif
  p_block(int nrows, int ncols, bool is_const, p_block* p);
  ~p_block();

  size_t size() { return (parent ? ptrs.size() : num_rows * num_cols); };

  p_block* parent;
  int num_rows;
  int num_cols;
  bool is_const;

private:
#ifdef LIB_FTFP
  std::vector<fixed*> ptrs;
#else
  std::vector<double*> ptrs;
#endif
};
#endif /* _INTERNALS_HPP */
