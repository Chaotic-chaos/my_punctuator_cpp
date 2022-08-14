#include <pybind11/pybind11.h>

#include "src/punctuator.cc"

namespace py = pybind11;

PYBIND11_MODULE(punctuator, m){
    py::class_<Punctuator>(m, "Punctuator")
        .def(py::init<>())
        .def("setup_model", &Punctuator::setup_model)
        .def("decode", &Punctuator::decode);
}
