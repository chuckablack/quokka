from sqlalchemy import desc

from quokka import db
from quokka.models.Event import Event
from quokka.models.util import get_model_as_dict


def log_event(time, source_type, source, severity, info):

    event = dict()
    event["time"] = time
    event["source_type"] = source_type
    event["source"] = source
    event["severity"] = severity
    event["info"] = info

    event_obj = Event(**event)
    db.session.add(event_obj)

    db.session.commit()


def get_all_events(num_events):

    event_objs = (
        db.session.query(Event).order_by(desc(Event.time)).limit(num_events).all()
    )

    events = list()
    for event_obj in event_objs:
        event = get_model_as_dict(event_obj)
        events.append(event)

    return events
