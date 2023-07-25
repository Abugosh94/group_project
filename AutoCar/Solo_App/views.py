from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.core.paginator import Paginator
from .models import Car ,User
from django.contrib import messages

def add_to_bookmarked(request):
    text = request.GET.get('text')
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        if text == "Add to Favorites":
            user = User.objects.get(id=request.session['user_id'])
            car_id = int(request.GET.get('id'))
            car = Car.objects.get(id=car_id)
            user.bookmarked.add(car)
            return JsonResponse({'text': text}, status=200)
        if text == "Remove From Favorites":
            user = User.objects.get(id=request.session['user_id'])
            car_id = int(request.GET.get('id'))
            car = Car.objects.get(id=car_id)
            user.bookmarked.remove(car)
            return JsonResponse({'text': text}, status=200)
    return render(request, '/')


def sort_properties(request):
    if int(request.GET.get('sort_id'))== 0:
        sorted_properties = Car.objects.all()
    elif int(request.GET.get('sort_id'))== 1:
        sorted_properties = Car.objects.order_by('-model')
    elif int(request.GET.get('sort_id'))== 2:
        sorted_properties = Car.objects.order_by('model')
    elif int(request.GET.get('sort_id'))== 4:
        sorted_properties = Car.objects.order_by('price')
    elif int(request.GET.get('sort_id'))== 5:
        sorted_properties = Car.objects.order_by('-price')
    else:
        sorted_properties = Car.objects.order_by('color')
    user = User.objects.get(id=request.session['user_id'])
    bookmarked = user.bookmarked.all()
    sorted_properties_data = []
    for property in sorted_properties:
        # Prepare the property data in a dictionary format
        for bookmark in bookmarked:
            if property.id == bookmark.id:
                property_data = {
                    'id': property.id,
                    'name': property.name,
                    'model': property.model,
                    'price': format(property.price, "3,d"),
                    'color': property.color,
                    'fuelType': property.fuelType,
                    'bookmarked': True,
                }
                break
            else:
                property_data = {
                    'id': property.id,
                    'name': property.name,
                    'model': property.model,
                    'price': format(property.price, "3,d"),
                    'color': property.color,
                    'fuelType': property.fuelType,
                    'bookmarked': False,
                }
        sorted_properties_data.append(property_data)
    return JsonResponse(sorted_properties_data, safe=False)



def index(request): 
    return render(request, 'home.html')
def regLog(request): 
    return render(request, 'index.html')

def register(request):
    errors = User.objects.regValidator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/regLog')
    else:
        User.objects.create(username=request.POST['username'], email=request.POST['email'], password=request.POST['password'])
        return redirect ('/regLog')

def login(request):
    errors = User.objects.loginValidator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/regLog')
    else:
        this_user = User.objects.get(email=request.POST['email2'])
        request.session['user_id'] = this_user.id
        request.session['username']=this_user.username
        if this_user.isAdmin==1 : 
            return redirect ('/admin') 
        else :
            return redirect('/user')
    
def admin(request): 
    context = {
        'username' : request.session['username'],
        'cars': Car.objects.all(),
    }
    return render(request, 'admin.html', context)

def user(request):
    user = User.objects.get(id=request.session['user_id'] ) 
    cars = Car.objects.all()
    p = Paginator(cars, 3)
    page = request.GET.get('page')
    cars = p.get_page(page)
    bookmarked = user.bookmarked.all()
   # bookmarkStatus = False
   # for bookmarked in bookmarked:
     #   for car in cars:
        #    if bookmarked == car:
        #        bookmarkStatus = True
    context = {
        'username' : user,
        'cars': cars,
        'bookmarked': bookmarked,
    }
    return render(request, 'user.html', context) 

def add(request):
    return render(request, 'add.html')

def addCar(request):
    errors = Car.objects.addValidator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/add')
    else:
    
        Car.objects.create(
                        name = request.POST['name'], 
                        model = request.POST['model'], 
                        color = request.POST['color'],
                        fuelType = request.POST['fuelType'],
                        price = request.POST['price'],
                        user = User.objects.get(id=request.session['user_id']), 
                    )
        return redirect('/admin')

def edit(request, car_id):
    context = {
        'cars' : Car.objects.get(id=car_id) 
    }
    return render(request,'edit.html',context)

def editCar(request, car_id):
    errors = Car.objects.editValidator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect(f'/edit/{car_id}')
    else:
        selected = Car.objects.get(id=car_id)
        selected.name = request.POST['name']
        selected.model = request.POST['model']
        selected.color = request.POST['color']
        selected.fuelType = request.POST['fuelType']
        selected.price = request.POST['price']
        selected.save()
        return redirect('/admin')

def delete(request, car_id):
    dell = Car.objects.get(id = car_id)
    dell.delete() 
    return redirect('/admin')

def book(request): 
    return render(request, 'book.html')


def remove_from_bookmarked(request, car_id):
    this_car = Car.objects.get(id=car_id)
    this_car.bookmarked.remove(
        User.objects.get(id=request.session['user_id']))
    return redirect('/user')


def bookmarked(request):
    user_id = request.session.get('user_id')
    user = User.objects.get(id=user_id)
    bookmarked = user.bookmarked.all()
    if user_id:
        context = {
            "user": user,
            "bookmarked": bookmarked,
        }
        return render(request, "bookmark.html", context)
    return redirect('/')

def add_to_cart(request):
    return None

def cart(request):
    cars=user.cart.cars.all()
    context={
        cars: cars
    }
    return render(request, 'cart.html', context)

def checkout(request):
    return None

def logout(request): 
    request.session.flush()
    return redirect('/')
