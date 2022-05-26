
class State():

    #minor Class attributes
    is_Reachable = None     # (1)yes/(0)no
    is_co_Reachable = None     # (1)yes/(0)no
    is_Blocking = None     # (1)yes/(0)no
    is_Dead = None     # (1)yes/(0)no
    is_co_Reachable_to_x0 = None     # (1)yes/(0)no

    def __init__(self, label=None, initial=False, final=False, is_Reachable=None, is_co_Reachable=None, is_Blocking = None, is_Dead = None, is_co_Reachable_to_x0 = None) -> None:
        self.label = label
        self.isInitial = initial
        self.isFinal = final
        self.is_Reachable = is_Reachable
        self.is_co_Reachable = is_co_Reachable
        self.is_Blocking = is_Blocking
        self.is_Dead = is_Dead
        self.is_co_Reachable_to_x0 = is_co_Reachable_to_x0

    # TODO: Setter da riscrivere
    
    def __repr__(self):
        
        return self.label
    
    def getLabel(self):

        if not self.label:

            print("Label not yet set")

        else:

            return self.label

    '''
    def setLabel(self, label):

        if isinstance(label, str):

            self.label = label

        else:

            print("Incorrect data type: the label must be a string")
            
    '''

    def getFinal(self):

        return self.isFinal

    '''

    def setFinal(self, state, isFinal):

        self.isFinal = isFinal
        
    '''

    def getInitial(self):

        return self.isInitial

    '''

    def setInitial(self, state, initial):

        self.isInitial = initial

    '''

    def __eq__(self, other):
        return self.label == other.label
