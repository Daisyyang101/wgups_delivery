import datetime
#Class defines the structure of the package
class Package:
    def __init__(self, package_id, address, city, state, zipcode, delivery_time, weight, status, notes):
        self.package_id = package_id #unqiue ID
        self.address = address
        self.city = city
        self.state = state
        self.zipcode = zipcode
        self.delivery_time = delivery_time
        self.weight = weight
        self.status = status
        self.notes = notes

#shows how package will be displayed when printed
    def __repr__(self):
        # Try to convert delivery_time to AM/PM format if it's a time
        try:
            time_obj = datetime.datetime.strptime(self.delivery_time.strip(), "%H:%M:%S").time()
            formatted_time = time_obj.strftime("%I:%M %p")
        except:
            formatted_time = self.delivery_time

        return "Package ID: " + str(
            self.package_id) + " , " + self.address + ", " + self.city + " " + self.state + " " + self.zipcode + \
            " , Due: " + formatted_time + " , Weight: " + self.weight + " , Status: " + self.status + " , Speical Notes: " + self.notes

