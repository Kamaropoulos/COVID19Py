import COVID19Py

covid19 = COVID19Py.COVID19()

print("Initial State is: ",covid19.current_state)  # prints initial state of the machine (should be start_state)
covid19.transition_to_latest_data_state()  # transition from start_state to latest_data state
print("After state change, current state is: ", covid19.current_state)  # verify current state (should be latest_data state)
print("Print most recent data: ", covid19.getMostRecentData())  # call getMostRecentData() to print latest data

##***************************Optional State Change To Initial State*******************************#
covid19.transition_to_start_state()  # transition back to the initial state: start_state
print("After switching back to initial state, current state is:", covid19.current_state)  # print current status, (should be start_state)
