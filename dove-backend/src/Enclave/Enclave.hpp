#ifndef __ENCLAVE_HPP
#define __ENCLAVE_HPP

#include <cstring>
#include "../App/App.hpp"

extern void ecall_parse(const char* transcript);
extern void ecall_dispatch();
extern void ecall_load_data(double* secrets, const char* dataset_name, size_t num_rows, 
        size_t num_cols, size_t scount);

#endif /* __ENCLAVE_HPP */
