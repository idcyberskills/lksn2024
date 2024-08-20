#include <stdio.h>
#include <string.h>
#include <stdlib.h>
//gcc chall.c -o chall
#define MAX_PARTICIPANTS 124
#define MAX_NAME_LENGTH 64

struct Participant {
    char name[MAX_NAME_LENGTH];
    int age;
    char category[64];
};

struct Participant participants[MAX_PARTICIPANTS];
int participantCount = 0;

void init() {
    setvbuf(stdin, 0, 2, 0);
    setvbuf(stdout, 0, 2, 0);
    setvbuf(stderr, 0, 2, 0);

}

int readint(){
    char buf[0x10];
    return atoi(fgets(buf,0x10,stdin));
}

void registerParticipant() {
    if (participantCount >= MAX_PARTICIPANTS) {
        printf("Maximum number of participants reached.\n");
        return;
    }

    struct Participant newParticipant;

    printf("Enter participant name: ");
    fgets(newParticipant.name, MAX_NAME_LENGTH, stdin);
    newParticipant.name[strcspn(newParticipant.name, "\n")] = 0;
    printf("Enter participant age: ");
    newParticipant.age=readint();
    printf("Enter participant category: ");
    fgets(newParticipant.category, 64, stdin);
    newParticipant.category[strcspn(newParticipant.category, "\n")] = 0;
    participants[participantCount++] = newParticipant;
    printf("Participant registered successfully.\n");
}

void viewParticipants() {
    int index;
    printf("Enter the index of the participant to view: ");
    index=readint();

    index--; // Adjust for 0-based array indexing
    printf("Participant details:\n");
    printf("Name: ");
    printf(participants[index].name);
    puts(";");
    printf("Age: %i",participants[index].age);
    puts(";");
    printf("Category: ");
    printf(participants[index].category);
    puts(";");
}

void deleteParticipant() {
    int index;
    printf("Enter the index of the participant to delete: ");
    index = readint();

    index-- ; // Adjust for 0-based array indexing
    for (int i = index; i < participantCount - 1; i++) {
        participants[i] = participants[i + 1];
    }
    participantCount-- ;
    printf("Participant deleted successfully.\n");
}

void editParticipant() {
    int index;
    int newAge;
    printf("Enter the index of the participant to edit: ");
    index = readint();

    index-- ; // Adjust for 0-based array indexing

    printf("Enter new name (or press enter to keep current): ");
    fgets(participants[index].name, MAX_NAME_LENGTH, stdin);
    participants[index].name[strcspn(participants[index].name, "\n")] = 0;

    printf("Enter new age (or 0 to keep current): ");
    newAge = readint();
    if (newAge != 0) participants[index].age = newAge;

    printf("Enter new category (or press enter to keep current): ");
    fgets(participants[index].category, 64, stdin);
    participants[index].category[strcspn(participants[index].category, "\n")] = 0;

    printf("Participant information updated successfully.\n");
}

int main() {
    int choice;
    init();
    do {
        printf("\n--- Competition Registration System ---\n");
        printf("1. Register Participant\n");
        printf("2. View Participant\n");
        printf("3. Delete Participant\n");
        printf("4. Edit Participant\n");
        printf("5. Exit\n");
        printf("Enter your choice: ");

        choice=readint();

        switch (choice) {
            case 1: registerParticipant(); break;
            case 2: viewParticipants(); break;
            case 3: deleteParticipant(); break;
            case 4: editParticipant(); break;
            case 5: printf("Exiting program.\n"); break;
            default: printf("Invalid choice. Please try again.\n");
        }
    } while (choice != 5);

    return 0;
}
