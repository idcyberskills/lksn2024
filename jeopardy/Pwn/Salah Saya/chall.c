#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#define MAX_BOOKINGS 100
#define MAX_FLIGHTS 5

#define MAX_name 124
#define MAX_flightNumber 16
#define MAX_bookingClass 24

typedef struct {
    int id;
    char name[MAX_name];
    char flightNumber[MAX_flightNumber];
    char bookingClass[MAX_bookingClass]; // e.g., Economic, Business
} Booking;

typedef struct {
    char flightNumber[10];
    char destination[50];
    int availableSeats;
} Flight;

Booking bookings[MAX_BOOKINGS];
Flight flights[MAX_FLIGHTS] = {
    {"FL001", "New York", 100},
    {"FL002", "London", 80},
    {"FL003", "Paris", 60},
    {"FL004", "Tokyo", 50},
    {"FL005", "Sydney", 40}
};

int bookingCount = 0;

void win(){
	FILE* file;
    int c = 0;

    file = fopen("flag.txt", "r");

    if (NULL == file) {
        fprintf(stderr, "Cannot open flag.txt");
        exit(EXIT_FAILURE);
    } else {
        while (1) {
            c = fgetc(file);
            if (c == EOF)
                break;
            putchar(c);
        }
        fclose(file);
    }	
}

void init()
{
    setvbuf(stdin, 0, 2, 0);
    setvbuf(stdout, 0, 2, 0);
    setvbuf(stderr, 0, 2, 0);
}

int readint(){
    char buf[0x10];
    return atoi(fgets(buf,0x10,stdin));
}

void viewBookingById() {
    char input[10];
    printf("Enter booking ID to view: ");
    fgets(input, 10, stdin);
    int id = atoi(input);

    for (int i = 0; i < bookingCount; i++) {
        if (bookings[i].id == id) {
            printf("Booking ID: %d\n", bookings[i].id);
            printf("Name: %s\n", bookings[i].name);
            printf("Flight Number: %s\n", bookings[i].flightNumber);
            printf("Booking Class: %s\n", bookings[i].bookingClass);
            if (strncmp(bookings[i].bookingClass,"Business",8) == 0 ){
                printf("Win :\n");
                win();
                return;
            }
        }
    }
    printf("Booking with ID %d not found.\n", id);
}

void displayFlights() {
    printf("\nAvailable Flights:\n");
    for (int i = 0; i < MAX_FLIGHTS; i++) {
        printf("Flight Number: %s, Destination: %s, Available Seats: %d\n", flights[i].flightNumber, flights[i].destination, flights[i].availableSeats);
    }
    printf("\n");
}

void bookFlight() {
    if (bookingCount >= MAX_BOOKINGS) {
        printf("Booking limit reached.\n");
        return;
    }

    Booking newBooking;
    newBooking.id = bookingCount + 1;

    printf("Enter your name: ");
    fgets(newBooking.name, 124, stdin);
    newBooking.name[strcspn(newBooking.name, "\n")] = 0; // Remove newline character

    displayFlights();

    printf("Enter flight number: ");
    fgets(newBooking.flightNumber, 16, stdin);
    newBooking.flightNumber[strcspn(newBooking.flightNumber, "\n")] = 0; // Remove newline character

    printf("Enter booking class (Economic/Business): ");
    fgets(newBooking.bookingClass, 24, stdin);
    newBooking.bookingClass[strcspn(newBooking.bookingClass, "\n")] = 0; // Remove newline character


    if (strncmp(newBooking.bookingClass,"Economic",8) != 0 && strncmp(newBooking.bookingClass,"Business",8) != 0 ){
        printf("Booking Class only Economic/Business.\n");
        return;
    }

    if (strncmp(newBooking.bookingClass,"Business",8) == 0 ){
        printf("Booking for Business Class is disabled.\n");
        return;
    }

    for (int i = 0; i < MAX_FLIGHTS; i++) {
        if (strcmp(flights[i].flightNumber, newBooking.flightNumber) == 0) {
            if (flights[i].availableSeats > 0) {
                flights[i].availableSeats--;
                bookings[bookingCount] = newBooking;
                bookingCount++;
                printf("Flight booked successfully!\n");
            } else {
                printf("No seats available on this flight.\n");
            }
            return;
        }
    }

    printf("Flight not found.\n");
}


void deleteBooking() {
    char input[10];
    printf("Enter booking ID to delete: ");
    fgets(input, 10, stdin);
    int id = atoi(input);

    int index = -1;
    for (int i = 0; i < bookingCount; i++) {
        if (bookings[i].id == id) {
            index = i;
            break;
        }
    }

    if (index == -1) {
        printf("Booking not found.\n");
        return;
    }

    for (int i = 0; i < MAX_FLIGHTS; i++) {
        if (strcmp(flights[i].flightNumber, bookings[index].flightNumber) == 0) {
            flights[i].availableSeats++;
            break;
        }
    }

    for (int i = index; i < bookingCount - 1; i++) {
        bookings[i] = bookings[i + 1];
    }
    bookingCount--;
    printf("Booking deleted successfully.\n");
}

void editBooking() {
    Booking newBooking;
    char input[10];
    printf("Enter booking ID to edit: ");
    fgets(input, 10, stdin);
    int id = atoi(input);

    int index = -1;
    for (int i = 0; i < bookingCount; i++) {
        if (bookings[i].id == id) {
            index = i;
            break;
        }
    }

    if (index == -1) {
        printf("Booking not found.\n");
        return;
    }

    printf("Editing Booking ID: %d\n", bookings[index].id);
    printf("Enter new name: ");
    fgets(newBooking.name, 121, stdin);
    newBooking.name[strcspn(newBooking.name, "\n")] = 0; // Remove newline character

    printf("Enter new flight number: ");
    fgets(newBooking.flightNumber, 16, stdin);
    newBooking.flightNumber[strcspn(newBooking.flightNumber, "\n")] = 0; // Remove newline character

    printf("Enter new booking class (Economic/Business): ");
    fgets(newBooking.bookingClass, 24, stdin);

    newBooking.bookingClass[strcspn(newBooking.bookingClass, "\n")] = 0; // Remove newline character

    if (strncmp(newBooking.bookingClass,"Economic",8) != 0 && strncmp(newBooking.bookingClass,"Business",8) != 0 ){
        printf("Booking Class only Economic/Business.\n");
        return;
    }

    if (strncmp(newBooking.bookingClass,"Business",8) == 0 ){
        printf("Booking for Business Class is disabled.\n");
        return;
    }
    newBooking.id = bookings[index].id;
    bookings[index] = newBooking;

    // for (int i = 0; i < MAX_FLIGHTS; i++) {
    //     if (strcmp(flights[i].flightNumber, newBooking.flightNumber) == 0) {
    //         if ( bookings[i].id == id )  {
    //             flights[i].availableSeats--;
    //             bookings[bookingCount] = newBooking;
    //             bookingCount++;
    //             printf("Flight booked successfully!\n");
    //         } else {
    //             printf("No seats available on this flight.\n");
    //         }
    //         return;
    //     }
    // }

    printf("Booking updated successfully for name : ");
    printf(bookings[index].name);


}

int main() {
    init();
    int choice;

    while (1) {
        printf("\nFlight Booking System\n");
        printf("1. View Booking by ID\n");
        printf("2. Book Flight\n");
        printf("3. Delete Booking\n");
        printf("4. Edit Booking\n");
        printf("5. Display Flights\n");
        printf("6. Exit\n");
        printf("Enter your choice: ");
        // scanf("%d", &choice);
        choice = readint();

        switch (choice) {
            case 1:
                viewBookingById();
                break;
            case 2:
                bookFlight();
                break;
            case 3:
                deleteBooking();
                break;
            case 4:
                editBooking();
                break;
            case 5:
                displayFlights();
                break;
            case 6:
                printf("Exiting the program.\n");
                exit(1);
                return 0;
            default:
                printf("Invalid choice. Please try again.\n");
        }
    }

    return 0;
}