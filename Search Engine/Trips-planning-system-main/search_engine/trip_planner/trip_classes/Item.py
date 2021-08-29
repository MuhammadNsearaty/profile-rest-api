class Item:
    def __init__(self,location, item_type: str, jsn: dict):
        self.city = location
        self.item_type = item_type
        self.name = jsn['name']
        self.item_id = jsn['id']
        self.coordinate = jsn['coordinate']
        self.rate = jsn['guestrating']
        self.distance = jsn.get('distance', 0)
        self.kinds = jsn.get('kinds', '').split(' ')

    def __repr__(self):
        # return f'{self.coordinate["lat"]},{self.coordinate["lon"]}'
        # return 'Item("%s",{"name":"","id":"%s","coordinate":%s,"guestrating":"%s"})' % (
        # self.item_type, self.item_id, self.coordinate
        # , self.rate)
        return self.item_type
