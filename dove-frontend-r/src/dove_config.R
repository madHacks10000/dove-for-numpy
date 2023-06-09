INSTR_FILE = "instr.asm"
# DATA_FILE = "data.csv"

# Prepare file for writing.
close(file(INSTR_FILE, open="w"))
# Load Pseudonyms from file.
# data_format <- read.csv(DATA_FILE, header=FALSE)

# dove_pseudonyms <- list()

# for (d in 1:nrow(data_format)) {
#     # data_list <- list()
#     # count <- 1
#     # for (j in 1:data_format[d,3]) {
#     #     for (i in 1:data_format[d,2]) {
#     #         data_list[[count]] <- new_dove_pointer(dove_matrix_counter, i, j)
#     #         count <- count + 1
#     #     }
#     # }
#   dove_pseudonyms[[length(dove_pseudonyms) + 1]] <-
#       dove.matrix(as.character(data_format[d,1]), data_format[d,2], data_format[d,3])
#     # new_dove_matrix(list(), c(data_format[d,2], data_format[d,3]),
#     #     data_format[d,1])
#     # if (data_format[i,2] == 1 && data_format[i,3] == 1) {
#     #     # Scalar value.
#     #     # Want to avoid dealing with factors, so we convert to char vector.
#     #     new_ptr <- new_dove_pointer(data_format[i,1], 1, 1)
#     #     dove_pseudonyms[[length(dove_pseudonyms) + 1]] <- new_ptr
#     # }
# }

