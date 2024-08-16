# summary
I want to include a feature on the timeslots page. Whenever the user clicks a slot, 
it should light up, slide over, and show a 'Book Now' button.

## thoughts
the tool i want to focus on utilizing in this project is mostly htmx.
this library should have a way of allowing me to do this. 

an hx-get or hx-post will be needed to fetch the UI updates, but what content should 
i put in that response?

if i just include the button, i will still have to track state separately in client-side
javascript. so i probably need to think about what i need to know state.

state determiners:
- BookingID of the clicked button

based on this ID, the page should have only that timeslot include a button.
i will still need to update all other timeslots because any one of them may have been
clicked before and the unclicked component should render. 

## plan
1. make a single component which includes at least the timeslots
2. add a route which returns a version of that component which accepts a booking_id
3. use the booking_id in a Jinja if block to render all time slots and include the button on match
