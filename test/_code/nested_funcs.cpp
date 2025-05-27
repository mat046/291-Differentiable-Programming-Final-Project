
#include <functional>
#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <memory>
        
typedef struct {
	float val;
	float dval;
} _dfloat;

float quartic(float x);
float quadruple(float x);
float func(float x);
void d_func(std::shared_ptr<_dfloat> x, const std::function<void(std::shared_ptr<_dfloat>)>& k);
std::shared_ptr<_dfloat> make__dfloat(float val, float dval);
std::shared_ptr<_dfloat> make__const__dfloat(float val);
float addf(float x, float y);
void d_addf(std::shared_ptr<_dfloat> x, std::shared_ptr<_dfloat> y, const std::function<void(std::shared_ptr<_dfloat>)>& k);
float subf(float x, float y);
void d_subf(std::shared_ptr<_dfloat> x, std::shared_ptr<_dfloat> y, const std::function<void(std::shared_ptr<_dfloat>)>& k);
float mulf(float x, float y);
void d_mulf(std::shared_ptr<_dfloat> x, std::shared_ptr<_dfloat> y, const std::function<void(std::shared_ptr<_dfloat>)>& k);
float divf(float x, float y);
void d_divf(std::shared_ptr<_dfloat> x, std::shared_ptr<_dfloat> y, const std::function<void(std::shared_ptr<_dfloat>)>& k);
void d_quartic(std::shared_ptr<_dfloat> x, const std::function<void(std::shared_ptr<_dfloat>)>& k);
void d_quadruple(std::shared_ptr<_dfloat> x, const std::function<void(std::shared_ptr<_dfloat>)>& k);

float quartic(float x) {
	return mulf(mulf(x,x),mulf(x,x));
}

float quadruple(float x) {
	return addf(addf(x,x),addf(x,x));
}

float func(float x) {
	return quadruple(quartic(x));
}

void d_func(std::shared_ptr<_dfloat> x, const std::function<void(std::shared_ptr<_dfloat>)>& k) {
	d_quartic(x,[x,k](std::shared_ptr<_dfloat>t0)
		-> void{d_quadruple(t0,k);});
}

std::shared_ptr<_dfloat> make__dfloat(float val, float dval) {
	std::shared_ptr<_dfloat> ret = std::make_shared<_dfloat>();
	(ret)->val = val;
	(ret)->dval = dval;
	return ret;
}

std::shared_ptr<_dfloat> make__const__dfloat(float val) {
	return make__dfloat(val,(float)(0.0));
}

float addf(float x, float y) {
	return (x) + (y);
}

void d_addf(std::shared_ptr<_dfloat> x, std::shared_ptr<_dfloat> y, const std::function<void(std::shared_ptr<_dfloat>)>& k) {
	std::shared_ptr<_dfloat> ret = make__dfloat(((x)->val) + ((y)->val),(float)(0.0));
	k(ret);
	(x)->dval = ((x)->dval) + ((ret)->dval);
	(y)->dval = ((y)->dval) + ((ret)->dval);
}

float subf(float x, float y) {
	return (x) - (y);
}

void d_subf(std::shared_ptr<_dfloat> x, std::shared_ptr<_dfloat> y, const std::function<void(std::shared_ptr<_dfloat>)>& k) {
	std::shared_ptr<_dfloat> ret = make__dfloat(((x)->val) - ((y)->val),(float)(0.0));
	k(ret);
	(x)->dval = ((x)->dval) + ((ret)->dval);
	(y)->dval = ((y)->dval) + (((float)(-1.0)) * ((ret)->dval));
}

float mulf(float x, float y) {
	return (x) * (y);
}

void d_mulf(std::shared_ptr<_dfloat> x, std::shared_ptr<_dfloat> y, const std::function<void(std::shared_ptr<_dfloat>)>& k) {
	std::shared_ptr<_dfloat> ret = make__dfloat(((x)->val) * ((y)->val),(float)(0.0));
	k(ret);
	(x)->dval = ((x)->dval) + (((y)->val) * ((ret)->dval));
	(y)->dval = ((y)->dval) + (((x)->val) * ((ret)->dval));
}

float divf(float x, float y) {
	return (x) / (y);
}

void d_divf(std::shared_ptr<_dfloat> x, std::shared_ptr<_dfloat> y, const std::function<void(std::shared_ptr<_dfloat>)>& k) {
	std::shared_ptr<_dfloat> ret = make__dfloat(((x)->val) / ((y)->val),(float)(0.0));
	k(ret);
	(x)->dval = ((x)->dval) + (((ret)->dval) / ((y)->val));
	(y)->dval = ((y)->dval) + (((float)(-1.0)) * ((((ret)->dval) * ((x)->val)) / (((y)->val) * ((y)->val))));
}

void d_quartic(std::shared_ptr<_dfloat> x, const std::function<void(std::shared_ptr<_dfloat>)>& k) {
	d_mulf(x,x,[x,k](std::shared_ptr<_dfloat>t1)
		-> void{d_mulf(x,x,[x,k,t1](std::shared_ptr<_dfloat>t0)
			-> void{d_mulf(t1,t0,k);});});
}

void d_quadruple(std::shared_ptr<_dfloat> x, const std::function<void(std::shared_ptr<_dfloat>)>& k) {
	d_addf(x,x,[x,k](std::shared_ptr<_dfloat>t1)
		-> void{d_addf(x,x,[x,k,t1](std::shared_ptr<_dfloat>t0)
			-> void{d_addf(t1,t0,k);});});
}


namespace py = pybind11;


PYBIND11_MODULE(nested_funcs, m) {
    py::class_<_dfloat, std::shared_ptr<_dfloat>>(m, "_dfloat")
        .def(py::init<>())
        .def_readwrite("val", &_dfloat::val)
        .def_readwrite("dval", &_dfloat::dval);

    m.def("make__dfloat", &make__dfloat,
          py::arg("val"), py::arg("dval"),
          "Create a _dfloat with specified value and derivative.");

    m.def("make__const__dfloat", &make__const__dfloat,
          py::arg("val"),
          "Create a constant _dfloat (zero derivative).");

    m.def("d_func", &d_func,py::arg("x"),py::arg("k"));
}
