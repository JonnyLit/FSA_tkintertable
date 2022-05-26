import json
import pandas as pd
from event import Event
from state import State


class FSA:
    """
    Class used to represent a Finite State Automaton (FSA)

    Parameters
    ----------
    X : list of State objects
        the set of states of which the automaton is composed
    E list of Event objects
        the alphabet of the automaton
    delta : DataFrame
        the transition relation / function of the automaton
    x0 : list of State objects
        the initial states of the automaton (all elements of x0 must be contained in X)
    Xm : list of State objects
        the final states of the automaton (all elements of Xm must be contained in X)

    """


    X = None  # States
    E = None  # Alphabet
    delta = None  # Delta relation
    x0 = None  # Initial states
    Xm = None  # Final states

    # minor Class attributes
    is_Reachable = None     # (1)yes/(0)no
    is_co_Reachable = None     # (1)yes/(0)no
    is_Blocking = None     # (1)yes/(0)no
    is_Trim = None     # (1)yes/(0)no
    is_Reversible = None     # (1)yes/(0)no

    def __init__(self, X=None, E=None, delta=None, x0=None, Xm=None, is_Reachable=None, is_co_Reachable = None, is_Blocking = None, is_Trim = None, is_Reversible = None) -> None:

        # main Class attributes
        self.X = X  # States
        self.E = E  # Alphabet
        self.delta = delta  # Delta relation
        self.x0 = x0  # Initial states
        self.Xm = Xm  # Final states
        self.is_Reachable = is_Reachable
        self.is_co_Reachable = is_co_Reachable
        self.is_Blocking = is_Blocking
        self.is_Trim = is_Trim
        self.is_Reversible = is_Reversible


    @classmethod
    def fromfile(self, filename):

        """Generates a FSA from file

        Parameters
        ----------
        filename: str
            the path of the .json file containing the definition of the FSA

        """

        # Load from file

        X = []  # States
        E = []  # Alphabet
        x0 = []  # Initial states
        Xm = []  # Final states

        # File opening

        with open(filename) as jsonFile:
            jsonObject = json.load(jsonFile)

            print("jsonfile content:")   # *****************************************************************************
            print(jsonObject)   # **************************************************************************************

        # Reading states and properties

        for key in jsonObject['X']:
            st_label = key  # State name

            if 'isInit' in jsonObject['X'][key]:
                isInit = eval(jsonObject['X'][key]['isInit'])  # Is the state initial?
            else:
                isInit = None
            if 'isFinal' in jsonObject['X'][key]:
                isFinal = eval(jsonObject['X'][key]['isFinal'])  # Is the state final?
            else:
                isFinal = None

            state = State(st_label, bool(isInit), bool(isFinal))

            if isInit:  # If the state is initial, add it to initial states
                x0.append(state)

            if isFinal:  # If the state is final, add it to final states
                Xm.append(state)
            X.append(state)

        self.Xm = Xm
        self.x0 = x0
        self.X = X
        '''
        print("Stati:", X)   # *****************************************************************************************
        print("Stati iniziali:", x0)   # *******************************************************************************
        print("Stati finali:", Xm)   # *********************************************************************************
        '''
        # Reading events and properties

        for key in jsonObject['E']:
            ev_label = key  # Event name

            if 'isObservable' in jsonObject['E'][key]:
                observable = eval(jsonObject['E'][key]['isObservable'])  # Is observable?
            else:
                observable = None
            if 'isControllable' in jsonObject['E'][key]:
                controllable = eval(jsonObject['E'][key]['isControllable'])  # Is controllable?
            else:
                controllable = None
            if 'isFaulty' in jsonObject['E'][key]:
                fault = eval(jsonObject['E'][key]['isFault'])  # Is faulty?
            else:
                fault = None

            E.append(Event(ev_label, bool(observable), controllable, fault))

        self.E=E
        '''
        print("Eventi/alfabeto:", E)   # *******************************************************************************
        '''
        data = []

        # Reading delta

        for key in jsonObject['delta']:

            start_state = jsonObject['delta'][key]['start']  # Start state

            if start_state not in [s.label for s in X]:  # Check if start state is in X
                raise ValueError("Invalid start state")
                
            else:
                
                idx = [x.label for x in X].index(start_state)
                i_state = X[idx]

            transition = jsonObject['delta'][key]['name']  # Transition

            if transition not in [e.label for e in E]:  # Check if transition is in E
                raise ValueError("Invalid event")
                
            else:
                
                idx = [x.label for x in E].index(transition)
                trans = E[idx]

            end_state = jsonObject['delta'][key]['ends']

            if end_state not in [s.label for s in X]:  # Check if end state is in X
                raise ValueError("Invalid end state")
                
            else:
                
                idx = [x.label for x in X].index(end_state)
                f_state = X[idx]

            data.append([i_state, trans, f_state])

        '''
        print("Transizioni delta:", data)   # **************************************************************************
        '''
        delta = pd.DataFrame(data, columns=["start", "transition", "end"])

        self.delta=delta
        '''
        print("Transizioni delta dataFrame view:\n", delta)   # **************************************************************************
        '''
        # return self(X, E, delta, x0, Xm)
        # return cls(X, E, delta, x0, Xm)

    @classmethod
    def print_X(self):

        """
        Prints the list of states of which the automaton is composed
        """
        '''
        states = [x.label for x in self.X]

        print(states)
        '''
        return self.X

    @classmethod
    def print_E(self):

        """
        Prints the list of events (alphabet) of which the automaton is composed
        """
        '''
        events = [x.label for x in self.E]
        print(events)
        '''
        return self.E

    @classmethod
    def print_delta(self):

        """
        Prints the delta relation / function of the automaton
        """
        '''
        print(self.delta)
        '''
        return self.delta

    @classmethod
    def filter_delta(self, start=None, transition=None, end=None):

        filt_delta = self.delta

        if start:
            condition = filt_delta["start"].apply(lambda x: x.label) == start
            filt_delta = filt_delta.loc[(condition)]

        if transition:
            condition = filt_delta["transition"].apply(lambda x: x.label) == transition
            filt_delta = filt_delta.loc[(condition)]

        if end:
            condition = filt_delta["end"].apply(lambda x: x.label) == end
            filt_delta = filt_delta.loc[(condition)]


        return filt_delta

    @classmethod
    def print_x0(self):

        '''
        in_states = [x.label for x in self.x0]
        print(in_states)
        '''
        return self.x0

    @classmethod
    def print_Xm(self):

        '''
        fin_states = [x.label for x in self.Xm]
        print(fin_states)
        '''
        return self.Xm

    @classmethod
    def add_state(self, state, isInitial=None, isFinal=None):

        if isinstance(state, State):

            if state.label not in [x.label for x in self.X]:

                self.X.append(state)

                if state.isFinal:
                    self.Xm.append(state)

                if state.isInitial:
                    self.x0.append(state)

            else:

                print("Error: We cannot have two states with the same label")
                return

        elif isinstance(state, str):

            if state not in [x.label for x in self.X]:

                new_state = State(state, isInitial, isFinal)

                self.X.append(new_state)

                if new_state.isFinal:
                    self.Xm.append(new_state)

                if new_state.isInitial:
                    self.x0.append(new_state)

            else:

                print("Error: We cannot have two states with the same label")
                return

        else:

            raise ValueError

    @classmethod
    def add_event(self, event, isObservable=None, isControllable=None, isFault=None):

        if isinstance(event, Event):

            if event not in [e.label for e in self.E]:

                self.E.append(event)

            else:

                print("Error: We cannot have two states with the same label")
                return

        elif isinstance(event, str):

            if event not in [x.label for x in self.E]:

                new_event = Event(event, isObservable, isControllable, isFault)

                self.E.append(new_event)

            else:

                print("Error: We cannot have two states with the same label")
                return

        else:

            raise ValueError

    @classmethod
    def add_transition(self, initial_state, event, end_state):
        
        try:
            
            idx = [x.label for x in self.X].index(initial_state)
            i_state = self.X[idx]
            
        except ValueError:
            
            print("Error: initial state not in X")
            return
        
        try:
            
            idx = [e.label for e in self.E].index(event)
            transition = self.E[idx]
            
        except ValueError:
            
            print("Error: event not in E")
            return
        
        try:
            
            idx = [x.label for x in self.X].index(end_state)
            e_state = self.X[idx]
            
        except ValueError:
            
            print("Error: end state not in X")
            return

        temp_df = pd.DataFrame([[i_state, transition, e_state]], columns=["start", "transition", "end"])

        self.delta = pd.concat([self.delta, temp_df], axis=0, ignore_index=True)



    @classmethod
    def get_reachability_info(self):
        reachable_states = []
        current_start_states = []
        current_start_states.append(self.x0[0])
        # print("reachable_states:\n", reachable_states)
        end_algorithm_flag = 0
        iter_loop = 0
        reachable_states.append(current_start_states[0])

        # print("reachable_states:\n", reachable_states)
        while end_algorithm_flag == 0:
            iter_loop += 1
            # print("iter_loop = ", iter_loop)
            num_failed_filtering = 0
            for i in range(len(current_start_states)):
                current_start_filtered_deltas = self.filter_delta(start=str(current_start_states[i].label), transition=None, end=None)
                if len(current_start_filtered_deltas) == 0:
                    # print("current_start_filtered_deltas:\n", current_start_filtered_deltas)
                    num_failed_filtering += 1
                    # print("num_failed_filtering = ", num_failed_filtering)
                else:
                    for iter in range(len(current_start_filtered_deltas)):
                        current_start_state = current_start_filtered_deltas.end[current_start_filtered_deltas.index[iter]]
                        if current_start_state.label not in [x.label for x in reachable_states]:
                            reachable_states.append(current_start_state)
                            current_start_states.insert(iter, current_start_state)
                            # print("reachable_states:\n", reachable_states)
                            # print("current_start_states:\n", current_start_states)
                if num_failed_filtering == len(current_start_filtered_deltas):
                    end_algorithm_flag = 1
                    # print("end_algorithm_flag = ", end_algorithm_flag)
                else:
                    pass

        for iter_x in range(len(self.X)):
            for iter_reach in range(len(reachable_states)):
                # print(str(reachable_states[iter_reach].label) + "=?=" + str(self.X[iter_x].label))
                if str(reachable_states[iter_reach].label) == str(self.X[iter_x].label):
                    self.X[iter_x].is_Reachable = 1
                    break
                else:
                    self.X[iter_x].is_Reachable = 0

        print("reachable_states:\n", reachable_states)
        if len(reachable_states) == len(self.X):
            print("The FSA is reachable")
            self.is_Reachable = 1
        else:
            print("The FSA is not reachable")
            self.is_Reachable = 0

        return self.is_Reachable

    
    
    @classmethod
    def get_co_reachability_info(self):
        co_reachable_states = []
        current_end_states = []
        for i in range(len(self.Xm)):
            current_end_states.append(self.Xm[i])
            co_reachable_states.append(self.Xm[i])
        end_algorithm_flag = 0
        iter_loop = 0
        # print("co_reachable_states:\n", co_reachable_states)
        while end_algorithm_flag == 0:
            iter_loop += 1
            # print("iter_loop = ", iter_loop)
            num_failed_filtering = 0
            for i in range(len(current_end_states)):
                current_end_filtered_deltas = self.filter_delta(start=None, transition=None, end=str(current_end_states[i].label))
                if len(current_end_filtered_deltas) == 0:
                    # print("current_end_filtered_deltas:\n", current_end_filtered_deltas)
                    num_failed_filtering += 1
                    # print("num_failed_filtering = ", num_failed_filtering)
                else:
                    for iter in range(len(current_end_filtered_deltas)):
                        current_end_state = current_end_filtered_deltas.start[current_end_filtered_deltas.index[iter]]
                        # print("current_end_states:\n", current_end_states)
                        if current_end_state.label not in [x.label for x in co_reachable_states]:
                            co_reachable_states.append(current_end_state)
                            current_end_states.insert(iter, current_end_state)
                            # print("co_reachable_states:\n", co_reachable_states)
                            # print("current_end_states:\n", current_end_states)
                if num_failed_filtering == len(current_end_filtered_deltas):
                    end_algorithm_flag = 1
                    # print("end_algorithm_flag = ", end_algorithm_flag)
                else:
                    pass

        for iter_x in range(len(self.X)):
            for iter_reach in range(len(co_reachable_states)):
                # print(str(co_reachable_states[iter_reach].label) + "=?=" + str(self.X[iter_x].label))
                if str(co_reachable_states[iter_reach].label) == str(self.X[iter_x].label):
                    self.X[iter_x].is_co_Reachable = 1
                    break
                else:
                    self.X[iter_x].is_co_Reachable = 0

        print("co_reachable_states:\n", co_reachable_states)
        if len(co_reachable_states) == len(self.X):
            print("The FSA is co_reachable")
            self.is_co_Reachable = 1
        else:
            print("The FSA is not co_reachable")
            self.is_co_Reachable = 0

        return self.is_co_Reachable


    @classmethod
    def get_blockingness_info(self):

        if self.is_Reachable == None:
            self.get_reachability_info()
        if self.is_co_Reachable == None:
            self.get_co_reachability_info()

        self.is_Blocking = 0
        for iter_x in range(len(self.X)):
            if self.X[iter_x].is_Reachable == 1 and self.X[iter_x].is_co_Reachable == 0:
                self.X[iter_x].is_Blocking = 1
                self.is_Blocking = 1
            else:
                self.X[iter_x].is_Blocking = 0


        return self.is_Blocking



    @classmethod
    def get_trim_info(self):

        if self.is_Reachable == None:
            self.get_reachability_info()
        if self.is_co_Reachable == None:
            self.get_co_reachability_info()

        if self.is_Reachable == 1 and self.is_co_Reachable == 1:
            self.is_Trim = 1
        else:
            self.is_Trim = 0

        return self.is_Trim


    @classmethod
    def get_deadness_info(self):

        for iter_x in range(len(self.X)):
            current_deltas = self.filter_delta(start=str(self.X[iter_x].label), transition=None, end=None)
            if len(current_deltas) != 0:
                self.X[iter_x].is_Dead = 0
            else:
                self.X[iter_x].is_Dead = 1


    @classmethod
    def get_co_reachability_to_x0_info(self):
        current_end_state = None
        co_reachable_to_x0_states = []
        current_end_states = []
        for i in range(len(self.x0)):
            current_end_states.append(self.x0[i])
            co_reachable_to_x0_states.append(self.x0[i])
        end_algorithm_flag = 0
        iter_loop = 0
        #print("co_reachable_to_x0_states:\n", co_reachable_to_x0_states)
        while end_algorithm_flag == 0:
            #print("end_algorithm_flag = ", end_algorithm_flag)
            iter_loop += 1
            # print("iter_loop = ", iter_loop)
            num_failed_filtering = 0
            #print("len(current_end_states) = ", len(current_end_states))
            for i in range(len(current_end_states)):
                # print("i: ", i)
                current_end_filtered_deltas = self.filter_delta(start=None, transition=None, end=str(current_end_states[i].label))
                # print("current_end_filtered_deltas:\n", current_end_filtered_deltas)
                if len(current_end_filtered_deltas) == 0:
                    #print("current_end_filtered_deltas:\n", current_end_filtered_deltas)
                    num_failed_filtering += 1
                    #print("num_failed_filtering = ", num_failed_filtering)
                else:
                    for iter in range(len(current_end_filtered_deltas)):
                        current_end_state = current_end_filtered_deltas.start[current_end_filtered_deltas.index[iter]]
                        # print("current_end_state:\n", current_end_state)
                        if current_end_state.label not in [x.label for x in co_reachable_to_x0_states]:
                            co_reachable_to_x0_states.append(current_end_state)
                            current_end_states.insert(iter, current_end_state)
                            #print("co_reachable_to_x0_states:\n", co_reachable_to_x0_states)
                            #print("current_end_states:\n", current_end_states)

                # print("num_failed_filtering :", num_failed_filtering)
                # print("len(current_end_filtered_deltas) :", len(current_end_filtered_deltas))
                if num_failed_filtering == len(current_end_filtered_deltas) or current_end_state == self.x0[0]:
                #if num_failed_filtering == len(current_end_filtered_deltas):
                    end_algorithm_flag = 1
                    # print("end_algorithm_flag = ", end_algorithm_flag)
                else:
                    pass

        for iter_x in range(len(self.X)):
            for iter_reach in range(len(co_reachable_to_x0_states)):
                # print(str(co_reachable_to_x0_states[iter_reach].label) + "=?=" + str(self.X[iter_x].label))
                if str(co_reachable_to_x0_states[iter_reach].label) == str(self.X[iter_x].label):
                    self.X[iter_x].is_co_Reachable_to_x0 = 1
                    break
                else:
                    self.X[iter_x].is_co_Reachable_to_x0 = 0

        print("co_reachable_to_x0_states:\n", co_reachable_to_x0_states)
        if len(co_reachable_to_x0_states) == len(self.X):
            print("The FSA is co_reachable to x0")
            self.is_co_Reachable_to_x0 = 1
        else:
            print("The FSA is not co_reachable to x0")
            self.is_co_Reachable_to_x0 = 0



    @classmethod
    def get_reversibility_info(self):

        if self.is_Reachable == None:
            self.get_reachability_info()
        if self.X[0].is_co_Reachable_to_x0 == None:
            self.get_co_reachability_to_x0_info()


        for iter_x in range(len(self.X)):
            if self.X[iter_x].is_Reachable == 1:
                if self.X[iter_x].is_co_Reachable_to_x0 == 0:
                    self.is_Reversible = 0
                    break
                else:
                    self.is_Reversible = 1
            else:
                pass

        return self.is_Reversible





