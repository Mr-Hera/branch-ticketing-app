from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Ticket
import datetime
from .form import CreateTicketForm, UpdateTicketForm

# Create your views here.

# view ticket details
def ticket_details(req, pk):
    ticket = Ticket.objects.get(pk=pk)
    context = { 'ticket': ticket }
    return render(req, 'ticket/ticket_details.html', context)

# -----------------------------------------------------------------------------

# for customers - create ticket
def create_ticket(req):
    if req.method == 'POST':
        form = CreateTicketForm(req.POST)
        if form.is_valid():
            var = form.save(commit=False)
            var.created_by = req.users
            var.ticket_status = 'Pending'
            var.save()
            messages.info(req, 'Ticket successfully submitted and is in queue to be assigned.')
            return redirect('dashboard')
        else:
            messages.warning(req, 'Oops! Something went wrong. Please check form inputs')
            return redirect('create-ticket')
    else:
        form = CreateTicketForm()
        context = { 'form': form }
        return render(req, 'ticket/create_ticket.html', context)

# for customers - update ticket
def update_ticket(req, pk):
    ticket = Ticket.objects.get(pk=pk)
    if req.method == 'POST':
        form = UpdateTicketForm(req.POST, instance=ticket)
        if form.is_valid():
            form.save()
            messages.info(req, 'Ticket successfully updated and is in queue to be assigned.')
            return redirect('dashboard')
        else:
            messages.warning(req, 'Oops! Something went wrong. Please check form inputs')
    else:
        form = UpdateTicketForm(instance=ticket)
        context = { 'form': form }
        return render(req, 'ticket/update_ticket.html', context)

# for customers - view all tickets
def all_tickets(req):
    tickets = Ticket.objects.filter(created_by=req.user)
    context = { 'tickets': tickets }
    return render(req, 'tickets/all_tickets.html', context)

# -----------------------------------------------------------------------------

# for engineers - ticket queue
def ticket_queue(req):
    tickets = Ticket.objects.filter(ticket_status='Pending')
    context = { 'tickets': tickets }
    return render(req, 'tickets/all_tickets.html', context)

# for engineers - accept ticket
def accept_ticket(req, pk):
    tickets = Ticket.objects.get(pk=pk)
    ticket.assigned_to = request.user
    ticket.ticket_status = 'Active'
    ticket.accepted_date = datetime.datetime.now()
    ticket.save()
    messages.info(req, 'Ticket assigned successfully. Proceed to resolving.')
    return redirect('ticket-queue')

# for engineers - close ticket
def close_ticket(req, pk):
    tickets = Ticket.objects.get(pk=pk)
    ticket.ticket_status = 'Completed'
    ticket.is_resolved = True
    ticket.closed_date = datetime.datetime.now()
    ticket.save()
    messages.info(req, 'Thank you. Ticket resolved and closed successfully.')
    return redirect('ticket-queue')

# for engineers - view assigned tickets
def workspace(req):
    tickets = Ticket.objects.filter(assigned_to=req.user, is_resolved=False)
    context = { 'tickets': tickets }
    return render(req, 'ticket/workspace.html', context)

# for engineers - view closed tickets
def all_closed_tickets(req):
    tickets = Ticket.objects.filter(assigned_to=req.user, is_resolved=True)
    context = { 'tickets': tickets }
    return render(req, 'ticket/all_closed_tickets.html', context)
