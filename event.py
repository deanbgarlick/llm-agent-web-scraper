subscribers = {}

def subscribe(event_name, fn):
    if event_name not in subscribers:
        subscribers[event_name] = []
    subscribers[event_name].append(fn)

def publish(event_name, data):
    if event_name in subscribers:
        for fn in subscribers[event_name]:
            fn(data)
