#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#ifdef _WIN32
  #include <windows.h>
  #include <psapi.h>
#else
  #include <sys/resource.h>
  #include <unistd.h>
  #include <time.h>
#endif

#include "matrix.h"


static double get_memory_usage_mb(void) {
#ifdef _WIN32
    PROCESS_MEMORY_COUNTERS_EX pmc;
    if (GetProcessMemoryInfo(GetCurrentProcess(), (PROCESS_MEMORY_COUNTERS*)&pmc, sizeof(pmc))) {
        return pmc.WorkingSetSize / (1024.0 * 1024.0);
    }
    return 0.0;
#else
    struct rusage usage;
    if (getrusage(RUSAGE_SELF, &usage) == 0) {
      #if defined(__APPLE__)
        return usage.ru_maxrss / (1024.0 * 1024.0);
      #else
        return usage.ru_maxrss / 1024.0; /* kB -> MB on Linux */
      #endif
    }
    return 0.0;
#endif
}

#ifdef __linux__

static void run_with_perf(int size, int rounds) {
    char cmd[512];
    
    snprintf(cmd, sizeof(cmd),
             "perf stat -e task-clock,cycles,instructions,cache-misses "
             "./matrix_bench %d %d 2> perf_output.txt",
             size, rounds);

    int ret = system(cmd);
    if (ret != 0) {
        fprintf(stderr, "Failed to run perf.\n");
        exit(1);
    }

    FILE *f = fopen("perf_output.txt", "r");
    if (!f) {
        perror("perf_output.txt");
        exit(1);
    }

    double seconds = 0.0;
    char line[512];
    while (fgets(line, sizeof(line), f)) {
        if (strstr(line, "task-clock")) {
           
            double ms = atof(line);
            seconds = ms / 1000.0;
            break;
        }
    }
    fclose(f);

    double mem_mb = get_memory_usage_mb();
    printf("%.6f %.2f\n", seconds, mem_mb);
}
#endif

int main(int argc, char *argv[]) {
    if (argc != 3) {
        fprintf(stderr, "Usage: %s <matrix_size> <rounds>\n", argv[0]);
        return 1;
    }
    int size   = atoi(argv[1]);
    int rounds = atoi(argv[2]);
    if (size <= 0 || rounds <= 0) {
        fprintf(stderr, "Size and rounds must be positive integers\n");
        return 1;
    }

#ifdef __linux__
    
    if (getenv("UNDER_PERF") == NULL) {
        setenv("UNDER_PERF", "1", 1);
        run_with_perf(size, rounds);
        return 0;
    }
   
#else
  
    LARGE_INTEGER freq, t0, t1;
    QueryPerformanceFrequency(&freq);
#endif

    
    double **A = allocate_matrix(size);
    double **B = allocate_matrix(size);
    double **C = allocate_matrix(size);
    initialize_matrix(A, size);
    initialize_matrix(B, size);

#ifndef __linux__
    double total_sec = 0.0;
#endif

    for (int r = 0; r < rounds; ++r) {
#ifdef __linux__
       
        matrix_multiply(A, B, C, size);
#else
        QueryPerformanceCounter(&t0);
        matrix_multiply(A, B, C, size);
        QueryPerformanceCounter(&t1);
        total_sec += (double)(t1.QuadPart - t0.QuadPart) / (double)freq.QuadPart;
#endif
    }

    free_matrix(A, size);
    free_matrix(B, size);
    free_matrix(C, size);

#ifndef __linux__
    
    double avg_time = total_sec / (double)rounds;
    double mem_mb   = get_memory_usage_mb();
    printf("%.6f %.2f\n", avg_time, mem_mb);
#endif

    return 0;
}
