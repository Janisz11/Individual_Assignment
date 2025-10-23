#ifndef MATRIX_H
#define MATRIX_H

double** allocate_matrix(int size);
void initialize_matrix(double** matrix, int size);
void matrix_multiply(double** A, double** B, double** C, int size);
void free_matrix(double** matrix, int size);

#endif