#include <cmath>
#include <stdexcept>

#ifndef NOENCLAVE
#include "Enclave_t.h"
#else
#include "../App/App.hpp"
#endif

#include "primitives.hpp"

#include "symbols.hpp"


#ifdef LIB_FTFP
int Symbols::is_r_na(double x)
{
  Primitives::_ieee_double y;
  y.value = x;
  return ((y.word[Primitives::_LW] == 1954) & (y.word[Primitives::_HW] == 0x7ff00000));
}
#endif

void Symbols::push_dataset(double* secrets, const char* dataset_name, int num_rows, int num_cols)
{
  int size = num_rows * num_cols;
#ifdef LIB_FTFP
  fixed* data_buf = new fixed[size];
#else
  double* data_buf = new double[size];
#endif

  std::string name(dataset_name);
  if(cblocks.find(name) == cblocks.end())
    cblocks[name] = data_buf;
  else
    std::invalid_argument("dataset name conflict is found");

  for(int i = 0; i < size; i++) {
#ifdef LIB_FTFP
    int is_na = Symbols::is_r_na(secrets[i]);
    fixed na_val = Primitives::na_value();
    data_buf[i] = fix_convert_from_double(secrets[i]);
    Primitives::cmov64(is_na, &na_val, &data_buf[i]);
#else
    data_buf[i] = secrets[i];
#endif
  }

  std::string metadata(dataset_name);
  ocall_write_metadata(metadata.c_str(), num_rows, num_cols);
}

void Symbols::push_mtx(int idx, p_block* new_block)
{
    if (hashmap.find(idx) == hashmap.end()) {
        hashmap[idx] = new_block;
    } else if (nest_level > 0) {
        hashmap[idx] = new_block;
    } else {
        throw std::invalid_argument("matrix index conflict found");
    }
}

#ifdef LIB_FTFP
void Symbols::push_register(int idx, fixed value)
#else
void Symbols::push_register(int idx, double value)
#endif
{
    if(nest_level > 0 || regs.find(idx) == regs.end()) {
        regs[idx] = value;
    } else {
        throw std::invalid_argument("register index conflict found in global scope");
    }

}

void Symbols::push_index(int idx, int init_val)
{
    if(indicies.find(idx) == indicies.end())
        indicies[idx] = init_val;
    else
        throw std::invalid_argument("loop index conflict found");
}
#ifdef LIB_FTFP
fixed* Symbols::pull_dataset(std::string& dsname)
#else
double* Symbols::pull_dataset(std::string& dsname)
#endif
{
  if(cblocks.find(dsname) != cblocks.end())
    return cblocks[dsname];
  throw std::invalid_argument("no dataset found to load with name " + dsname);
}

p_block* Symbols::pull_mtx(int idx)
{
  if(hashmap.find(idx) != hashmap.end())
    return hashmap[idx];
  throw std::invalid_argument("no matrix found to load with index");
}

#ifdef LIB_FTFP
fixed* Symbols::pull_ptr(int mtxidx, int row, int col)
#else
double* Symbols::pull_ptr(int mtxidx, int row, int col)
#endif
{
  if(hashmap.find(mtxidx) != hashmap.end()) {
      p_block* p = pull_mtx(mtxidx);
      int nrows = p->num_rows;
      int ncols = p->num_cols;
      // R indexes by 1, C by 0.
      if(nrows > row-1 && ncols > col-1)
        return p->get(ncols * (row-1) + (col-1));
      throw std::invalid_argument("incorrect row and/or col");
  }
  throw std::invalid_argument("no matrix pointer found to load with index");
}
#ifdef LIB_FTFP
fixed Symbols::pull_register(int idx)
#else
double Symbols::pull_register(int idx)
#endif /* LIB_FTFP */
{
  if(regs.find(idx) != regs.end())
    return regs[idx];
  throw std::invalid_argument("no register found to load with index");
}

int Symbols::pull_index(int idx)
{
    if(indicies.find(idx) != indicies.end())
        return indicies[idx];
    throw std::invalid_argument("no loop index found to load with index");
}

void Symbols::update_index(int idx, int new_val)
{
    indicies[idx] = new_val;
}

void Symbols::pop_dataset(std::string& dsname)
{
  if(nest_level == 0 && cblocks.find(dsname) != cblocks.end()) {
    delete[] cblocks[dsname];
    cblocks.erase(dsname);
  }
  else if (nest_level == 0)
    throw std::invalid_argument("no dataset found to free with name " + dsname);
}

void Symbols::pop_mtx(int idx)
{
  if (nest_level == 0 && hashmap.find(idx) != hashmap.end()) {
    delete hashmap[idx];
    hashmap.erase(idx);
  }
  else if (nest_level == 0)
    throw std::invalid_argument("no matrix found to free with index in global scope");
}

void Symbols::pop_register(int idx)
{
  if(nest_level == 0 && regs.find(idx) != regs.end())
    regs.erase(idx);
  else if (nest_level == 0)
    throw std::invalid_argument("no register found to free with index in global scope");
}


void Symbols::cleanup()
{
    while (nest_level == 0 && !to_delete.empty()) {
        int idx = to_delete.front();
        // Debug
        // ocall_print(std::to_string(idx).c_str());
        pop_mtx(idx);
        to_delete.pop_front();
    }
}

Symbols::~Symbols()
{
    for (auto it = hashmap.cbegin(); it != hashmap.cend(); it++) {
        delete it->second;
    }
}
