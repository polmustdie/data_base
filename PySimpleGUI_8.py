import PySimpleGUI as sg
import psycopg2

sg.theme('Reddit')
conn = psycopg2.connect(dbname='postgres', user='soulfade',
                        host='localhost')
cursor = conn.cursor()


layoutInsert = [[sg.Text('Вставить новое нарушение')], [sg.Button('Вставить')]]

layoutView = [[sg.Text('Просмотреть список водителей, совершивших нарушение в\n определенный временной промежуток')], [sg.Button('Просмотр')]]

layoutAdd = [[sg.Text('Добавить машину')], [sg.Button('Добавить')]]
layoutUpdate = [[sg.Text('Обновить тип нарушения')], [sg.Button('Обновить')]]

window = sg.Window('Window Title', (layoutInsert, layoutView, layoutAdd, layoutUpdate), size=(500, 300))
comlist = ['drunk driving', 'speeding', 'person hit', 'wrong parking', 'running a red light', 'going through stop line']
indlist=[1, 2, 3, 4, 5, 6]

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break
    if event == 'Вставить':
        layout = [
            [sg.Text('Пожалуйста, введите необходимые данные. \nМожно не вводить поле даты, тогда автоматически '
                     'будет поставлена текущая')],
            #sg.Text('id', size=(15, 1)), sg.InputText()],[
            #[sg.Text('violation_type_id', size=(15, 1)), sg.InputText()],
            [sg.Text('violation type'), sg.Combo(comlist, size=(10, 1))],
            [sg.Text('car_id', size=(15, 1)), sg.InputText()],
            [sg.Text('date', size=(15, 1)), sg.InputText()],
            [sg.Submit()]
        ]
        windowEntry = sg.Window('Окно ввода', layout, keep_on_top=True)
        _date = "null"
        result = ''
        while True:
            eventEntry, valuesEntry = windowEntry.read()
            if eventEntry == 'Submit':
                if str(valuesEntry[2]) != '':
                    cursor.execute("insert into violations(violation_type_id, car_id,violation_date)"\
                        "values({}, {}, {});".format(indlist[comlist.index(valuesEntry[0])],  #wrong, inserts current date
                                                     valuesEntry[1], "'" + str(valuesEntry[2]) + "'"))
                else:
                    cursor.execute("insert into violations(violation_type_id, car_id)" \
                                   "values({}, {});".format(indlist[comlist.index(valuesEntry[0])], valuesEntry[1]))
                conn.commit()
                break


            if eventEntry == sg.WIN_CLOSED:
                break
            elif event == 'Date Popup':
                sg.popup('You chose:', sg.popup_get_date())
        windowEntry.close()
    if event == 'Просмотр':

        idViolation = 0
        layout = [
            [sg.Text('Пожалуйста, введите необходимые данные.')],
            [sg.Text('_start', size=(15, 1)), sg.InputText()],
            [sg.Text('_end', size=(15, 1)), sg.InputText()],
            #[sg.Text('v_id', size=(15, 1)), sg.InputText()],
            [sg.Text('violation type'), sg.Combo(comlist, size=(10, 1))],
            [sg.Submit()]
        ]
        windowEntry = sg.Window('Окно ввода', layout, keep_on_top=True)
        while True:
            eventEntry, valuesEntry = windowEntry.read()
            if eventEntry == 'Submit':
                idViolation = int(indlist[comlist.index(valuesEntry[2])])
                startDate = str(valuesEntry[0])
                endDate = str(valuesEntry[1])

                break

            if eventEntry == sg.WIN_CLOSED:
                break
        windowEntry.close()

        if idViolation != 0:
            param_list = [startDate, endDate, idViolation]
            cursor.callproc('func8', param_list)
            data = cursor.fetchall()
            my_data = []
            for i in data:
                my_data.append(list(i))
            print(my_data)
            headings = ['driver_id', 'driver_name', 'driver_d_o_b', 'car_id', 'car_color', 'car_model', 'v_date']

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
    if event == 'Добавить':
        idViolationType = 0
        layout = [
            [sg.Text('Пожалуйста, введите необходимые данные.')],
            [sg.Text('car_vin', size=(15, 1)), sg.InputText()],
            [sg.Text('color', size=(15, 1)), sg.InputText()],
            [sg.Text('id_driver', size=(15, 1)), sg.InputText()],
            [sg.Text('model', size=(15, 1)), sg.InputText()],
            [sg.Text('Пожалуйста, введите необходимые данные для второй машины.')],
            [sg.Text('car_vin2', size=(15, 1)), sg.InputText()],
            [sg.Text('color2', size=(15, 1)), sg.InputText()],
            [sg.Text('id_driver2', size=(15, 1)), sg.InputText()],
            [sg.Text('model2', size=(15, 1)), sg.InputText()],
            [sg.Submit()]
        ]

        windowEntry = sg.Window('Окно ввода', layout, keep_on_top=True)
        while True:
            eventEntry, valuesEntry = windowEntry.read()
            if eventEntry == 'Submit':
                if type(valuesEntry[0]) == str and type(valuesEntry[2]) == str:
                    #sg.popup("Ура, данные введены правильно!", keep_on_top=True)
                    try:
                        cursor.execute("INSERT INTO cars(car_vin, color, id_driver, model)" \
                                       " VALUES({}, {}, {}, {});".format(valuesEntry[0], valuesEntry[1],
                                                                         valuesEntry[2], valuesEntry[3]))
                        cursor.execute("INSERT INTO cars(car_vin, color, id_driver, model)" \
                                       " VALUES({}, {}, {}, {});".format(valuesEntry[4], valuesEntry[5],
                                                                         valuesEntry[6], valuesEntry[7]))
                        # cursor.execute("delete from author where idAuthor = {};".format(int(valuesEntry[0])))
                        # cursor.execute("delete from author where idAuthor = {};".format(int(valuesEntry[1])))
                        conn.commit()
                    except (Exception, psycopg2.DatabaseError) as error:
                        print()
                        sg.popup("Ошибка в транзакции. Отмена всех остальных операций транзакции", keep_on_top=True)
                        conn.rollback()
                    break
                else:
                    sg.popup("Ошибка, вы не ввели необходимый параметр", keep_on_top=True)
            if eventEntry == sg.WIN_CLOSED:
                break
        windowEntry.close()

    if event == 'Обновить':
        idViolation = 0
        layout = [
            [sg.Text('Пожалуйста, введите необходимые данные.')],
            # [sg.Text('v_id', size=(15, 1)), sg.InputText()],
            [sg.Text('violation type', size=(15, 1)), sg.Combo(comlist, size=(10, 1))],
            [sg.Text('new violation type'), sg.InputText()],
            [sg.Submit()]
        ]
        windowEntry = sg.Window('Окно ввода', layout, keep_on_top=True)
        while True:
            eventEntry, valuesEntry = windowEntry.read()
            if eventEntry == 'Submit':
                # sg.popup("Данные введены правильно!", keep_on_top=True)
                idViolation = int(indlist[comlist.index(valuesEntry[0])])
                newViolationName = valuesEntry[1]
                break

            if eventEntry == sg.WIN_CLOSED:
                break
        windowEntry.close()


        comlist[idViolation-1] = newViolationName
        cursor.execute("update violation_types set violation_description = {} " \
                                   "where violation_type = {};".format("'" + str(newViolationName) + "'", idViolation))
        conn.commit()

        #windowView = sg.Window('The Table Element', layout)

        if eventEntry == sg.WIN_CLOSED:
            break
        windowEntry.close()



window.close()
conn.close()

