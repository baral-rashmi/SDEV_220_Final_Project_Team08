from django.shortcuts import render, get_object_or_404
from app.forms import ConfirmationIdForm

from app.forms import TicketPurchaseForm
from .models import ConfirmPurchase, ticket, event
from django.utils import timezone

# Create your views here.
#  defined a view function named home(). When calling this function, it’ll render an HTML file named home.html.


def home(request):
    events = event.objects.order_by("date")
    print(events)
    return render(request, 'app/home.html', {'events': events})


def purchase_ticket(request, pk):
    selected_event = get_object_or_404(event, pk=pk)
    ticket_types = ticket.objects.order_by("ticket_price")
    ticket_choices = [
        (ticket.ticket_type, f"{ticket.ticket_type} - ${ticket.ticket_price}") for ticket in ticket_types
    ]

    if request.method == 'POST':
        form = TicketPurchaseForm(request.POST, ticket_choices=ticket_choices)
        if form.is_valid():
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            ticket_type = form.cleaned_data.get('ticket_type')
            email = form.cleaned_data.get('email')

            selected_ticket = get_object_or_404(
                ticket, ticket_type=ticket_type)

            purchase_confirmation = ConfirmPurchase(
                event=selected_event,
                ticket=selected_ticket,
                first_name=first_name,
                last_name=last_name,
                email=email,
            )
            purchase_confirmation.save()

            return render(request, 'app/confirm_purchase.html', {"confirmation": purchase_confirmation})

        else:
            print("Form is not valid. Errors:")
            for field, errors in form.errors.items():
                print(f"Field: {field}")
                for error in errors:
                    print(f"  {error}")
    else:
        form = TicketPurchaseForm(ticket_choices=ticket_choices)

    return render(request, 'app/ticket_purchase.html', {'event': selected_event, 'ticket_types': ticket_types, 'form': form})


def confirmation_details(request):
    if request.method == 'POST':
        form = ConfirmationIdForm(request.POST)
        if form.is_valid():
            confirmation_id = form.cleaned_data.get('confirmation_id')

            confirmation = get_object_or_404(ConfirmPurchase, confirmation_id=confirmation_id)

            context = {
                'confirmation': confirmation,
            }

            return render(request, 'app/confirmation_details.html', context)
    else:
        form = ConfirmationIdForm()

    context = {
        'form': form,
    }

    return render(request, 'app/enter_confirmation_id.html', context)
