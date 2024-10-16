#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "memory_utils.h"

// Callback function to write response data into memory
size_t WriteMemoryCallback(void *contents, size_t size, size_t nmemb, MemoryStruct *mem) {
    size_t realsize = size * nmemb;
    char *ptr = realloc(mem->memory, mem->size + realsize + 1);

    if (!ptr) {
        fprintf(stderr, "Memory allocation failed\n");
        return 0; // Indicate failure
    }

    mem->memory = ptr;
    memcpy(&(mem->memory[mem->size]), contents, realsize);
    mem->size += realsize;
    mem->memory[mem->size] = '\0'; // Null-terminate

    return realsize;
}

// Helper function to initialize the memory structure
MemoryStruct *init_memory() {
    MemoryStruct *mem = malloc(sizeof(MemoryStruct));
    if (!mem) {
        fprintf(stderr, "Memory allocation for MemoryStruct failed\n");
        return NULL;
    }
    mem->memory = malloc(1); // Initial allocation
    mem->size = 0;
    return mem;
}

// Function to free the memory structure
void free_memory(MemoryStruct *mem) {
    free(mem->memory);
    free(mem);
}
