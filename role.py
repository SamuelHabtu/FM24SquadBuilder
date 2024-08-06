class Role():
    def __init__(self, role, duty, attribute_weights = None):
        
        self.role = role
        self.duty = duty
        self.weights = attribute_weights

    def updateWeights(self, key_attributes, important_attributes):

        non_important_cap = 3.0
        key_atr = 10.0
        important_atr = 8.0

        for attribute in self.weights:
            self.weights[attribute] = min(non_important_cap, self.weights[attribute])
        
        for attribute in key_attributes:
            self.weights[attribute] = key_atr

        for attribute in important_attributes:
            self.weights[attribute] = important_atr

