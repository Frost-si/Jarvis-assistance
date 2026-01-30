def apply_mode_to_tasks(mode, tasks):
    updated = []

    for task in tasks:

        # RECOVERY MODE
        if mode == "recovery":
            if task.energy_cost == "high" or task.difficulty == "heavy":
                if task.flexible:
                    task.status = "delayed"
            else:
                task.difficulty = "light"
                task.priority = 1

        # OVERLOAD MODE
        elif mode == "overload":
            if task.time_cost == "long" and task.flexible:
                task.status = "delayed"

        # NORMAL MODE
        elif mode == "normal":
            task.difficulty = "normal"

        updated.append(task)

    return updated
