import easygui as g
import sys
import bd_func
import config as c

data_base = bd_func.DataBase(c.db_ip, c.db_port, c.db_name)


def edit_data():
    pass


def delete_data(data):
    if data:
        data_base.delete_vacancy_from_bd()


def show_all(ret=None, data=None):
    # get data from db
    choices = ['<-', 'Return', '->']
    if not ret:
        data_text = data_base.show_all()
    elif ret == '<-':
        data_text = data_base.show_prev()
    elif ret == '->':
        data_text = data_base.show_next()
    elif ret in ['by_salary', 'by_name', 'by_employer', 'by_city', 'by_metro']:
        data_text = data_base.search_data(ret, data)
    else:
        data_text = 'error'
    button = g.buttonbox(data_text, c.prog_name, choices)

    if button == '<-':
        return show_all(button)
    elif button == 'Return':
        return main_menu()
    elif button == '->':
        return show_all(button)


def add_data():
    choices = ['Name', 'Employer', 'City', 'Metro', 'Salary_min', 'Salary_max']
    button = g.multenterbox('dad', c.prog_name, choices)
    # set to db (button)
    return edit_menu() # add func


def edit_menu(successful=None):
    choices = ['Add', 'Delete', 'Edit', 'Return']
    lable = 'Text'
    if successful:
        lable += 'Added'

    button = g.buttonbox(lable, c.prog_name, choices)

    if button == 'Add':
        add_data()
    elif button in ['Delete', 'Edit']:
        search_menu(button)
    elif button == 'Return':
        return main_menu()


def main_menu():
    choices = ['Watch db', 'Search db', 'Edit db', 'Exit']
    lable = 'Select menu item'
    button = g.buttonbox(lable, c.prog_name, choices)
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
    button = g.buttonbox(lable, c.prog_name, choices)

    if button == 'Show All':
        show_all()
    elif button == 'Show by search':
        search_menu(button)
    elif button == 'Return':
        return main_menu()


def enter_search_data(s_type, mode):
    lable = s_type
    data = g.enterbox(lable, c.prog_name)
    if not mode:
        show_all(lable, data)
    elif mode == 'Edit':
        pass
    elif mode == 'Delete':
        delete_data(data)


def search_menu(prev_menu, mode=None):
    choices = ['Search by Name', 'Search by Sallary', 'Search by Metro', 'Search by Employer', 'Return']
    lable = ''
    button = g.buttonbox(lable, c.prog_name, choices)

    if button == 'Search by Name':
        enter_search_data('by_name', mode)
    elif button == 'Search by Sallary':
        enter_search_data('by_salary', mode)
    elif button == 'Search by Metro':
        enter_search_data('by_metro', mode)
    elif button == 'Search by Employer':
        enter_search_data('by_employer', mode)
    elif button == 'Return':
        if prev_menu == 'Search db':
            return main_menu()
        elif prev_menu == 'Show by search':
            return watch_menu()
        elif prev_menu in ['Delete', 'Edit']:
            return edit_menu()


main_menu()
