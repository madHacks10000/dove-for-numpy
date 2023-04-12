#include <stdio.h>
#include <iostream>
#include <fstream>
#include <string>
#include <sstream>

#ifndef NOENCLAVE
#include "Enclave_u.h"
#include "sgx_urts.h"
#include "sgx_utils/sgx_utils.h"
#else
#include "../Enclave/Enclave.hpp"
#include "App.hpp"
#endif /* NOENCLAVE */

#define RESULT_DUMP_PATH "../examples/"
#define ENCLAVE_TOKEN_PATH "enclave.token"
#define ENCLAVE_SO_PATH "enclave.signed.so"
#define ASSEMBLY_PATH "../../modified_dove/dove-frontend-r/src/instr.asm"
#define METADATA_PATH "../examples/sample.metadata"
#define PROG_DATA_PATH "../examples/data.csv"

#ifndef NOENCLAVE
/* Global EID shared by multiple threads */
sgx_enclave_id_t global_eid = 0;
#endif /* NOENCLAVE */

// OCall implementations
void ocall_print(const char* str) {
    printf("%s\n", str);
}

/* WARNING: TLS implementation is required for this function. */
size_t ctr = 0; //global print counter
void ocall_dump(double* result, size_t len) {
    std::string s(RESULT_DUMP_PATH);
    s = s+"result_"+std::to_string(ctr)+".data";
    std::ofstream ret_fs(s.c_str(), std::ios::binary | std::ios::out);
    ret_fs.write((char*) result, len);
    ret_fs.close();
    ctr++;
}

std::ofstream prog_data(PROG_DATA_PATH);
void ocall_write_metadata(const char* str, int nrow, int ncol) {
    prog_data << str  << "," << nrow << "," << ncol << std::endl;
}

int main(int argc, char const *argv[]) {
#ifndef NOENCLAVE
    if (initialize_enclave(&global_eid, ENCLAVE_TOKEN_PATH, ENCLAVE_SO_PATH) < 0) {
        std::cout << "Fail to initialize enclave." << std::endl;
        return 1;
    }
#endif /* NOENCLAVE */

    /* WARNING:
     * TLS implementation is required for this process of loading data from clients.
     * Current implementation loads data in plaintext.
     */
    std::ifstream metadata(METADATA_PATH);
    std::string line;
    std::string filename;
    size_t num_rows, num_cols;
    while (std::getline(metadata,line)) {
        std::istringstream instream(line);
        std::string temp_string;
        instream >> filename;
        instream >> temp_string;
        std::string dsname(temp_string);
        instream >> temp_string;
        num_rows = stoi(temp_string);
        instream >> temp_string;
        num_cols = stoi(temp_string);

        std::ifstream plaintext(filename, std::ios::binary | std::ios::in);
        size_t scount = num_rows * num_cols;
        double* secrets_c = (double*)malloc(sizeof(double) * num_rows * num_cols);
        plaintext.read((char*)secrets_c, sizeof(double) * num_rows * num_cols);
        const char* dsname_c = dsname.c_str();

#ifndef NOENCLAVE
        if (ecall_load_data(global_eid, secrets_c, dsname_c, num_rows, num_cols, scount) != 0) {
            std::cout << "Fail to load data in the enclave." << std::endl;
            return 1;
        }
#else
        ecall_load_data(secrets_c, dsname_c, num_rows, num_cols, scount);
#endif /* NOENCLAVE */
        free(secrets_c);
        plaintext.close();
    }
    metadata.close();
    prog_data.close();

    /* WARNING:
     * TLS implementation is required for this process of loading transcripts from clients.
     * Current implementation loads transcripts in plaintext.
     */
    std::ifstream assembly(ASSEMBLY_PATH);
    std::string asm_str((std::istreambuf_iterator<char>(assembly)),
                            std::istreambuf_iterator<char>());
    const char* transcript = asm_str.c_str();
#ifndef NOENCLAVE
    if (ecall_parse(global_eid, transcript) < 0) {
        std::cout << "Parsing failed." <<std::endl;
        return 1;
    }

    if (ecall_dispatch(global_eid) < 0) {
        std::cout << "Dispatch failed." <<std::endl;
        return 1;
    }

    sgx_status_t status = sgx_destroy_enclave(global_eid);
    if(status != SGX_SUCCESS) {
        std::cout <<  "Failed to destroy the enclave." << std::endl;
        return 1;
    }
#else
    ecall_parse(transcript);
    ecall_dispatch();
#endif /* NOENCLAVE */
    return 0;
}
