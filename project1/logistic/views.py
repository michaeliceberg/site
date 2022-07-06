from django.shortcuts import render
import pygsheets
from .models import *
from django.shortcuts import redirect
import telebot

# TOKEN='5430967625:AAGqxbHhZbJ4m22zOBA4W6pcUm6uDhYPdrk'
TOKEN = '5513496006:AAHlF8b6BrIz-IASkOvhLLGIwXm4uIiCViY'

#def home_page(request):
#    return render(request, "home_page.html")



def home_page(request):
    driverModel_all = coor.objects.all()
    context = {"driverModel_all": driverModel_all, "title": "this is title"}
    if request.method == 'POST':
        selected_car_nums = request.POST.getlist('selected_car_nums')
        print(selected_car_nums[0])
        # abc = coor.objects.get(car_num=selected_car_nums[0])
        # print(f"abc={abc}")

        # s = coor.objects.filter(car_num=selected_car_nums[0])
        print(selected_car_nums)
        bot = telebot.TeleBot(TOKEN)
        for car_index in selected_car_nums:
            s = coor.objects.get(car_num=car_index)
            bot.send_message(1005641275, s.car_driver)
            s.tg_id = 8
            s.save()


        # for i in driverModel_all:
        #     if i.car_num == selected_car_nums[0]:
        #         i.tg_id = 8

        return render(request, 'home_page.html', {"title": selected_car_nums})
        


    return render(request, 'home_page.html', context)


def index_page(request):
    st = status.objects.all()
    context = {"st": st}
    return render(request, "index.html", context)


def reboot_status_page(request):
    gc = pygsheets.authorize(service_file='secret.json')
    sh = gc.open_by_key('1HhRBqMXxmE2uA06pNKc1HI1lnBAgJkfGKABGqmAhJAQ')
    wks = sh.worksheet_by_title('Status')
    length = len(wks.get_all_values())
    length = 10
    todo = wks.get_values('AC6', 'AC{}'.format(length))
    done = wks.get_values('AB6', 'AB{}'.format(length))
    contrag = wks.get_values('X6', 'X{}'.format(length))
    time = wks.get_values('AA6', 'AA{}'.format(length))
    amount_cars = wks.get_values('Y6', 'Y{}'.format(length))
    num_cars = wks.get_values('Z6', 'Z{}'.format(length))
    for item in status.objects.all():
        item.delete()
    for i in range(len(done)):
        item = status(id=i + 1, ToDo=float(todo[i][0]), Done=float(done[i][0]), Contrag=contrag[i][0],
                      Time=time[i][0], Amount_Cars=amount_cars[i][0], Num_Cars=num_cars[i][0])
        item.save()
    return redirect('/')

