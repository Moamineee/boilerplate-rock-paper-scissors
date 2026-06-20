# The example function below keeps track of the opponent's history and plays whatever the opponent played two plays ago. It is not a very good player so you will need to change the code to pass the challenge.
def player(prev_play, opponent_history=[], my_history=[]):
    # Detect start of a new match and reset all state
    if prev_play == "":
        opponent_history.clear()
        my_history.clear()
    else:
        opponent_history.append(prev_play)

    beats = {"R": "P", "P": "S", "S": "R"}
    n = len(opponent_history)

    if not my_history:
        my_history.append("R")
        return "R"

    # ── KRIS: deterministic check, beats[my_history[-1]] every round ─
    if n >= 3:
        kris_match = sum(
            1 for i in range(1, n)
            if opponent_history[i] == beats[my_history[i - 1]]
        )
        kris_total = n - 1
        if kris_match == kris_total:
            move = beats[beats[my_history[-1]]]
            my_history.append(move)
            return move

    # ── QUINCY: fixed 5-cycle ─────────────────────────────────────────
    quincy_choices = ["R", "R", "P", "P", "S"]
    if n >= 5:
        quincy_match = sum(
            1 for i in range(min(10, n))
            if opponent_history[-(i + 1)] == quincy_choices[(n - i) % 5]
        )
        if quincy_match >= 9:
            quincy_next = quincy_choices[(n + 1) % 5]
            move = beats[quincy_next]
            my_history.append(move)
            return move

    # ── MRUGESH: verify retroactively before trusting it ─────────────
    if len(my_history) >= 11 and n >= 11:
        checks = 0
        correct = 0
        for i in range(10, n):
            window = my_history[i - 10:i]
            if len(window) < 10:
                continue
            most_freq = max(set(window), key=window.count)
            expected = beats[most_freq]
            checks += 1
            if opponent_history[i] == expected:
                correct += 1
        if checks >= 3 and correct == checks:
            last_ten = my_history[-10:]
            most_freq = max(set(last_ten), key=last_ten.count)
            mrugesh_move = beats[most_freq]
            move = beats[mrugesh_move]
            my_history.append(move)
            return move

    # ── ABBEY (default fallback, also used for early game) ────────────
    abbey_order = {
        "RR": 0, "RP": 0, "RS": 0,
        "PR": 0, "PP": 0, "PS": 0,
        "SR": 0, "SP": 0, "SS": 0,
    }
    for i in range(1, len(my_history)):
        pair = my_history[i - 1] + my_history[i]
        if pair in abbey_order:
            abbey_order[pair] += 1

    our_last = my_history[-1]
    potential = [our_last + "R", our_last + "P", our_last + "S"]
    sub = {k: abbey_order[k] for k in potential}
    abbey_predicts_we_play = max(sub, key=sub.get)[-1]
    abbey_move = beats[abbey_predicts_we_play]
    move = beats[abbey_move]
    my_history.append(move)
    return move
