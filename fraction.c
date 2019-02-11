#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <unistd.h>

#define CF_MAX_SIZE 16

#define MAX(m, n) \
    (m >= n ? m : n)

#define MIN(m, n) \
    (m < n ? m : n)

#define ACCURACY 0.00001

long factorial(n) {
    if (n == 1 || n == 0)
        return 1;

    return n*factorial(n-1);
}

double e() {
    double d = (double) 2;
    for (int i=2; i<=CF_MAX_SIZE; i++)
        d += (double) 1/(double) factorial(i);

    return d;
}

double pi() {
    double d = (double) 0;
    for (int i=0; i<=CF_MAX_SIZE; i++)
        d += (double)(factorial(4*i)*(1103+26390*i))/(double)(pow(factorial(i), 4)*pow(396,4*i));

    return (double) 9801 / (d * (double) 2 * (double) pow(2, 0.5));
}

void PrintContinuedFraction(long *continuedFraction, int sign) {
    if (sign < 0)
        printf("Continued Fraction: -[%ld", continuedFraction[0]);
    else
        printf("Continued Fraction: [%ld", continuedFraction[0]);

    for (int i=1; i<CF_MAX_SIZE; i++) {
        if (continuedFraction[i] != -1) {
            if (continuedFraction[i+1] == 1 && i+1 < CF_MAX_SIZE && continuedFraction[i+2] == -1) {
                continuedFraction[i] += 1;
                continuedFraction[i+1] = -1;
            }
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
    int lensqrt = strlen("sqrt(");
    int lencurt = strlen("curt(");

    if (strcmp(s, "pi") == 0) {
        printf("pi is irrational. So fractional form doesn't exist but here is an approximation\n");
        return (double) pi();
    }

    else if (strcmp(s, "e") == 0) {
        printf("e is irrational. So fractional form doesn't exist but here is an approximation\n");
        return (double) e();
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
        return (double) pow(e(), -1*pi()/2);
    }

    else if (strncmp(s, "sqrt(", lensqrt) == 0) {
        long n;
        sscanf(s+lensqrt, "%ld", &n);
        if (n < 0) {
            printf("No square roots of a negative number, please\n");
            exit(1);
        }
        double d = pow(n, 0.5);
        if (d - (long) d > 0)
            printf("sqrt(%ld) is irrational. So fractional form doesn't exist but here is an approximation\n", n);
        return d;
    }

    else if (strncmp(s, "curt(", lensqrt) == 0) {
        long n;
        sscanf(s+lencurt, "%ld", &n);
        if (n < 0) {
            printf("No cube roots of a negative number, please\n");
            exit(1);
        }
        double d = pow(n, ((double) 1/(double) 3));
        if (d - (long) d > 0)
            printf("cuberoot(%ld) is irrational. So fractional form doesn't exist but here is an approximation\n", n);
        return d;
    }

    else {
        int pipe1[2];
        int pipe2[2];
        pipe(pipe1);
        pipe(pipe2);

        pid_t parent = getpid();
        pid_t child = fork();
        if (child == -1) {
            printf("Something went wrong...exiting\n");
            exit(-1);
        }
        else if (child > 0) {
            // parent
            close(pipe1[0]);
            close(pipe2[1]);

            char _s[strlen(s)+2];
            sprintf(_s, "%s\n", s);
            write(pipe1[1], _s, sizeof(_s)-1);

            char result[256];
            read(pipe2[0], result, sizeof(result));

            close(pipe1[1]);
            close(pipe2[0]);

            int status;
            waitpid(child, &status, 0);

            double d;
            sscanf(result, "%lf", &d);
            return d;
        }
        else {
            close(pipe1[1]);
            close(pipe2[0]);
            dup2(pipe1[0], 0);
            dup2(pipe2[1], 1);
            close(pipe1[0]);
            close(pipe2[1]);

            execlp("bc", "bc", "-l", NULL);
            exit(-1);
        }
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
