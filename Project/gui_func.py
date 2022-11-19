import easygui as g
import sys
import bd_func
import config as c

data_base = bd_func.DataBase(c.db_ip, c.db_port, c.db_name)


def show_all():
    # get data from db
    button = ['<-', 'Return', '->']
    g.buttonbox('wef', 'errgrg', button)
    if button == '<-':
        pass
    elif button == 'Return':
        pass
    elif button == '->':
        pass


def add_data():
    choices = ['Name', 'Employer', 'City', 'Metro', 'Salary_min', 'Salary_max']
    button = g.multenterbox('dad', 'dad', choices)
    # set to db (button)
    return edit_menu() # add func


def edit_menu(successful=None):
    choices = ['Add', 'Delete', 'Edit', 'Return']
    lable = 'Text'
    if successful:
        lable += 'Added'

    button = g.buttonbox(lable, 'Edit Menu', choices)

    if button == 'Add':
        add_data()
    elif button in ['Delete', 'Edit']:
        search_menu(button)
    elif button == 'Return':
        return main_menu()


def main_menu():
    choices = ['Watch db', 'Search db', 'Edit db', 'Exit']
    lable = 'Select menu item'
    button = g.buttonbox(lable, 'Добро пожаловать!', choices)
    if button in ['Watch db', 'Search db', 'Edit db']:
        if button == 'Watch db':
            watch_menu()
        elif button == 'Search db':
            search_menu(button)
        else:
            edit_menu()
    elif button == 'Exit':
        sys.exit(0)


def watch_menu():
    choices = ['Show All', 'Show by search', 'Return']
    lable = 'Show by search - enter Search menu'
    button = g.buttonbox(lable, 'Watch Menu', choices)

    if button == 'Show All':
        show_all()
    elif button == 'Show by search':
        search_menu(button)
    elif button == 'Return':
        return main_menu()


def search_menu(prev_menu):
    choices = ['Search by Name', 'Search by Sallary', 'Search by Metro', 'Search by Employer', 'Return']
    lable = ''
    button = g.buttonbox(lable, 'Search Menu', choices)

    if button == 'Search by Name':
        pass
    elif button == 'Search by Sallary':
        pass
    elif button == 'Search by Metro':
        pass
    elif button == 'Search by Employer':
        pass
    elif button == 'Return':
        if prev_menu == 'Search db':
            return main_menu()
        elif prev_menu == 'Show by search':
            return watch_menu()
        elif prev_menu in ['Delete', 'Edit']:
            return edit_menu()


main_menu()
