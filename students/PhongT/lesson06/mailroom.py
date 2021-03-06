"""
Lesson 06: Assignment Mailroom-part4 Unit test
- Refactor code to support Unit testing
- Add logging
"""
import sys
import logging

# init logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# create a file handler
handler = logging.FileHandler(logger.name + 'debug.log', mode='w')
handler.setLevel(logging.INFO)

# create a logging format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# add the handlers to the logger
logger.addHandler(handler)


#
# data structure that holds a list of donors and a history of the amounts
# they have donated. This structure should be populated at first with at
# least five donors,  with between 1 and 3 donations each.
#
def get_donor_data():
    """ initial donor data list """
    return [
        {"name": "Ken Lenning", "donations": [1325, 1232.24, 16325.5]},
        {"name": "Thomas Timmy","donations": [521.3, 869.14]},
        {"name": "Jane Chung", "donations": [3259.3, 1282.74, 1525.5]},
        {"name": "Lucy Nguyen", "donations": [5253.82]},
        {"name": "Ben Cormack", "donations": [56230.25, 89532.0, 12025.8]}]


donors_data = get_donor_data()


def print_thank_you():
    """ Add or Update a donor record, then print a Thank You letter """
    while True:
        print()
        response = input(''' sub_menu --- Donation Entries ---
        Type your Full Name,
        or 'list' to display list of the donor names,
        or 'quit' to quit and return to main program prompt.
        Enter your choice here: > ''')

        if response.lower().strip() in ["q", "quit"]:
            break
        elif response.lower().strip() in ["l", "list"]:
            print_donor_list()
            continue
        else:

            amount = input("Enter Donation amount: ")
            try:
                donate_amount = float(amount)
            except ValueError as e:
                print("{} - The donation amount must be numeric!".format(e))
            else:  # no exception occurs - nothing went wrong: add or update a record

                record_id = find_donor_id(response)
                donor_to_print = add_donor_to_db(response, donate_amount, record_id)

                # now print a thank you letter
                print(get_thankyou_message(donor_to_print))


def find_donor_id(donor_name):
    """
    Find whether or not the input donor is in the db.
    :param donor_name: the donor to search for in donor db
    :return: donor key id if there is existing one in db. Otherwise return None
    """
    for index, existing_donor in enumerate(donors_data):
        if existing_donor["name"].lower().strip() == donor_name.lower().strip():
            return index
    return None


def add_donor_to_db(donor_name, amount, record_id=None):
    """
    Add a donor to the db.
    :param donor_name: a donor to add
    :param amount: donation amount
    :param record_id: record id of an existing entry in db. Equals None if is new record
    :return: a new added donor entry in db
    """
    if record_id is None:
        logger.info('Add a new record entry')
        donors_data.append({"name": donor_name, "donations": [amount]})
        return donors_data[-1]
    else:
        logger.info('Update an existing record entry')
        donors_data[record_id]["donations"].append(amount)
        return donors_data[record_id]


def get_thankyou_message(donor):
    """ generate a formatted thank you letter message"""
    message = '''Dear {}, 
            Thank you so much for your generosity with your most recent donation of ${}. 
            It will be put to very good use.
            Sincerely.'''
    return message.format(donor["name"], donor["donations"][-1])


def print_donor_list():
    """ print out list of current donors"""
    print('Below are the existing donors: ')
    for donor in donors_data:
        print('\t- ', donor["name"], ' ', donor["donations"])


def print_report():
    """ print a list of your donors, sorted by total historical donation amount. """
    width = 68
    dash = "-" * width
    print(dash)
    header = ("Donor Name", "Total Given", "Num Gifts", "Average Gift")
    print("{:20} | {:15} | {:10} | {:12}".format(*header))
    print(dash)
    for index, donor in enumerate(donors_data):
        name = donor["name"]
        total = sum(donor["donations"])
        num_gift = len(donor["donations"])
        average = total/num_gift
        print("{:22} ${:12,.2f} {:12d}     ${:12,.2f}".format(name, total, num_gift, average ))
    print(dash)


def write_letters_to_file():
    """
    goes through all the donors in donor data structure, generates a thank you
    letter, and writes it to disk as a text file.
    :return: n/a
    """
    for donor in donors_data:
        message = get_thankyou_message(donor)
        filename = donor["name"].replace(" ", "_") + ".rpt"
        logger.info("write letter to:" + donor["name"])
        with open(filename, 'w') as outfile:
            outfile.write(message)


def exit():
    """ exit the program """
    sys.exit(0)


def main_menu():
    menu_dict = {"1": print_thank_you,
                "2": print_report,
                "3": write_letters_to_file,
                "4": exit}
    while True:
        print()
        answer = str(input('''Please choose from one of the following options:
        (1) Send a Thank You
        (2) Create a Report
        (3) Send letters to everyone
        (4) Exit
        Enter your choice here: > '''))
        try:
            menu_dict[answer]()
        except KeyError as e:
            print("\n{} - Invalid input! Please type 1, 2, 3, or 4".format(e))


if __name__ == '__main__':
    main_menu()
