#ifndef NOENCLAVE
#include "Enclave_t.h"
#include <sgx_trts.h>
#else
#include <cmath>
#include <iostream>
#include <fstream>
#endif

#include "runtime.hpp"
#include "primitives.hpp"
#include <string>
#include <cstring>

#ifdef LIB_FTFP
fixed* Runtime::alloc_buf(instruction* instr, size_t& nrows, size_t& ncols) {
#else
double* Runtime::alloc_buf(instruction* instr, size_t& nrows, size_t& ncols) {
#endif
    std::vector<sequence*> seqs = instr->get_seqs();
    if(seqs.size() != 2)
        throw std::runtime_error("seq size incorrect at alloc_buf");

    std::vector<int> rrange = seqs[0]->get_seq();
    std::vector<int> crange = seqs[1]->get_seq();
    nrows = rrange[0];
    ncols = crange[0];
    size_t len = nrows * ncols;

#ifdef LIB_FTFP
    fixed* retval = new fixed[len];
#else
    double* retval = new double[len];
#endif
    for(size_t i = 0; i < len; i++)
        retval[i] = Primitives::na_value();

    return retval;
}

p_block* Runtime::deref_mtx(argument* arg) {
    int idx;
    int ref_count = arg->get_matrix(idx);
    p_block* result = table.pull_mtx(idx);
    if (ref_count == 0) {
        int current_ref = ref_count;
        int current_idx = idx;
        while (current_ref == 0) {
            table.set_cleanup(current_idx);
            current_idx = argument::get_parent_of(current_idx);
            if (current_idx == 0) {
                break;
            }
            current_ref = argument::get_matrix_reference(current_idx);
        }
    }
    return result;
}

#ifdef LIB_FTFP
fixed Runtime::deref_scalar(argument* arg) {
    fixed ret;
#else
double Runtime::deref_scalar(argument* arg) {
    double ret;
#endif
    int idx, row, col;
    arg_type atype = arg->get_type();
    if(atype == ptr) {  //ptr
        int ref_count = arg->get_pointer(idx, row, col);
        // handle loop indicies
        if (arg->is_row_index()) {
            row = table.pull_index(row);
        }
        if (arg->is_col_index()) {
            col = table.pull_index(col);
        }
#ifdef LIB_FTFP
        fixed* ptr = table.pull_ptr(idx,row,col);
#else
        double* ptr = table.pull_ptr(idx,row,col);
#endif
        ret = *ptr;
        if (ref_count == 0) {
            int current_ref = ref_count;
            int current_idx = idx;
            while (current_ref == 0) {
                table.set_cleanup(current_idx);
                current_idx = argument::get_parent_of(current_idx);
                if (current_idx == 0) {
                    break;
                }
                current_ref = argument::get_matrix_reference(current_idx);
            }
        }
    }
    else if(atype == reg) { //reg
        int ref_count = arg->get_register(idx);
        ret = table.pull_register(idx);
        if (ref_count == 0) {
            table.pop_register(idx);
        }
    }
    else if(atype == val) {
#ifdef LIB_FTFP
        double dret;
        fixed na_val;
        arg->get_value(dret);
        ret = fix_convert_from_double(dret);
        int is_na = fix_is_nan(ret);
#else
        double na_val;
        arg->get_value(ret);
        int is_na = Primitives::is_na(ret);
#endif
        na_val = Primitives::na_value();
        Primitives::cmov64(is_na, &na_val, &ret);
    }
    else if(atype == arg_type::idx) {
        arg->get_index(idx);
#ifdef LIB_FTFP
        ret = fix_convert_from_int64((int64_t) table.pull_index(idx));
#else
        ret = (double) table.pull_index(idx);
#endif
    }
    else {
        ocall_print(std::to_string(atype).c_str());
        throw std::runtime_error("invalid arg type"); }

    return ret;
}

#ifdef LIB_FTFP
void Runtime::def_dispatch(std::list<instruction*>& instrs, fixed* dbuf, size_t len) {
#else
void Runtime::def_dispatch(std::list<instruction*>& instrs, double* dbuf, size_t len) {
#endif
    instruction* this_inst = instrs.front();
    std::string opname = this_inst->get_name();
    if(opname == "end") { //base case: end of def
        instrs.pop_front();
        return;
    }

    if (opname == "rand") {
        fill_rand(dbuf, len);
    } else if (opname == "row") {
        for (auto arg: this_inst->get_args()) {
            if (arg->get_type() == arg_type::mtx) {
                p_block *src_mtx = deref_mtx(arg);
                size_t mtx_sz = src_mtx->num_rows * src_mtx->num_cols;
                for (size_t i = 0; i < mtx_sz; i++) {
                    *dbuf = *src_mtx->get(i);
                    dbuf++;
                }
            } else {
                *dbuf = deref_scalar(arg);
                dbuf++;
            }
        }
    } else {
        line_dispatch(this_inst, dbuf, len);
    }

    instrs.pop_front();
    def_dispatch(instrs, dbuf, len);
}

#ifdef LIB_FTFP
void Runtime::fill_rand(fixed* dbuf, size_t len) {
    int16_t tseed;
#else
void Runtime::fill_rand(double* dbuf, size_t len) {
    uint16_t xseed[3];
#endif /* LIB_FTFP */

    for (size_t i = 0; i < len; i++) {

#ifdef NOENCLAVE
        std::ifstream urandom("/dev/urandom", std::ios::in | std::ios::binary);

#ifdef LIB_FTFP
        urandom.read(reinterpret_cast<char*>(&tseed), sizeof(int16_t));
#else
        urandom.read(reinterpret_cast<char*>(&xseed), sizeof(uint16_t) * 3);
#endif /* LIB_FTFP */

#else

#ifdef LIB_FTFP
        sgx_read_rand(reinterpret_cast<unsigned char*>(&tseed), sizeof(int16_t));
#else
        sgx_read_rand(reinterpret_cast<unsigned char*>(&xseed), sizeof(uint16_t) * 3);
#endif /* LIB_FTFP */


#endif /* NOENCLAVE */


#ifdef LIB_FTFP
        fixed rand_val = fix_abs(fix_div(fix_convert_from_int64((int64_t)tseed), fix_convert_from_int64((int64_t)(INT16_MAX))));
#else
        // Adapted from the NetBSD drand48() implementation 
        double rand_val = std::ldexp(xseed[0], -48) + std::ldexp(xseed[1], -32) + std::ldexp(xseed[2], -16);
#endif /* LIB_FTFP */

        dbuf[i] = rand_val;
    }
}

#ifdef LIB_FTFP
void Runtime::line_dispatch(instruction* instr, fixed* dbuf, size_t len) {
#else
void Runtime::line_dispatch(instruction* instr, double* dbuf, size_t len) {
#endif
    std::vector<argument*> args = instr->get_args();
    std::vector<sequence*> seqs = instr->get_seqs();
    std::string opname = instr->get_name();
    
    if (opname == "cbind" || opname == "rbind") {
        size_t max_size = 1;
        for (size_t i = 0; i < args.size(); i++) {
            if (args[i]->get_type() != arg_type::mtx) {
#ifdef LIB_FTFP
                fixed to_set = deref_scalar(args[i]);
#else
                double to_set = deref_scalar(args[i]);
#endif
                if (opname == "rbind") {
                    for (size_t j = 0; j < max_size; j++) {
                        dbuf[i * max_size + j] = to_set;
                    }
                } else { // cbind
                    for (size_t j = 0; j < max_size; j++) {
                        dbuf[i + (j * args.size())] = to_set;
                    }
                }
            } else { // matrices
                p_block* to_append = deref_mtx(args[i]);
                if (opname == "rbind") {
                    max_size = to_append->num_cols;
                    size_t app_size = to_append->num_rows * to_append->num_cols;
                    for (size_t j = 0; j < app_size; j++) {
                        dbuf[i * app_size + j] = *to_append->get(j);
                    }
                } else { // cbind
                    max_size = to_append->num_rows;
                    size_t app_size = to_append->num_rows * to_append->num_cols;
                    for (size_t j = 0; j < app_size; j++) {
                        dbuf[i + (j * args.size())] = *to_append->get(j);
                    }
                }
            }
        }
    }
    else if (args.size() == 0) {
#ifdef LIB_FTFP
        fixed* ds_chunk = table.pull_dataset(opname);
        memcpy(dbuf, ds_chunk, len * sizeof(fixed));
#else
        double* ds_chunk = table.pull_dataset(opname);
        memcpy(dbuf, ds_chunk, len * sizeof(double));
#endif
        if (0 == instruction::get_ref_for_dataset(opname)) {
            table.pop_dataset(opname);
        }
    } else if (args.size() == 1) {
        if(opname == "set")
        {
            set(instr);
            return;
        }

        if(opname == "indexvar"){
            indexvar(instr);
            return;
        }

        if(opname == "dim") {
            if(args[0]->get_type() != mtx)
                throw std::runtime_error("dim is called on non-matrix argument");
            p_block* mat = deref_mtx(args[0]);
            std::vector<int> rows = seqs[0]->get_seq();
            std::vector<int> cols = seqs[1]->get_seq();
            size_t rowdim = rows[0];
            size_t coldim = cols[0];
            if(mat->num_rows * mat->num_cols != rowdim * coldim) {
                throw std::runtime_error("dim is called with incorrect dimensions");
            }
            else if(mat->is_const)
                throw std::runtime_error("dim is called on const matrix");
            mat->num_rows = rowdim;
            mat->num_cols = coldim;
            return;
        }

        UnaryOp *u_op = UnaryOpFactory::get_op_for_name(opname.c_str());
        arg_type atype = args[0]->get_type();

        if(atype == mtx) { //mtx
            p_block* pb = deref_mtx(args[0]);
            u_op->call(pb, dbuf);
        }
        else if(atype == ptr || atype == reg || atype == val || atype == arg_type::idx) {
#ifdef LIB_FTFP
            fixed scalar = deref_scalar(args[0]);
#else
            double scalar = deref_scalar(args[0]);
#endif
            u_op->call(scalar, dbuf);
        }
        else
            throw std::runtime_error("invalid argument type");

        delete u_op;
    } else if (args.size() == 2) {
        if(opname == "slice") {
            slice(args, seqs);
            return;
        }
        else if(opname == "update") {
            update(args, seqs);
            return;
        }

        BinaryOp * b_op = BinaryOpFactory::get_op_for_name(opname.c_str());

        bool is_scalar[2];
        for(int i = 0; i < 2; i++)
            is_scalar[i] = (args[i]->get_type() != mtx);

        if(is_scalar[0] && is_scalar[1]) {
#ifdef LIB_FTFP
            fixed scalars[2];
#else
            double scalars[2];
#endif
            for(int i = 0; i < 2; i++)
                scalars[i] = deref_scalar(args[i]);
            b_op->call(scalars[0], scalars[1], dbuf);
        }
        else if(!is_scalar[0] && is_scalar[1]) {
            p_block* p0 = deref_mtx(args[0]);
#ifdef LIB_FTFP
            fixed s1 = deref_scalar(args[1]);
#else
            double s1 = deref_scalar(args[1]);
#endif
            b_op->call(p0, s1, dbuf);
        }
        else if(is_scalar[0] && !is_scalar[1]) {
#ifdef LIB_FTFP
            fixed s0 = deref_scalar(args[0]);
#else
            double s0 = deref_scalar(args[0]);
#endif
            p_block* p1 = deref_mtx(args[1]);
            b_op->call(s0, p1, dbuf);
        }
        else {
            p_block* pbs[2];
            for(int i = 0; i < 2; i++)
               pbs[i] = deref_mtx(args[i]);
            size_t s0 = pbs[0]->num_rows * pbs[0]->num_cols;
            size_t s1 = pbs[1]->num_rows * pbs[1]->num_cols;
            if(s0 != s1 && opname != "%*%") //do not coerce when it is matrix multiply
                coerce_dim(pbs[0], pbs[1], (s0 > s1));

            b_op->call(pbs[0], pbs[1], dbuf);

            if(s0 > s1 && opname != "%*%")
                delete pbs[1];
            else if(s1 > s0 && opname != "%*%")
                delete pbs[0];
        }

        delete b_op;
        return;
    } else if (opname == "update" && args.size() == 3) {
        update(args, seqs);
        return;
    } else if (opname == "ifelse" && args.size() == 3) {
        if (args[0]->get_type() != mtx) {
#ifdef LIB_FTFP
            int flag = Primitives::fixed_to_int(deref_scalar(args[0]));
#else
            int flag = (int) (deref_scalar(args[0]));
#endif /* LIB_FTFP */

            if (args[2]->get_type() != mtx) {
#ifdef LIB_FTFP
                fixed if_true = deref_scalar(args[1]);
#else
                double if_true = deref_scalar(args[1]);
#endif
                *dbuf = deref_scalar(args[2]);
                Primitives::cmov64(flag, &if_true, dbuf);
            } else {
                p_block* if_true_mtx = deref_mtx(args[1]);
                p_block* result_mtx = deref_mtx(args[2]);
                
                size_t mtx_sz = result_mtx->num_rows * result_mtx->num_cols;
                for (size_t i = 0; i < mtx_sz; i++) {
                    Primitives::cmov64(flag, if_true_mtx->get(i), result_mtx->get(i));
                }
            }
        } else {
            p_block* cond_mtx = deref_mtx(args[0]);
            p_block* if_true_mtx = deref_mtx(args[1]);
            p_block* result_mtx = deref_mtx(args[2]);

            size_t cond_sz = cond_mtx->num_rows * cond_mtx->num_cols;
            for (size_t i = 0; i < cond_sz; i++) {
#ifdef LIB_FTFP
                Primitives::cmov64(Primitives::fixed_to_int(*cond_mtx->get(i)), 
                        if_true_mtx->get(i), result_mtx->get(i));
#else
                Primitives::cmov64((int) *cond_mtx->get(i), if_true_mtx->get(i), result_mtx->get(i));
#endif /* LIB_FTFP */
            }
        }
    } else
        throw std::runtime_error("too many arguments");
}

void Runtime::coerce_dim(p_block* & left_p, p_block* & right_p, bool change_right) {
    int new_rows, new_cols;
    new_rows = (change_right) ? left_p->num_rows : right_p->num_rows;
    new_cols = (change_right) ? left_p->num_cols : right_p->num_cols;

    p_block* orig_pb = (!change_right) ? left_p : right_p;
    p_block* ret = new p_block(new_rows, new_cols, 0, orig_pb);

    if(orig_pb->num_rows != new_rows && orig_pb->num_cols != new_cols)
        throw std::runtime_error("both dimensions do not match for coercing mtxs");

    if(orig_pb->num_rows == new_rows) {
        int orig_cols = orig_pb->num_cols;
        if(new_cols % orig_cols != 0)
            throw std::runtime_error("coercing cannot happen due to non-integer ratio");

        for(int i = 0; i < new_rows; i++)
            for(int j = 0; j < new_cols; j++)
                for(int k = 0; k < orig_cols; k++) {
                    size_t idx = i * orig_cols + k;
                    ret->add(orig_pb->get(idx));
                }
    }
    else {
        if(new_rows % orig_pb->num_rows != 0)
            throw std::runtime_error("coercing cannot happen due to non-integer ratio");
        size_t iters = new_rows / orig_pb->num_rows;
        for(size_t i = 0; i < iters; i++) {
            size_t orig_sz = orig_pb->num_rows * orig_pb->num_cols;
            for(size_t i = 0; i < orig_sz; i++)
                ret->add(orig_pb->get(i));
        }
    }

    //this is fine since p_block* is passed by reference
    if(change_right)
        right_p = ret;
    else
        left_p = ret;
}

void Runtime::dispatch(std::list<instruction*>& instrs) {
    while(instrs.size() != 0)
    {
        instruction* this_inst = instrs.front();
        std::string opname = this_inst->get_name();

        // Print statements take a lot of time; we comment them out
        // ocall_print(opname.c_str()); //print dispatch opcode


        if(opname == "endloop") { //base case: end of def
            instrs.pop_front();
        } else if (opname == "forloop") {
            std::vector<argument*> args = this_inst->get_args();
            std::vector<sequence*> seqs = this_inst->get_seqs();
            std::list<instruction*> loop_instrs = this_inst->get_loop_instrs();
            int idx_no;
            args[0]->get_index(idx_no);
            std::vector<int> loop_seq = check_ordered(seqs[0]);
            // Turn off the symbol table clean up for the loop
            table.inc_nest_level();
            for(int i = 0; i < loop_seq.size(); i++) {
                int loop_index = loop_seq[i];
                std::list<instruction*> this_iter_instrs(loop_instrs);
                table.update_index(idx_no, loop_index);
                dispatch(this_iter_instrs);
            }
            table.dec_nest_level();
            instrs.pop_front();
        } else if (opname == "def") {
            int idx;
            size_t nrows, ncols, len;
#ifdef LIB_FTFP
            fixed *dbuf;
#else
            double *dbuf;
#endif /* LIB_FTFP */
            p_block* p;

            std::vector<argument*> args = this_inst->get_args();
            bool is_const = args[0]->is_const();
            args[0]->get_matrix(idx); //decrement ref count

            if (table.is_mtx(idx)) {
                p = table.pull_mtx(idx);
                dbuf = p->get(0);
                nrows = p->num_rows;
                ncols = p->num_cols;
            } else {
                dbuf = alloc_buf(this_inst, nrows, ncols);
            }

            len = nrows * ncols;

            instrs.pop_front();
            def_dispatch(instrs, dbuf, len);

            if (!table.is_mtx(idx)) {
                // We didn't have this matrix already
                p = new p_block(nrows, ncols, is_const, dbuf);
                table.push_mtx(idx, p);
            }
        } else {
            line_dispatch(this_inst, &tempreg, 1);
            instrs.pop_front();
        }

        table.cleanup();
    }
}

void Runtime::load_data(double* secrets, const char* dataset_name,
        size_t num_rows, size_t num_cols) {
   table.push_dataset(secrets, dataset_name, num_rows, num_cols);
}

int Runtime::idx_convert(int row, int col, int ncols) {
    int crow = row - 1;
    int ccol = col - 1;
    return ncols * crow + ccol;
}

std::vector<int> Runtime::check_ordered(sequence* seq) {
    std::vector<int> input = seq->get_seq();
    std::vector<int> retval;
    std::vector<bool> is_index = seq->get_seq_is_index();
    if(seq->is_ordered())
    {
        int start = input[0];
        if (is_index[0]) {
            start = table.pull_index(input[0]);
        }
        int end = input[1];
        if (is_index[1]) {
            end = table.pull_index(input[1]);
        }
        int step = input[2];
        if (is_index[2]) {
            step = table.pull_index(input[2]);
        }
        if (step > 0) {
            for(int i = start; i <= end; i += step) {
                retval.push_back(i);
            }
        } else if (step < 0) {
            for(int i = start; i >= end; i += step) {
                retval.push_back(i);
            }
        } else {
            throw std::invalid_argument("sequence with step 0");
        }
    } else {
        for (int i = 0; i < input.size(); i++) {
            if (is_index[i]) {
                retval.push_back(table.pull_index(input[i]));
            } else {
                retval.push_back(input[i]);
            }
        }
    }
    return retval;
}

void Runtime::slice(std::vector<argument*>& args, std::vector<sequence*>& seqs) {
    int dst_num;
    args[1]->get_matrix(dst_num);
    bool isConst = args[1]->is_const();
    p_block* src_blk = deref_mtx(args[0]);

    std::vector<int> rows = check_ordered(seqs[0]);
    std::vector<int> cols = check_ordered(seqs[1]);

    p_block* dst_blk;
    bool realloc = table.is_mtx(dst_num);
    if (!realloc) {
        dst_blk = new p_block(rows.size(), cols.size(), isConst, src_blk);
    } else {
        dst_blk = table.pull_mtx(dst_num);
        if (rows.size() != dst_blk->num_rows) {
            throw std::runtime_error("mismatched rows for realloc slice");
        }
        if (cols.size() != dst_blk->num_cols) {
            throw std::runtime_error("mismatched cols for realloc slice");
        }
    }

    int dst_position = 0;
    for(int i : rows) {
        for(int j : cols) {
            int idx = idx_convert(i, j, src_blk->num_cols);
            if (!realloc) {
                dst_blk->add(src_blk->get(idx));
            } else {
                dst_blk->set(dst_position,src_blk->get(idx));
            }
            dst_position++;
        }
    }

    // sanity check
    if (dst_blk->size() != rows.size() * cols.size()) {
        throw std::runtime_error("dimension mismatch after slicing");
    }

    if (!realloc) {
        table.push_mtx(dst_num, dst_blk);
    }
}

void Runtime::update(std::vector<argument*>& args, std::vector<sequence*>& seqs) {
    p_block* dst_blk = deref_mtx(args[0]);
    if(dst_blk->is_const)
        throw std::runtime_error("trying to update a const mtx");

    if (args.size() == 3) {
        p_block* logical_blk = deref_mtx(args[1]);
        int ctr = 0;
        size_t lblk_size = logical_blk->num_rows * logical_blk->num_cols;

        if(args[2]->get_type() == arg_type::mtx) {       
            p_block* src_blk = deref_mtx(args[2]);
            for(size_t i = 0; i < lblk_size; i++) {
#ifdef LIB_FTFP
                int flag = Primitives::fixed_to_int(*logical_blk->get(i));
                fixed* src_ptr = src_blk->get(ctr);
                fixed* dst_ptr = dst_blk->get(ctr);
#else
                int flag = (int) *logical_blk->get(i);
                double* src_ptr = src_blk->get(ctr);
                double* dst_ptr = dst_blk->get(ctr);
#endif /* LIB_FTFP */
                Primitives::cmov64(flag, src_ptr, dst_ptr);
                ctr++;
            }
        } else {
#ifdef LIB_FTFP
            fixed src_val = deref_scalar(args[2]);
#else
            double src_val = deref_scalar(args[2]);
#endif /* LIB_FTFP */
            for(size_t i = 0; i < lblk_size; i++) {
#ifdef LIB_FTFP
                int flag = Primitives::fixed_to_int(*logical_blk->get(i));
                fixed* dst_ptr = dst_blk->get(ctr);
#else
                int flag = (int) *logical_blk->get(i);
                double* dst_ptr = dst_blk->get(ctr);
#endif /* LIB_FTFP */
                Primitives::cmov64(flag, &src_val, dst_ptr);
                ctr++;
            }
        }
    } else {
        std::vector<int> rows = check_ordered(seqs[0]);
        std::vector<int> cols = check_ordered(seqs[1]);
        if (args[1]->get_type() == arg_type::mtx) {
            p_block* src_blk = deref_mtx(args[1]);
            int ctr = 0;
            for(int i : rows) {
                for(int j : cols) {
                    int dst_idx = idx_convert(i, j, dst_blk->num_cols);
#ifdef LIB_FTFP
                    fixed src_val = *(src_blk->get(ctr));
                    fixed* dst_ptr = dst_blk->get(dst_idx);
#else
                    double src_val = *(src_blk->get(ctr));
                    double* dst_ptr = dst_blk->get(dst_idx);
#endif
                    *dst_ptr = src_val;
                    ctr++;
                }
            }
        } else {
#ifdef LIB_FTFP
            fixed value = deref_scalar(args[1]);
#else
            double value = deref_scalar(args[1]);
#endif
            int ctr = 0;
            for(int i : rows) {
                for(int j : cols) {
                    int dst_idx = idx_convert(i, j, dst_blk->num_cols);
#ifdef LIB_FTFP
                    fixed* dst_ptr = dst_blk->get(dst_idx);
#else
                    double* dst_ptr = dst_blk->get(dst_idx);
#endif
                        *dst_ptr = value;
                        ctr++;
                }
            }
        }
    }
}

void Runtime::set(instruction* instr) {
    std::vector<argument*> args = instr->get_args();
    if(args.size() != 1)
        throw std::runtime_error("too many args for set");
    if(args[0]->get_type() != reg)
        throw std::runtime_error("incorrect arg type for set");

    int idx;
    args[0]->get_register(idx);
    table.push_register(idx, tempreg);
}

void Runtime::indexvar(instruction* instr) {
    std::vector<argument*> args = instr->get_args();
    if(args.size() != 1)
        throw std::runtime_error("too many args for indexvar");
    if(args[0]->get_type() != idx)
        throw std::runtime_error("incorrect arg type for indexvar");

    int idx;
    args[0]->get_index(idx);

#ifdef LIB_FTFP
    table.update_index(idx, fix_convert_to_int64(tempreg));
#else
    table.update_index(idx, (int64_t)tempreg);
#endif
}
