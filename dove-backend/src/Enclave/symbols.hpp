#ifndef _SYMBOLS_HPP
#define _SYMBOLS_HPP

#include <map>
#include <list>
#include <string>

#include "p_block.hpp"

#ifdef LIB_FTFP
extern "C" {
#include "ftfp.h"
}
#endif

class Symbols {
  public:
    Symbols(): hashmap(), to_delete(), regs(), cblocks(), indicies(), nest_level(0) {}
    ~Symbols();
    void push_dataset(double* secrets, const char* dataset_name, int num_rows, int num_cols);
#ifdef LIB_FTFP
    int is_r_na(double x);
    void push_register(int idx, fixed value);
    fixed* pull_dataset(std::string& dsname);
    fixed* pull_ptr(int mtxidx, int row, int col);
    fixed pull_register(int idx);
#else
    void push_register(int idx, double value);
    double* pull_dataset(std::string& dsname);
    double* pull_ptr(int mtxidx, int row, int col);
    double pull_register(int idx);
#endif
    void push_mtx(int idx, p_block* new_block);
    p_block* pull_mtx(int idx);
    void push_index(int idx, int init_val);
    int pull_index(int idx);
    void update_index(int idx, int new_val);
    void pop_dataset(std::string& dsname);
    void pop_mtx(int idx);
    void pop_register(int idx);

    bool is_mtx(int idx) { return (hashmap.find(idx) != hashmap.end()); };
    void set_cleanup(int idx) { if (nest_level == 0) {to_delete.push_back(idx);} ; } ;
    void cleanup();

    void inc_nest_level() { nest_level++; } ;
    void dec_nest_level() { nest_level--; } ;
  private:
    std::map<int, p_block*> hashmap;
    std::list<int> to_delete;

#ifdef LIB_FTFP
    std::map<int, fixed> regs;
    std::map<std::string, fixed*> cblocks;
#else
    std::map<int, double> regs;
    std::map<std::string, double*> cblocks;
#endif
    std::map<int, int> indicies;
    size_t nest_level;
};


#endif
