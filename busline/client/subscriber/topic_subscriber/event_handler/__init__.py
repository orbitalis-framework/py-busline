import inspect
from typing import TypeVar, Callable, Coroutine, Optional, Dict

from busline.client.subscriber.topic_subscriber.event_handler.callback_event_handler import CallbackEventHandler, \
    SchemafullCallbackEventHandler
from busline.event.event import Event


F = TypeVar('F', bound=Callable[[str, Event], Coroutine])





def event_handler(func):
    def decorator(method_or_func):
        if not inspect.iscoroutinefunction(method_or_func):
            raise TypeError("Event handler must be an async function or method.")

        is_method = 'self' in method_or_func.__code__.co_varnames

        if not is_method:
            # standalone async function
            return CallbackEventHandler(on_event_callback=method_or_func)

        # method in a class
        method_name = method_or_func.__name__

        class HandlerDescriptor:
            def __get__(self, instance, owner):
                if instance is None:
                    return self

                # callback that binds the method to self
                async def callback(topic: str, event: Event):
                    await method_or_func(instance, topic, event)

                handler = CallbackEventHandler(on_event_callback=callback)

                # replace the method with the handler
                setattr(instance, method_name, handler)
                return handler

        return HandlerDescriptor()

    return decorator(func)


def schemafull_event_handler(schema: Dict):
    def decorator(method_or_func):
        if not inspect.iscoroutinefunction(method_or_func):
            raise TypeError("Event handler must be an async function or method.")

        is_method = 'self' in method_or_func.__code__.co_varnames

        if not is_method:
            # standalone async function
            return SchemafullCallbackEventHandler(schema=schema, on_event_callback=method_or_func)

        # method in a class
        method_name = method_or_func.__name__

        class HandlerDescriptor:
            def __get__(self, instance, owner):
                if instance is None:
                    return self

                # callback that binds the method to self
                async def callback(topic: str, event: Event):
                    await method_or_func(instance, topic, event)

                handler = SchemafullCallbackEventHandler(schema=schema, on_event_callback=callback)

                # replace the method with the handler
                setattr(instance, method_name, handler)
                return handler

        return HandlerDescriptor()

    return decorator



