// http_client.c
#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <curl/curl.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "http_client.h"
#include "memory_utils.h"
#include "http_request.h" // Ensure this is included for fetch and convert_headers

// Python interface function
PyObject *py_fetch(PyObject *self, PyObject *args) {
    const char *method, *url, *body = NULL;
    PyObject *headers_list;
    const char **headers = NULL;
    long http_code;
    char *response_body = NULL;

    // Parse Python arguments
    if (!PyArg_ParseTuple(args, "ss|Os", &method, &url, &headers_list, &body)) {
        return NULL;
    }

    // Convert Python list to C array
    headers = convert_headers(headers_list); // Now this should be correctly declared
    if (!headers) {
        return NULL; // Allocation failure
    }

    // Perform the fetch
    if (fetch(method, url, headers, body, &http_code, &response_body) != 0) {
        free(headers);
        return NULL; // Indicate error
    }

    // Build and return the response and HTTP status code as a tuple
    PyObject *result = PyTuple_Pack(2, PyUnicode_FromString(response_body), PyLong_FromLong(http_code));

    free(headers); // Free headers array
    free(response_body); // Free the response body

    return result; // Return response body and HTTP code
}

// Method definitions for the module
static PyMethodDef HttpClientMethods[] = {
    {"fetch", py_fetch, METH_VARARGS, "Perform an HTTP request and return the response body and HTTP response code."},
    {NULL, NULL, 0, NULL} // Sentinel
};

// Module definition
static struct PyModuleDef httpclientmodule = {
    PyModuleDef_HEAD_INIT,
    "http_client", // Module name
    NULL, // Module documentation (can be NULL)
    -1, // Size of per-interpreter state (-1 means global state)
    HttpClientMethods // Method definitions
};

// Module initialization
PyMODINIT_FUNC PyInit_http_client(void) {
    return PyModule_Create(&httpclientmodule);
}
