---
title: Simple calculator in C and Assembly.
categories: [web, resources]
date: 09-05-2024
draft: false
---
## Simple calculator in C and Assembly


This is the C code for the fronted, should be under 'main.c'
```C
#include <stdio.h>

// Declaring the external Assembly functions
extern int add(int a, int b);
extern int subtract(int a, int b);
extern int multiply(int a, int b);
extern int divide(int a, int b);

int main() {
    int choice, a, b, result;

    while (1) {
        // Display the menu
        printf("Calculator Menu:\n");
        printf("1. Add\n");
        printf("2. Subtract\n");
        printf("3. Multiply\n");
        printf("4. Divide\n");
        printf("5. Exit\n");
        printf("Select an option (1-5): ");
        scanf("%d", &choice);

        if (choice == 5) {
            break; // Exit the loop if the user selects 5
        }

        // Ask for input numbers
        printf("Enter 1st integer: ");
        scanf("%d", &a);
        printf("Enter 2nd integer: ");
        scanf("%d", &b);


        // Perform the chosen operation
        switch (choice) {
        case 1:
            result = add(a, b);
            printf("Result: %d\n", result);
            break;
        case 2:
            result = subtract(a, b);
            printf("Result: %d\n", result);
            break;
        case 3:
            result = multiply(a, b);
            printf("Result: %d\n", result);
            break;
        case 4:
            if (b == 0) {
                printf("Error: Division by zero is not allowed.\n");
            }
            else {
                result = divide(a, b);
                printf("Result: %d\n", result);
            }
            break;
        default:
            printf("Invalid choice. Please select between 1 and 5.\n");
        }
    }

    return 0;
}

```

This is Assembly code and be filed under 'operations.s'

``` assembly

    .section .text
    .global add
    .global subtract
    .global multiply
    .global divide

// Add Function
add:
    ADD r0, r0, r1      // r0 = r0 + r1
    BX lr               // Return

// Subtract Function
subtract:
    SUB r0, r0, r1      // r0 = r0 - r1
    BX lr               // Return

// Multiply Function
multiply:
    MUL r0, r0, r1      // r0 = r0 * r1
    BX lr               // Return

// Divide Function (with integer division)
divide:
    MOV r2, r0          // Move dividend to r2
    MOV r0, r0          // Ensure r0 holds the dividend for return
    BL __aeabi_idiv     // Call integer division routine
    BX lr               // Return

```
