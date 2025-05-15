class Package:
    def __init__(self,
                 package_id='',
                 address='',
                 city='',
                 state='',
                 zipcode='',
                 delivery_time='',
                 weight='',
                 status='',
                 notes=''):
        self.package_id = package_id
        self.address = address
        self.city = city
        self.state = state
        self.zipcode = zipcode
        self.delivery_time = delivery_time
        self.weight = weight
        self.status = status
        self.notes = notes

    def __repr__(self):
        return (
            f"Shipment Details - ID: {self.package_id}, "
            f"ADDRESS: {self.address}, "
            f"CITY: {self.city}, "
            f"STATE: {self.state}, "
            f"ZIP: {self.zipcode}, "
            f"DELIVERY TIME: {self.delivery_time}, "
            f"WEIGHT: {self.weight}, "
            f"STATUS: {self.status}, "
            f"NOTES: {self.notes}"
        )
