class Role():
    def __init__(self, role, duty, attribute_weights = None):
        
        self.role = role
        self.duty = duty
        self.weights = attribute_weights

    def updateWeights(self, key_attributes, important_attributes):

        non_important_cap = 7
        key_atr = 10
        important_atr = 9

        #for attribute in self.weights:
            #self.weights[attribute] = min(non_important_cap, self.weights[attribute])
        
        for attribute in key_attributes:
            #if self.weights[attribute] != 0:
            self.weights[attribute] = key_atr
            #else:
            #    self.weights[attribute] = 9*key_atr

        for attribute in important_attributes:
            #if self.weights[attribute] != 0:
            self.weights[attribute] = important_atr
            #else:
            #    self.weights[attribute] = 7*important_atr

    def __repr__(self):
        return f"{self.role} on {self.duty}"

