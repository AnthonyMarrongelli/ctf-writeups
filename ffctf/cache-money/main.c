#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define CHUNK_SIZE 0x10
#define MAX_CHUNKS 10

void *chunks[MAX_CHUNKS];

void menu() {
    printf("1. Allocate chunk\n");
    printf("2. Free chunk\n");
    printf("3. Edit chunk\n");
    printf("4. View chunk\n");
    printf("5. Exit\n");
    printf("Choice: ");
}

void allocate() {
    int index;
    printf("Index (0-%d): ", MAX_CHUNKS - 1);
    scanf("%d", &index);

    if (index < 0 || index >= MAX_CHUNKS) {
        printf("Invalid index\n");
        return;
    }

    if (chunks[index] != NULL) {
        printf("Chunk already allocated\n");
        return;
    }

    chunks[index] = malloc(CHUNK_SIZE);
    if (chunks[index] == NULL) {
        printf("Failed to allocate memory\n");
        exit(1);
    }
}

void free_chunk() {
    int index;
    printf("Index (0-%d): ", MAX_CHUNKS - 1);
    scanf("%d", &index);

    if (index < 0 || index >= MAX_CHUNKS) {
        printf("Invalid index\n");
        return;
    }

    if (chunks[index] == NULL) {
        printf("Chunk already free\n");
        return;
    }

    free(chunks[index]);
}

void edit() {
    int index;
    printf("Index (0-%d): ", MAX_CHUNKS - 1);
    scanf("%d", &index);

    if (index < 0 || index >= MAX_CHUNKS) {
        printf("Invalid index\n");
        return;
    }

    if (chunks[index] == NULL) {
        printf("Invalid chunk\n");
        return;
    }

    printf("Enter data: ");
    char input[CHUNK_SIZE];
    scanf("%16s", input);

    strncpy(chunks[index], input, CHUNK_SIZE - 1);
}

void view() {
    int index;
    printf("Index (0-%d): ", MAX_CHUNKS - 1);
    scanf("%d", &index);

    if (index < 0 || index >= MAX_CHUNKS) {
        printf("Invalid index\n");
        return;
    }

    if (chunks[index] == NULL) {
        printf("Invalid chunk\n");
        return;
    }

    printf("%s\n", (char *)chunks[index]);
}

int main() {
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);

    int choice;
    memset(chunks, 0, sizeof(chunks));

    while (1) {
        menu();
        scanf("%d", &choice);

        switch (choice) {
            case 1:
                allocate();
                break;
            case 2:
                free_chunk();
                break;
            case 3:
                edit();
                break;
            case 4:
                view();
                break;
            case 5:
                printf("Exiting...\n");
                exit(0);
            default:
                printf("Invalid choice\n");
        }
    }

    return 0;
}

