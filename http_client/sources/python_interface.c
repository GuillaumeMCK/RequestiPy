#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <stdlib.h>
#include "http_client.h"

// Function to convert Python list of headers to a C array
const char **convert_headers(PyObject *headers_list) {
    if (!PyList_Check(headers_list)) {
        return NULL; // Invalid type
    }

    Py_ssize_t n = PyList_Size(headers_list);
    const char **headers = malloc((n + 1) * sizeof(char *));
    if (!headers) {
        return NULL; // Allocation failure
    }

    for (Py_ssize_t i = 0; i < n; i++) {
        PyObject *item = PyList_GetItem(headers_list, i);
        headers[i] = PyUnicode_AsUTF8(item);
        if (!headers[i]) {
            free(headers);
            return NULL; // Failed to convert header
        }
    }
    headers[n] = NULL; // Null-terminate the array
    return headers;
}
