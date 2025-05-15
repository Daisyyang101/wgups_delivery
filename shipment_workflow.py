from truck_data import Truck
import datetime

#Determines the expected delivery time of a package based on distance and time.
def tick(mileage, time):
    return time + datetime.timedelta(seconds=(mileage / 18) * 3600)

#assigns a package to a truck
def truck_allocation(pkg, truck, pkg_data, addresses_to_visit, label):
    truck.add_package(pkg_data)
    pkg.status = label
    if pkg.address not in addresses_to_visit:
        addresses_to_visit.append(pkg.address)

#improves route by trying different arrangments
def two_opt_swap(route, i, k):
    return route[:i] + route[i:k + 1][::-1] + route[k + 1:]

# reduce total travel distance
def optimize(route, distance_data):
    route = ['HUB'] + route[:] + ['HUB']
    index = 2 if '4580 S 2300 E' in route else 1
    best = route
    improved = True

    while improved:
        improved = False
        for i in range(index, len(route) - 1):
            for k in range(i + 1, len(route)):
                new_route = two_opt_swap(best, i, k)
                if cost(new_route, distance_data)[0] < cost(best, distance_data)[0]:
                    best = new_route
                    improved = True
        route = best
    return best

# calculates total distance and updates/checks delivery status
def cost(route, data, time=-1, pkgs=None, check_time=0, package=None, search=False):
    total_miles, start = 0, route[0]
    visited = [start]
    count = 0

    while len(visited) < len(route):
        for row in data:
            if row[0] == start:
                for dest, dist in row[1]:
                    if dest == route[count + 1]:
                        miles = float(dist)
                        total_miles += miles
                        visited.insert(0, dest)
                        if time != -1:
                            time = tick(miles, time)
                        if check_time and time >= check_time:
                            if search:
                                return find_pkg_status(package, check_time, pkgs)
                            return True
                        if pkgs:
                            pkg_status_update(dest, pkgs, time)
                        start = dest
                        count += 1
                        break
                break
    if check_time:
        return find_pkg_status(package, check_time, pkgs) if search else False
    return [total_miles, time]

#updates delivery status of a package
def pkg_status_update(address, pkgs, time):
    for pkg in pkgs:
        if pkg[1].address == address:
            pkg[1].status = 'Delivered at ' + time.strftime("%H:%M:%S")

#finds and prints the status of a specific package
def find_pkg_status(package, check_time, pkgs):
    for pkg in pkgs:
        if pkg[1].package_id == package.package_id:
            print('\nAt', check_time.time(), '\n\n', package)
            return True
    return False

#prints all packages
def print_all_packages(pkg_data):
    for pkg in pkg_data.list:
        if pkg:
            print(pkg[1])

# main delivery control function
# - Normal delivery
# - Time-check for package status at a specific time
# - Range-based delivery verification
# - Package lookup by ID
def deliver_packages(pkg_data, dist_data, status='normal', hour=0, minute=0, pkg_id=0):
    if status != 'range':
        try:
            hour = int(hour)
            minute = int(minute)
        except ValueError:
            print("Re-Enter: Hour and minute must be an integer.")
            return

    t1, t2, t3 = [datetime.datetime(100, 1, 1, h, m) for h, m in [(8, 0), (9, 5), (10, 30)]]
    t1_list, t2_list, t3_list = [], [], []
    truck1, truck2, truck3 = Truck(), Truck(), Truck()

    truck_load_up(truck1, pkg_data, t1_list, 1)
    for attr in ['address', 'city', 'zipcode']:
        setattr(pkg_data.get(9), attr, {'address': '410 S State St', 'city': 'Salt Lake City', 'zipcode': '84111'}[attr])
    truck_load_up(truck2, pkg_data, t2_list, 2)
    truck_load_up(truck3, pkg_data, t3_list, 3)

    r1 = optimize(t1_list, dist_data)
    r2 = optimize(t2_list, dist_data)
    r3 = optimize(t3_list, dist_data)

    if status == 'normal':
        m1 = cost(r1, dist_data, t1, truck1.truck)
        m2 = cost(r2, dist_data, t2, truck2.truck)
        m3 = cost(r3, dist_data, t3, truck3.truck)
        print(f"Truck 1: {m1[0]} miles")
        print(f"Time: {t1.time()} to {m1[1].time()}\n")
        print(f"Truck 2: {m2[0]} miles")
        print(f"Time: {t2.time()} to {m2[1].time()}\n")
        print(f"Truck 3: {m3[0]} miles")
        print(f"Time: {t3.time()} to {m3[1].time()}\n")
        print(f"TOTAL MILES: {m1[0] + m2[0] + m3[0]} miles")

    elif status == 'ap':
        time_check = datetime.datetime(100, 1, 1, hour, minute)
        if hour < 1 or hour > 24 or minute < 0 or minute > 59:
            return print('Time is invalid')
        if time_check < t1:
            print_all_packages(pkg_data)
            return
        for args in [(r1, t1, truck1), (r2, t2, truck2), (r3, t3, truck3)]:
            if cost(args[0], dist_data, args[1], args[2].truck, time_check):
                print_all_packages(pkg_data)
                return
        print_all_packages(pkg_data)

    elif status == 'range':
        sh, eh = hour
        sm, em = minute
        start = datetime.datetime(100, 1, 1, sh, sm)
        end = datetime.datetime(100, 1, 1, eh, em)

        for route, time_start, truck in [(r1, t1, truck1), (r2, t2, truck2), (r3, t3, truck3)]:
            cost(route, dist_data, time_start, truck.truck)

        print(f"\nPackages delivered between {start.strftime('%I:%M %p')} and {end.strftime('%I:%M %p')}:\n")
        delivered_any = False
        for pkg in pkg_data.list:
            if pkg and pkg[1].status.startswith("Delivered at"):
                try:
                    d_time = datetime.datetime.strptime(pkg[1].status.replace("Delivered at ", ""), "%H:%M:%S").time()
                    if start.time() <= d_time <= end.time():
                        print(pkg[1])
                        delivered_any = True
                except:
                    pass
        if not delivered_any:
            print("No packages were delivered in this time window.")

    else:
        time_check = datetime.datetime(100, 1, 1, hour, minute)
        package = pkg_data.get(pkg_id)
        if not package:
            return
        if time_check < t1:
            print('Not loaded yet.\n', package)
            return True
        for route, time_start, truck in [(r1, t1, truck1), (r2, t2, truck2), (r3, t3, truck3)]:
            if cost(route, dist_data, time_start, truck.truck, time_check, package, True):
                return True

# loads packages onto assigned trucks
def truck_load_up(truck, pkg_data, addresses, num):
    count, done = 0, False
    while not done:
        for entry in pkg_data.list:
            if not entry or entry in truck.truck:
                continue
            pkg = entry[1]
            if pkg.status != 'At HUB':
                continue
            addr, notes, time_due = pkg.address, pkg.notes, pkg.delivery_time
            id = float(pkg.package_id)
            needs = [13, 14, 15, 16, 19, 20]

            if len(truck.truck) >= truck.capacity:
                done = True
                break

            if num == 1 and (
                time_due == '9:00 AM' or
                (count >= 1 and id in needs) or
                (count >= 1 and time_due != 'EOD' and 'Delayed' not in notes and 'Wrong' not in notes) or
                (count >= 2 and 'Delayed' not in notes and notes != 'Can only be on truck 2' and addr in addresses and 'Wrong' not in notes) or
                (count >= 3 and notes != 'Can only be on truck 2' and 'Delayed' not in notes and 'Wrong' not in notes)):
                truck_allocation(pkg, truck, entry, addresses, 'ON TRUCK ONE')

            elif num == 2 and (
                (notes == 'Can only be on truck 2' and addr != '2530 S 500 E') or
                (count >= 1 and addr in addresses and addr != '2530 S 500 E' and 'Wrong' not in notes) or
                (count >= 2 and 'Delayed' in notes and addr != '2530 S 500 E') or
                (count >= 3 and addr != '2530 S 500 E')):
                truck_allocation(pkg, truck, entry, addresses, 'ON TRUCK ONE')

            elif num == 3:
                truck_allocation(pkg, truck, entry, addresses, 'ON TRUCK THREE')
                done = True

        if num == 3:
            done = True
        count += 1
    return truck, addresses
