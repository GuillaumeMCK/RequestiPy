#ifndef HTTP_CLIENT_H
#define HTTP_CLIENT_H

#include <Python.h>


// Function prototypes
int fetch(const char *method, const char *url, const char *const headers[], const char *body, long *http_code, char **response_body);
PyObject *py_fetch(PyObject *self, PyObject *args);

#endif // HTTP_CLIENT_H
