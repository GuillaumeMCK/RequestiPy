#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <curl/curl.h>
#include "http_client.h"
#include "memory_utils.h"

// Function to perform an HTTP request (returns both response body and HTTP status code)
int fetch(const char *method, const char *url, const char *const headers[], const char *body, long *http_code, char **response_body) {
    CURL *curl = curl_easy_init();
    if (!curl) {
        fprintf(stderr, "Failed to initialize libcurl\n");
        return 1;
    }

    MemoryStruct *chunk = init_memory();
    if (!chunk) {
        curl_easy_cleanup(curl);
        return 1;
    }

    struct curl_slist *chunk_headers = NULL;
    if (headers) {
        for (int i = 0; headers[i]; i++) {
            chunk_headers = curl_slist_append(chunk_headers, headers[i]);
        }
    }

    curl_easy_setopt(curl, CURLOPT_URL, url);
    curl_easy_setopt(curl, CURLOPT_HTTPHEADER, chunk_headers);
    curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, WriteMemoryCallback);
    curl_easy_setopt(curl, CURLOPT_WRITEDATA, (void *)chunk);

    // Set request method
    if (strcmp(method, "POST") == 0) {
        curl_easy_setopt(curl, CURLOPT_POST, 1L);
    } else if (strcmp(method, "GET") == 0) {
        curl_easy_setopt(curl, CURLOPT_HTTPGET, 1L);
    } else {
        curl_easy_setopt(curl, CURLOPT_CUSTOMREQUEST, method);
    }

    if (body && body[0]) {
        curl_easy_setopt(curl, CURLOPT_POSTFIELDS, body);
    }

    // Perform the request
    CURLcode res = curl_easy_perform(curl);
    if (res != CURLE_OK) {
        fprintf(stderr, "HTTP request failed: %s\n", curl_easy_strerror(res));
        free_memory(chunk);
        curl_easy_cleanup(curl);
        curl_slist_free_all(chunk_headers);
        return 1;
    }

    // Get the HTTP response code
    curl_easy_getinfo(curl, CURLINFO_RESPONSE_CODE, http_code);

    // Copy the response body
    *response_body = strdup(chunk->memory);

    // Clean up
    free_memory(chunk);
    curl_easy_cleanup(curl);
    curl_slist_free_all(chunk_headers);

    return 0; // Success
}
