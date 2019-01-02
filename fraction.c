#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>

#define CF_MAX_SIZE 16

#define MAX(m, n) \
    (m >= n ? m : n)

#define MIN(m, n) \
    (m < n ? m : n)

#define ACCURACY 0.00001

void PrintContinuedFraction(long *continuedFraction, int sign) {
    if (sign < 0)
        printf("Continued Fraction: -[%ld", continuedFraction[0]);
    else
        printf("Continued Fraction: [%ld", continuedFraction[0]);

    for (int i=1; i<CF_MAX_SIZE; i++) {
        if (continuedFraction[i] != -1) {
            if (i == 1)
                printf("; %ld", continuedFraction[i]);
            else
                printf(", %ld", continuedFraction[i]);
        }
    }
    if (continuedFraction[CF_MAX_SIZE] == -1)
            printf("]\n");
    else
        printf(", %ld, ...(truncated)]\n", continuedFraction[CF_MAX_SIZE]);
}

long GCD(long m, long n) {
    if (MAX(m, n) % MIN(m, n) == 0) return MIN(m, n);
    return GCD(MIN(m, n), MAX(m, n) % MIN(m, n));
}

long* GenerateContinuedFraction(double decimal) {
    long *continuedFraction = (long *) malloc(sizeof(long) * CF_MAX_SIZE+1);
    for (int i=0; i<=CF_MAX_SIZE; i++) {
        continuedFraction[i] = (long) -1;
    }

    long whole = (long) decimal;
    double remaining = (double) decimal - (double) whole;
    continuedFraction[0] = whole;

    int loop=0;
    while (remaining > ACCURACY && loop<CF_MAX_SIZE) {
        loop++;
        double reciprocal = (double) 1/ (double) remaining;
        whole = (long) reciprocal;
        remaining = (double) reciprocal - (double) whole;
        continuedFraction[loop] = whole;
    }

    return continuedFraction;
}

long* RollupContinuedFraction(long *continuedFraction, int sign) {
    long *fraction = (long *) malloc(sizeof(long) * 2);
    fraction[0] = 0;
    fraction[1] = 1;
    int first = 1;

    for (int i=CF_MAX_SIZE; i>=0; i--) {
        if (continuedFraction[i] == -1) continue;

        if (i == 0) {
            if (continuedFraction[i] != 0) {
                fraction[0] += continuedFraction[i] * fraction[1];
                int gcd = GCD(fraction[0], fraction[1]);
                fraction[0] /= gcd;
                fraction[1] /= gcd;
            }
            fraction[0] *= sign;
            free(continuedFraction);
            return fraction;
        }

        if (first) {
            first = 0;
            fraction[0] = 1;
            fraction[1] = continuedFraction[i];
        } else {
            long nr = fraction[0] + continuedFraction[i] * fraction[1];
            fraction[0] = fraction[1];
            fraction[1] = nr;
            int gcd = GCD(fraction[0], fraction[1]);
            fraction[0] /= gcd;
            fraction[1] /= gcd;
        }
    }

    free(continuedFraction);
    return fraction;
}

long* FromDecimal(double d) {
    int sign = 1;
    if (d < 0) sign = -1;
    long *continuedFraction = GenerateContinuedFraction(d * (double) sign);
    PrintContinuedFraction(continuedFraction, sign);
    return RollupContinuedFraction(continuedFraction, sign);
}

double ConvertToDecimal(char *s) {
    int lensqrt = strlen("sqrt");
    int lencurt = strlen("curt");

    if (strcmp(s, "pi") == 0) {
        printf("pi is irrational. So fractional form doesn't exist but here is an approximation\n");
        return (double) M_PI;
    }

    else if (strcmp(s, "e") == 0) {
        printf("e is irrational. So fractional form doesn't exist but here is an approximation\n");
        return (double) exp(1);
    }

    else if (strcmp(s, "golden") == 0) {
        printf("The golden ratio is irrational. So fractional form doesn't exist but here is an approximation\n");
        return (double) (1+pow(5,0.5))/2;
    }

    else if (strcmp(s, "golden ratio") == 0) {
        printf("The golden ratio is irrational. So fractional form doesn't exist but here is an approximation\n");
        return (double) (1+pow(5,0.5))/2;
    }

    else if (strcmp(s, "golden_ratio") == 0) {
        printf("The golden ratio is irrational. So fractional form doesn't exist but here is an approximation\n");
        return (double) (1+pow(5,0.5))/2;
    }

    else if (strcmp(s, "gr") == 0) {
        printf("The golden ratio is irrational. So fractional form doesn't exist but here is an approximation\n");
        return (double) (1+pow(5,0.5))/2;
    }

    else if (strcmp(s, "phi") == 0) {
        printf("The golden ratio is irrational. So fractional form doesn't exist but here is an approximation\n");
        return (double) (1+pow(5,0.5))/2;
    }

    else if (strcmp(s, "little golden") == 0) {
        printf("The little golden ratio is irrational. So fractional form doesn't exist but here is an approximation\n");
        return (double) (1-pow(5,0.5))/2;
    }

    else if (strcmp(s, "little golden ratio") == 0) {
        printf("The little golden ratio is irrational. So fractional form doesn't exist but here is an approximation\n");
        return (double) (1-pow(5,0.5))/2;
    }

    else if (strcmp(s, "little golden_ratio") == 0) {
        printf("The little golden ratio is irrational. So fractional form doesn't exist but here is an approximation\n");
        return (double) (1-pow(5,0.5))/2;
    }

    else if (strcmp(s, "lgr") == 0) {
        printf("The little golden ratio is irrational. So fractional form doesn't exist but here is an approximation\n");
        return (double) (1-pow(5,0.5))/2;
    }

    else if (strcmp(s, "little phi") == 0) {
        printf("The little golden ratio is irrational. So fractional form doesn't exist but here is an approximation\n");
        return (double) (1-pow(5,0.5))/2;
    }

    else if (strcmp(s, "i^i") == 0) {
        printf("Yeah, i^i is real but irrational. So fractional form doesn't exist but here is an approximation\n");
        return (double) pow(exp(1), -1*M_PI/2);
    }

    else if (strncmp(s, "sqrt", lensqrt) == 0) {
        long n;
        sscanf(s+lensqrt, "%ld", &n);
        double d = pow(n, 0.5);
        if (d - (long) d > 0)
            printf("sqrt(%ld) is irrational. So fractional form doesn't exist but here is an approximation\n", n);
        return d;
    }

    else if (strncmp(s, "curt", lensqrt) == 0) {
        long n;
        sscanf(s+lencurt, "%ld", &n);
        double d = pow(n, ((double) 1/(double) 3));
        if (d - (long) d > 0)
            printf("cuberoot(%ld) is irrational. So fractional form doesn't exist but here is an approximation\n", n);
        return d;
    }

    else {
        double d;
        sscanf(s, "%lf", &d);
        return d;
    }
}

int main() {
    char dStr[256];
    double decimal;
    long *fraction;

    printf("Enter decimal to convert to fraction: ");
    scanf("%s", dStr);
    decimal = ConvertToDecimal(dStr);
    fraction = FromDecimal(decimal);
    printf("Fraction: %ld/%ld\n", fraction[0], fraction[1]);
    free(fraction);

    return 0;
}
