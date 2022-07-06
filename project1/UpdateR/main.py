import geopy.distance
from const import *
import pygsheets
import sqlite3 as sq
import datetime
from usefulFun import *
from Yandex_parser import get_Y_time_km
import schedule


def update():

    print('start')

    current_time = datetime.datetime.now()
    timestamp = current_time.timestamp()

    # -------- GET NEW DATA FROM GOOGLE (lat lng vel) --------

    gc = pygsheets.authorize(service_file='secret.json')
    sh = gc.open_by_key('1xnkJuqTwRnKZRYtNPxeJ4BkbPEN_a3zFqv9RkXZtodM')
    wks = sh.worksheet_by_title('Table')

    length = 83
    load = wks.get_values('A2', 'I84'.format(length))
    tsm_load = wks.get_values('AJ2', 'AJ84'.format(length))

    Air_y_url = []; Air_y_min = []; Air_y_km = []; Air_msg = []; Air_time = []; Air_car_driver = []; Air_car_num = []
    Air_car_tsm = []; Air_zone = []; Air_task_full = []; Air_task_left = []; Air_uid = []

    lat = []; lng = []; vel = []; chat_id = []; phone = []; uid = []; car_driver = []; car_driver_short = []
    car_num = []; in_zoneList = []; tsm = []

    for i in range(0, length):
        lat.append(load[i][6])
        lng.append(load[i][7])
        vel.append(load[i][8])
        chat_id.append(load[i][0])
        phone.append(load[i][1])
        uid.append(load[i][2])
        car_driver.append(load[i][4])
        car_driver_short.append(load[i][5])
        car_num.append(load[i][3])
        tsm.append(tsm_load[i][0])

    # -------- GET OLD DATA FROM SQLITE DB --------

    # base = sq.connect('../log.db')
    # base = sq.connect('/Users/mac/Desktop/site/project1/log.db')
    base = sq.connect('/Users/mac/Desktop/site/project1/db.sqlite3')

    cur = base.cursor()
    if base:
        print('Data base connected OK!')
    cur.execute("SELECT lat,lng FROM logistic_coor")
    lat_lng_old = cur.fetchall()
    cur.execute("SELECT in_zoneList FROM logistic_coor")
    was_in_zonelist_load = cur.fetchall()
    cur.execute("SELECT airport_msg FROM logistic_coor")
    airport_msg_load = cur.fetchall()
    cur.execute("SELECT airport_msg_time FROM logistic_coor")
    airport_msg_time_load = cur.fetchall()
    cur.execute("SELECT zone FROM logistic_coor")
    zoneList_load = cur.fetchall()

    cur.execute("SELECT task_full_name FROM logistic_coor")
    task_full_name_load = cur.fetchall()
    cur.execute("SELECT task_full_coor FROM logistic_coor")
    task_full_coor_load = cur.fetchall()
    cur.execute("SELECT task_left_name FROM logistic_coor")
    task_left_name_load = cur.fetchall()
    cur.execute("SELECT task_right_name FROM logistic_coor")
    task_right_name_load = cur.fetchall()
    cur.execute("SELECT task_left_coor FROM logistic_coor")
    task_left_coor_load = cur.fetchall()
    cur.execute("SELECT task_right_coor FROM logistic_coor")
    task_right_coor_load = cur.fetchall()
    cur.execute("SELECT rope_ZoneCoorList FROM logistic_coor")
    rope_ZoneCoorList_load = cur.fetchall()

    cur.execute("SELECT isTask FROM logistic_coor")
    isTask_load = cur.fetchall()
    cur.execute("SELECT task_amount FROM logistic_coor")
    task_amount_load = cur.fetchall()
    cur.execute("SELECT task_cur FROM logistic_coor")
    task_cur_load = cur.fetchall()

    cur.execute("SELECT y_url FROM logistic_coor")
    y_url_load = cur.fetchall()
    cur.execute("SELECT y_min FROM logistic_coor")
    y_min_load = cur.fetchall()
    cur.execute("SELECT y_km FROM logistic_coor")
    y_km_load = cur.fetchall()

    airport_msg = [''] * length
    airport_msg_time = [''] * length
    was_in_zonelist = [''] * length
    zoneList = [''] * length

    task_full_name = [''] * length
    task_full_coor = [''] * length
    task_left_name = [''] * length
    task_right_name = [''] * length
    task_left_coor = [''] * length
    task_right_coor = [''] * length
    rope_ZoneCoorList = [''] * length

    y_url = [''] * length
    y_min = [''] * length
    y_km = [''] * length

    isTask = [''] * length
    task_amount = [''] * length
    task_cur = [''] * length

    for i in range(0, length):
        airport_msg[i] = airport_msg_load[i][0]
        airport_msg_time[i] = airport_msg_time_load[i][0]
        was_in_zonelist[i] = was_in_zonelist_load[i][0]
        zoneList[i] = zoneList_load[i][0]

        task_full_name[i] = task_full_name_load[i][0]
        task_full_coor[i] = task_full_coor_load[i][0]
        task_left_name[i] = task_left_name_load[i][0]
        task_right_name[i] = task_right_name_load[i][0]
        task_left_coor[i] = task_left_coor_load[i][0]
        task_right_coor[i] = task_right_coor_load[i][0]
        rope_ZoneCoorList[i] = rope_ZoneCoorList_load[i][0]

        isTask[i] = isTask_load[i][0]
        task_amount[i] = task_amount_load[i][0]
        task_cur[i] = task_cur_load[i][0]

        y_url[i] = y_url_load[i][0]
        y_min[i] = y_min_load[i][0]
        y_km[i] = y_km_load[i][0]

    car_num_short = []
    for num in car_num:
        car_num_short.append(num[1:4])

    in_zoneList = was_in_zonelist[:]
    prev_zoneList = zoneList[:]

    # ------------------------------------ IF HAS TASK ------------------------------------ ENTER

    for i in range(0, length):
        if int(isTask[i]) == 1 and int(was_in_zonelist[i]) == 0:
            target = strToCoor(task_left_coor[i])
            CTT = geopy.distance.geodesic((float(lat[i].replace(",", ".")), float(lng[i].replace(",", "."))), target).km
            print('ctt=', CTT)
            if CTT < 0.5:
                in_zoneList[i] = 1
                rope_ZoneCoorList[i] = str(target)

                airport_msg[i] = f'enter {task_left_name[i]}'
                airport_msg_time[i] = current_time

                if int(task_cur[i]) == int(task_amount[i]):
                    # FINISH
                    print('finish')
                    isTask[i] = 0
                    task_cur[i] = 0
                    task_amount[i] = 0
                    task_right_coor[i] = '-'
                    task_left_coor[i] = '-'
                    task_right_name[i] = '-'
                    task_left_name[i] = '-'
                    task_full_name[i] = '-'
                    task_full_coor[i] = '-'
                    rope_ZoneCoorList[i] = '-'
                    zoneList[i] = task_left_name[i]
                    # break
                else:
                    print(task_right_coor[i])
                    # MOVE TARGET COOR
                    tmp_coor = strToCoorBig(task_right_coor[i])
                    task_left_coor[i] = str(tmp_coor[0])
                    del tmp_coor[0]
                    task_right_coor[i] = str(tmp_coor)

                    # MOVE TARGET NAME
                    zoneList[i] = task_left_name[i]
                    tmp_name = strToNameVec(task_right_name[i])
                    task_left_name[i] = str(tmp_name[0])
                    del tmp_name[0]
                    task_right_name[i] = str(tmp_name)

                    # if int(task_cur[i]) == int(task_amount[i]):
                    #     # FINISH
                    #     print('finish')
                    #     isTask[i] = 0

                    print('yes')

                airport_msg[i] = f'enter {zoneList[i]}'
                airport_msg_time[i] = current_time

                Air_y_url.append('-')
                Air_y_min.append('-')
                Air_y_km.append('-')
                Air_msg.append(airport_msg[i])
                Air_time.append(airport_msg_time[i])
                Air_car_driver.append(car_driver[i])
                Air_car_num.append(car_num[i])
                Air_car_tsm.append(tsm[i])
                Air_zone.append(zoneList[i])
                Air_task_full.append(task_full_name[i])
                Air_task_left.append(task_left_name[i])
                Air_uid.append(uid[i])

            else:
                print('no')

    # ------------------------------------ END IF HAS TASK ------------------------------------





    # ---------------------------- IF HAS TASK AND IN ZONE ---------------------------- OUT

    for i in range(0, length):
        # print(f"{car_num[i]} {int(isTask[i])} {int(was_in_zonelist[i])}")
        if int(isTask[i]) == 1 and int(was_in_zonelist[i]) == 1:
            # print('go')
            target = strToCoor(rope_ZoneCoorList[i])
            CTZ = geopy.distance.geodesic((float(lat[i].replace(",", ".")), float(lng[i].replace(",", "."))), target).km
            print('ctz=', CTZ)
            if CTZ > 0.5:
                # УЕХАЛ
                url = createUlrForYandex([float(lat[i].replace(",", ".")), float(lng[i].replace(",", "."))],
                                         strToCoor(task_left_coor[i]))
                print(url)

                alpha = get_Y_time_km(url)
                print(alpha)
                y_url[i] = url
                y_min[i] = alpha[0]
                y_km[i] = alpha[1]

                in_zoneList[i] = 0
                zoneList[i] = zoneOut
                task_cur[i] = str(int(task_cur[i]) + 1)

                airport_msg[i] = f'exit {prev_zoneList[i]}'
                airport_msg_time[i] = current_time

                Air_y_url.append(y_url[i])
                Air_y_min.append(y_min[i])
                Air_y_km.append(y_km[i])
                Air_msg.append(airport_msg[i])
                Air_time.append(airport_msg_time[i])
                Air_car_driver.append(car_driver[i])
                Air_car_num.append(car_num[i])
                Air_car_tsm.append(tsm[i])
                Air_zone.append(zoneList[i])
                Air_task_full.append(task_full_name[i])
                Air_task_left.append(task_left_name[i])
                Air_uid.append(uid[i])

                print('out')
            else:
                print('still in')


    # ---------------------------- END IF HAS TASK AND IN ZONE ----------------------------



    # ------------------------------------ IF NO TASK ------------------------------------

    for i in range(0, length):
        if int(isTask[i]) == 0:
            for x in MapCoordinateTable:
                if geopy.distance.geodesic((float(lat[i].replace(",", ".")), float(lng[i].replace(",", "."))),
                                           (MapCoordinateTable[x])).km < getRad(x):
                    zoneList[i] = x
                    in_zoneList[i] = 1
                    break
                else:
                    zoneList[i] = 'EDET'
                    in_zoneList[i] = 0



    for i in range(0, length):
        if int(isTask[i]) == 0:
            # print(f"{car_num[i]} {int(in_zoneList[i])} {int(was_in_zonelist[i])}")
            if int(in_zoneList[i]) == 1 and int(was_in_zonelist[i]) == 0:
                print('enter')
                airport_msg[i] = f'enter {zoneList[i]}'
                airport_msg_time[i] = current_time

                Air_y_url.append('-')
                Air_y_min.append('-')
                Air_y_km.append('-')
                Air_msg.append(airport_msg[i])
                Air_time.append(airport_msg_time[i])
                Air_car_driver.append(car_driver[i])
                Air_car_num.append(car_num[i])
                Air_car_tsm.append(tsm[i])
                Air_zone.append(zoneList[i])
                Air_task_full.append('-')
                Air_task_left.append('-')
                Air_uid.append('-')

            elif int(in_zoneList[i]) == 0 and int(was_in_zonelist[i]) == 1:
                print('exit')
                airport_msg[i] = f'exit {prev_zoneList[i]}'
                airport_msg_time[i] = current_time

                Air_y_url.append('-')
                Air_y_min.append('-')
                Air_y_km.append('-')
                Air_msg.append(airport_msg[i])
                Air_time.append(airport_msg_time[i])
                Air_car_driver.append(car_driver[i])
                Air_car_num.append(car_num[i])
                Air_car_tsm.append(tsm[i])
                Air_zone.append(zoneList[i])
                Air_task_full.append('-')
                Air_task_left.append('-')
                Air_uid.append('-')

            # airport_msg[i] = f'enter {zoneList[i]}'
            # airport_msg_time[i] = current_time


    # ------------------------------------ END IF NO TASK ------------------------------------




    # -------UPDATE SQLITE DATABASE--------

    if len(lat_lng_old) == 0:
        lat_lng_old = [[None for y in range(2)] for x in range(length)]
    all = []
    for i in range(0, length):
        all.append([chat_id[i], phone[i], uid[i], car_num[i], car_num_short[i], tsm[i], car_driver[i],
                    car_driver_short[i], float(lat[i].replace(",", ".")), float(lng[i].replace(",", ".")), vel[i],
                    lat_lng_old[i][0], lat_lng_old[i][1], zoneList[i], in_zoneList[i],
                    airport_msg[i], airport_msg_time[i],
                    y_url[i], y_min[i], y_km[i],
                    task_full_name[i], task_full_coor[i], task_left_name[i], task_right_name[i], task_left_coor[i],
                    task_right_coor[i], isTask[i], task_amount[i], task_cur[i], rope_ZoneCoorList[i]])

    base.execute('DROP TABLE IF EXISTS logistic_coor')
    base.commit()
    base.execute('CREATE TABLE IF NOT EXISTS logistic_coor(chat,phone,uid PRIMARY KEY,car_num,car_num_short,tsm,'
                 'car_driver,car_driver_short,lat,lng,vel,lat_old,lng_old,zone,in_zoneList,'
                 'airport_msg,airport_msg_time,y_url,y_min,y_km,'
                 'task_full_name,task_full_coor,task_left_name,task_right_name,task_left_coor,task_right_coor,'
                 'isTask,task_amount,task_cur,rope_ZoneCoorList)')
    base.commit()
    cur.executemany('INSERT INTO logistic_coor VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)', all)
    base.commit()


    # --------------------------- UPDATE AIRPORT DB ---------------------------


    all_air = []
    for i in range(0, len(Air_time)):
        all_air.append([Air_time[i], Air_car_tsm[i], Air_car_num[i], Air_msg[i], Air_zone[i], Air_task_left[i],
                        Air_task_full[i], Air_y_min[i], Air_y_km[i], Air_y_url[i], Air_car_driver[i]])

    base.execute('CREATE TABLE IF NOT EXISTS logistic_airport(Air_time, Air_car_tsm, Air_car_num, Air_msg, Air_zone, '
                 'Air_task_left,Air_task_full, Air_y_min, Air_y_km, Air_y_url, Air_car_driver)')
    base.commit()
    cur.executemany('INSERT INTO logistic_airport VALUES(?,?,?,?,?,?,?,?,?,?,?)', all_air)
    base.commit()


# def main():
#
#     schedule.every(60).seconds.do(update)
#
#     while True:
#         schedule.run_pending()

# if __name__ == '__main__':
#     main()


update()



