#ifdef PARSER_DEBUG
#include <iostream>
#endif

#include <vector>
#include <string>
#include <map>
#include <list>

enum arg_type {mtx, ptr, val, reg, idx};

class argument {
    public:
        argument(bool is_const, bool is_end, int id): type(arg_type::mtx), data({id}),
            is_c(is_const) { add_matrix_reference(id, is_end); }
        argument(int id, int m, int n): type(arg_type::ptr), data({id, m, n}),
            is_index({false, false, false}), is_c(false) { add_matrix_reference(id, false); }
        argument(int id, int m, bool is_index_m, int n, bool is_index_n): type(arg_type::ptr), data({id, m, n}),
            is_index({false, is_index_m, is_index_n}), is_c(false) { add_matrix_reference(id, false); }
        argument(double val): type(arg_type::val), value(val), is_c(false) { }
        argument(int reg_no): type(arg_type::reg), data({reg_no}),
            is_c(false) { add_register_reference(reg_no); }
        argument(int idx_no, arg_type idx_type): type(idx_type), data({idx_no}),
            is_c(false) { add_index_reference(idx_no); }

        arg_type get_type() { return type; };
        bool is_const() const { return is_c; };

        int get_matrix(int& matrix_id);
        int get_pointer(int& matrix_id, int& pos_m, int& pos_n);
        int get_value(double& val);
        int get_register(int& reg_no);
        int get_index(int& idx_no);

        static const std::vector<int>& get_matrix_references() { return matrix_references; };
        static const std::vector<int>& get_register_references() { return register_references; };

        /* static void inc_multiplier(int to_mult) { reference_multiplier *= to_mult; };
        static void dec_multiplier(int to_idiv) { reference_multiplier /= to_idiv; };
        static int get_multiplier() { return reference_multiplier; };

        static void set_index_start(int idx, int start) { index_starts[idx] = start; };
        static int get_index_start(int idx) { return index_starts[idx]; }; */

        bool is_row_index() { return type == arg_type::ptr && is_index[1]; };
        bool is_col_index() { return type == arg_type::ptr && is_index[2]; };

        static void add_matrix_reference(int id, bool is_end);
        static void add_register_reference(int reg_no);
        static void add_index_reference(int idx_no);
        static void set_slice_of(argument *child, argument *parent);
        static int get_matrix_reference(int matrix_id) { return matrix_references[matrix_id - 1];};
        static int get_parent_of(int matrix_id) { return slice_relations[matrix_id - 1]+1; };

    private:
#ifdef PARSER_DEBUG
        friend std::ostream& operator<<(std::ostream &os, const argument &a);
#endif
        static std::vector<int> matrix_references;
        static std::vector<int> register_references;
        static std::vector<int> index_references;
        static std::vector<int> slice_relations;
        /* static std::map<int, int> index_starts; */
        static int reference_multiplier;

        arg_type type;
        std::vector<int> data;
        std::vector<bool> is_index;
        double value;
        bool is_c;
};

class sequence {
    public:
        sequence(): seq(), is_index(), ordered(false) { }
        sequence(bool is_ordered): seq(), is_index(), ordered(is_ordered) { }
        sequence(int start, int stop, int step): seq({start, stop, step}), is_index({false, false, false}), ordered(true) { }
        sequence(int pos): seq({pos}), is_index({false}), ordered(false) { }

        const std::vector<int>& get_seq() { return seq; };
        const std::vector<bool>& get_seq_is_index() { return is_index; };
        bool is_ordered() const { return ordered; };
        void add(int i) { seq.push_back(i); is_index.push_back(false); };
        void add(int i, bool is_idx) { seq.push_back(i); is_index.push_back(is_idx); };

    private:
#ifdef PARSER_DEBUG
        friend std::ostream& operator<<(std::ostream &os, const sequence &s);
#endif
        std::vector<int> seq;
        std::vector<bool> is_index;
        bool ordered;
};

class instruction {
    public:
        instruction(std::string n): name(n), args(), seqs(), loop_instrs() { }
        ~instruction() {
            for (argument* arg: args) {
                delete arg;
            }
            for (sequence* seq: seqs) {
                delete seq;
            }
            for (instruction* loop_instr: loop_instrs) {
                delete loop_instr;
            }
        }
        const std::string& get_name() { return name; };
        const std::vector<argument*>& get_args() { return args; };
        const std::vector<sequence*>& get_seqs() { return seqs; };
        const std::list<instruction*>& get_loop_instrs() { return loop_instrs; };
        void add_arg(argument *a) { args.push_back(a); };
        void add_seq(sequence *s) { seqs.push_back(s); };
        void add_loop_instr(std::list<instruction*> instrs) { loop_instrs = instrs; };

        static int add_ref_for_dataset(std::string dset);
        static int get_ref_for_dataset(std::string dset) { return --dataset_refs[dset]; };
    
    private:
#ifdef PARSER_DEBUG
        friend std::ostream& operator<<(std::ostream &os, const instruction &instr);
#endif
        std::string name;
        std::vector<argument*> args;
        std::vector<sequence*> seqs;
        std::list<instruction*> loop_instrs;
        static std::map<std::string, int> dataset_refs;
};
