from django.db import transaction
from datetime import datetime
from django.utils import timezone


from django.db.models import QuerySet

from db.models import Order, Ticket, User, MovieSession


def create_order(tickets: list[dict],
                 username: str, date:
                 datetime = None):
    if date is None:
        movie_session_id = tickets[0]['movie_session']
        movie_session = MovieSession.objects.get(id=movie_session_id)
        date = movie_session.show_time
    elif isinstance(date, str):
        date = datetime.strptime(date, "%Y-%m-%d %H:%M")
    with transaction.atomic():
        user = User.objects.get(username=username)
        order = Order.objects.create(created_at=date, user=user)
        for ticket in tickets:
            movie_session = MovieSession.objects.get(id=ticket['movie_session'])
            ticket['movie_session'] = movie_session
            Ticket.objects.create(order=order, **ticket)

        return order

def get_orders(username: str = None) -> QuerySet:
    if not username:
        return Order.objects.all()
    else:
        return Order.objects.filter(user__username=username)