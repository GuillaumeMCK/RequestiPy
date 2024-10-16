#ifndef MEMORY_UTILS_H
#define MEMORY_UTILS_H

#include <stddef.h>

// Structure to hold the response memory
typedef struct {
    char *memory;
    size_t size;
} MemoryStruct;

// Function prototypes
size_t WriteMemoryCallback(void *contents, size_t size, size_t nmemb, MemoryStruct *mem);
MemoryStruct *init_memory();
void free_memory(MemoryStruct *mem);

#endif // MEMORY_UTILS_H
