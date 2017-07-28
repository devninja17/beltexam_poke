from django.shortcuts import render, HttpResponse, redirect
from .models import User, Poke
from django.contrib import messages
import bcrypt

def index(request):
    if request.method == "POST": #Register user on POST
        errors = User.objects.validate_reg(request.POST)
        if errors:
            for tag, error in errors.iteritems():
                messages.error(request, error, extra_tags=tag)
            return redirect('/main')
        else:
            found_users = User.objects.filter(email=request.POST['email'])
            if found_users.count() > 0:
                messages.error(request, "Sorry, this email had previously registered.", extra_tags="email")
                return redirect('/main')
            else:
                hashed_pw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
                created_user = User.objects.create(name=request.POST['name'], alias=request.POST['alias'], email=request.POST['email'], password=hashed_pw, birthdate=request.POST['birthdate'])
                request.session['user_id'] = created_user.id
                request.session['user_name'] = created_user.name
                return redirect('/pokes')
    return render(request, 'pokesapp/index.html')

def login(request):
	found_users = User.objects.filter(email=request.POST['email'])
	if found_users.count() > 0:
		found_user = found_users.first()
		if bcrypt.checkpw(request.POST['password'].encode(), found_user.password.encode()) == True:
			request.session['user_id'] = found_user.id
			request.session['user_name'] = found_user.name
			print found_user
			return redirect('/pokes')
		else:
			messages.error(request, "Login Failed, incorrect password", extra_tags="password")
			return redirect('/')
	else:
		messages.error(request, "Login Failed, email is not registered", extra_tags="email")
		return redirect('/')

def logout(request):
    request.session['user_id'] = 0
    return redirect('/')

def dashboard(request):
    people = User.objects.exclude(id=request.session['user_id'])
    people_poked_you = User.objects.get(id=request.session['user_id']).pokes_received.all()
    
    '''Count how many pokers '''
    counter = 0
    for count in people:
        if count.pokes_made.count > 0:
            counter += 1

    context = {
        "people": people.all(),
        "counter": counter,
    }
    return render(request, 'pokesapp/pokes.html', context)

def got_poked(request, user_id):
    the_poker = User.objects.get(id=request.session['user_id'])
    the_pokee = User.objects.get(id=user_id)
    Poke.objects.create(poker=the_poker, pokee=the_pokee)
    return redirect('/pokes')