# Jordan Durant 000663838

import datetime
import time
import csv


def main():
    global destination_list  # stores all destinations
    destination_list = create_destination_list('WGUPS Distance Table.csv')
    global package_list  # stores all package info in hash table
    package_list = HashTable()
    global desired_time  # stores user time input

    import_packages('WGUPS Package File.csv')

    user_input = input("Please enter the time you wish to check the package statuses (Please user ##:##:## format)\n"
                       "type 'quit' to exit the program\n\nDesired Time: ")

    while user_input != 'quit':

        # convert user input into a useable time object
        desired_time_string = "2020-01-01 " + user_input
        desired_time = datetime.datetime.strptime(desired_time_string, '%Y-%m-%d %H:%M:%S')

        # if time is 8am or sooner all of the packages remain at hub and can be listed as such

        if desired_time <= datetime.datetime(2020, 1, 1, 8, 00, 00):
            list_all_packages()
            print("\nTotal miles traveled: 0")
            user_input = input(
                "\nPlease enter the time you wish to check the package statuses (Please user ##:##:## format)\n"
                "type 'quit' to exit the program\n\nDesired Time: ")
        else:

            print("Checking packages at " + desired_time.strftime("%H:%M:%S"))

            # create and load first truck
            truck1 = Truck()

            truck1.load_package(package_list.get(4))
            truck1.load_package(package_list.get(8))
            truck1.load_package(package_list.get(13))
            truck1.load_package(package_list.get(14))
            truck1.load_package(package_list.get(15))
            truck1.load_package(package_list.get(16))
            truck1.load_package(package_list.get(19))
            truck1.load_package(package_list.get(20))
            truck1.load_package(package_list.get(21))
            truck1.load_package(package_list.get(23))
            truck1.load_package(package_list.get(27))
            truck1.load_package(package_list.get(29))
            truck1.load_package(package_list.get(30))
            truck1.load_package(package_list.get(31))
            truck1.load_package(package_list.get(34))
            truck1.load_package(package_list.get(35))

            # marks all packages on truck en route O(N)
            for package in truck1.packages:
                package.status = "EN ROUTE"

            # create and load second truck
            truck2 = Truck()
            truck2.time = datetime.datetime(2020, 1, 1, 9, 5, 00)

            truck2.load_package(package_list.get(1))
            truck2.load_package(package_list.get(2))
            truck2.load_package(package_list.get(3))
            truck2.load_package(package_list.get(5))
            truck2.load_package(package_list.get(6))
            truck2.load_package(package_list.get(7))
            truck2.load_package(package_list.get(10))
            truck2.load_package(package_list.get(11))
            truck2.load_package(package_list.get(12))
            truck2.load_package(package_list.get(17))
            truck2.load_package(package_list.get(18))
            truck2.load_package(package_list.get(28))
            truck2.load_package(package_list.get(36))
            truck2.load_package(package_list.get(37))
            truck2.load_package(package_list.get(38))
            truck2.load_package(package_list.get(40))

            # marks all packages on truck en route O(N)
            for package in truck2.packages:
                package.status = "EN ROUTE"

            # deliver packages on truck up to desired time - O(N^4)
            while truck1.packages:
                if truck1.time > desired_time:
                    break
                elif truck1.time <= desired_time:
                    deliver_next_package(truck1)

            # return truck to hub and load the last packages if truck no longer has packages on it
            if not truck1.packages:
                truck1.return_to_hub()

            truck1.load_package(package_list.get(9))
            truck1.load_package(package_list.get(22))
            truck1.load_package(package_list.get(23))
            truck1.load_package(package_list.get(25))
            truck1.load_package(package_list.get(24))
            truck1.load_package(package_list.get(26))
            truck1.load_package(package_list.get(32))
            truck1.load_package(package_list.get(33))
            truck1.load_package(package_list.get(39))

            # marks all packages on truck en route O(N)
            if truck1.time <= desired_time:
                for package in truck1.packages:
                    package.status = "EN ROUTE"

            # deliver packages on truck up to desired time - O(N^4)
            while truck1.packages:
                if truck1.time > desired_time:
                    break
                elif truck1.time <= desired_time:
                    deliver_next_package(truck1)

            # return truck to hub and load the last packages if truck no longer has packages on it
            if not truck1.packages:
                truck1.return_to_hub()

            # deliver packages on truck 2 and adjust package 9 to the correct address at 10:20 - O(N^4)
            while truck2.packages:
                if truck2.time >= datetime.datetime(2020, 1, 1, 10, 20, 00):
                    for package in truck1.packages:
                        if package.package_id == 9:
                            package.delivery_address = "410 S State St"
                            package.city = "Salt Lake City"
                            package.zipcode = 84111
                            print("\n--- address changed ---\n")
                if truck2.time > desired_time:
                    break
                elif truck2.time <= desired_time:
                    deliver_next_package(truck2)

            if not truck2.packages:
                truck2.return_to_hub()
            # list the status of all the packages at the desired time and prompt the user to check another time
            list_all_packages()
            print("\nTotal miles traveled: " + str(truck1.miles_traveled + truck2.miles_traveled))
            user_input = input(
                "\nPlease enter the time you wish to check the package statuses (Please user ##:##:## format)\n"
                "type 'quit' to exit the program\n\nDesired Time: ")


# main delivery algorithm - O(N^3)
def deliver_next_package(truck):
    predicted_distances = []

    # create list of all possible distances based on current payload - O(N^3)
    for package in truck.packages:
        current_location = truck.current_location
        next_location = package.delivery_address
        predicted_distance = find_distance(current_location, next_location)
        predicted_distances.append(predicted_distance)

    # set next delivery to the shortest distance
    next_delivery = predicted_distances.index(min(predicted_distances))

    predicted_time = truck.time + time_to_travel(predicted_distance)

    # prevents packages being delivered after desired time
    if predicted_time > desired_time:
        truck.time = predicted_time
    else:
        truck.drive_to_destination(truck.packages[next_delivery])
        package_update = truck.packages.pop(next_delivery)
        package_update.status = 'DELIVERED'
        package_update.time_delivered = truck.time
        package_list.insert(package_update.package_id, package_update)


# list all packages in a clean - readable format - O(N)
def list_all_packages():
    print("%2s | %40s | %20s| %10s | %15s | %10s | %10s | %10s" % (
        "ID", "Delivery Address", "City", "Zipcode", "Delivery Time", "Deadline", "Weight", "Status"))
    print('-' * 150)
    for counter in range(1, 41):
        package = package_list.get(counter)
        id = package.package_id
        delivery_address = package.delivery_address
        city = package.city
        zip = package.zipcode
        delivery_time = package.time_delivered
        delivery_time_string = " "
        if isinstance(delivery_time, datetime.datetime):
            delivery_time_string = delivery_time.strftime("%H:%M:%S")
        else:
            delivery_time_string = delivery_time
        deadline = package.deadline
        weight = package.weight
        status = package.status
        print("%2d | %40s | %20s| %10s | %15s | %10s | %10s | %10s" % (
            id, delivery_address, city, zip, delivery_time_string, deadline, weight, status))


# determine time taken to travel a certain distance - O(1)
def time_to_travel(distance):
    speed = 18
    time = distance / speed
    hours = int(time)
    minutes = int(time * 60) % 60
    seconds = int(time * 3600) % 60
    time_to_add = datetime.timedelta(hours=hours, minutes=minutes, seconds=seconds)
    return time_to_add


# creates list of destinations - used in conjunction with find_distance function to find the distance between two locations - O(N)
def create_destination_list(file):
    destination_list = []

    #read data from file - O(N)
    with open(file, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            destination_list.append(row[0].rstrip().lstrip())
    f.close()

    # corrects for type in data - O(N)
    for item in destination_list:
        new_string_index = destination_list.index(item)
        new_string = item.replace("South", "S")
        destination_list[new_string_index] = new_string
    return destination_list


# finds the distance between two locations in the distance table - O(N^2)
def find_distance(current_location, destination):
    distance = 0.0

    with open('WGUPS Distance Table.csv', 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            test = row[0].rstrip().lstrip().replace('South', 'S')
            if test == current_location:
                distance = row[destination_list.index(destination)]
                if distance == '':
                    distance = 0.0
                    f.seek(0)
                    for row1 in reader:
                        test = row1[0].rstrip().lstrip().replace('South', 'S')
                        if test == destination:
                            distance = row1[destination_list.index(current_location)]
                break
    f.close()
    return float(distance)


# Hash Table Class
class HashTable:

    def __init__(self):
        self.size = 10
        self.table = [None] * self.size

    def hash_function(self, key):
        return key % 10

    # inserts new item into hash table - O(N)
    def insert(self, key, value):
        hash_key = self.hash_function(key)
        key_value = [key, value]

        if self.table[hash_key] is None:
            self.table[hash_key] = list([key_value])
            return True
        else:
            for pair in self.table[hash_key]:
                if pair[0] == key:
                    pair[1] = value
                    return True
                self.table[hash_key].append(key_value)

    # allows for package look up by key (package ID) - O(N)
    def get(self, key):
        hash_key = self.hash_function(key)

        if self.table[hash_key] is not None:
            for pair in self.table[hash_key]:
                if pair[0] == key:
                    return pair[1]
        return None

    # Deletes item from hash table - O(N)
    def delete(self, key):
        hash_key = self.hash_function(key)

        if self.table[hash_key] is None:
            return False
        for item in range(0, len(self.table[hash_key])):
            if self.table[hash_key][item][0] == key:
                self.table[hash_key].pop(item)
                return True

    # prints all items from hash table - O(N)
    def print(self):
        print('------Packages------')
        for item in self.table:
            if item is not None:
                print(str(item))


# imports packages from file - O(N)
def import_packages(file):
    with open(file, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            package = Package(int(row[0]), row[1].replace("South", "S"), row[2], row[4], row[5], "None", row[6])
            package_list.insert(package.package_id, package)

    return package_list


# Package Class - creates package objects that hold info about individual packages
class Package:
    deadline: datetime

    def __init__(self, package_id=None, delivery_address=None, city=None, zipcode=None, deadline=None,
                 time_delivered=datetime.datetime(2020, 1, 1, 00, 00, 00), weight=None,
                 status='AT_HUB'):
        self.package_id = package_id
        self.delivery_address = delivery_address
        self.city = city
        self.zipcode = zipcode
        self.deadline = deadline
        self.time_delivered = time_delivered
        self.weight = weight
        self.status = status

    def get_id(self):
        return self.package_id


# truck class - allows for loading and offloading of packages onto trucks for delivery
class Truck:

    def __init__(self, current_location='HUB', miles_traveled=0, time=datetime.datetime(2020, 1, 1, 8, 00, 00)):
        self.current_location = current_location
        self.packages = []
        self.miles_traveled = miles_traveled
        self.time = time

    def load_package(self, package):
        self.packages.append(package)

    # moves truck to next destination and updates necessary information - O(N^2)
    def drive_to_destination(self, package):
        next_delivery = package.delivery_address
        distance = find_distance(self.current_location, next_delivery)
        current_mileage = self.miles_traveled
        self.miles_traveled += distance
        self.time += time_to_travel(self.miles_traveled - current_mileage)
        self.current_location = next_delivery

    def return_to_hub(self):
        self.miles_traveled += find_distance(self.current_location, 'HUB')

    def print_packages(self):
        for package in self.packages:
            print(package.__dict__)


if __name__ == "__main__":
    main()
