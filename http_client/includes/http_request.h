// http_request.h
#ifndef HTTP_REQUEST_H
#define HTTP_REQUEST_H

#include <stddef.h>
#include <Python.h>

// Function prototypes
int fetch(const char *method, const char *url, const char *const headers[], const char *body, long *http_code, char **response_body);
const char **convert_headers(PyObject *headers_list); // Add this line

#endif // HTTP_REQUEST_H
