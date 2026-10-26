import sys
from customer_support_crew.crew import CustomerSupportCrew

def run():
    inputs = {
        'customer_query': 'What is your policy on damaged product refunds?'
    }
    CustomerSupportCrew().crew().kickoff(inputs=inputs)

if __name__ == '__main__':
    run()
