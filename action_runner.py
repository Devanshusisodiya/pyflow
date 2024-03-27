from celery import shared_task
from actions import repository

@shared_task 
def action_runner(actions_map, action_index_string):
    # get the action details
    current_action_details = actions_map[action_index_string]
    # base case for the recursive workflow
    if current_action_details["action"] == "end":
        print(f"INFO: Workflow completed successfully!")
        return
    
    try:
        action = repository[current_action_details["action"]]

        print(f"\n\nexecuting action {action_index_string} {action.__name__}\n\n")
        action(current_action_details["details"])
    except Exception as e:
        print(f"ERROR: something wrong running the first task {e}")

    # schedule the next action
    try:
        action_runner.apply_async(
            args=[
                actions_map, 
                current_action_details["next_action"]
            ]
        )
    except Exception as err:
        print(f"ERROR: something wrong with next action scheduling - {err}")
