

class Hash:


# stores package using package ID
    def __init__(self, size=10):
        self.size = size * 2  # make table a little bigger than needed
        self.table = [None] * self.size

    def _hash_key(self, key):
# turns package ID into a number for quick searching
        return int(key)

    def add(self, key, value):

    # Adds a package into the hash table using the ID

        try:
            idx = self._hash_key(key)
            if self.table[idx] is None:
                self.table[idx] = [key, value]
                return True
            else:
                print("Package already exists.")
                return False
        except IndexError:
            print(f"ID is out of range (max = {len(self.table) - 1})")

    def get(self, key):
    # Looks up using package ID



        try:
            idx = self._hash_key(key)
            if self.table[idx] is not None:
                return self.table[idx][1]
            else:
                print("Can't find Package.")
                return False
        except IndexError:
            print("Can't find Package.")
            return False


    @property
    def list(self):

        # Returns the internal table for iteration purposes
        return self.table
