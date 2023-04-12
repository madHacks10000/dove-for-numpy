#ifndef NOENCLAVE
#include "Enclave_t.h"

#else
#include "Enclave.hpp"

#endif /* NOENCLAVE */

#include "parser/parser.hpp"
#include "runtime.hpp"

#include <string>

Runtime r;
parser *p;
char* t;

void ecall_parse(const char* transcript) {
    t = new char[strlen(transcript) + 1];
    strncpy(t, transcript, strlen(transcript));
    t[strlen(transcript)] = '\0';
    p = new parser(t);

    try {
        p->parse();
    } catch (const std::exception& e) {
        std::string s("parsing error at ");
        s = s + std::to_string(p->get_pos());
        s = s + ": ";
        s = s + e.what();
        ocall_print(s.c_str());
        return;
    }
}

void ecall_dispatch() {
    std::list<instruction*> instrs = p->get_instrs();
    size_t instr_len = instrs.size();
    try {
        r.dispatch(instrs);
    } catch (const std::exception& e) {
        std::string s("dispatch error at ");
        s = s + std::to_string(instr_len - instrs.size() + 2);
        s = s + ": ";
        s = s + e.what();
        ocall_print(s.c_str());
    }

    delete p;
    delete[] t;
}

void ecall_load_data(double* secrets, const char* dataset_name, size_t num_rows, 
        size_t num_cols, size_t scount)
{
    r.load_data(secrets, dataset_name, num_rows, num_cols);
}
