
#include <functional>
#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <memory>
#include <stdbool.h>
        
typedef struct {
	double val;
	double dval;
} _dfloat;

double square(double x);
double relu(double x);
double hidden_layer_helper(double input, double w_in, double b_in);
double output_layer_helper(double w1, double t1, double w2, double t2, double w3, double t3, double w4, double t4);
double output_layer(double w_out_1, double temp_in_1, double w_out_2, double temp_in_2, double w_out_3, double temp_in_3, double w_out_4, double temp_in_4, double w_out_5, double temp_in_5, double w_out_6, double temp_in_6, double w_out_7, double temp_in_7, double w_out_8, double temp_in_8, double b_out);
double model(double input, double w_in_1, double w_in_2, double w_in_3, double w_in_4, double w_in_5, double w_in_6, double w_in_7, double w_in_8, double b_in_1, double b_in_2, double b_in_3, double b_in_4, double b_in_5, double b_in_6, double b_in_7, double b_in_8, double w_out_1, double w_out_2, double w_out_3, double w_out_4, double w_out_5, double w_out_6, double w_out_7, double w_out_8, double b_out);
double loss(double input, double w_in_1, double w_in_2, double w_in_3, double w_in_4, double w_in_5, double w_in_6, double w_in_7, double w_in_8, double b_in_1, double b_in_2, double b_in_3, double b_in_4, double b_in_5, double b_in_6, double b_in_7, double b_in_8, double w_out_1, double w_out_2, double w_out_3, double w_out_4, double w_out_5, double w_out_6, double w_out_7, double w_out_8, double b_out, double target);
void d_loss(std::shared_ptr<_dfloat> input, std::shared_ptr<_dfloat> w_in_1, std::shared_ptr<_dfloat> w_in_2, std::shared_ptr<_dfloat> w_in_3, std::shared_ptr<_dfloat> w_in_4, std::shared_ptr<_dfloat> w_in_5, std::shared_ptr<_dfloat> w_in_6, std::shared_ptr<_dfloat> w_in_7, std::shared_ptr<_dfloat> w_in_8, std::shared_ptr<_dfloat> b_in_1, std::shared_ptr<_dfloat> b_in_2, std::shared_ptr<_dfloat> b_in_3, std::shared_ptr<_dfloat> b_in_4, std::shared_ptr<_dfloat> b_in_5, std::shared_ptr<_dfloat> b_in_6, std::shared_ptr<_dfloat> b_in_7, std::shared_ptr<_dfloat> b_in_8, std::shared_ptr<_dfloat> w_out_1, std::shared_ptr<_dfloat> w_out_2, std::shared_ptr<_dfloat> w_out_3, std::shared_ptr<_dfloat> w_out_4, std::shared_ptr<_dfloat> w_out_5, std::shared_ptr<_dfloat> w_out_6, std::shared_ptr<_dfloat> w_out_7, std::shared_ptr<_dfloat> w_out_8, std::shared_ptr<_dfloat> b_out, std::shared_ptr<_dfloat> target, const std::function<void(std::shared_ptr<_dfloat>)>& k);
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
void d_model(std::shared_ptr<_dfloat> input, std::shared_ptr<_dfloat> w_in_1, std::shared_ptr<_dfloat> w_in_2, std::shared_ptr<_dfloat> w_in_3, std::shared_ptr<_dfloat> w_in_4, std::shared_ptr<_dfloat> w_in_5, std::shared_ptr<_dfloat> w_in_6, std::shared_ptr<_dfloat> w_in_7, std::shared_ptr<_dfloat> w_in_8, std::shared_ptr<_dfloat> b_in_1, std::shared_ptr<_dfloat> b_in_2, std::shared_ptr<_dfloat> b_in_3, std::shared_ptr<_dfloat> b_in_4, std::shared_ptr<_dfloat> b_in_5, std::shared_ptr<_dfloat> b_in_6, std::shared_ptr<_dfloat> b_in_7, std::shared_ptr<_dfloat> b_in_8, std::shared_ptr<_dfloat> w_out_1, std::shared_ptr<_dfloat> w_out_2, std::shared_ptr<_dfloat> w_out_3, std::shared_ptr<_dfloat> w_out_4, std::shared_ptr<_dfloat> w_out_5, std::shared_ptr<_dfloat> w_out_6, std::shared_ptr<_dfloat> w_out_7, std::shared_ptr<_dfloat> w_out_8, std::shared_ptr<_dfloat> b_out, const std::function<void(std::shared_ptr<_dfloat>)>& k);
void d_output_layer(std::shared_ptr<_dfloat> w_out_1, std::shared_ptr<_dfloat> temp_in_1, std::shared_ptr<_dfloat> w_out_2, std::shared_ptr<_dfloat> temp_in_2, std::shared_ptr<_dfloat> w_out_3, std::shared_ptr<_dfloat> temp_in_3, std::shared_ptr<_dfloat> w_out_4, std::shared_ptr<_dfloat> temp_in_4, std::shared_ptr<_dfloat> w_out_5, std::shared_ptr<_dfloat> temp_in_5, std::shared_ptr<_dfloat> w_out_6, std::shared_ptr<_dfloat> temp_in_6, std::shared_ptr<_dfloat> w_out_7, std::shared_ptr<_dfloat> temp_in_7, std::shared_ptr<_dfloat> w_out_8, std::shared_ptr<_dfloat> temp_in_8, std::shared_ptr<_dfloat> b_out, const std::function<void(std::shared_ptr<_dfloat>)>& k);
void d_output_layer_helper(std::shared_ptr<_dfloat> w1, std::shared_ptr<_dfloat> t1, std::shared_ptr<_dfloat> w2, std::shared_ptr<_dfloat> t2, std::shared_ptr<_dfloat> w3, std::shared_ptr<_dfloat> t3, std::shared_ptr<_dfloat> w4, std::shared_ptr<_dfloat> t4, const std::function<void(std::shared_ptr<_dfloat>)>& k);
void d_hidden_layer_helper(std::shared_ptr<_dfloat> input, std::shared_ptr<_dfloat> w_in, std::shared_ptr<_dfloat> b_in, const std::function<void(std::shared_ptr<_dfloat>)>& k);
void d_relu(std::shared_ptr<_dfloat> x, const std::function<void(std::shared_ptr<_dfloat>)>& k);
void d_square(std::shared_ptr<_dfloat> x, const std::function<void(std::shared_ptr<_dfloat>)>& k);

double square(double x) {
	return mulf(x,x);
}

double relu(double x) {
	return ifelsef(greaterf(x,(float)(0.0)),x,(float)(0.0));
}

double hidden_layer_helper(double input, double w_in, double b_in) {
	return relu(addf(mulf(input,w_in),b_in));
}

double output_layer_helper(double w1, double t1, double w2, double t2, double w3, double t3, double w4, double t4) {
	return addf(addf(mulf(w1,t1),mulf(w2,t2)),addf(mulf(w3,t3),mulf(w4,t4)));
}

double output_layer(double w_out_1, double temp_in_1, double w_out_2, double temp_in_2, double w_out_3, double temp_in_3, double w_out_4, double temp_in_4, double w_out_5, double temp_in_5, double w_out_6, double temp_in_6, double w_out_7, double temp_in_7, double w_out_8, double temp_in_8, double b_out) {
	return addf(addf(output_layer_helper(w_out_1,temp_in_1,w_out_2,temp_in_2,w_out_3,temp_in_3,w_out_4,temp_in_4),output_layer_helper(w_out_5,temp_in_5,w_out_6,temp_in_6,w_out_7,temp_in_7,w_out_8,temp_in_8)),b_out);
}

double model(double input, double w_in_1, double w_in_2, double w_in_3, double w_in_4, double w_in_5, double w_in_6, double w_in_7, double w_in_8, double b_in_1, double b_in_2, double b_in_3, double b_in_4, double b_in_5, double b_in_6, double b_in_7, double b_in_8, double w_out_1, double w_out_2, double w_out_3, double w_out_4, double w_out_5, double w_out_6, double w_out_7, double w_out_8, double b_out) {
	return output_layer(w_out_1,hidden_layer_helper(input,w_in_1,b_in_1),w_out_2,hidden_layer_helper(input,w_in_2,b_in_2),w_out_3,hidden_layer_helper(input,w_in_3,b_in_3),w_out_4,hidden_layer_helper(input,w_in_4,b_in_4),w_out_5,hidden_layer_helper(input,w_in_5,b_in_5),w_out_6,hidden_layer_helper(input,w_in_6,b_in_6),w_out_7,hidden_layer_helper(input,w_in_7,b_in_7),w_out_8,hidden_layer_helper(input,w_in_8,b_in_8),b_out);
}

double loss(double input, double w_in_1, double w_in_2, double w_in_3, double w_in_4, double w_in_5, double w_in_6, double w_in_7, double w_in_8, double b_in_1, double b_in_2, double b_in_3, double b_in_4, double b_in_5, double b_in_6, double b_in_7, double b_in_8, double w_out_1, double w_out_2, double w_out_3, double w_out_4, double w_out_5, double w_out_6, double w_out_7, double w_out_8, double b_out, double target) {
	return square(subf(model(input,w_in_1,w_in_2,w_in_3,w_in_4,w_in_5,w_in_6,w_in_7,w_in_8,b_in_1,b_in_2,b_in_3,b_in_4,b_in_5,b_in_6,b_in_7,b_in_8,w_out_1,w_out_2,w_out_3,w_out_4,w_out_5,w_out_6,w_out_7,w_out_8,b_out),target));
}

void d_loss(std::shared_ptr<_dfloat> input, std::shared_ptr<_dfloat> w_in_1, std::shared_ptr<_dfloat> w_in_2, std::shared_ptr<_dfloat> w_in_3, std::shared_ptr<_dfloat> w_in_4, std::shared_ptr<_dfloat> w_in_5, std::shared_ptr<_dfloat> w_in_6, std::shared_ptr<_dfloat> w_in_7, std::shared_ptr<_dfloat> w_in_8, std::shared_ptr<_dfloat> b_in_1, std::shared_ptr<_dfloat> b_in_2, std::shared_ptr<_dfloat> b_in_3, std::shared_ptr<_dfloat> b_in_4, std::shared_ptr<_dfloat> b_in_5, std::shared_ptr<_dfloat> b_in_6, std::shared_ptr<_dfloat> b_in_7, std::shared_ptr<_dfloat> b_in_8, std::shared_ptr<_dfloat> w_out_1, std::shared_ptr<_dfloat> w_out_2, std::shared_ptr<_dfloat> w_out_3, std::shared_ptr<_dfloat> w_out_4, std::shared_ptr<_dfloat> w_out_5, std::shared_ptr<_dfloat> w_out_6, std::shared_ptr<_dfloat> w_out_7, std::shared_ptr<_dfloat> w_out_8, std::shared_ptr<_dfloat> b_out, std::shared_ptr<_dfloat> target, const std::function<void(std::shared_ptr<_dfloat>)>& k) {
	d_model(input,w_in_1,w_in_2,w_in_3,w_in_4,w_in_5,w_in_6,w_in_7,w_in_8,b_in_1,b_in_2,b_in_3,b_in_4,b_in_5,b_in_6,b_in_7,b_in_8,w_out_1,w_out_2,w_out_3,w_out_4,w_out_5,w_out_6,w_out_7,w_out_8,b_out,[input,w_in_1,w_in_2,w_in_3,w_in_4,w_in_5,w_in_6,w_in_7,w_in_8,b_in_1,b_in_2,b_in_3,b_in_4,b_in_5,b_in_6,b_in_7,b_in_8,w_out_1,w_out_2,w_out_3,w_out_4,w_out_5,w_out_6,w_out_7,w_out_8,b_out,target,k](std::shared_ptr<_dfloat>tloss1)
		-> void{d_subf(tloss1,target,[input,w_in_1,w_in_2,w_in_3,w_in_4,w_in_5,w_in_6,w_in_7,w_in_8,b_in_1,b_in_2,b_in_3,b_in_4,b_in_5,b_in_6,b_in_7,b_in_8,w_out_1,w_out_2,w_out_3,w_out_4,w_out_5,w_out_6,w_out_7,w_out_8,b_out,target,k,tloss1](std::shared_ptr<_dfloat>tloss0)
			-> void{d_square(tloss0,k);});});
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

void d_model(std::shared_ptr<_dfloat> input, std::shared_ptr<_dfloat> w_in_1, std::shared_ptr<_dfloat> w_in_2, std::shared_ptr<_dfloat> w_in_3, std::shared_ptr<_dfloat> w_in_4, std::shared_ptr<_dfloat> w_in_5, std::shared_ptr<_dfloat> w_in_6, std::shared_ptr<_dfloat> w_in_7, std::shared_ptr<_dfloat> w_in_8, std::shared_ptr<_dfloat> b_in_1, std::shared_ptr<_dfloat> b_in_2, std::shared_ptr<_dfloat> b_in_3, std::shared_ptr<_dfloat> b_in_4, std::shared_ptr<_dfloat> b_in_5, std::shared_ptr<_dfloat> b_in_6, std::shared_ptr<_dfloat> b_in_7, std::shared_ptr<_dfloat> b_in_8, std::shared_ptr<_dfloat> w_out_1, std::shared_ptr<_dfloat> w_out_2, std::shared_ptr<_dfloat> w_out_3, std::shared_ptr<_dfloat> w_out_4, std::shared_ptr<_dfloat> w_out_5, std::shared_ptr<_dfloat> w_out_6, std::shared_ptr<_dfloat> w_out_7, std::shared_ptr<_dfloat> w_out_8, std::shared_ptr<_dfloat> b_out, const std::function<void(std::shared_ptr<_dfloat>)>& k) {
	d_hidden_layer_helper(input,w_in_1,b_in_1,[input,w_in_1,w_in_2,w_in_3,w_in_4,w_in_5,w_in_6,w_in_7,w_in_8,b_in_1,b_in_2,b_in_3,b_in_4,b_in_5,b_in_6,b_in_7,b_in_8,w_out_1,w_out_2,w_out_3,w_out_4,w_out_5,w_out_6,w_out_7,w_out_8,b_out,k](std::shared_ptr<_dfloat>tmodel7)
		-> void{d_hidden_layer_helper(input,w_in_2,b_in_2,[input,w_in_1,w_in_2,w_in_3,w_in_4,w_in_5,w_in_6,w_in_7,w_in_8,b_in_1,b_in_2,b_in_3,b_in_4,b_in_5,b_in_6,b_in_7,b_in_8,w_out_1,w_out_2,w_out_3,w_out_4,w_out_5,w_out_6,w_out_7,w_out_8,b_out,k,tmodel7](std::shared_ptr<_dfloat>tmodel6)
			-> void{d_hidden_layer_helper(input,w_in_3,b_in_3,[input,w_in_1,w_in_2,w_in_3,w_in_4,w_in_5,w_in_6,w_in_7,w_in_8,b_in_1,b_in_2,b_in_3,b_in_4,b_in_5,b_in_6,b_in_7,b_in_8,w_out_1,w_out_2,w_out_3,w_out_4,w_out_5,w_out_6,w_out_7,w_out_8,b_out,k,tmodel6,tmodel7](std::shared_ptr<_dfloat>tmodel5)
				-> void{d_hidden_layer_helper(input,w_in_4,b_in_4,[input,w_in_1,w_in_2,w_in_3,w_in_4,w_in_5,w_in_6,w_in_7,w_in_8,b_in_1,b_in_2,b_in_3,b_in_4,b_in_5,b_in_6,b_in_7,b_in_8,w_out_1,w_out_2,w_out_3,w_out_4,w_out_5,w_out_6,w_out_7,w_out_8,b_out,k,tmodel5,tmodel6,tmodel7](std::shared_ptr<_dfloat>tmodel4)
					-> void{d_hidden_layer_helper(input,w_in_5,b_in_5,[input,w_in_1,w_in_2,w_in_3,w_in_4,w_in_5,w_in_6,w_in_7,w_in_8,b_in_1,b_in_2,b_in_3,b_in_4,b_in_5,b_in_6,b_in_7,b_in_8,w_out_1,w_out_2,w_out_3,w_out_4,w_out_5,w_out_6,w_out_7,w_out_8,b_out,k,tmodel4,tmodel5,tmodel6,tmodel7](std::shared_ptr<_dfloat>tmodel3)
						-> void{d_hidden_layer_helper(input,w_in_6,b_in_6,[input,w_in_1,w_in_2,w_in_3,w_in_4,w_in_5,w_in_6,w_in_7,w_in_8,b_in_1,b_in_2,b_in_3,b_in_4,b_in_5,b_in_6,b_in_7,b_in_8,w_out_1,w_out_2,w_out_3,w_out_4,w_out_5,w_out_6,w_out_7,w_out_8,b_out,k,tmodel3,tmodel4,tmodel5,tmodel6,tmodel7](std::shared_ptr<_dfloat>tmodel2)
							-> void{d_hidden_layer_helper(input,w_in_7,b_in_7,[input,w_in_1,w_in_2,w_in_3,w_in_4,w_in_5,w_in_6,w_in_7,w_in_8,b_in_1,b_in_2,b_in_3,b_in_4,b_in_5,b_in_6,b_in_7,b_in_8,w_out_1,w_out_2,w_out_3,w_out_4,w_out_5,w_out_6,w_out_7,w_out_8,b_out,k,tmodel2,tmodel3,tmodel4,tmodel5,tmodel6,tmodel7](std::shared_ptr<_dfloat>tmodel1)
								-> void{d_hidden_layer_helper(input,w_in_8,b_in_8,[input,w_in_1,w_in_2,w_in_3,w_in_4,w_in_5,w_in_6,w_in_7,w_in_8,b_in_1,b_in_2,b_in_3,b_in_4,b_in_5,b_in_6,b_in_7,b_in_8,w_out_1,w_out_2,w_out_3,w_out_4,w_out_5,w_out_6,w_out_7,w_out_8,b_out,k,tmodel1,tmodel2,tmodel3,tmodel4,tmodel5,tmodel6,tmodel7](std::shared_ptr<_dfloat>tmodel0)
									-> void{d_output_layer(w_out_1,tmodel7,w_out_2,tmodel6,w_out_3,tmodel5,w_out_4,tmodel4,w_out_5,tmodel3,w_out_6,tmodel2,w_out_7,tmodel1,w_out_8,tmodel0,b_out,k);});});});});});});});});
}

void d_output_layer(std::shared_ptr<_dfloat> w_out_1, std::shared_ptr<_dfloat> temp_in_1, std::shared_ptr<_dfloat> w_out_2, std::shared_ptr<_dfloat> temp_in_2, std::shared_ptr<_dfloat> w_out_3, std::shared_ptr<_dfloat> temp_in_3, std::shared_ptr<_dfloat> w_out_4, std::shared_ptr<_dfloat> temp_in_4, std::shared_ptr<_dfloat> w_out_5, std::shared_ptr<_dfloat> temp_in_5, std::shared_ptr<_dfloat> w_out_6, std::shared_ptr<_dfloat> temp_in_6, std::shared_ptr<_dfloat> w_out_7, std::shared_ptr<_dfloat> temp_in_7, std::shared_ptr<_dfloat> w_out_8, std::shared_ptr<_dfloat> temp_in_8, std::shared_ptr<_dfloat> b_out, const std::function<void(std::shared_ptr<_dfloat>)>& k) {
	d_output_layer_helper(w_out_1,temp_in_1,w_out_2,temp_in_2,w_out_3,temp_in_3,w_out_4,temp_in_4,[w_out_1,temp_in_1,w_out_2,temp_in_2,w_out_3,temp_in_3,w_out_4,temp_in_4,w_out_5,temp_in_5,w_out_6,temp_in_6,w_out_7,temp_in_7,w_out_8,temp_in_8,b_out,k](std::shared_ptr<_dfloat>toutput_layer2)
		-> void{d_output_layer_helper(w_out_5,temp_in_5,w_out_6,temp_in_6,w_out_7,temp_in_7,w_out_8,temp_in_8,[w_out_1,temp_in_1,w_out_2,temp_in_2,w_out_3,temp_in_3,w_out_4,temp_in_4,w_out_5,temp_in_5,w_out_6,temp_in_6,w_out_7,temp_in_7,w_out_8,temp_in_8,b_out,k,toutput_layer2](std::shared_ptr<_dfloat>toutput_layer1)
			-> void{d_addf(toutput_layer2,toutput_layer1,[w_out_1,temp_in_1,w_out_2,temp_in_2,w_out_3,temp_in_3,w_out_4,temp_in_4,w_out_5,temp_in_5,w_out_6,temp_in_6,w_out_7,temp_in_7,w_out_8,temp_in_8,b_out,k,toutput_layer1,toutput_layer2](std::shared_ptr<_dfloat>toutput_layer0)
				-> void{d_addf(toutput_layer0,b_out,k);});});});
}

void d_output_layer_helper(std::shared_ptr<_dfloat> w1, std::shared_ptr<_dfloat> t1, std::shared_ptr<_dfloat> w2, std::shared_ptr<_dfloat> t2, std::shared_ptr<_dfloat> w3, std::shared_ptr<_dfloat> t3, std::shared_ptr<_dfloat> w4, std::shared_ptr<_dfloat> t4, const std::function<void(std::shared_ptr<_dfloat>)>& k) {
	d_mulf(w3,t3,[w1,t1,w2,t2,w3,t3,w4,t4,k](std::shared_ptr<_dfloat>toutput_layer_helper5)
		-> void{d_mulf(w4,t4,[w1,t1,w2,t2,w3,t3,w4,t4,k,toutput_layer_helper5](std::shared_ptr<_dfloat>toutput_layer_helper4)
			-> void{d_mulf(w1,t1,[w1,t1,w2,t2,w3,t3,w4,t4,k,toutput_layer_helper4,toutput_layer_helper5](std::shared_ptr<_dfloat>toutput_layer_helper3)
				-> void{d_mulf(w2,t2,[w1,t1,w2,t2,w3,t3,w4,t4,k,toutput_layer_helper3,toutput_layer_helper4,toutput_layer_helper5](std::shared_ptr<_dfloat>toutput_layer_helper2)
					-> void{d_addf(toutput_layer_helper3,toutput_layer_helper2,[w1,t1,w2,t2,w3,t3,w4,t4,k,toutput_layer_helper2,toutput_layer_helper3,toutput_layer_helper4,toutput_layer_helper5](std::shared_ptr<_dfloat>toutput_layer_helper1)
						-> void{d_addf(toutput_layer_helper5,toutput_layer_helper4,[w1,t1,w2,t2,w3,t3,w4,t4,k,toutput_layer_helper1,toutput_layer_helper2,toutput_layer_helper3,toutput_layer_helper4,toutput_layer_helper5](std::shared_ptr<_dfloat>toutput_layer_helper0)
							-> void{d_addf(toutput_layer_helper1,toutput_layer_helper0,k);});});});});});});
}

void d_hidden_layer_helper(std::shared_ptr<_dfloat> input, std::shared_ptr<_dfloat> w_in, std::shared_ptr<_dfloat> b_in, const std::function<void(std::shared_ptr<_dfloat>)>& k) {
	d_mulf(input,w_in,[input,w_in,b_in,k](std::shared_ptr<_dfloat>thidden_layer_helper1)
		-> void{d_addf(thidden_layer_helper1,b_in,[input,w_in,b_in,k,thidden_layer_helper1](std::shared_ptr<_dfloat>thidden_layer_helper0)
			-> void{d_relu(thidden_layer_helper0,k);});});
}

void d_relu(std::shared_ptr<_dfloat> x, const std::function<void(std::shared_ptr<_dfloat>)>& k) {
	d_ifelsef(d_greaterf(x,make__const__dfloat((float)(0.0))),x,make__const__dfloat((float)(0.0)),k);
}

void d_square(std::shared_ptr<_dfloat> x, const std::function<void(std::shared_ptr<_dfloat>)>& k) {
	d_mulf(x,x,k);
}


namespace py = pybind11;


PYBIND11_MODULE(mlp, m) {
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

    m.def("square", &square,py::arg("x"));
    m.def("relu", &relu,py::arg("x"));
    m.def("hidden_layer_helper", &hidden_layer_helper,py::arg("input"),py::arg("w_in"),py::arg("b_in"));
    m.def("output_layer_helper", &output_layer_helper,py::arg("w1"),py::arg("t1"),py::arg("w2"),py::arg("t2"),py::arg("w3"),py::arg("t3"),py::arg("w4"),py::arg("t4"));
    m.def("output_layer", &output_layer,py::arg("w_out_1"),py::arg("temp_in_1"),py::arg("w_out_2"),py::arg("temp_in_2"),py::arg("w_out_3"),py::arg("temp_in_3"),py::arg("w_out_4"),py::arg("temp_in_4"),py::arg("w_out_5"),py::arg("temp_in_5"),py::arg("w_out_6"),py::arg("temp_in_6"),py::arg("w_out_7"),py::arg("temp_in_7"),py::arg("w_out_8"),py::arg("temp_in_8"),py::arg("b_out"));
    m.def("model", &model,py::arg("input"),py::arg("w_in_1"),py::arg("w_in_2"),py::arg("w_in_3"),py::arg("w_in_4"),py::arg("w_in_5"),py::arg("w_in_6"),py::arg("w_in_7"),py::arg("w_in_8"),py::arg("b_in_1"),py::arg("b_in_2"),py::arg("b_in_3"),py::arg("b_in_4"),py::arg("b_in_5"),py::arg("b_in_6"),py::arg("b_in_7"),py::arg("b_in_8"),py::arg("w_out_1"),py::arg("w_out_2"),py::arg("w_out_3"),py::arg("w_out_4"),py::arg("w_out_5"),py::arg("w_out_6"),py::arg("w_out_7"),py::arg("w_out_8"),py::arg("b_out"));
    m.def("loss", &loss,py::arg("input"),py::arg("w_in_1"),py::arg("w_in_2"),py::arg("w_in_3"),py::arg("w_in_4"),py::arg("w_in_5"),py::arg("w_in_6"),py::arg("w_in_7"),py::arg("w_in_8"),py::arg("b_in_1"),py::arg("b_in_2"),py::arg("b_in_3"),py::arg("b_in_4"),py::arg("b_in_5"),py::arg("b_in_6"),py::arg("b_in_7"),py::arg("b_in_8"),py::arg("w_out_1"),py::arg("w_out_2"),py::arg("w_out_3"),py::arg("w_out_4"),py::arg("w_out_5"),py::arg("w_out_6"),py::arg("w_out_7"),py::arg("w_out_8"),py::arg("b_out"),py::arg("target"));
    m.def("d_loss", &d_loss,py::arg("input"),py::arg("w_in_1"),py::arg("w_in_2"),py::arg("w_in_3"),py::arg("w_in_4"),py::arg("w_in_5"),py::arg("w_in_6"),py::arg("w_in_7"),py::arg("w_in_8"),py::arg("b_in_1"),py::arg("b_in_2"),py::arg("b_in_3"),py::arg("b_in_4"),py::arg("b_in_5"),py::arg("b_in_6"),py::arg("b_in_7"),py::arg("b_in_8"),py::arg("w_out_1"),py::arg("w_out_2"),py::arg("w_out_3"),py::arg("w_out_4"),py::arg("w_out_5"),py::arg("w_out_6"),py::arg("w_out_7"),py::arg("w_out_8"),py::arg("b_out"),py::arg("target"),py::arg("k"));
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
    m.def("d_model", &d_model,py::arg("input"),py::arg("w_in_1"),py::arg("w_in_2"),py::arg("w_in_3"),py::arg("w_in_4"),py::arg("w_in_5"),py::arg("w_in_6"),py::arg("w_in_7"),py::arg("w_in_8"),py::arg("b_in_1"),py::arg("b_in_2"),py::arg("b_in_3"),py::arg("b_in_4"),py::arg("b_in_5"),py::arg("b_in_6"),py::arg("b_in_7"),py::arg("b_in_8"),py::arg("w_out_1"),py::arg("w_out_2"),py::arg("w_out_3"),py::arg("w_out_4"),py::arg("w_out_5"),py::arg("w_out_6"),py::arg("w_out_7"),py::arg("w_out_8"),py::arg("b_out"),py::arg("k"));
    m.def("d_output_layer", &d_output_layer,py::arg("w_out_1"),py::arg("temp_in_1"),py::arg("w_out_2"),py::arg("temp_in_2"),py::arg("w_out_3"),py::arg("temp_in_3"),py::arg("w_out_4"),py::arg("temp_in_4"),py::arg("w_out_5"),py::arg("temp_in_5"),py::arg("w_out_6"),py::arg("temp_in_6"),py::arg("w_out_7"),py::arg("temp_in_7"),py::arg("w_out_8"),py::arg("temp_in_8"),py::arg("b_out"),py::arg("k"));
    m.def("d_output_layer_helper", &d_output_layer_helper,py::arg("w1"),py::arg("t1"),py::arg("w2"),py::arg("t2"),py::arg("w3"),py::arg("t3"),py::arg("w4"),py::arg("t4"),py::arg("k"));
    m.def("d_hidden_layer_helper", &d_hidden_layer_helper,py::arg("input"),py::arg("w_in"),py::arg("b_in"),py::arg("k"));
    m.def("d_relu", &d_relu,py::arg("x"),py::arg("k"));
    m.def("d_square", &d_square,py::arg("x"),py::arg("k"));
}
