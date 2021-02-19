from django.contrib import messages
from django.db import IntegrityError, transaction
from django.shortcuts import redirect
from django.shortcuts import HttpResponseRedirect
from django.shortcuts import render
from django.utils import timezone
from .models import Borrow
from .models import Card
from .models import Librarian
from .models import Book
from .models import User


# Create your views here.


def Register(request):
    if request.method == "POST":
        user_id = request.POST.get('user_id', None)
        password = request.POST.get('password', None)
        if user_id and password:
            User.objects.create(user_id=user_id, password=password)
            print(user_id, password)
            return HttpResponseRedirect('/index/')
    return render(request, "Register.html")


def logout(request):
    if not request.session.get('is_login', None):
        return redirect("/Login/")
    request.session.flush()
    return redirect("/Login/")


def Login(request):
    if request.session.get('is_login', None):
        return redirect("/index/")
    if request.method == "POST":
        user_id = request.POST.get('user_id', None)
        password = request.POST.get('password', None)
        error_msg = "Please log in！"
        # no encryption

        if user_id and password:
            # noinspection PyBroadException
            try:
                user = User.objects.filter(user_id=user_id, password=password).first()
                if user.password == password:
                    request.session['is_login'] = True
                    request.session['user_id'] = user.admin_id
                    request.session['user_id'] = user.user_id
                    return redirect('/index/', user)
                else:
                    error_msg = "Password error！"
            except:
                error_msg = "User does not exist！"
            return render(request, "Login.html", {"message": error_msg})
    return render(request, "Login.html")


def index(request):
    user_list = Librarian.objects.all()
    return render(request, "index.html", {"data": user_list})


def books(request):
    try:
        cur_page = int(request.GET.get('cur_page', '1'))
    except ValueError:
        cur_page = 1

    if request.method == "POST":
        return render(request, "sort_books.html")

    return render(request, "books.html", locals())


def sort_books(request):
    all_books = Book.objects.all()
    if request.method == "POST":
        if request.POST.get("order_bno"):
            all_books = Book.objects.order_by("bno")
        if request.POST.get("order_title"):
            all_books = Book.objects.order_by("-title")
        if request.POST.get("time_up"):
            all_books = Book.objects.order_by("year")
        if request.POST.get("time_down"):
            all_books = Book.objects.order_by("-year")
        if request.POST.get("price_up"):
            all_books = Book.objects.order_by("price")
        if request.POST.get("price_down"):
            all_books = Book.objects.order_by("-price")
    return render(request, "sort_books.html", locals())


def search(request):
    if request.method == "POST":
        b_category = request.POST.get('category')
        b_title = request.POST.get('title')
        b_press = request.POST.get('press')
        b_author = request.POST.get('author')
        b_year_from = request.POST.get('year_from')
        b_year_to = request.POST.get('year_to')
        b_price_from = request.POST.get('price_from')
        b_price_to = request.POST.get('price_to')

        if not (b_category or b_title or b_press or b_author or b_year_from or b_year_to or b_price_from or b_price_to):
            message = "Please input values!"
            return render(request, "search.html", {"message": message})

        search_books = Book.objects.filter(
            category__icontains=b_category, title__icontains=b_title, press__icontains=b_press,
            author__icontains=b_author
        )
        if b_year_from and b_year_to:
            search_books = search_books.filter(year__range=(b_year_from, b_year_to))
        elif b_year_from:
            search_books = search_books.filter(year__gte=b_year_from)
        elif b_year_to:
            search_books = search_books.filter(year__lte=b_year_to)

        if b_price_from and b_price_to:
            search_books = search_books.filter(price__range=(b_price_from, b_price_to))
        elif b_price_from:
            search_books = search_books.filter(price__gte=b_price_from)
        elif b_price_to:
            search_books = search_books.filter(price__lte=b_price_to)

        if search_books.count() == 0:
            message = "Oops... No result!"
        else:
            ok_message = "OK"

    return render(request, "search.html", locals())


def book_manage(request):
    if request.method == "POST":
        if request.POST.get("single_add"):
            b_bno = request.POST.get('bno')
            b_category = request.POST.get('category')
            b_title = request.POST.get('title')
            b_press = request.POST.get('press')
            b_author = request.POST.get('author')
            b_stock = request.POST.get('stock')
            b_year = request.POST.get('year')
            b_price = request.POST.get('price')
            b_total = request.POST.get('total')

            try:
                new_book = Book.objects.create(
                    bno=b_bno, category=b_category, title=b_title, press=b_press, author=b_author,
                    year=b_year, price=b_price, total=b_total, stock=b_stock
                )
                messages.success(request, "Add OK!")
            except:
                messages.error(request, "Add failed...")
    return render(request, "book_manage.html", locals())


def delete(request):
    b_bno = request.POST.get('bno')
    b_title = request.POST.get('title')
    if request.POST.get("btn_delete"):
        try:
            if b_bno:
                cancel_book = Book.objects.get(bno=b_bno, title=b_title)
                cancel_book.delete()
                messages.success(request, "Delete OK!")
        except:
            messages.error(request, "This book does not exist!")
        else:
            messages.error(request, 'Input bno or title to delete!')
    return render(request, "delete.html", locals())


def card(request):
    if request.method == "POST":
        if request.POST.get("btn_show"):
            cards = Card.objects.all()
            show_message = "Show all..."
            return render(request, "card.html", {"cards": cards, "show_message": show_message})
        c_cno = request.POST.get('cno')
        c_name = request.POST.get('name')
        c_department = request.POST.get("department")
        c_type = request.POST.get("type")
        if request.POST.get("btn_add"):
            if not (c_cno and c_name and c_department and c_type):
                messages.error(request, 'Please fill all values!')
                return render(request, "card.html")
            try:
                new_card = Card.objects.create(cno=c_cno, name=c_name, department=c_department, type=c_type)
                messages.success(request, 'Added!')

            except:
                messages.error(request, 'Failed!')

        if request.POST.get("btn_search"):
            cards = Card.objects.filter(
                cno__icontains=c_cno, name__icontains=c_name,
                department__icontains=c_department, type__icontains=c_type
            )
            return render(request, "card.html", locals())

        if request.POST.get("btn_delete"):
            if c_cno:
                try:
                    del_card = Card.objects.get(cno=c_cno)
                    borrow_record = Borrow.objects.filter(cno_id=c_cno, return_date=None)
                    if not borrow_record.exists():
                        del_card.delete()
                        messages.success(request, "Deleted!")
                    else:
                        messages.error(request, "Please return all books with the card!")
                except:
                    messages.error(request, "This card does not exist!")
            else:
                messages.error(request, 'Input cno to delete!')
            return render(request, "card.html")

    return render(request, "card.html", locals())


def borrow_book(request):
    # global card_record
    if request.method == "POST":
        if request.POST.get("btn_borrow_record"):
            c_cno = request.POST.get('cno')
            borrowed_books = []
            try:
                i_card = Card.objects.get(cno=c_cno)
                borrow_record = Borrow.objects.filter(cno=i_card, return_date=None)
                for i in borrow_record:
                    borrowed_books.extend(Book.objects.filter(bno=i.bno_id))
                messages.success(request, "Successful!")
                return render(request, "borrow_book.html", locals())
            except:
                messages.error(request, "Search failed...")
                return render(request, "borrow_book.html")

        if request.POST.get("btn_borrow"):
            c_cno = request.POST.get('cno')
            b_bno = request.POST.get('bno')
            card_record = Borrow.objects.filter(cno_id=c_cno)
            try:
                i_card = Card.objects.get(cno=c_cno)
                i_book = Book.objects.get(bno=b_bno)
                if i_book.stock:
                    try:
                        with transaction.atomic():
                            Borrow.objects.create(cno=i_card, bno=i_book, borrow_date=timezone.now(),
                                                  return_date=None)
                            i_book.stock -= 1
                            i_book.save()
                            messages.success(request, "Borrowed")
                    except IntegrityError:
                        messages.error(request, "Failed to borrow...")
                    return render(request, "borrow_book.html")
                else:
                    messages.error(request, "Book out of stock!")
            except:
                messages.error(request, "Card/Book not found...")
        return render(request, "borrow_book.html", {"card_record": card_record})
    return render(request, "borrow_book.html")


def return_book(request):
    if request.method == "POST":
        if request.POST.get("btn_return_record"):
            c_cno = request.POST.get('cno')
            borrowed_books = []
            try:
                i_card = Card.objects.get(cno=c_cno)
                borrow_record = Borrow.objects.filter(cno=i_card, return_date=None)
                for i in borrow_record:
                    borrowed_books.extend(Book.objects.filter(bno=i.bno_id))
                messages.success(request, "Successful!")
                return render(request, "return_book.html", locals())
            except:
                messages.error(request, "Search failed...")
                return render(request, "return_book.html")

        if request.POST.get("btn_return"):
            c_cno = request.POST.get('cno')
            b_bno = request.POST.get('bno')
            card_record = Borrow.objects.filter(cno_id=c_cno)
            try:
                i_card = Card.objects.get(cno=c_cno)
                i_book = Book.objects.get(bno=b_bno)
                try:
                    with transaction.atomic():
                        i_borrow = Borrow.objects.get(cno_id=c_cno, bno_id=b_bno, return_date=None)
                        i_borrow.return_date = timezone.now()
                        i_borrow.save()
                        i_book.stock += 1
                        i_book.save()
                        messages.success(request, "Returned!")
                        return render(request, "return_book.html")
                except IntegrityError:
                    messages.error(request, "The book is not in your record!")
            except:
                messages.error(request, "Card/Book not found...")
        return render(request, "return_book.html", {"card_record": card_record})
    return render(request, "return_book.html")
