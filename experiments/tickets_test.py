print("STEP 24 RUNNING")

from tickets import create_ticket, list_tickets

new_id = create_ticket("I can't print to the office printer")
print("Created ticket:", new_id)

for ticket in list_tickets():
    print(ticket)