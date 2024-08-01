class Player():

    def __init__(self, name, attributes = None):
        '''
        Class that will have player information:

        Attributes of the class:
            name: Name of the player
            attributes: a dictionairy of the players attributes
        '''
        self.name = name
        self.attributes = attributes if attributes is not None else {}
    def getAttributes(self):
        return self.attributes