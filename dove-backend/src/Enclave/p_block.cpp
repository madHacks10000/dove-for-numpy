#include "p_block.hpp"

#ifdef LIB_FTFP

p_block::p_block(int nrows, int ncols, bool is_const, fixed* chunk): parent(NULL), num_rows(nrows), num_cols(ncols), is_const(is_const), ptrs()
{
  ptrs.push_back(chunk);
}

p_block::p_block(int nrows, int ncols, bool is_const, p_block* p, std::vector<fixed*>& src_ptrs): parent(p), num_rows(nrows), num_cols(ncols), is_const(is_const), ptrs()
{
  for (fixed* curr_ptr: src_ptrs)
    ptrs.push_back(curr_ptr);
}

//this should only be used for sliced matrix
void p_block::add(fixed* d)
{
    if(!parent)
        throw std::runtime_error("you cannot use this function to a non-sliced matrix");
    ptrs.push_back(d);
}

fixed* p_block::get(int idx)
{
  if(parent)
    return ptrs.at(idx);
  else {
    fixed* blk = ptrs[0];
    return &blk[idx];
  }
}

#else

p_block::p_block(int nrows, int ncols, bool is_const, double* chunk): parent(NULL), num_rows(nrows), num_cols(ncols), is_const(is_const), ptrs()
{
    ptrs.push_back(chunk);
}

p_block::p_block(int nrows, int ncols, bool is_const, p_block* p, std::vector<double*>& src_ptrs): parent(p), num_rows(nrows), num_cols(ncols), is_const(is_const), ptrs()
{
  for (double* curr_ptr: src_ptrs)
    ptrs.push_back(curr_ptr);
}

//this should only be used for sliced matrix
void p_block::add(double* d)
{
    if(!parent)
        throw std::runtime_error("you cannot use this function to a non-sliced matrix");
    ptrs.push_back(d);
}

double* p_block::get(int idx)
{
  if(parent)
    return ptrs.at(idx);
  else {
    double* blk = ptrs[0];
    return &blk[idx];
  }
}

#endif

p_block::p_block(int nrows, int ncols, bool is_const, p_block* p): parent(p), num_rows(nrows), num_cols(ncols), is_const(is_const), ptrs() {}

p_block::~p_block()
{
  if(!parent)
    delete[] ptrs[0];
}
