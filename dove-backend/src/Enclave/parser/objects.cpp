#include <stdexcept>

#include "objects.hpp"

#ifndef NOENCLAVE
#include "Enclave_t.h"
#else
#ifndef PARSER_DEBUG
#include "../App/App.hpp"
#endif
#endif

#ifdef PARSER_DEBUG
	std::ostream& operator<<(std::ostream &os, const argument &a)
	{
	    os << "arg{";
	    if (a.type == arg_type::val) {
		os << "#" << a.value << "}";
	    } else if (a.type == arg_type::ptr) {
		os << "$" << a.data[0] << "@(" << ((a.is_index[1]) ? "\\" : "") << a.data[1]  << "," << ((a.is_index[2]) ? "\\" : "") << a.data[2] << ")";
	    } else if (a.type == arg_type::reg) {
		os << "%" << a.data[0] << "}";
	    } else if (a.type == arg_type::idx) {
		os << "\\" << a.data[0] << "}";
	    } else {
		if (a.is_const()) {
		    os << "const ";
		}
		os << "$" << a.data[0] << "}";
	    }

	    return os;
	}

	std::ostream& operator<<(std::ostream &os, const sequence &s)
	{
	    os << "seq{";
	    if (s.is_ordered()) {
		if (s.seq.size() == 3) {
		    os << "[" << ((s.is_index[0]) ? "\\" : "") << s.seq[0];
		    os << ":" << ((s.is_index[1]) ? "\\" : "") << s.seq[1];
		    os << ":" << ((s.is_index[2]) ? "\\" : "") << s.seq[2] << "]";
		} else {
		    /* os << "[" << ((s.is_index[0]) ? "\\" : "") << s.seq[0] << "]"; */
		    throw std::invalid_argument("cannot have ordered sequences not of size 3");
		}
	    } else {
		for (int i = 0; i < s.seq.size(); i++) {
		    os << ((s.is_index[i]) ? "\\" : "") << s.seq[i] << ",";
		}
	    }
	    os << "}";

	    return os;
	}

	std::ostream& operator<<(std::ostream &os, const instruction &instr)
	{
	    os << "instr{" << instr.name << ": ";
	    for (argument* const arg: instr.args) {
		os << *arg << ",";
	    }
	    for (sequence* const seq: instr.seqs) {
		os << *seq << ",";
	    }
	    os << "}";
	    if (instr.name == "forloop") {
		for (auto i: instr.loop_instrs) {
		    os << std::endl;
		    os << *i;
		}
	    }
	    return os;
	}
#endif

	/* std::map<int, int> argument::index_starts;
	size_t sequence::size()
	{
	    size_t count = 0;
	    if (is_index.size() != seq.size()) {
		throw std::runtime_error("mismatched index and sequence arrays");
	    }
	    if (!ordered) {
		for (int i = 0; i < is_index.size(); i++) {
		    count += (is_index[i] ? argument::get_index_start(seq[i]) : 1);
		}
	    } else {
		int start = (is_index[0] ? argument::get_index_start(seq[0]) : seq[0]);
		int stop = (is_index[1] ? argument::get_index_start(seq[1]) : seq[1]);
		int step = (is_index[2] ? argument::get_index_start(seq[2]) : 1);
		int calculation = (stop - step + 1) / step;
		if (calculation >= 0) {
		    count = static_cast<size_t>(calculation);
		}
	    }
	    return count;
	} */

	int argument::reference_multiplier = 1;

	std::vector<int> argument::matrix_references;
	void argument::add_matrix_reference(int id, bool is_end)
	{
	    size_t matrix_id = static_cast<size_t>(id-1);
	    if (matrix_id == matrix_references.size()) {
		matrix_references.push_back(reference_multiplier);
		slice_relations.push_back(-1);
	    } else if (matrix_id < matrix_references.size()) {
		if (!is_end) {
		    matrix_references[matrix_id] += reference_multiplier;
		    int parent = slice_relations[matrix_id];
		    while (parent > 0) {
			matrix_references[parent] += reference_multiplier;
			parent = slice_relations[parent];
		    }
		}
	    } else {
		throw std::invalid_argument("matrix $" + std::to_string(id) + " referenced before defined");
	    }
	}

	std::vector<int> argument::register_references;
	void argument::add_register_reference(int reg_no)
	{
	    size_t register_num = static_cast<size_t>(reg_no-1);
	    if (register_num == register_references.size()) {
		register_references.push_back(reference_multiplier);
	    } else if (register_num < register_references.size()) {
		register_references[register_num] += reference_multiplier;
	    } else {
		throw std::invalid_argument("register %" + std::to_string(reg_no) + " referenced before set");
	    }
	}

	std::vector<int> argument::index_references;
	void argument::add_index_reference(int idx_no)
	{
	    size_t index_num = static_cast<size_t>(idx_no-1);
	    if (index_num == index_references.size()) {
		index_references.push_back(reference_multiplier);
	    } else if (index_num < index_references.size()) {
		index_references[index_num] += reference_multiplier;
	    } else {
		throw std::invalid_argument("index \\" + std::to_string(idx_no) + " referenced before bound");
	    }
	}

	std::vector<int> argument::slice_relations;
	void argument::set_slice_of(argument *child, argument *parent)
	{
	    if (child == NULL || parent == NULL) {
		throw std::invalid_argument("cannot set slice of NULL");
	    }

	    if (child->type != parent->type || child->type != arg_type::mtx) {
		throw std::invalid_argument("can only set matrix slices");
	    }

	    size_t parent_id = static_cast<size_t>((parent->data[0]) - 1);
	    size_t child_id = static_cast<size_t>((child->data[0]) - 1);
	    matrix_references[parent_id] += reference_multiplier;  // because slice calls both parent and child
	    slice_relations[child_id] = parent_id;
	}

	int argument::get_matrix(int& matrix_id)
	{
	    if (type == arg_type::mtx) {
		matrix_id = data[0];
		// ocall_print(("getting matrix " + std::to_string(data[0])).c_str());
		size_t matrix_ref_id = static_cast<size_t>(data[0] - 1);
		// ocall_print(("matrix arg_refs " + std::to_string(matrix_references[matrix_ref_id])).c_str());
		matrix_references[matrix_ref_id] -= 1;
		int parent = slice_relations[matrix_ref_id];
		while (parent > 0) {
		    // ocall_print(("found parent " + std::to_string(parent+1)).c_str());
		    // ocall_print(("parent arg_refs " + std::to_string(matrix_references[parent])).c_str());
		    matrix_references[parent] -= 1;
		    parent = slice_relations[parent];
		}
		return matrix_references[matrix_ref_id];
	    }
	    return -1;
	}

	int argument::get_pointer(int& matrix_id, int& pos_m, int& pos_n)
	{
	    if (type == arg_type::ptr) {
		matrix_id = data[0];
		pos_m = data[1];
		pos_n = data[2];
		size_t matrix_ref_id = static_cast<size_t>(data[0] - 1);
		matrix_references[matrix_ref_id] -= 1;
		int parent = slice_relations[matrix_ref_id];
		while (parent > 0) {
		    matrix_references[parent] -= 1;
		    parent = slice_relations[parent];
		}
		return matrix_references[matrix_ref_id];
	    }
	    return -1;
	}

	int argument::get_value(double& val)
	{
	    if (type == arg_type::val) {
		val = value;
		return 1;
	    }
	    return 0;

	}

	int argument::get_register(int& reg_no)
	{
	    if (type == arg_type::reg) {
		reg_no = data[0];
		size_t register_num = static_cast<size_t>(reg_no-1);
		register_references[register_num] -= 1;
		return register_references[register_num];
	    }
	    return 0;
	}

	int argument::get_index(int& idx_no)
	{
	    if (type == arg_type::idx) {
		idx_no = data[0];
    }
    return 0;
}

std::map<std::string, int> instruction::dataset_refs;
int instruction::add_ref_for_dataset(std::string dset) {
    if (dataset_refs.find(dset) == dataset_refs.end()) {
        dataset_refs[dset] = 1;
    } else {
        dataset_refs[dset] += 1;
    }
    return dataset_refs[dset];
}
