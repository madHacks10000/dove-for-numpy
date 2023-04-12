#ifndef _FACTORY_HPP
#define _FACTORY_HPP

#include <string>

#include "unary/plusminus.hpp"
#include "unary/mathgen.hpp"
#include "unary/mathtrig.hpp"
#include "unary/print.hpp"
#include "unary/summary.hpp"
#include "unary/ischeck.hpp"

#include "binary/arith.hpp"
#include "binary/compare.hpp"
#include "binary/logic.hpp"
//#include "binary/pminmax.hpp"
#include "binary/matmul.hpp"
#include "binary/log_bin.hpp"

class UnaryOpFactory {
public:
  static UnaryOp* get_op_for_name(std::string name)
  {
    // True unary operations: plus, minus, bitwise not.
    if (name == "+") {
      return new NoOp();
    } else if (name == "-") {
      return new NegationOp();
    } else if (name == "!") {
      return new BitwiseNotOp();
    }

    // Math group generics, general functions.
    if (name == "abs") {
        return new AbsOp();
    } else if (name == "sign") {
        return new SignOp();
    } else if (name == "sqrt") {
        return new SqrtOp();
    } else if (name == "floor") {
        return new FloorOp();
    } else if (name == "ceiling") {
        return new CeilingOp();
    }
    
    // Math group generics, trigonometry-related functions.
    if (name == "exp") {
        return new ExpOp();
    } else if (name == "log") {
        return new LogOp();    
    } else if (name == "cos") {
        return new CosOp();
    } else if (name == "sin") {
        return new SinOp();
    } else if (name == "tan") {
        return new TanOp();
    }
    
    // Math group generics, cumulative functions.

    // Print.
    if (name == "print") {
        return new PrintOp();
    }

    // is. checks.
    if (name == "NA?") {
        return new IsNaOp();
    } else if (name == "NAN?") {
        return new IsNanOp();
    } else if (name == "INF?") {
        return new IsInfiniteOp();
    }

    // Summary group generics (uses variadic arguments).   
    auto na_pos = name.find("|NA");
    name = name.substr(0, na_pos);
    int is_na = na_pos != std::string::npos;
    if (name == "sum") {
      return new SumFunc(is_na);
    } else if (name == "prod") { 
      return new ProdFunc(is_na);
    } else if (name == "any") { 
      return new AnyFunc(is_na);
    } else if (name == "all") {
      return new AllFunc(is_na);
    } else if (name == "min") {
      return new MinFunc(is_na);
    } else if (name == "max") {
      return new MaxFunc(is_na);
    } else if (name == "range") {
      return new RangeFunc(is_na);
    }
    
    throw std::invalid_argument("no unary op found for name " + name);
  };

  UnaryOpFactory(UnaryOpFactory const&) = delete;
  void operator=(UnaryOpFactory const&) = delete;
};

class BinaryOpFactory {
public:
  static BinaryOp* get_op_for_name(std::string name)
  {
    // Arithmetic operators.
    if (name == "+") {
      return new AdditionOp();
    } else if (name == "-") {
      return new SubtractionOp();
    } else if (name == "*") {
      return new MultiplicationOp();
    } else if (name == "/") {
      return new DivisionOp();
    } else if (name == "^") {
      return new PowOp();
    } else if (name == "%%") {
      return new ModOp();
    } else if (name == "%/%") {
      return new IDivOp();
    } else if (name == "%*%") {
      return new MatMultOp();
    }

    // Comparison operators.
    if (name == "==") {
      return new EqualOp();
    } else if (name == ">") {
      return new GreaterThanOp();
    } else if (name == "<") {
      return new LessThanOp();
    } else if (name == "!=") {
      return new NotEqualOp();
    } else if (name == ">=") {
      return new GreaterThanEqualOp();
    } else if (name == "<=") {
      return new LessThanEqualOp();
    }

    // Logic operators.
    if (name == "&") {
      return new BitwiseAndOp();
    } else if (name == "|") {
      return new BitwiseOrOp();
    }

    //log operator
    if (name == "log") {
      return new LogBinOp();
    }

    throw std::invalid_argument("no binary op found for name " + name);
  };

  BinaryOpFactory(BinaryOpFactory const&) = delete;
  void operator=(BinaryOpFactory const&) = delete;
};

#endif /* _FACTORY_HPP */
