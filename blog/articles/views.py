from .models import Article
from django.shortcuts import render
from django.http import Http404
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

def archive(request):
    return render(request, 'archive.html', {"posts": Article.objects.all()})

# Create your views here.
def get_article(request, article_id):
    try:
        post = Article.objects.get(id=article_id)
        return render(request, 'article.html', {"post": post})
    except Article.DoesNotExist:
        raise Http404

def create_post(request):
    if request.user.is_authenticated:
        # Здесь будет основной код представления
        if request.method == "POST":
            # обработать данные формы, если метод POST
            form = {
                'text': request.POST["text"], 'title': request.POST["title"]
            }
            # в словаре form будет храниться информация, введенная пользователем
            if form["text"] and form["title"] and not Article.objects.filter(title=form["title"]).exists():
                # если поля заполнены без ошибок
                Article.objects.create(text=form["text"], title=form["title"], author=request.user)
                return redirect('get_article', article_id=Article.objects.get(text=form["text"], title=form["title"], author=request.user).id)
                # перейти на страницу поста
            else:
                # если введенные данные некорректны
                if Article.objects.filter(title=form["title"]).exists() and not (form["text"] and form["title"]):
                    form['errors'] = u"Название статьи не уникально!\nНе все поля заполнены!"
                elif Article.objects.filter(title=form["title"]).exists():
                    form['errors'] = u"Название статьи не уникально!"
                else:
                    form['errors'] = u"Не все поля заполнены!"
                # print(Article.objects.filter(title='dsfsf').exists())
                return render(request, 'create_post.html', {'form': form})
        else:
        # просто вернуть страницу с формой, если метод GET
            return render(request, 'create_post.html', {})
    else:
        raise Http404


def create_user(request):
# Здесь будет основной код представления
     # обработать данные формы, если метод POST
    if request.method == "POST":
        # в словаре form будет храниться информация, введенная пользователем
        form = {
            'username':request.POST["username"],
            'mail':request.POST["mail"],
            'password':request.POST["password"],
        }
        art = None
        # проверим,  попробовав найти его в базе данных 
        # с помощью метода get, который вызовет исключение, если объекта не существует:
        try:
            art = User.objects.get(username=form["username"])
            art = User.objects.get(email=form["mail"])
            # если пользователь существует, то ошибки не произойдет и программа 
            # удачно доберется до следующей строчки 
            form['errors'] = u"Такой пользователь уже существует"
            return render(request, 'register.html', {'form': form})
        except User.DoesNotExist:
            form['errors'] = u"Этот логин свободен"       
        # Если поле логина,маила, пароля, не пустые
        if form["username"] and form["mail"] and form["password"] and art is None:
            art = User.objects.create_user(
                username=form["username"],  
                email=form["mail"], 
                password=form["password"],)
            return redirect(archive)
        # Проверка на  введенные данные некорректны
        else:
            if art is not None:
                form['errors'] = u"Логин или почта уже заняты"
                return render(request, 'register.html', {'form': form})
            else:
                form['errors'] = u"Не все поля заполнены"
                return render(request, 'register.html', {})
    #  Если методом ГЕТ то возращаем.
    else:
        return render(request, 'register.html', {})


def input_user(request):
    # Здесь будет основной код представления
    # обработать данные формы, если метод POST
    if request.method == "POST":
         # в словаре form будет храниться информация, введенная пользователем
        form = {
            'username':request.POST["username"],
            'password':request.POST["password"],
        }
        if form["username"] and form["password"]:
            # Проверка на существования 
            user = authenticate(request, username=form["username"], password=form["password"])
            if user is None:
                form['errors'] = u"Такой пользеватель не зарегистрирован"
                return render(request, 'authorization.html', {'form': form})
            else:
                login(request,user)
            return redirect(archive)
        #  Проверка на некоректные данные
        else:
            form['errors'] = u"Не все поля заполнены"
            return render(request, 'authorization.html', {'form': form})
    # Не тот метод вызыва, вернуть
    else:
        return render(request, 'authorization.html', {})