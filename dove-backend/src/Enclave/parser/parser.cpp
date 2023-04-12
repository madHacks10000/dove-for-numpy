#include <vector>
#include <string>
#include <stdexcept>
#include <algorithm>
#include <cstring>

#ifdef PARSER_DEBUG
#include <iostream>
#include <fstream>
#endif

#include "parser.hpp"
#include "bscanf.h"

const std::vector<std::string> parser::view_ops = {"update", "slice"};

const std::vector<std::string> parser::arith_ops {"+", "-", "*", "/", "^", "%%", "%/%", "%*%"};
const std::vector<std::string> parser::compare_ops {"==", ">=", "<=", "<", ">", "!="};
const std::vector<std::string> parser::logic_ops {"&", "&&", "|", "||", "!"};
const std::vector<std::string> parser::math_general_ops = {"abs", "sign",
    "sqrt", "floor", "ceiling", "trunc", "round", "signif"};
const std::vector<std::string> parser::math_trig_ops = {"exp", "log",
    "expm1", "log1p", "cos", "sin", "tan", "cospi", "sinpi", "tanpi", "acos",
    "asin", "atan", "cosh", "sinh", "tanh", "acosh", "asinh", "atanh"};
const std::vector<std::string> parser::math_gamma_ops = {"lgamma",
    "gamma", "digamma", "trigamma"};
const std::vector<std::string> parser::math_cuml_ops = {"cumsum",
    "cumprod", "cummax", "cummin"};
const std::vector<std::string> parser::summary_ops = {"any", "all", "sum",
    "rowSums", "colSums", "prod", "min", "max", "range", "mean", "rowMeans",
    "colMeans", "pmin", "pmax"};
const std::vector<std::string> parser::stats_ops = {"pchisq", "fisher_test"};
const std::vector<std::string> parser::flow_ops = {"ifelse", "rapply", "capply", "mapply"};
const std::vector<std::string> parser::bind_ops = {"cbind", "rbind"};
    const std::vector<std::string> parser::other_ops = {"set", "dataset", "empty", "print", "NA?", "NAN?", "INF?", "indexvar", "rand"};

const std::vector<std::string> parser::na_ops = {"any|NA", "all|NA", "sum|NA",
    "rowSums|NA", "colSums|NA", "prod|NA", "min|NA", "max|NA", "range|NA", "mean|NA", "rowMeans|NA",
    "colMeans|NA", "pmin|NA", "pmax|NA"};

const std::vector<std::string> parser::all_func_ops = {"+", "-", "*", "/", "^", "%%", "%/%", "%*%",
    "==", ">=", "<=", "<", ">", "!=", "%*%", "&", "|", "!", "abs", "sign", "sqrt", "floor",
    "ceiling", "trunc", "round", "signif", "exp", "log", "expm1", "log1p", "cos",
    "sin", "tan", "cospi", "sinpi", "tanpi", "acos", "asin", "atan", "cosh",
    "sinh", "tanh", "acosh", "asinh", "atanh", "lgamma", "gamma", "digamma",
    "trigamma", "cumsum", "cumprod", "cummax", "cummin", "set", "any", "all",
    "sum", "rowSums", "colSums", "prod", "min", "max", "range", "mean", "rowMeans",
    "colMeans", "ifelse", "fisher_test", "pchisq", "print", "cbind", "rbind", "pmin", "pmax", "NA?", "NAN?", "INF?", "indexvar"};


void parser::parse()
{
    // next();
    char* string_buffer = new char[input_asm.size() + 1];
    std::copy(input_asm.begin(), input_asm.end(), string_buffer);
    string_buffer[input_asm.size()] = '\0';
    token = std::strtok(string_buffer, " \t\n");
    current = token;

    while (token != NULL) {
        if (current == "def") {
            instr_list.splice(instr_list.end(), def_matrix());
        } else if (current == "forloop") {
            // instr_list.splice(instr_list.end(), loop());
            instr_list.push_back(loop());
        } else if (current == "update" || current == "slice") {
            instr_list.push_back(view_instr());
        } else if (current == "dim") {
            instr_list.push_back(dim_instr());
        } else {
            instr_list.push_back(func_instr());
        }
    }
    delete[] string_buffer;
}

void parser::next()
{
    if (token == NULL) {
        throw std::runtime_error("could not read next token");
    }

    last = current;
    token = std::strtok(NULL, " \t\n");
    if (token != NULL) {
        current = token;
    } else {
        current = "";
    }
    pos_index += last.size();
}

void parser::match(std::string kind)
{
    if (kind == current) {
        next();
        return;
    }

    throw std::invalid_argument(kind + " expected, not " + current);
}

int parser::match_any(std::vector<std::string> kinds, std::string kind_name)
{
    for (auto it = kinds.cbegin(); it != kinds.cend(); it++) {
        if (*it == current) {
            next();
            return it - kinds.cbegin();
        }
    }

    throw std::invalid_argument(kind_name + " expected, not " + current);
}

void parser::match_num(int *result)
{
    if (bscanf(current.data(), "%d", result) < 1) {
        throw std::invalid_argument("row number expected, not " + current);
    }

    next();
}

std::list<instruction*> parser::def_matrix()
{
    char dataset_name[9];
    match("def");

    if (current == "const") {
        next();
    }

    std::list<instruction*> matrix_instrs;
    instruction* top_level = new instruction("def");
    top_level->add_arg(arg());
    top_level->add_seq(length());
    top_level->add_seq(length());
    matrix_instrs.push_back(top_level);

    if (current == "row") {
        while (current == "row") {
            int row_num;
            instruction* row_instr = new instruction("row");
            match("row");
            match_num(&row_num);
            while (current[0] == '$' || current[0] == '%' || current[0] == '#') {
                row_instr->add_arg(arg());
            }
            matrix_instrs.push_back(row_instr);
        }
    } else if (current == "dataset") {
        next();
        if (bscanf(current.data(), "%8s", dataset_name) < 1) {
            throw std::invalid_argument("dataset name expected, not " + current);
        }
        matrix_instrs.push_back(new instruction(dataset_name));
        std::string map_key = dataset_name;
        instruction::add_ref_for_dataset(map_key);
        next();
    } else if (current == "empty") {
        next();
    } else if (current == "rand") {
        matrix_instrs.push_back(new instruction("rand"));
        next();
    } else {
        matrix_instrs.push_back(func_instr());
    }

    match("end");
    instruction* end_matrix = new instruction("end");
    end_matrix->add_arg(arg());
    matrix_instrs.push_back(end_matrix);

    return matrix_instrs;

}

// std::list<instruction*> parser::loop()
instruction* parser::loop()
{
  match("forloop");
  std::list<instruction*> loop_instrs;
  instruction* top_level = new instruction("forloop");
  sequence* seq = select_sequence();
  top_level->add_seq(seq);
  argument* loop_idx = loop_index();
  top_level->add_arg(loop_idx);

  int index_no = 0;
  loop_idx->get_index(index_no);
  // Old reference count mechanism
  /* argument::set_index_start(index_no, seq->get_start());
     argument::inc_multiplier(seq->size()); */
  // loop_instrs.push_back(top_level);
  next();

  while (current != "endloop") {
      if (current == "def") {
          loop_instrs.splice(loop_instrs.end(), def_matrix());
      } else if (current == "forloop") {
          //loop_instrs.splice(loop_instrs.end(), loop());
          loop_instrs.push_back(loop());
      } else if (current == "update" || current == "slice") {
          loop_instrs.push_back(view_instr());
      } else if (current == "dim") {
            instr_list.push_back(dim_instr());
      } else {
          loop_instrs.push_back(func_instr());
      }
  }
  match("endloop");

  instruction* end_loop = new instruction("endloop");
  end_loop->add_arg(loop_index());
  loop_instrs.push_back(end_loop);
  // Old reference count mechanism
  /* argument::dec_multiplier(seq->size()); */
  next();
  top_level->add_loop_instr(loop_instrs);
  return top_level;
}

sequence* parser::length()
{
    int len;
    if (bscanf(current.data(), "[1:%d]", &len) < 1) {
        throw std::invalid_argument("length expected, not " + current);
    }
    next();
    return new sequence(len);
}

sequence* parser::select_sequence()
{
    sequence *sq;
    int start = 0, stop = 0, step = 0;
    if (bscanf(current.data(), "[%d:%d:%d]", &start, &stop, &step) == 3) {
        sq = new sequence(start, stop, step);
    } else {
        if (current.find(',') == std::string::npos) {
            if (current.find(':') == std::string::npos && bscanf(current.data(), "[\\%d]", &start) == 1) {
                // or else it will work with [%d:%d:%d] sequences
                sq = new sequence();
                sq->add(start, true);
            } else if (bscanf(current.data(), "[%d]", &start) == 1) {
                sq = new sequence(start);
            } else {
                if (current.find(':') != std::string::npos) {
                    char* idx_seq = new char[current.size()-1];
                    std::copy(current.begin()+1, current.end()-1, idx_seq);
                    idx_seq[current.size()-2] = '\0';
                    int j = 0;
                    sq = new sequence(true);
                    while (idx_seq[j] != '\0') {
                        bool is_index = false;
                        if (idx_seq[j] == '\\') {
                            is_index = true;
                            j++;
                        }
                        int numeric = 0;
                        if (bscanf(&idx_seq[j], "%d", &numeric) < 1) {
                            throw std::invalid_argument("numeric/index sequence expected, not " + current);
                        }
                        sq->add(numeric, is_index);

                        while (idx_seq[j] != ':' && idx_seq[j] != '\0') {
                            j++;
                        }
                        if (idx_seq[j] != '\0') {
                            j++;
                        }
                    }
                    delete[] idx_seq;
                } else {
                    throw std::invalid_argument("sequence expected, not " + current);
                }
            }
        } else {
            // now try unordered sequence
            sq = new sequence();
            int next_num;
            char* unordered_seq = new char[current.size()-1];
            std::copy(current.begin()+1, current.end()-1, unordered_seq);
            unordered_seq[current.size()-2] = '\0';

            int idx = 0;
            while (unordered_seq[idx] != '\0') {
                bool is_index = false;
                if (unordered_seq[idx] == '\\') {
                    is_index = true;
                    idx++;
                }
                if (bscanf(&unordered_seq[idx], "%d", &next_num) < 1) {
                    throw std::invalid_argument("numeric sequence expected, not " + current);
                }
                sq->add(next_num, is_index);
                while (unordered_seq[idx] != ',' && unordered_seq[idx] != '\0') {
                    idx++;
                }
                if (unordered_seq[idx] != '\0') {
                    idx++;
                }
            }

            delete[] unordered_seq;
        }
    }
    next();
    return sq;

}

instruction* parser::view_instr()
{
    std::string name = view_ops[match_any(view_ops, "slice/update")];
    instruction *instr = new instruction(name);
    if (current == "const") {
        next();
    }
    argument* parent = arg();
    instr->add_arg(parent);

    if (current[0] == '[') {
        // Sequence-based
        instr->add_seq(select_sequence());
        instr->add_seq(select_sequence());
    } else {
        // Logical matrix-based
        instr->add_arg(arg());
    }

    argument* child = arg();
    instr->add_arg(child);

    if (name == "slice") {
        argument::set_slice_of(child, parent);
    }

    return instr;
}

instruction* parser::dim_instr()
{
    instruction *instr = new instruction("dim");
    next();
    if (current == "const") {
        next();
    }
    argument* parent = arg();
    instr->add_arg(parent);

    if (current[0] == '[') {
        // Sequence-based
        instr->add_seq(length());
        instr->add_seq(length());
    } else {
        // Logical matrix-based
        instr->add_arg(arg());
    }

    return instr;
}

instruction* parser::func_instr()
{
    std::string name;
    if (current == "t") {
        next();
        if (current == "const") {
            next();
        }
        name = "t";
    } else if (std::string::npos != current.find("|NA")) {
            name = na_ops[match_any(na_ops, "summary")];
        } else {
            name = all_func_ops[match_any(all_func_ops, "operation")];
    }

    instruction *instr = new instruction(name);
    while (current[0] == '$' || current[0] == '%' || current[0] == '#' || current[0] == '\\') {
        instr->add_arg(arg());
    }

    return instr;
}

argument* parser::loop_index()
{
    int idx_no;

    if (current[0] == '\\') {
        int r = bscanf(current.substr(1, current.size()).data(), "%d", &idx_no);
        if (r == 1) {
            return new argument(idx_no, arg_type::idx);
        }
    }

    throw std::invalid_argument("index argument expected, not " + current);
}

argument* parser::arg() {
    int r, id, pos_m, pos_n;
    double value;
    argument *ret_val;

    if (current[0] == '$') {
        auto loc = current.find(',');
        if (loc == std::string::npos) {
            r = bscanf(current.substr(1, current.size()).data(), "%d", &id);
            if (r < 1) {
                throw std::invalid_argument("matrix argument expected, not " + current);
            }

            ret_val = new argument(last == "const", last == "end", id);
        } else {
            if (current.find("\\") == std::string::npos) {
                r = bscanf(current.substr(1, current.size()).data(), "%d@(%d,%d)", &id, &pos_m, &pos_n);
                if (r < 3) {
                    throw std::invalid_argument("pointer argument expected, not " + current);
                }
                ret_val = new argument(id, pos_m, pos_n);
            } else {
                if (bscanf(current.substr(1, current.size()).data(), "%d@(\\%d,\\%d)", &id, &pos_m, &pos_n) == 3) {
                    ret_val = new argument(id, pos_m, true, pos_n, true);
                } else if (bscanf(current.substr(1, current.size()).data(), "%d@(\\%d,%d)", &id, &pos_m, &pos_n) == 3){

                    ret_val = new argument(id, pos_m, true, pos_n, false);
                } else if (bscanf(current.substr(1, current.size()).data(), "%d@(%d,\\%d)", &id, &pos_m, &pos_n) == 3){
                    ret_val = new argument(id, pos_m, false, pos_n, true);
                } else {
                    throw std::invalid_argument("pointer/index argument expected, not " + current);
                }
            }

        }

    } else if (current[0] == '%') {
        r = bscanf(current.substr(1, current.size()).data(), "%d", &id);
        if (r < 1) {
            throw std::invalid_argument("register argument expected, not " + current);
        }
        ret_val = new argument(id);

    } else if (current[0] == '#') {
        r = bscanf(current.substr(1, current.size()).data(), "%lg", &value);
        if (r < 1) {
            throw std::invalid_argument("value argument expected, not " + current);
        }
        ret_val = new argument(value);
    } else if (current[0] == '\\') {
        r = bscanf(current.substr(1, current.size()).data(), "%d", &id);
        if (r < 1) {
            throw std::invalid_argument("index argument expected, not " + current);
        }
        ret_val = new argument(id, arg_type::idx);
    } else {
        throw std::invalid_argument("argument expected, not " + current);
    }
    next();
    return ret_val;
}

#ifdef PARSER_DEBUG
static void print_results(parser& p)
{
    std::cout << "INSTRUCTIONS:" << std::endl;
    for (const instruction* instr: p.get_instrs()) {
        std::cout << *instr << std::endl;
    }
    std::cout << "REFERENCES:" << std::endl;
    std::vector<int> mtx_refs = argument::get_matrix_references();
    for (auto it = mtx_refs.cbegin(); it != mtx_refs.cend(); it++) {
        std::cout << "($" << it - mtx_refs.cbegin() + 1 << "," << *it << ")" << std::endl;
    }
    std::vector<int> reg_refs = argument::get_register_references();
    for (auto it = reg_refs.cbegin(); it != reg_refs.cend(); it++) {
        std::cout << "(%" << it - reg_refs.cbegin() + 1 << "," << *it << ")" << std::endl;
    }
    
}
#endif

int main(void)
{
#ifdef PARSER_DEBUG
    std::ifstream infile;
    infile.open("instr.asm");
    std::string in_buf((std::istreambuf_iterator<char>(infile)),
            std::istreambuf_iterator<char>());
    infile.close();

    parser p(in_buf);

    try {
        p.parse();
    } catch (const std::exception& e) {
        std::cerr << "error at pos " << p.get_pos() << ": " << e.what() << std::endl;
        return 1;
    }

    print_results(p);
#endif
    return 0;
}

