
#include <functional>
#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <memory>
        
typedef struct {
	double val;
	double dval;
} _dfloat;

double plussquare(double x, double y);
double poly(double x, double y, double z);
void d_poly(std::shared_ptr<_dfloat> x, std::shared_ptr<_dfloat> y, std::shared_ptr<_dfloat> z, const std::function<void(std::shared_ptr<_dfloat>)>& k);
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
void d_plussquare(std::shared_ptr<_dfloat> x, std::shared_ptr<_dfloat> y, const std::function<void(std::shared_ptr<_dfloat>)>& k);

double plussquare(double x, double y) {
	return mulf(addf(x,y),addf(x,y));
}

double poly(double x, double y, double z) {
	return addf(plussquare(x,y),plussquare(y,z));
}

void d_poly(std::shared_ptr<_dfloat> x, std::shared_ptr<_dfloat> y, std::shared_ptr<_dfloat> z, const std::function<void(std::shared_ptr<_dfloat>)>& k) {
	d_plussquare(x,y,[x,y,z,k](std::shared_ptr<_dfloat>t1)
		-> void{d_plussquare(y,z,[x,y,z,k,t1](std::shared_ptr<_dfloat>t0)
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

void d_plussquare(std::shared_ptr<_dfloat> x, std::shared_ptr<_dfloat> y, const std::function<void(std::shared_ptr<_dfloat>)>& k) {
	d_addf(x,y,[x,y,k](std::shared_ptr<_dfloat>t1)
		-> void{d_addf(x,y,[x,y,k,t1](std::shared_ptr<_dfloat>t0)
			-> void{d_mulf(t1,t0,k);});});
}


namespace py = pybind11;


PYBIND11_MODULE(polynomial, m) {
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

    m.def("plussquare", &plussquare,py::arg("x"),py::arg("y"));
    m.def("poly", &poly,py::arg("x"),py::arg("y"),py::arg("z"));
    m.def("d_poly", &d_poly,py::arg("x"),py::arg("y"),py::arg("z"),py::arg("k"));
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
    m.def("d_plussquare", &d_plussquare,py::arg("x"),py::arg("y"),py::arg("k"));
}
