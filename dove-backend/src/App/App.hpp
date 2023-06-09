#ifndef __APP_HPP
#define __APP_HPP

extern void ocall_print(const char* str);
extern void ocall_dump(double* result, size_t len);
extern void ocall_write_metadata(const char* str, int nrow, int ncol);

#endif /* __APP_HPP */
