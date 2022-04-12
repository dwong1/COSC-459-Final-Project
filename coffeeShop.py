import simpy
import random
import numpy

NUM_CUSTOMERS = 100                          
NUM_CASHIERS = 1
NUM_BARISTAS = 1

#Menus for the coffee shop
Menu = {1:["Regular Coffee",10,15],
        2:["Latte",30,45], 
        3:["Mocha",30,45], 
        4:["Cold Brew",10,20], 
        5:["Frappe",50,70], 
        6:["Espresso",20,35]}

#Payments required for coffee
Payment = {1:["Cash",15,30], 
            2:["Card",10,20]}

Payment_Wait_Time = []  #list to hold the time until a cashier is available
Payment_Time = []       #list to hold the time taken to make payments
Order_Wait_Time = []    #list to hold te time until a barista is available
Order_Time = []         #list to hold the time taken to prepare the order

#Creates a customer
def create_customer(env, cashier, barista):
    for i in range(NUM_CUSTOMERS):
        yield env.timeout(random.randint(1,20))
        env.process(customer(env, i, cashier, barista))


def customer(env, name, cashier, barista):
    print("Customer %s arrived at time %.1f" % (name, env.now))
    with cashier.request() as req:
        start_cq = env.now
        yield req
        Payment_Wait_Time.append(env.now-start_cq)
        menu_item = random.randint(1,6)
        payment_type = random.randint(1,2)
        time_to_order = random.randint(Payment[payment_type][1], Payment[payment_type][2])
        payment_name = Payment[payment_type][0]
        yield env.timeout(time_to_order)
        print("> > > Customer %s finished paying by %s in %.1f seconds" % (name, payment_name, env.now-start_cq))
        Payment_Time.append(env.now-start_cq)
        
    with barista.request() as req:
        start_bq = env.now
        yield req
        Order_Wait_Time.append(env.now-start_bq)        
        time_to_prepare = random.randint(Menu[menu_item][1], Menu[menu_item][2])
        item_name = Menu[menu_item][0]
        yield env.timeout(time_to_prepare)
        print(">> >> >> Customer %s served %s in %.1f seconds" % (name, item_name, env.now-start_cq))
        Order_Time.append(env.now-start_cq)

env = simpy.Environment()
cashier = simpy.Resource(env, NUM_CASHIERS)
barista = simpy.Resource(env, NUM_BARISTAS)

env.process(create_customer(env, cashier, barista))
env.run(until=400)

print("\n\nWITH %s CASHIERS and %s BARISTAS and %s SERIALLY ARRIVING CUSTOMERS..." % (NUM_CASHIERS, NUM_BARISTAS, NUM_CUSTOMERS))
print("Average wait time in payment queue: %.1f seconds." % (numpy.mean(Payment_Wait_Time)))
print("Average time until making the payment: %.1f seconds." % (numpy.mean(Payment_Time)))
print("Average wait time in order queue: %.1f seconds." % (numpy.mean(Order_Wait_Time)))
print("Average time until order is serviced: %.1f seconds." % (numpy.mean(Order_Time)))