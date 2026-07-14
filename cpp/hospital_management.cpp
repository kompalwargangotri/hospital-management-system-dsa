#include <iostream>
#include <string>
using namespace std;

class Node {
public:
    int id;
    string name;
    int age;
    string disease;
    Node* next;

    Node(int id, string name, int age, string disease) {
        this->id = id;
        this->name = name;
        this->age = age;
        this->disease = disease;
        this->next = nullptr;
    }
};

class LinkedList {
private:
    Node* head;

public:
    LinkedList() {
        head = nullptr;
    }

    void addPatient(int id, string name, int age, string disease) {
        Node* newNode = new Node(id, name, age, disease);
        if (!head) head = newNode;
        else {
            Node* temp = head;
            while (temp->next) temp = temp->next;
            temp->next = newNode;
        }
        cout << "Patient added successfully!\n";
    }

    void displayPatients() {
        if (!head) {
            cout << "No patient records available.\n";
            return;
        }
        Node* temp = head;
        cout << "\n Patient List:\n";
        while (temp) {
            cout << "---------------------\n";
            cout << "ID      : " << temp->id << "\n";
            cout << "Name    : " << temp->name << "\n";
            cout << "Age     : " << temp->age << "\n";
            cout << "Disease : " << temp->disease << "\n";
            temp = temp->next;
        }
        cout << "---------------------\n";
    }

    void deletePatient(int id) {
        if (!head) {
            cout << "No records to delete.\n";
            return;
        }

        Node* temp = head;
        Node* prev = nullptr;

        if (head->id == id) {
            head = head->next;
            delete temp;
            cout << "Patient deleted successfully.\n";
            return;
        }

        while (temp && temp->id != id) {
            prev = temp;
            temp = temp->next;
        }

        if (!temp) {
            cout << "Patient with ID " << id << " not found.\n";
            return;
        }

        prev->next = temp->next;
        delete temp;
        cout << "Patient deleted successfully.\n";
    }
};

class DoctorNode {
public:
    int id;
    string name;
    string specialization;
    bool available;
    DoctorNode* next;

    DoctorNode(int id, string name, string specialization, bool available) {
        this->id = id;
        this->name = name;
        this->specialization = specialization;
        this->available = available;
        this->next = nullptr;
    }
};

class DoctorList {
private:
    DoctorNode* head;

public:
    DoctorList() {
        head = nullptr;
    }

    void addDoctor(int id, string name, string specialization, bool available) {
        DoctorNode* newNode = new DoctorNode(id, name, specialization, available);
        if (!head) head = newNode;
        else {
            DoctorNode* temp = head;
            while (temp->next) temp = temp->next;
            temp->next = newNode;
        }
        cout << "Doctor added successfully!\n";
    }

    void displayDoctors() {
        if (!head) {
            cout << "No doctors available.\n";
            return;
        }

        DoctorNode* temp = head;
        cout << "\nDoctor List:\n";
        while (temp) {
            cout << "---------------------\n";
            cout << "ID             : " << temp->id << "\n";
            cout << "Name           : " << temp->name << "\n";
            cout << "Specialization : " << temp->specialization << "\n";
            cout << "Available      : " << (temp->available ? "Yes" : "No") << "\n";
            temp = temp->next;
        }
        cout << "---------------------\n";
    }
};

class BedManager {
private:
    int totalBeds;
    int occupiedBeds;

public:
    BedManager(int total) {
        totalBeds = total;
        occupiedBeds = 0;
    }

    void admitPatient() {
        if (occupiedBeds < totalBeds) {
            occupiedBeds++;
            cout << "Patient admitted. Bed assigned.\n";
        } else {
            cout << "No beds available!\n";
        }
    }

    void dischargePatient() {
        if (occupiedBeds > 0) {
            occupiedBeds--;
            cout << "Patient discharged. Bed freed.\n";
        } else {
            cout << "No patients to discharge.\n";
        }
    }

    void displayBedStatus() {
        cout << "\nBed Availability:\n";
        cout << "Total Beds     : " << totalBeds << "\n";
        cout << "Occupied Beds  : " << occupiedBeds << "\n";
        cout << "Available Beds : " << (totalBeds - occupiedBeds) << "\n";
    }
};

int main() {
    LinkedList patients;
    DoctorList doctors;
    BedManager beds(10); 

    int choice;

    do {
        cout << "\nHospital Management System\n";
        cout << "1. Add Patient\n";
        cout << "2. Display Patients\n";
        cout << "3. Delete Patient\n";
        cout << "4. Add Doctor\n";
        cout << "5. Display Doctors\n";
        cout << "6. Admit Patient (Bed)\n";
        cout << "7. Discharge Patient (Bed)\n";
        cout << "8. Check Bed Availability\n";
        cout << "9. Exit\n"<< endl;
        cout << "Enter your choice: ";
        cin >> choice;

        int id, age;
        string name, disease, specialization;
        bool available;

        switch (choice) {
            case 1:
                cout << "Enter Patient ID: ";
                cin >> id;
                cout << "Enter Name: ";
                cin >> name;
                cout << "Enter Age: ";
                cin >> age;
                cout << "Enter Disease: ";
                cin >> disease;
                patients.addPatient(id, name, age, disease);
                break;

            case 2:
                patients.displayPatients();
                break;

            case 3:
                cout << "Enter Patient ID to delete: ";
                cin >> id;
                patients.deletePatient(id);
                break;

            case 4:
                cout << "Enter Doctor ID: ";
                cin >> id;
                cout << "Enter Name: ";
                cin >> name;
                cout << "Enter Specialization: ";
                cin >> specialization;
                cout << "Is Doctor Available (1 for Yes / 0 for No): ";
                cin >> available;
                doctors.addDoctor(id, name, specialization, available);
                break;

            case 5:
                doctors.displayDoctors();
                break;

            case 6:
                beds.admitPatient();
                break;

            case 7:
                beds.dischargePatient();
                break;

            case 8:
                beds.displayBedStatus();
                break;

            case 9:
                cout << "Exiting system. Stay healthy!\n";
                break;

            default:
                cout << "Invalid choice. Try again.\n";
        }
    } while (choice != 9);

    return 0;
}
