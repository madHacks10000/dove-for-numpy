#ifndef PARSER_HPP
#define PARSER_HPP

#include <string>
#include <vector>
#include <list>

#include "objects.hpp"

class parser {
    public:
        parser(std::string in): input_asm(in), last(), current(), pos_index(), instr_list() {}
        ~parser() {
            for (instruction* instr: instr_list) {
                delete instr;
            }
        }

        void parse();
        size_t get_pos() { return pos_index; };

        const std::list<instruction*>& get_instrs() { return instr_list; };

        static const std::vector<std::string> view_ops;
        static const std::vector<std::string> arith_ops;
        static const std::vector<std::string> compare_ops;
        static const std::vector<std::string> logic_ops;
        static const std::vector<std::string> math_general_ops;
        static const std::vector<std::string> math_trig_ops;
        static const std::vector<std::string> math_gamma_ops;
        static const std::vector<std::string> math_cuml_ops;
        static const std::vector<std::string> summary_ops;
        static const std::vector<std::string> stats_ops;
        static const std::vector<std::string> flow_ops;
        static const std::vector<std::string> bind_ops;
        static const std::vector<std::string> other_ops;
    private:
        void next();
        void match(std::string kind);
        int match_any(std::vector<std::string> kinds, std::string kind_name);
        void match_num(int *result);

        std::list<instruction*> def_matrix();
        std::vector<argument*> rows();
        std::string dataset();

        //std::list<instruction*> loop();
        instruction* loop();
        argument* loop_index();

        instruction* func_instr();
        argument* arg();

        instruction* dim_instr();
        instruction* view_instr();
        sequence* length();
        sequence* select_sequence();


        std::string input_asm;

        // std::istringstream instream;
        char* token;
        std::string last;
        std::string current;
        size_t pos_index;

        std::list<instruction*> instr_list;

        static const std::vector<std::string> na_ops;
        static const std::vector<std::string> all_func_ops;
};
#endif //PARSER_HPP
