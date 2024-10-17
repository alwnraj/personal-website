---
title: Simple calculator in C and Assembly.
categories: [web, resources]
date: 09-13-2024
draft: false
---
## Simple calculator in C and Assembly

---------------------------------------------------------------------------

#### This is the C code for the 'frontend', should be under 'main.c'

```C
#include <stdio.h>

// Declaring the external Assembly functions
extern int add(int a, int b);
extern int subtract(int a, int b);
extern int multiply(int a, int b);
extern int divide(int a, int b);

int main() {
    int choice, a, b, result, remainder, quotient;

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
        
        else if (choice > 5) {
   printf("Invalid choice, choose between 1 and 5\n");
   break;
  };

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
                quotient = divide(a, b);
                //I moved the value from r0 directly to  the 'remainder' variable
                asm("mov %0, r1" : "=r"(remainder)); 
                printf("Result:\n", result);
                printf("Quotient: %d, Remainder: %d\n", quotient, remainder);                
            }
            break;
  };
    
    printf("\n");
    return 0;
} 

}

```

#### This is Assembly code and be filled under 'operations.s'

``` assembly

.section .text
    .global add
add:
    ADD r0, r0, r1      // r0 = r0 + r1
    bx lr               // Return

.section .text
    .global subtract
subtract:
    SUB r0, r0, r1      // r0 = r0 - r1
    bx lr               // Return

.section .text
    .global multiply
multiply:
    MUL r0, r0, r1      // r0 = r0 * r1
    bx lr               // Return

.section .text
    .global divide
divide:
    push {r4, r5, r6, lr}   // Save registers
    mov r4, r0              // r4 = dividend
    mov r5, r1              // r5 = divisor
    

    // Initialize quotient and remainder as zero
    mov r0, #0              // r0 = quotient
    mov r1, #0              // r1 = remainder
    mov r3, #0              // r3 = controls the sign flags

    // Handle negative dividend
    cmp r4, #0    // Compare divident with zero
    bge dividend_positive   // If dividend is greater than or equal to
       // zero then skip
    neg r4, r4              // Make dividend positive
    add r3, r3, #1          // Increment the sign flag

dividend_positive:
    // Handle negative divisor
    cmp r5, #0    // Compare divisor by zero
    bge divisor_positive    // If divisor is greater than or equal to
       // zero then skip
    neg r5, r5              // Make divisor positive
    add r3, r3, #1          // Toggle the sign flag

divisor_positive:
    // Perform division by repeated subtraction
division_loop:
    cmp r4, r5              // Compare dividend and divisor
    blt division_done       // If dividend is less than divisor,branch  
       // to division_done 
    sub r4, r4, r5          // Subtract divisor from dividend
    add r0, r0, #1          // Increment quotient
    b division_loop         // Repeat loop

division_done:
    mov r1, r4              // r1 is the remaining dividend

    // Applies correct sign to the quotient by checking if num is even 
    //or odd. Even is positive and odd is negative.
    ands r6, r3, #1         // Check if sign flag is odd
    beq result_positive     // If even, quotient is positive
    neg r0, r0              // Make the quotient negative

result_positive:
    pop {r4, r5, r6, lr}    // Restore registers
    bx lr                   // Return quotient in r0 and remainder in r1


```
