
#include <functional>
        
typedef struct {
	float val;
	float dval;
} _dfloat;

void func(float x, float y);
void d_func(_dfloat& x, _dfloat& y, const std::function<void(_dfloat&)>& k);
_dfloat make__dfloat(float val, float dval);
float addf(float x, float y);
void d_addf(_dfloat& x, _dfloat& y, const std::function<void(_dfloat&)>& k);
float subf(float x, float y);
void d_subf(_dfloat& x, _dfloat& y, const std::function<void(_dfloat&)>& k);
float mulf(float x, float y);
void d_mulf(_dfloat& x, _dfloat& y, const std::function<void(_dfloat&)>& k);
float divf(float x, float y);
void d_divf(_dfloat& x, _dfloat& y, const std::function<void(_dfloat&)>& k);

void func(float x, float y) {
	addf(mulf(x,y),divf(x,y));
}

void d_func(_dfloat& x, _dfloat& y, const std::function<void(_dfloat&)>& k) {
	d_mulf(x,y,[&x,&y,&k](_dfloat& t1)
		-> void{d_divf(x,y,[&x,&y,&k,&t1](_dfloat& t0)
			-> void{d_addf(t1,t0,k);});});
}

_dfloat make__dfloat(float val, float dval) {
	_dfloat ret;
	(ret).val = val;
	(ret).dval = dval;
	return ret;
}

float addf(float x, float y) {
	return (x) + (y);
}

void d_addf(_dfloat& x, _dfloat& y, const std::function<void(_dfloat&)>& k) {
	_dfloat ret = make__dfloat(((x).val) + ((y).val),(float)(0.0));
	k(ret);
	(x).dval = ((x).dval) + ((ret).dval);
	(y).dval = ((y).dval) + ((ret).dval);
}

float subf(float x, float y) {
	return (x) - (y);
}

void d_subf(_dfloat& x, _dfloat& y, const std::function<void(_dfloat&)>& k) {
	_dfloat ret = make__dfloat(((x).val) - ((y).val),(float)(0.0));
	k(ret);
	(x).dval = ((x).dval) + ((ret).dval);
	(y).dval = ((y).dval) + (((float)(-1.0)) * ((ret).dval));
}

float mulf(float x, float y) {
	return (x) * (y);
}

void d_mulf(_dfloat& x, _dfloat& y, const std::function<void(_dfloat&)>& k) {
	_dfloat ret = make__dfloat(((x).val) * ((y).val),(float)(0.0));
	k(ret);
	(x).dval = ((x).dval) + (((y).val) * ((ret).dval));
	(y).dval = ((y).dval) + (((x).val) * ((ret).dval));
}

float divf(float x, float y) {
	return (x) / (y);
}

void d_divf(_dfloat& x, _dfloat& y, const std::function<void(_dfloat&)>& k) {
	_dfloat ret = make__dfloat(((x).val) / ((y).val),(float)(0.0));
	k(ret);
	(x).dval = ((x).dval) + (((ret).dval) / ((y).val));
	(y).dval = ((y).dval) + (((float)(-1.0)) * ((((ret).dval) * ((x).val)) / (((y).val) * ((y).val))));
}

