import PySimpleGUI as sg
import psycopg2

sg.theme('Reddit')
conn = psycopg2.connect(dbname='db_lab', user='soulfade',
                        host='localhost')
# cursor = conn.cursor()
#TODO: добавить клиента, починить продажи сотрудников
layoutEmployeesView = [[sg.Text('Просмотреть информацию о  покупках')], [sg.Button('Просмотр покупок')]] #done
layoutSuppliersView = [[sg.Text('Просмотреть препаратов по назначению')], [sg.Button('Просмотр препаратов')]] #done
layoutDrugsView = [[sg.Text('Просмотреть историю клиентов')], [sg.Button('Просмотр истории')]] #done
layoutPhoneView = [[sg.Text('Просмотреть продажи сотрудников')], [sg.Button('Просмотр продаж')]] #done НЕ РАБОТАЕТ
layoutPhoneInsert = [[sg.Text('Добавить номер телефона')], [sg.Button('Вставить номер')]] #done WORKS
layoutDrugInsert = [[sg.Text('Добавить лекарство')], [sg.Button('Вставить лекарство')]] #done WORKS
layoutEmployeeInsert = [[sg.Text('Добавить сотрудника')], [sg.Button('Вставить сотрудника')]]#done WORKS
layoutSupplierInsert = [[sg.Text('Добавить поставщика')], [sg.Button('Вставить поставщика')]] #done WORKS

layoutArrivalInsert = [[sg.Text('Поставка лекарства')], [sg.Button('Ввести поставку')]] #done WORKS
layoutSaleInsert = [[sg.Text('Покупка лекарства')], [sg.Button('Ввести покупку')]] #done WORKS

layoutUpdate = [[sg.Text('Обновить стоимость лекарства')], [sg.Button('Обновить')]] # done WORKS

window = sg.Window('Window Title',
                   (layoutEmployeesView, layoutSuppliersView, layoutDrugsView, layoutPhoneView,
                    layoutPhoneInsert, layoutDrugInsert, layoutEmployeeInsert, layoutSupplierInsert,
                    layoutArrivalInsert, layoutSaleInsert, layoutUpdate), size=(700, 700))
# comlist_prescription = ['painkiller', 'antidepressant', 'sorbent', 'antispasmodic', 'sedative', 'laxative']
# indlist_prescription=[1, 2, 3, 4, 5, 6]
# comlist_position = ['cashier', 'director', 'pharmacist']
# indlist_position = [2, 3, 4]
# comlist_number = ['89966669039', '89966669036', '89964449039', '87987788345', '89987654637']
# indlist_number = [1, 2, 3, 4, 5]
# comlist_supplier = ['SuperPharm', 'PharmaceuticalComp']
# indlist_supplier = [1, 2]
# comlist_drug = ['Pentalgin', 'Analgin','Activated charcoal','Polysorb','Fenasepam','Xanax','Spasgan','Persen','Microlax']
# indlist_drug = [1, 2, 3, 4, 5, 6, 7, 8, 9]
# comlist_employee = ['Stepanova Anna Pavlovna', 'Fedorov Anatoly Ivanovich', 'Somov Sergey Sergeevich']
# indlist_employee = [2, 3, 4]
# comlist_client = ['Ivanov Ivan Ivanovich', 'Petrov Petr Petrovich', 'Sokolova Anna Alekseevna']
# indlist_client = ['7316193360', '7316193361', '3345672387']



while True:
    cursor = conn.cursor()
    cursor.execute("SELECT name from employees")
    comlist_employee_2 = cursor.fetchall()
    cursor.execute("SELECT id_employee from employees")
    indlist_employee_2 = cursor.fetchall()
    # print(comlist_employee_2)

    cursor.execute("SELECT drug_type from prescriptions")
    comlist_prescription_2 = cursor.fetchall()
    cursor.execute("SELECT id_prescription from prescriptions")
    indlist_prescription_2 = cursor.fetchall()
    # print(comlist_prescription_2)

    cursor.execute("SELECT name from positions")
    comlist_position_2 = cursor.fetchall()
    cursor.execute("SELECT id_position from positions")
    indlist_position_2 = cursor.fetchall()
    # print(comlist_prescription_2)

    cursor.execute("SELECT phone_number from phone_numbers")
    comlist_number_2 = cursor.fetchall()
    cursor.execute("SELECT id_phone_number from phone_numbers")
    indlist_number_2 = cursor.fetchall()

    cursor.execute("SELECT name from suppliers")
    comlist_supplier_2 = cursor.fetchall()
    cursor.execute("SELECT id_supplier from suppliers")
    indlist_supplier_2 = cursor.fetchall()

    cursor.execute("SELECT name from drugs")
    comlist_drug_2 = cursor.fetchall()
    cursor.execute("SELECT id_drug from drugs")
    indlist_drug_2 = cursor.fetchall()

    cursor.execute("SELECT name from clients")
    comlist_client_2 = cursor.fetchall()
    cursor.execute("SELECT id_client from clients")
    indlist_client_2 = cursor.fetchall()
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break
    if event == 'Вставить номер':
        layout = [
            [sg.Text('Пожалуйста, введите необходимые данные.')],
            [sg.Text('phone_number', size=(15, 1)), sg.InputText()],
            [sg.Text('description', size=(15, 1)), sg.InputText()],
            [sg.Submit()]
        ]
        windowEntry = sg.Window('Окно ввода', layout, keep_on_top=True)
        result = ''
        while True:
            eventEntry, valuesEntry = windowEntry.read()
            if eventEntry == 'Submit':
                if str(valuesEntry[0]) != '':
                    try :
                        cursor.execute("insert into phone_numbers(id_phone_number, phone_number,description)" \
                                       "values((select max(id_phone_number) from phone_numbers)+1, {}, {});".format(
                            valuesEntry[0], "'" + str(valuesEntry[1]) + "'"))
                        conn.commit()

                    except (Exception, psycopg2.DatabaseError) as error:
                        print()
                        sg.popup("Wrong number!", keep_on_top=True)
                        conn.rollback()
                    break
                else:
                    sg.popup("Упс, вы не ввели номер телефона!", keep_on_top=True)
                conn.commit()
                # print(comlist_number)
                comlist_number_2.append(valuesEntry[0])
                cursor.execute("select max(id_phone_number)+1 from phone_numbers")
                num = cursor.fetchall()
                indlist_number_2.append(num)
                break

            if eventEntry == sg.WIN_CLOSED:
                break
        windowEntry.close()

    if event == 'Вставить лекарство':
        layout = [
            [sg.Text('Пожалуйста, введите необходимые данные.')],
            # [sg.Text('violation type'), sg.Combo(comlist, size=(10, 1))],
            [sg.Text('drug_name', size=(15, 1)), sg.InputText()],
            [sg.Text('prescription'), sg.Combo(comlist_prescription_2, size=(15, 1))],
            [sg.Text('amount', size=(15, 1)), sg.InputText()],
            [sg.Text('price', size=(15, 1)), sg.InputText()],
            [sg.Submit()]
        ]
        windowEntry = sg.Window('Окно ввода', layout, keep_on_top=True)
        result = ''
        while True:
            eventEntry, valuesEntry = windowEntry.read()
            if eventEntry == 'Submit':
                if str(valuesEntry[0]) != '':
                    cursor.execute("insert into drugs(id_drug, name, id_prescription, amount, price)" \
                                   "values((select max(id_drug) from drugs)+1, {}, {}, {}, {});".format("'" + str(valuesEntry[0]) + "'",
                        indlist_prescription_2[comlist_prescription_2.index(valuesEntry[1])], valuesEntry[2], valuesEntry[3]))
                else:
                    sg.popup("Упс, вы не ввели название препарата!", keep_on_top=True)
                conn.commit()
                comlist_drug_2.append(valuesEntry[0])
                cursor.execute("select max(id_drug)+1 from drugs")
                num = cursor.fetchall()
                indlist_drug_2.append(num)
                break

            if eventEntry == sg.WIN_CLOSED:
                break
        windowEntry.close()

    if event == 'Вставить сотрудника':
        layout = [
            [sg.Text('Пожалуйста, введите необходимые данные.')],
            # [sg.Text('violation type'), sg.Combo(comlist, size=(10, 1))],
            [sg.Text('position'), sg.Combo(comlist_position_2, size=(15, 1))],
            [sg.Text('phone_number'), sg.Combo(comlist_number_2, size=(15, 1))],
            [sg.Text('date_of_birth', size=(15, 1)), sg.InputText()],
            [sg.Text('name', size=(15, 1)), sg.InputText()],
            [sg.Submit()]
        ]
        windowEntry = sg.Window('Окно ввода', layout, keep_on_top=True)
        result = ''
        while True:
            eventEntry, valuesEntry = windowEntry.read()
            if eventEntry == 'Submit':
                if str(valuesEntry[3]) != '':
                    # try:
                    date = (valuesEntry[2]) + "'"
                    words = date.split("-")
                    year = int(words[0])
                    date = "'" + (valuesEntry[2]) + "'"
                    print(year)
                    if 2022 - year > 18:
                        cursor.execute("insert into employees(id_position, id_phone, d_o_b, name)" \
                                       "values( {}, {}, {}, {});".format(
                            # indlist_position_2[comlist_position_2.index(valuesEntry[0])],
                            list(indlist_position_2[comlist_position_2.index(valuesEntry[0])])[0],
                            list(indlist_number_2[comlist_number_2.index(valuesEntry[1])])[0],
                            date, "'" + str(valuesEntry[3]) + "'"))

                        conn.commit()
                    else:
                        sg.popup("Too young!", keep_on_top=True)
                        conn.rollback()
                    break
                    # except (Exception, psycopg2.DatabaseError) as error:
                    #     print()
                    #     sg.popup("Too young!", keep_on_top=True)
                    #     conn.rollback()
                    # break
                else:
                    sg.popup("Упс, вы не ввели имя!", keep_on_top=True)
                conn.commit()
                comlist_employee_2.append(valuesEntry[3])
                cursor.execute("select max(id_employee)+1 from employees")
                num = cursor.fetchall()
                indlist_employee_2.append(num)

                break

            if eventEntry == sg.WIN_CLOSED:
                break
        windowEntry.close()

    if event == 'Вставить поставщика':
        layout = [
            [sg.Text('Пожалуйста, введите необходимые данные.')],
            # [sg.Text('violation type'), sg.Combo(comlist, size=(10, 1))],
            [sg.Text('name', size=(15, 1)), sg.InputText()],
            [sg.Text('phone_number'), sg.Combo(comlist_number_2, size=(15, 1))],
            [sg.Submit()]
        ]
        windowEntry = sg.Window('Окно ввода', layout, keep_on_top=True)
        result = ''
        while True:
            eventEntry, valuesEntry = windowEntry.read()
            if eventEntry == 'Submit':
                if str(valuesEntry[0]) != '':
                    cursor.execute("insert into suppliers(id_supplier, name, id_phone_number)" \
                                   "values((select max(id_supplier) from suppliers)+1, {}, {});".format(
                        "'" + str(valuesEntry[0]) + "'",
                        list(indlist_number_2[comlist_number_2.index(valuesEntry[1])])[0]))
                else:
                    sg.popup("Упс, вы не ввели название!", keep_on_top=True)
                conn.commit()
                comlist_supplier_2.append(valuesEntry[0])
                # indlist_supplier_2.append(indlist_supplier_2[-1] + 1)
                cursor.execute("select max(id_supplier)+1 from suppliers")
                num = cursor.fetchall()
                indlist_supplier_2.append(num)
                break

            if eventEntry == sg.WIN_CLOSED:
                break
        windowEntry.close()


    if event == 'Просмотр покупок':
        query = """select drugs.name, sum(sales.amount_sale), date_time_sale from drugs, sales
            where drugs.id_drug = sales.id_drug
group by drugs.name, date_time_sale"""
        cursor.execute(query)
        data = cursor.fetchall()
        my_data = []
        for i in data:
            my_data.append(list(i))
        print(my_data)
        headings = ['name', 'amount', 'date']

        layout = [[sg.Table(values=my_data, headings=headings, max_col_width=35,
                            auto_size_columns=True,
                            display_row_numbers=True,
                            justification='right',
                            num_rows=20,
                            alternating_row_color='lightyellow',
                            key='-TABLE-',
                            row_height=35)]]

        windowView = sg.Window('The Table Element', layout)

        while True:
            eventView, valuesView = windowView.read()
            print(eventView, valuesView)
            if eventView == sg.WIN_CLOSED:
                break
        windowView.close()

        print("View")

    if event == 'Просмотр препаратов':
        query = """select illnesses.name, drugs.name, drug_type, amount, price from drugs,
         prescriptions, illnesses, prescription_per_illness
where illnesses.id_illness = prescription_per_illness.illness_id
  and prescription_per_illness.prescription_id = prescriptions.id_prescription
  and prescriptions.id_prescription = drugs.id_prescription"""
        cursor.execute(query)
        data = cursor.fetchall()
        my_data = []
        for i in data:
            my_data.append(list(i))
        print(my_data)
        headings = ['illness', 'drug', 'drug type', 'amount', 'price']

        layout = [[sg.Table(values=my_data, headings=headings, max_col_width=35,
                            auto_size_columns=True,
                            display_row_numbers=True,
                            justification='right',
                            num_rows=20,
                            alternating_row_color='lightyellow',
                            key='-TABLE-',
                            row_height=35)]]

        windowView = sg.Window('The Table Element', layout)

        while True:
            eventView, valuesView = windowView.read()
            print(eventView, valuesView)
            if eventView == sg.WIN_CLOSED:
                break
        windowView.close()

        print("View")

    if event == 'Просмотр истории':
        query = """select clients.name, date_of_birth, drugs.name,sales.date_time_sale, sum(sales.amount_sale) from drugs
            join sales on drugs.id_drug = sales.id_drug
            join clients on sales.id_client = clients.id_client
group by drugs.name, date_of_birth, clients.name, sales.date_time_sale"""
        cursor.execute(query)
        data = cursor.fetchall()
        my_data = []
        for i in data:
            my_data.append(list(i))
        print(my_data)
        headings = ['name', 'date_of_birth', 'drug', 'date_of_sale', 'amount']

        layout = [[sg.Table(values=my_data, headings=headings, max_col_width=35,
                            auto_size_columns=True,
                            display_row_numbers=True,
                            justification='right',
                            num_rows=20,
                            alternating_row_color='lightyellow',
                            key='-TABLE-',
                            row_height=35)]]

        windowView = sg.Window('The Table Element', layout)

        while True:
            eventView, valuesView = windowView.read()
            print(eventView, valuesView)
            if eventView == sg.WIN_CLOSED:
                break
        windowView.close()

        print("View")

        if event == 'Просмотр продаж':
            query = """select employees.name, drugs.name, sum(sales.amount_sale)*drugs.price from employees, drugs, sales
            where sales.id_employee = employees.id_employee
            and sales.id_drug = drugs.id_drug
group by employees.name, drugs.name, drugs.price"""
            cursor.execute(query)
            data = cursor.fetchall()
            my_data = []
            for i in data:
                my_data.append(list(i))
            print(my_data)
            headings = ['name', 'drug', 'sold [rub]']

            layout = [[sg.Table(values=my_data, headings=headings, max_col_width=35,
                                auto_size_columns=True,
                                display_row_numbers=True,
                                justification='right',
                                num_rows=20,
                                alternating_row_color='lightyellow',
                                key='-TABLE-',
                                row_height=35)]]

            windowView = sg.Window('The Table Element', layout)

            while True:
                eventView, valuesView = windowView.read()
                print(eventView, valuesView)
                if eventView == sg.WIN_CLOSED:
                    break
            windowView.close()

            print("View")

    if event == 'Ввести поставку':
        id_drug = 0
        id_supplier = 0
        layout = [
            [sg.Text('Пожалуйста, введите необходимые данные.')],
            [sg.Text('drug'), sg.Combo(comlist_drug_2, size=(10, 1))],
            [sg.Text('supplier'), sg.Combo(comlist_supplier_2, size=(10, 1))],
            [sg.Text('date_of_supply', size=(15, 1)), sg.InputText()],
            [sg.Text('amount', size=(15, 1)), sg.InputText()],
            [sg.Submit()]
        ]
        windowEntry = sg.Window('Окно ввода', layout, keep_on_top=True)
        while True:
            eventEntry, valuesEntry = windowEntry.read()
            if eventEntry == 'Submit':
                id_drug = list(indlist_drug_2[comlist_drug_2.index(valuesEntry[0])])[0]
                id_supplier = list(indlist_supplier_2[comlist_supplier_2.index(valuesEntry[1])])[0]
                d_o_s = str(valuesEntry[2])
                amount_drugs = valuesEntry[3]

                break

            if eventEntry == sg.WIN_CLOSED:
                break
        windowEntry.close()

        if id_drug != 0 and id_supplier != 0:
            param_list = [id_drug, id_supplier, d_o_s, amount_drugs]
            cursor.execute('CALL update_amount(%s, %s, %s, %s);', param_list)
            # data = cursor.fetchall()
            conn.commit()
            # cursor.close()
            # conn.close()
            # break
        if eventEntry == sg.WIN_CLOSED:
            break
    # windowEntry.close()

    if event == 'Ввести покупку':
        id_drug = 0
        id_employee = 0
        id_client = ''
        layout = [
            [sg.Text('Пожалуйста, введите необходимые данные.')],
            [sg.Text('drug'), sg.Combo(comlist_drug_2, size=(10, 1))],
            [sg.Text('employee'), sg.Combo(comlist_employee_2, size=(10, 1))],
            [sg.Text('sale_amount', size=(15, 1)), sg.InputText()],
            [sg.Text('date_of_sale', size=(15, 1)), sg.InputText()],
            [sg.Text('client'), sg.Combo(comlist_client_2, size=(10, 1))],
            [sg.Submit()]
        ]
        windowEntry = sg.Window('Окно ввода', layout, keep_on_top=True)
        while True:
            eventEntry, valuesEntry = windowEntry.read()
            if eventEntry == 'Submit':
                print(comlist_employee_2)
                print(indlist_employee_2)
                id_drug = list(indlist_drug_2[comlist_drug_2.index(valuesEntry[0])])[0]
                cursor.execute("select id_employee from employees where name = {}"\
                    .format(
                        "'" + str(list(valuesEntry[1])[0]) +"'" ))
                # id_employee = list(indlist_supplier_2[comlist_employee_2.index(valuesEntry[1])])[0]
                id_employee = cursor.fetchall();
                amount_drugs = valuesEntry[2]
                d_o_s = str(valuesEntry[3])
                cursor.execute("select id_client from clients where name = {}" \
                    .format(
                    "'" + str(list(valuesEntry[4])[0]) + "'"))
                # id_employee = list(indlist_supplier_2[comlist_employee_2.index(valuesEntry[1])])[0]
                id_client = cursor.fetchall();
                # id_client = str(list(indlist_drug_2[comlist_drug_2.index(valuesEntry[4])])[0])

                break

            if eventEntry == sg.WIN_CLOSED:
                break
        windowEntry.close()

        if id_drug != 0 and id_employee != 0 and id_client != '':
            values = id_employee[0]
            values_2 = id_client[0]
            # print(values[0])
            param_list = [str(id_drug), ''.join([str(value) for value in values]), amount_drugs, d_o_s, ''.join([str(value) for value in values_2])]
            # print(param_list)
            cursor.execute('CALL update_amount_sale(%s, %s, %s, %s, %s);', param_list)
            # data = cursor.fetchall()
            conn.commit()
            cursor.close()
            conn.close()
        if eventEntry == sg.WIN_CLOSED:
            break
    # windowEntry.close()

    if event == 'Обновить':
        idViolation = 0
        layout = [
            [sg.Text('Пожалуйста, введите необходимые данные.')],
            # [sg.Text('v_id', size=(15, 1)), sg.InputText()],
            [sg.Text('drug', size=(15, 1)), sg.Combo(comlist_drug_2, size=(10, 1))],
            [sg.Text('new price'), sg.InputText()],
            [sg.Submit()]
        ]
        windowEntry = sg.Window('Окно ввода', layout, keep_on_top=True)
        while True:
            eventEntry, valuesEntry = windowEntry.read()
            if eventEntry == 'Submit':
                # sg.popup("Данные введены правильно!", keep_on_top=True)
                # id_drug = int(indlist_drug_2[comlist_drug_2.index(valuesEntry[0])])
                id_drug = list(indlist_drug_2[comlist_drug_2.index(valuesEntry[0])])[0]
                new_price = valuesEntry[1]
                break

            if eventEntry == sg.WIN_CLOSED:
                break
        windowEntry.close()

        # comlist[idViolation - 1] = newViolationName
        cursor.execute("update drugs set price = {} " \
                       "where id_drug = {};".format(new_price, id_drug))
        conn.commit()

        # windowView = sg.Window('The Table Element', layout)

        if eventEntry == sg.WIN_CLOSED:
            break
        windowEntry.close()

window.close()
conn.close()

