
#include <functional>
#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <memory>
#include <stdbool.h>
        
typedef struct {
	double val;
	double dval;
} _dfloat;

double func(double x, double y);
void d_func(std::shared_ptr<_dfloat> x, std::shared_ptr<_dfloat> y, const std::function<void(std::shared_ptr<_dfloat>)>& k);
std::shared_ptr<_dfloat> make__dfloat(double val, double dval);
std::shared_ptr<_dfloat> make__const__dfloat(double val);
double addf(double x, double y);
void d_addf(std::shared_ptr<_dfloat> x, std::shared_ptr<_dfloat> y, const std::function<void(std::shared_ptr<_dfloat>)>& k);
double subf(double x, double y);
void d_subf(std::shared_ptr<_dfloat> x, std::shared_ptr<_dfloat> y, const std::function<void(std::shared_ptr<_dfloat>)>& k);
double mulf(double x, double y);
void d_mulf(std::shared_ptr<_dfloat> x, std::shared_ptr<_dfloat> y, const std::function<void(std::shared_ptr<_dfloat>)>& k);
double divf(double x, double y);
void d_divf(std::shared_ptr<_dfloat> x, std::shared_ptr<_dfloat> y, const std::function<void(std::shared_ptr<_dfloat>)>& k);
int addi(int x, int y);
int subi(int x, int y);
int muli(int x, int y);
int divi(int x, int y);
double ifelsef(bool cond, double _then, double _else);
void d_ifelsef(bool cond, std::shared_ptr<_dfloat> _then, std::shared_ptr<_dfloat> _else, const std::function<void(std::shared_ptr<_dfloat>)>& k);
int ifelsei(bool cond, int _then, int _else);
bool lessi(int x, int y);
bool lessf(double x, double y);
bool d_lessf(std::shared_ptr<_dfloat> x, std::shared_ptr<_dfloat> y);
bool less_equali(int x, int y);
bool less_equalf(double x, double y);
bool d_less_equalf(std::shared_ptr<_dfloat> x, std::shared_ptr<_dfloat> y);
bool greateri(int x, int y);
bool greaterf(double x, double y);
bool d_greaterf(std::shared_ptr<_dfloat> x, std::shared_ptr<_dfloat> y);
bool greater_equali(int x, int y);
bool greater_equalf(double x, double y);
bool d_greater_equalf(std::shared_ptr<_dfloat> x, std::shared_ptr<_dfloat> y);
bool equali(int x, int y);
bool equalf(double x, double y);
bool d_equalf(std::shared_ptr<_dfloat> x, std::shared_ptr<_dfloat> y);
bool and_b(bool x, bool y);
bool or_b(bool x, bool y);

double func(double x, double y) {
	return addf(mulf(x,y),divf(x,y));
}

void d_func(std::shared_ptr<_dfloat> x, std::shared_ptr<_dfloat> y, const std::function<void(std::shared_ptr<_dfloat>)>& k) {
	d_mulf(x,y,[x,y,k](std::shared_ptr<_dfloat>t1)
		-> void{d_divf(x,y,[x,y,k,t1](std::shared_ptr<_dfloat>t0)
			-> void{d_addf(t1,t0,k);});});
}

std::shared_ptr<_dfloat> make__dfloat(double val, double dval) {
	std::shared_ptr<_dfloat> ret = std::make_shared<_dfloat>();
	(ret)->val = val;
	(ret)->dval = dval;
	return ret;
}

std::shared_ptr<_dfloat> make__const__dfloat(double val) {
	return make__dfloat(val,(float)(0.0));
}

double addf(double x, double y) {
	return (x) + (y);
}

void d_addf(std::shared_ptr<_dfloat> x, std::shared_ptr<_dfloat> y, const std::function<void(std::shared_ptr<_dfloat>)>& k) {
	std::shared_ptr<_dfloat> ret = make__dfloat(((x)->val) + ((y)->val),(float)(0.0));
	k(ret);
	(x)->dval = ((x)->dval) + ((ret)->dval);
	(y)->dval = ((y)->dval) + ((ret)->dval);
}

double subf(double x, double y) {
	return (x) - (y);
}

void d_subf(std::shared_ptr<_dfloat> x, std::shared_ptr<_dfloat> y, const std::function<void(std::shared_ptr<_dfloat>)>& k) {
	std::shared_ptr<_dfloat> ret = make__dfloat(((x)->val) - ((y)->val),(float)(0.0));
	k(ret);
	(x)->dval = ((x)->dval) + ((ret)->dval);
	(y)->dval = ((y)->dval) + (((float)(-1.0)) * ((ret)->dval));
}

double mulf(double x, double y) {
	return (x) * (y);
}

void d_mulf(std::shared_ptr<_dfloat> x, std::shared_ptr<_dfloat> y, const std::function<void(std::shared_ptr<_dfloat>)>& k) {
	std::shared_ptr<_dfloat> ret = make__dfloat(((x)->val) * ((y)->val),(float)(0.0));
	k(ret);
	(x)->dval = ((x)->dval) + (((y)->val) * ((ret)->dval));
	(y)->dval = ((y)->dval) + (((x)->val) * ((ret)->dval));
}

double divf(double x, double y) {
	return (x) / (y);
}

void d_divf(std::shared_ptr<_dfloat> x, std::shared_ptr<_dfloat> y, const std::function<void(std::shared_ptr<_dfloat>)>& k) {
	std::shared_ptr<_dfloat> ret = make__dfloat(((x)->val) / ((y)->val),(float)(0.0));
	k(ret);
	(x)->dval = ((x)->dval) + (((ret)->dval) / ((y)->val));
	(y)->dval = ((y)->dval) + (((float)(-1.0)) * ((((ret)->dval) * ((x)->val)) / (((y)->val) * ((y)->val))));
}

int addi(int x, int y) {
	return (x) + (y);
}

int subi(int x, int y) {
	return (x) - (y);
}

int muli(int x, int y) {
	return (x) - (y);
}

int divi(int x, int y) {
	return (x) - (y);
}

double ifelsef(bool cond, double _then, double _else) {
	if (cond) {
		return _then;
	} else {
		return _else;
	}
}

void d_ifelsef(bool cond, std::shared_ptr<_dfloat> _then, std::shared_ptr<_dfloat> _else, const std::function<void(std::shared_ptr<_dfloat>)>& k) {
	if (cond) {
		k(_then);
	} else {
		k(_else);
	}
}

int ifelsei(bool cond, int _then, int _else) {
	if (cond) {
		return _then;
	} else {
		return _else;
	}
}

bool lessi(int x, int y) {
	return (x) < (y);
}

bool lessf(double x, double y) {
	return (x) < (y);
}

bool d_lessf(std::shared_ptr<_dfloat> x, std::shared_ptr<_dfloat> y) {
	return ((x)->val) < ((y)->val);
}

bool less_equali(int x, int y) {
	return (x) <= (y);
}

bool less_equalf(double x, double y) {
	return (x) <= (y);
}

bool d_less_equalf(std::shared_ptr<_dfloat> x, std::shared_ptr<_dfloat> y) {
	return ((x)->val) <= ((y)->val);
}

bool greateri(int x, int y) {
	return (x) > (y);
}

bool greaterf(double x, double y) {
	return (x) > (y);
}

bool d_greaterf(std::shared_ptr<_dfloat> x, std::shared_ptr<_dfloat> y) {
	return ((x)->val) > ((y)->val);
}

bool greater_equali(int x, int y) {
	return (x) >= (y);
}

bool greater_equalf(double x, double y) {
	return (x) >= (y);
}

bool d_greater_equalf(std::shared_ptr<_dfloat> x, std::shared_ptr<_dfloat> y) {
	return ((x)->val) >= ((y)->val);
}

bool equali(int x, int y) {
	return (x) == (y);
}

bool equalf(double x, double y) {
	return (x) == (y);
}

bool d_equalf(std::shared_ptr<_dfloat> x, std::shared_ptr<_dfloat> y) {
	return ((x)->val) == ((y)->val);
}

bool and_b(bool x, bool y) {
	return (x) && (y);
}

bool or_b(bool x, bool y) {
	return (x) || (y);
}


namespace py = pybind11;


PYBIND11_MODULE(builtins, m) {
    py::class_<_dfloat, std::shared_ptr<_dfloat>>(m, "_dfloat", py::module_local())
        .def(py::init<>())
        .def_readwrite("val", &_dfloat::val)
        .def_readwrite("dval", &_dfloat::dval);

    m.def("make__dfloat", &make__dfloat,
          py::arg("val"), py::arg("dval"),
          "Create a _dfloat with specified value and derivative.");

    m.def("make__const__dfloat", &make__const__dfloat,
          py::arg("val"),
          "Create a constant _dfloat (zero derivative).");

    m.def("func", &func,py::arg("x"),py::arg("y"));
    m.def("d_func", &d_func,py::arg("x"),py::arg("y"),py::arg("k"));
    m.def("make__dfloat", &make__dfloat,py::arg("val"),py::arg("dval"));
    m.def("make__const__dfloat", &make__const__dfloat,py::arg("val"));
    m.def("addf", &addf,py::arg("x"),py::arg("y"));
    m.def("d_addf", &d_addf,py::arg("x"),py::arg("y"),py::arg("k"));
    m.def("subf", &subf,py::arg("x"),py::arg("y"));
    m.def("d_subf", &d_subf,py::arg("x"),py::arg("y"),py::arg("k"));
    m.def("mulf", &mulf,py::arg("x"),py::arg("y"));
    m.def("d_mulf", &d_mulf,py::arg("x"),py::arg("y"),py::arg("k"));
    m.def("divf", &divf,py::arg("x"),py::arg("y"));
    m.def("d_divf", &d_divf,py::arg("x"),py::arg("y"),py::arg("k"));
    m.def("addi", &addi,py::arg("x"),py::arg("y"));
    m.def("subi", &subi,py::arg("x"),py::arg("y"));
    m.def("muli", &muli,py::arg("x"),py::arg("y"));
    m.def("divi", &divi,py::arg("x"),py::arg("y"));
    m.def("ifelsef", &ifelsef,py::arg("cond"),py::arg("_then"),py::arg("_else"));
    m.def("d_ifelsef", &d_ifelsef,py::arg("cond"),py::arg("_then"),py::arg("_else"),py::arg("k"));
    m.def("ifelsei", &ifelsei,py::arg("cond"),py::arg("_then"),py::arg("_else"));
    m.def("lessi", &lessi,py::arg("x"),py::arg("y"));
    m.def("lessf", &lessf,py::arg("x"),py::arg("y"));
    m.def("d_lessf", &d_lessf,py::arg("x"),py::arg("y"));
    m.def("less_equali", &less_equali,py::arg("x"),py::arg("y"));
    m.def("less_equalf", &less_equalf,py::arg("x"),py::arg("y"));
    m.def("d_less_equalf", &d_less_equalf,py::arg("x"),py::arg("y"));
    m.def("greateri", &greateri,py::arg("x"),py::arg("y"));
    m.def("greaterf", &greaterf,py::arg("x"),py::arg("y"));
    m.def("d_greaterf", &d_greaterf,py::arg("x"),py::arg("y"));
    m.def("greater_equali", &greater_equali,py::arg("x"),py::arg("y"));
    m.def("greater_equalf", &greater_equalf,py::arg("x"),py::arg("y"));
    m.def("d_greater_equalf", &d_greater_equalf,py::arg("x"),py::arg("y"));
    m.def("equali", &equali,py::arg("x"),py::arg("y"));
    m.def("equalf", &equalf,py::arg("x"),py::arg("y"));
    m.def("d_equalf", &d_equalf,py::arg("x"),py::arg("y"));
    m.def("and_b", &and_b,py::arg("x"),py::arg("y"));
    m.def("or_b", &or_b,py::arg("x"),py::arg("y"));
}
