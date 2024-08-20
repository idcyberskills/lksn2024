#include<stdio.h>
#include<string.h>
#include<stdlib.h>
#include<unistd.h>

#define MAX_SPOTS 10
#define MAX_PLATE_LENGTH 16

// gcc ./chall.c -o chall -g -Wl,-z,relro,-z,now -no-pie

// Function prototypes
void displayMenu();
void parkCar(char parkingSpots[MAX_SPOTS][MAX_PLATE_LENGTH]);
void removeCar(char parkingSpots[MAX_SPOTS][MAX_PLATE_LENGTH]);
void displayStatus(char parkingSpots[MAX_SPOTS][MAX_PLATE_LENGTH]);

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

int main() {
    init();
    char parkingSpots[MAX_SPOTS][MAX_PLATE_LENGTH] = {""}; // Initialize all spots to be empty
    int choice;
    
    do {
        displayMenu();
        printf("Enter your choice: ");
        choice = readint();
        
        switch(choice) {
            case 1:
                parkCar(parkingSpots);
                break;
            case 2:
                removeCar(parkingSpots);
                break;
            case 3:
                displayStatus(parkingSpots);
                break;
            case 4:
                printf("Exiting the program.\n");
                break;
            default:
                printf("Invalid choice. Please try again.\n");
        }
    } while (choice != 4);
    
    return 0;
}

void displayMenu() {
    printf("\nCar Parking System\n");
    printf("1. Park a car\n");
    printf("2. Remove a car\n");
    printf("3. Display parking status\n");
    printf("4. Exit\n");
}

void parkCar(char parkingSpots[MAX_SPOTS][MAX_PLATE_LENGTH]) {
    int spot;
    char licensePlate[80];
    
    printf("Enter spot number to park the car (0-%d): ", MAX_SPOTS - 1);
    spot = readint();
    
    if (spot < 0 || spot >= MAX_SPOTS) {
        printf("Invalid spot number. Please try again.\n");
    } else if (parkingSpots[spot][0] != '\0') {
        printf("Spot %d is already occupied.\n", spot);
    } else {
        printf("Enter the vehicle license plate: ");
        read(0,licensePlate,80);
        strcpy(parkingSpots[spot], licensePlate);
        printf("Car with license plate %s parked at spot %d.\n", licensePlate, spot);
    }
}

void removeCar(char parkingSpots[MAX_SPOTS][MAX_PLATE_LENGTH]) {
    int spot;
    
    printf("Enter spot number to remove the car (0-%d): ", MAX_SPOTS - 1);
    spot = readint();
    
    if (spot < 0 || spot >= MAX_SPOTS) {
        printf("Invalid spot number. Please try again.\n");
    } else if (parkingSpots[spot][0] == '\0') {
        printf("Spot %d is already empty.\n", spot);
    } else {
        printf("Car with license plate %s removed from spot %d.\n", parkingSpots[spot], spot);
        parkingSpots[spot][0] = '\0'; // Clear the license plate to indicate the spot is empty
    }
}

void displayStatus(char parkingSpots[MAX_SPOTS][MAX_PLATE_LENGTH]) {
    printf("Parking status:\n");
    for (int i = 0; i < MAX_SPOTS; i++) {
        if (parkingSpots[i][0] == '\0') {
            printf("Spot %d: Empty\n", i);
        } else {
            printf("Spot %d: Occupied by %s\n", i, parkingSpots[i]);
        }
    }
}