#ifndef _RUNTIME_HPP
#define _RUNTIME_HPP

#include "p_block.hpp"
#include "symbols.hpp"
#include "parser/parser.hpp"
#include "factory.hpp"

#include <list>
#include <vector>

#ifdef LIB_FTFP
extern "C" {
#include "ftfp.h"
}

class Runtime {
    public:
        void load_data(double* secrets, const char* dataset_name, 
                size_t num_rows, size_t num_cols);
        void dispatch(std::list<instruction*>& instrs);
    private:
        fixed* alloc_buf(instruction* instr, size_t& nrow, size_t& ncol);
        p_block* deref_mtx(argument* arg);
        fixed deref_scalar(argument* arg);
        void def_dispatch(std::list<instruction*>& instrs, fixed* dbuf, size_t len);
        void fill_rand(fixed* dbuf, size_t len);
        void line_dispatch(instruction* instr, fixed* dbuf, size_t len);
        int idx_convert(int row, int col, int ncols);
        std::vector<int> check_ordered(sequence* seq);
        void coerce_dim(p_block* & left_p, p_block* & right_p, bool change_right);
        
        //internal ops
        void slice(std::vector<argument*>& args, std::vector<sequence*>& seqs);
        void update(std::vector<argument*>& args, std::vector<sequence*>& seqs);
        void set(instruction* instr);
        void indexvar(instruction* instr);
        
        //variables
        Symbols table;
        fixed tempreg;
};

#else

class Runtime {
    public:
        void load_data(double* secrets, const char* dataset_name, 
                size_t num_rows, size_t num_cols);
        void dispatch(std::list<instruction*>& instrs);
    private:
        double* alloc_buf(instruction* instr, size_t& nrow, size_t& ncol);
        p_block* deref_mtx(argument* arg);
        double deref_scalar(argument* arg);
        void def_dispatch(std::list<instruction*>& instrs, double* dbuf, size_t len);
        void fill_rand(double* dbuf, size_t len);
        void line_dispatch(instruction* instr, double* dbuf, size_t len);
        int idx_convert(int row, int col, int ncols);
        std::vector<int> check_ordered(sequence* seq);
        void coerce_dim(p_block* & left_p, p_block* & right_p, bool change_right);
        
        //internal ops
        void slice(std::vector<argument*>& args, std::vector<sequence*>& seqs);
        void update(std::vector<argument*>& args, std::vector<sequence*>& seqs);
        void set(instruction* instr);
        void indexvar(instruction* instr);
        
        //variables
        Symbols table;
        double tempreg;
};
#endif /* LIB_FTFP */

#endif
