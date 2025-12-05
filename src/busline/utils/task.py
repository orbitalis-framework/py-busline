import asyncio

_background_tasks = set()

def fire_and_forget_task(coro):
    """Create a task safe from Garbage Collection."""
    
    task = asyncio.create_task(coro)
    
    _background_tasks.add(task)
    
    # Remove the task from the set when it's done
    task.add_done_callback(_background_tasks.discard)