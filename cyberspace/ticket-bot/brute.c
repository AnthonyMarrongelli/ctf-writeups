#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[]) {
    if (argc != 2) {
        fprintf(stderr, "Usage: %s <target_value>\n", argv[0]);
        return 1;
    }

    int target_value = atoi(argv[1]);
    int seed;

    for (seed = 1; seed <= 10000000; seed++) {  // Iterate over the range 1 to 10,000,000
        srand(seed);  // Seed the random number generator
        int first_value = rand();  // Generate the first random value
        int second_value = rand();  // Generate the second random value

        if (second_value == target_value) {
            printf("%d\n", first_value);
            return 0;  // Exit after finding the correct seed
        }
    }

    // If no seed was found, return a non-zero exit code
    return 1;
}