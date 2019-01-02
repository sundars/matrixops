#include <stdio.h>
#include <stdlib.h>
#include <math.h>

#define CF_MAX_SIZE 16

#define MAX(m, n) \
    (m >= n ? m : n)

#define MIN(m, n) \
    (m < n ? m : n)

#define ACCURACY 0.00001

void PrintContinuedFraction(long *continuedFraction) {
    printf("Continued Fraction: [");
    for (int i=0; i<CF_MAX_SIZE; i++) {
        if (continuedFraction[i] == -1)
            printf("-, ");
        else
            if (i == 0)
                printf("%ld; ", continuedFraction[i]);
            else
                printf("%ld, ", continuedFraction[i]);
    }
    if (continuedFraction[CF_MAX_SIZE] == -1)
            printf("-]\n");
    else
        printf("%ld]\n", continuedFraction[CF_MAX_SIZE]);
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
            if (continuedFraction[i] != 0) fraction[0] += continuedFraction[i] * fraction[1];
            int gcd = GCD(fraction[0], fraction[1]);
            fraction[0] /= gcd * sign;
            fraction[1] /= gcd;
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
    PrintContinuedFraction(continuedFraction);
    return RollupContinuedFraction(continuedFraction, sign);
}

int main() {
    double decimal;
    long *fraction;

    printf("Enter decimal to convert to fraction: ");
    scanf("%lf", &decimal);

    fraction = FromDecimal(decimal);
    printf("Fraction: %ld/%ld\n", fraction[0], fraction[1]);
    free(fraction);

    return 0;
}
