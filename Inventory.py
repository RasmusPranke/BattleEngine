class Inventory:
    '''An inventory contains counts of items, up to a given capacity of different items'''
    def __init__(self, capacity):
        self.capacity = capacity
        self.contents = {}
        
    def addItem(self, item, count):
        '''Adds the given item and the given count to the inventory. Count has to be > 0. Returns whether the operation was successful'''
        succ = False
        if count > 0:
            if item in self.contents:
                self.contents[item] += count
                succ = True
            elif len(self.contents) < self.capacity:
                self.contents[item] = count
                succ = True
        return succ
        
    def hasItem(self, item):
        return item in self.contents
        
    def hasItemCount(self, item, count):
        if self.hasItem(item):
            return self.contents[item] >= count
            
    def removeItem(self, item):
        '''Removes all items of this type from the inventory and returns how many there were.'''
        return self.contents.pop(item, None)
        
    def removeItemCount(self, item, count):
        '''Removes the given count of the given item if and only if enough of the item are present'''
        succ = False
        if self.hasItemCount(item, count):
            have = self.removeItem(item)
            if have - count > 0:
                self.addItem(item, have - count)
            succ = True
        return succ