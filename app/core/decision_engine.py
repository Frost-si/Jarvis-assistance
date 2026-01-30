def decide_mode(user_state):
    energy = user_state.energy
    stress = user_state.stress
    load = user_state.load

    if energy < 40 or stress > 70:
        return "recovery"
    elif load > 80:
        return "overload"
    else:
        return "normal"
