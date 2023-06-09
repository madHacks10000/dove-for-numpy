# File name to automate
#file_name <- './unmod-scripts/calc_neiFis_onepop.R'
args <- commandArgs()
#fname <- args[length(args)]
file_name <- args[length(args)]
#file_name <- paste('./unmod-scripts/calc_', fname, '.R', sep='')

## Automation routines
# TEXT: Automate multiple assignment
automate_multi <- function(lines) {
    while (TRUE) {
        idx <- grep("<-.*<-", lines, value = FALSE)
        if (length(idx) == 0) {
            break
        }
        i <- idx[[1]]
        line <- lines[i]
        print(line)
        split_line <- unlist(strsplit(line, "<-"))
        new_lines <- NULL
        lines <- lines[-i]
        for (j in 1:(length(split_line)-1)) {
            new_line <- sprintf("%s<-%s", split_line[[j]], split_line[[length(split_line)]])
            lines <- append(lines, new_line, after=i-1)  # i.e., before i
        }
    }
    lines
}

# TEXT: Manually source in files from top level
load_source <- function(lines) {
    while (TRUE) {
        idx <- grep("source\\(.*\\)", lines, value = FALSE)
        if (length(idx) == 0) {
            break
        }
        i <- idx[[1]]
        line <- lines[i]
        split_line <- unlist(strsplit(line, "\'"))
        if (identical(split_line[[2]], "dove.R")) {
            # don't transform internal DOVE stuff
            break
        }
        new_lines <- NULL
        lines <- lines[-i]
        source_file <- file(split_line[[2]])
        source_lines <- readLines(source_file)
        close(source_file)

        for (j in 1:(length(source_lines))) {
            new_line <- source_lines[[j]]
            lines <- append(lines, new_line, after=i-2+j)  # i.e., before i
        }

    }
    lines
}

# AST: Automate for loops, both general and special-break case
# TODO: Loops over lists and more complex sequences
modify_for <- function(x) {
    for_loop <- x[[1]]
    index_var <- x[[2]]
    from <- x[[3]][[2]]
    to <- x[[3]][[3]]
    step <- 1  # TODO: more interesting (negative loops)
    x[[4]] <- recur_eval(x[[4]])
    # loop_func <- parse_expr(sprintf("function (%s, break_cond = dove.matrix(0)) {}", as_string(index_var)))
    loop_func <- parse_expr(sprintf("function (%s) {}", as_string(index_var)))
    loop_func[[3]] <- x[[4]]

    call2(dove.for, from, to, step, loop_func)
}

modify_while <- function(x) {
    while_loop <- x[[1]]
    condition <- x[[2]]
    index_var <- condition[[2]]
    if (is_call(condition, ">=") || is_call(condition, "<=")) {
        from <- condition[[2]]
        to <- condition[[3]]
    } else {
        # TODO raise error
    }
    step <- 1
    x[[3]] <- recur_eval(x[[3]])
    # try to pull the step from the last entry in the loop
    to_step_check <- x[[3]][[length(x[[3]])]]
    if (is_call(to_step_check, "if")) {
        to_step_check <- to_step_check[[4]]
    }
    if (is_call(to_step_check[[length(to_step_check)]], "<-") || is_call(to_step_check[[length(to_step_check)]], "=")) {
        asgn_call <- to_step_check[[length(to_step_check)]]
        if (identical(index_var, asgn_call[[2]])) {
            if (is_call(asgn_call[[3]], "-")) {
                step <- -asgn_call[[3]][[3]]
            } else {
                step <- asgn_call[[3]][[3]]
            }
        }
        # TODO error
    }
    # loop_func <- parse_expr(sprintf("function (%s, break_cond = dove.matrix(0)) {}", as_string(index_var)))
    loop_func <- parse_expr(sprintf("function (%s) {}", as_string(index_var)))
    add_break <- parse_expr("{ break_cond <- matrix(0) }")
    for (i in 2:length(x[[3]])) {
        add_break[[1+i]] <- x[[3]][[i]]
    }
    # loop_func[[3]] <- x[[3]]
    loop_func[[3]] <- add_break
    # print(loop_func)

    # print(condition[[2]])
    call2(dove.for, from, to, step, loop_func)
}

# AST: Automate if statements
# If the value exists, it will have a valid class we can use as a default value
check_exists <- function(sym) { if (class(try(sym, TRUE)) != 'try-error') sym else NA }
check_exists_logical <- function(sym) { (class(try(sym, TRUE)) != 'try-error') }
is_break <<- FALSE
modify_if <- function(x) {
    if_list <- x[[1]]  # the actual "if" statement
    predicate <- x[[2]]  # the if condition
    condition <- x[[2]]
    # Iterate over compound expressions x[[3]]
    for (i in 2:length(x[[3]])) { # x[[3]][[1]] is `{`
        item <- x[[3]][[i]]
        if (is_call(item, "if")) {
            # TODO: Nested if statements -- more recursion?
            item <- call2(ifelse, predicate, modify_if(item), NA)
        } else if (is_call(item, "break")) {
            # We're in a loop, and we're calling break
            break_expr <- parse_expr("break_cond[,] <- !break_cond[[1]] & TRUE")
            break_expr[[3]][[3]] <- predicate
            item <- break_expr
            is_break <<- TRUE 
            # Ignore everything else from this block
            predicate <- break_expr[[3]] 
        } else if (is_call(item, "<-") || is_call(item, "=")) {
            # Semantics: x <- y  >>> item[[2]] item[[1]] item[[3]]
            check_call <- call2(check_exists, item[[2]])
            item[[3]] <- call2(ifelse, predicate, item[[3]], check_call)
        } else {
            item <- call2(ifelse, predicate, (item), NA)
        }
        x[[3]][[i]] <- item
    }
    if (length(x) == 4) {
        # TODO: else if case (recursive call), also it needs to handle break
        if (is_break) {
            predicate <- parse_expr("!break_cond[[1]] & !(TRUE)")
            predicate[[3]][[2]] <- condition

        } else {
            predicate <- parse_expr("!(TRUE)")
            predicate[[2]] <- condition
        }

        to_modify <- parse_expr("if (TRUE) {}")
        to_modify[[2]] <- predicate
        to_modify[[3]] <- x[[4]]
        to_modify <- modify_if(to_modify)

        x[[3]][[i+1]] <- to_modify
        x[[4]] <- parse_expr("{}") # empty out else clause
    }
    x[[2]] <- TRUE # always run this -- in place replacement
    is_break <<- FALSE
    x
}

lapply_supported <- c("fisher.test", "[[")
modify_lapply <- function(x) {
    if (is_call(x[[2]], "split")) {
        x <- x[[2]][[2]]
    } else if (is_symbol(x[[2]]) && (as_string(x[[3]]) %in% lapply_supported)) {
        if (x[[3]] == "[[") {
            # HACK for indexing
            x <- call2(`[`, x[[2]], , x[[4]])
        } else {
        x[[1]] <- x[[3]]
        x[[3]] <- NULL
        }
    }

    x
}

recur_eval <- function(x) {
    if (is_call(x, "while")) {
        x <- modify_while(x)
    } else if (is_call(x, "for")) {
        x <- modify_for(x)
    } else if (is_call(x, "if")) {
        x <- modify_if(x)
    } else if (is_call(x, "lapply")) {
        x <- modify_lapply(x)
    } else if ((is_call(x, "<-") || is_call(x, "=")) && (is_symbol(x[[2]])) && is_symbol(x[[3]])) {
        # Make a copy when moving a symbol around
        x[[3]] <- call2(`+`, x[[3]])
    } else if (((is_call(x, "<-") || is_call(x, "=")) && (is_call(x[[3]]) && (!is_call(x[[3]], "cbind")) && (!is_call(x[[3]], "rbind")) && (!is_call(x[[3]], "apply")) && (!is_call(x[[3]], "lapply")) && identical(x[[3]][[2]], x[[2]])))) {
        # found_apply <- FALSE
        # for(i in 1:length(x[[3]])) {
        #     if(grepl('apply',x[[3]][i]) == TRUE || grepl('apply',x[[3]][i]) == TRUE) {
        #         found_apply <- TRUE
        #         break
        #     }
        # }
 
        # if(found_apply == TRUE) {
        #     #HACK to deal with dimensionality issue when with apply
        #     # Added additional HACK for lapply
        # } else {
        check_if_update <- parse_expr(sprintf("if (class(x) == \"dove_matrix\") { x[,] <- NA } else { x <- NA }"))
        check_if_update[[2]][[2]][[2]] <- x[[2]] # inherits
        check_if_update[[3]][[2]][[1]] <- x[[1]] # operation
        check_if_update[[3]][[2]][[2]][[2]] <- x[[2]] # variable
        check_if_update[[3]][[2]][[3]] <- x[[3]] # value
        check_if_update[[4]][[2]][[1]] <- x[[1]] # else operation
        check_if_update[[4]][[2]][[2]] <- x[[2]] # else variable
        check_if_update[[4]][[2]][[3]] <- x[[3]] # else value
        x <- check_if_update
        # }
        #print(check_if_update)
        # TODO: if problems in other scripts, look here
    } else {
        for (i in 1:length(x)) {
            item <- x[[i]]
            if (missing(item)) {
                # Skip empty arguments that get parsed in
                next
            }
            if (is_call(item)) {
                item <- recur_eval(item)
                x[[i]] <- item
            } 
        }
    }
    x
}

# TODO: Recurse on SOURCE blocks

library('rlang')
library('readr')
source('dove.R')

# Load file for automation 
file_conn <- file(file_name)
lines <- readLines(file_conn)
close(file_conn)

# Apply text transformations
lines <- automate_multi(lines)
lines <- load_source(lines)

# Write file to temp directory
tmp_name <- "/tmp/dove_automate_autogen.R"
tmp_conn <- file(tmp_name, open="w")
writeLines(lines, tmp_conn)
close(tmp_conn)

# Apply AST transformations
eval_list <- parse_exprs(read_file(tmp_name))
eval_list <- recur_eval(eval_list)
print(eval_list)

# Run the AST
for (e in eval_list) { eval(e) }
