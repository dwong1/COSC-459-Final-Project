#https://joecoelhosj.github.io/tutorial/simpy-example/
#The above guide was followed, the code below is commented to show we understand the process the guide writer followed to acheive the results

#Required packages
import simpy
import random
import numpy

#Constants for testing
NUM_CUSTOMERS = 20                          
NUM_CASHIERS = 1
NUM_BARISTAS = 1

#Items on menu for the coffee shop
#Dictionary has item name as well as time it takes to prepare each item
Menu = {1:["Regular Coffee",10,15],
        2:["Latte",30,45], 
        3:["Mocha",30,45], 
        4:["Cold Brew",10,20], 
        5:["Frappe",50,70], 
        6:["Espresso",20,35]}

#The time each payment method requires to process
Payment = {1:["Cash",15,30], 
           2:["Card",10,20]}

#List to hold the time until a cashier is available
Payment_Wait_Time = []

#List to hold the time taken to make payments
Payment_Time = []

#List to hold the time until a barista is available
Order_Wait_Time = []

#List to hold the time taken to prepare the order
Order_Time = []         

#Generates customers
def generate_customer (env, cashier, barista):
    for i in range(NUM_CUSTOMERS):
        yield env.timeout(random.randint(1,20))
        env.process(simulation(env, i, cashier, barista))


def simulation (env, name, cashier, barista):
    
    #Prints customer number as well as arrival time
    print("Customer %s arrived at time %.1f" % (name, env.now))
   
    with cashier.request() as req:
        start_cashier_que = env.now
        yield req
        Payment_Wait_Time.append(env.now-start_cashier_que)
        menu_item = random.randint(1,6)
        payment_type = random.randint(1,2)
        time_to_order = random.randint(Payment[payment_type][1], Payment[payment_type][2])
        payment_name = Payment[payment_type][0]
        yield env.timeout(time_to_order)
        print("Customer %s finished paying by %s in %.1f seconds" % (name, payment_name, env.now-start_cashier_que))
        Payment_Time.append(env.now-start_cashier_que)
        
    with barista.request() as req:
        start_barista_que = env.now
        yield req
        Order_Wait_Time.append(env.now-start_barista_que)        
        time_to_prepare = random.randint(Menu[menu_item][1], Menu[menu_item][2])
        item_name = Menu[menu_item][0]
        yield env.timeout(time_to_prepare)
        print("Customer %s served %s in %.1f seconds" % (name, item_name, env.now-start_cashier_que))
        Order_Time.append(env.now-start_cashier_que)

#Creates simulation enviornment
env = simpy.Environment()

cashier = simpy.Resource(env, NUM_CASHIERS)
barista = simpy.Resource(env, NUM_BARISTAS)
env.process(generate_customer(env, cashier, barista))
#Run for 6.5 minutes
env.run(until=400)

print("\n\nWITH %s CASHIERS and %s BARISTAS and %s SERIALLY ARRIVING CUSTOMERS..." % (NUM_CASHIERS, NUM_BARISTAS, NUM_CUSTOMERS))
print("Average wait time in payment queue: %.1f seconds." % (numpy.mean(Payment_Wait_Time)))
print("Average time until making the payment: %.1f seconds." % (numpy.mean(Payment_Time)))
print("Average wait time in order queue: %.1f seconds." % (numpy.mean(Order_Wait_Time)))
print("Average time until order is serviced: %.1f seconds." % (numpy.mean(Order_Time)))