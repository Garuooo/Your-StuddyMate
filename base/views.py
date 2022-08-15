from django.shortcuts import redirect, render
from .models import Room, Topic ,Message , User
from django.http import HttpResponse
from django.contrib.auth import login , logout
from django.contrib.auth.decorators import login_required
from .forms import RoomForm , UpdateForm , UserForm  , MyUserCreationForm
from django.db.models import Q
from django.contrib import messages

#request object is the http object -> we get the type of the request we pass in (post /get)

def register(request):
    form = MyUserCreationForm()
    page="register"
    context={"page":page,"form":form}
    if request.method =="POST":
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            print("hello2")
            user = form.save(commit=False) # commit = False --> to get a userobject after save
            user.save()
            login(request,user)
            return redirect("home")
        else:
            messages.error(request,"Invalid request")
    return render(request,"base/login_regirster.html",context)



def login_page(request):
    page="login"
    if request.method == "GET":
        if request.user.is_authenticated :
            return HttpResponse("You are Already logged in")
    if request.method=="POST":
        email=request.POST["email"]
        password=request.POST["password"]
        try:
            user = User.objects.get(Q(email=email) )
            if user.check_password(password):
                login(request,user) # add session id in our db and browser
                messages.success(request,"logged in successfuly")
                return redirect("home")
            else:
                messages.error(request,"User does not exist")
        except:
            messages.error(request,"User does not exist")
    context = {"page":page}
    return render(request,"base/login_regirster.html",context)    

@login_required(login_url="../user-login")
def logout_page(request):
    logout(request)
    messages.success(request,"logged out successfully")
    return redirect("home")

def home_page(request):
    q = request.GET.get('q')
    if q != None:
        rooms = Room.objects.filter(
            Q(topic__name__icontains=q ) |
            Q(name__icontains=q) |
            Q(description__icontains=q) 
               )
        messages=Message.objects.filter(Q(room_topic__name__icontains=q))
    else:
        rooms = Room.objects.all()
        messages = Message.objects.all()[:]
    topics = Topic.objects.all()[0:3]
    context = {"rooms":rooms,"topics":topics,"size":rooms.count(),"room_messages":messages}
    return render(request,"base/home.html",context)


def profile(request,id):
    user = User.objects.get(id=id)
    rooms=Room.objects.filter(host=user)    
    messages = Message.objects.filter(user=user)  
    topics = Topic.objects.all() 
    context = {"rooms":rooms , "room_messages":messages,"topics":topics,"profile_user":user}
    return render(request,'base/profile.html',context)

def room(request,pk):
   
    room = Room.objects.get(id=pk)
    messages = Message.objects.filter(room=room).order_by("-created")
    participants = room.participants.all()
   
    if request.method=="POST":
        message = Message.objects.create(body = request.POST["body"] , user = request.user , room=room,room_topic=room.topic)
        room.participants.add(request.user)
        return redirect("room",pk=room.id)
    context = {"room":room,"room_messages":messages,"participants":participants ,"participant_size":participants.count()}
    return render(request,"base/room.html",context)


@login_required(login_url="../user-login")
def create_room(request):
    form = RoomForm()
    user = request.user
    if request.method == "POST":
        print(request.POST)
        # {"name":request.POST["name"],"description":request.POST["description"]}
        form = RoomForm(request.POST)
        
        if form.is_valid():
            room = form.save(commit=False) #gives us instance of room so we can operate on
            room.host=user
            room.save()
            return redirect("home") #name in the path module
    context = {"form":form}
    return render(request,"base/room_form.html",context)

@login_required(login_url="../user-login")
def update_room(request,pk):
    room = Room.objects.get(id=pk)
    
    if request.user != room.host:
        return HttpResponse("You are not the Owner of the room")


    form = UpdateForm(instance = room)
    if request.method == "POST":
        form = RoomForm(request.POST,instance=room)
        if form.is_valid():
            form.save()
            return redirect("home")
    context = {"form":form}
    return render(request,"base/room_form.html",context)


@login_required(login_url="../user-login")
def delete_room(request,pk):
    room = Room.objects.get(id=pk)
    if request.user != room.host:
        return HttpResponse("You are not the Owner of the room")

    if request.method == "POST":
        room.delete()
        return redirect("home")
    return render(request,"base/delete.html",context={"room":room})


@login_required(login_url="../user-login")
def delete_message(request,room_id,message_id):
    message= Message.objects.get(id=message_id)
    if message.user != request.user:
        return HttpResponse("you are not the owner")
    
    if request.method == "POST":
        message.delete()
        return redirect("room",room_id)    
    return render(request,"base/delete.html",context={"message":message})

@login_required(login_url="../user-login")
def update_user(request):
    user = request.user
    form = UserForm(instance = user)
    context = {"form":form}
    if request.method == "POST":
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect("profile",id=user.id)
    return render(request,"base/edit-user.html",context)


def all_topics(request):
    try:
        q = request.GET.get('q')
        topics = Topic.objects.filter(name__icontains = q)
    except:
        topics = Topic.objects.all()
    return render(request,"base/topics.html",{"topics":topics})

def recents(request):
    rooms = Room.objects.all()
    messages = Message.objects.all()
    topics = Topic.objects.all()
    context = {"rooms":rooms,"topics":topics,"size":rooms.count(),"room_messages":messages}
    return render(request,"base/recents.html",context)