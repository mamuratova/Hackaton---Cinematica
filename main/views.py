from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.urls import reverse
from django.views.generic import ListView
from main.forms import FilmForm
from .models import *
from django.core.paginator import Paginator


def index(request):
    films = Films.objects.order_by('pk')
    categories = Genre.objects.all()
    return render(request, 'index.html', locals())


def category_detail(request, slug):
    categories = Genre.objects.order_by('pk')
    categori = Genre.objects.get(slug=slug)
    films = Films.objects.filter(genre__slug=slug)
    paginator = Paginator(films, 2)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'categories.html', locals())


def film_detail(request, pk):
    film = Films.objects.get(pk=pk)
    comment_list = film.comment_set.order_by('pk')
    return render(request, 'details.html', locals())


def watch(request, pk):
    film = Films.objects.get(pk=pk)
    comment_list = film.comment_set.order_by('pk')
    return render(request, 'watch.html', locals())


def create(request):
    if request.method == 'POST':
        film_form = FilmForm(request.POST, request.FILES)
        if film_form.is_valid():
            film = film_form.save()
            return redirect(film.get_absolute_url())
    else:
        film_form = FilmForm()
    return render(request, 'create.html', locals())


def update(request, pk):
    if request.method == "POST":
        film_form = FilmForm(request.POST, request.FILES)
        if film_form.is_valid():
            film = film_form.save()
            return redirect(film.get_absolute_url())
    else:
        film = get_object_or_404(Films, pk=pk)
        film_form = FilmForm(request.POST or None, instance=film)
        return render(request, 'update.html', locals())


def delete(request, pk):
    film = get_object_or_404(Films, pk=pk)
    if request.method == 'POST':
        film.delete()
        return redirect('home')
    return render(request, 'delete.html', locals())


class SearchListView(ListView):
    model = Films
    template_name = 'search.html'
    context_object_name = 'results'

    def get_queryset(self):
        queryset = super().get_queryset()
        q = self.request.GET.get('q')
        queryset = queryset.filter(Q(title__icontains=q) |
                                   Q(description__icontains=q))
        return queryset


def leave_comment(request, pk):
    film = Films.objects.get(pk=pk)
    comment = Comment(film=film, author=request.user.username, comment_text=request.POST.get('comment', False))
    comment.save()
    return HttpResponseRedirect(reverse('detail', args=(film.pk,)))


#  -------------------------------------------------Избранное---------------------------------------------------------

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from cart.cart import Cart


@login_required
def cart_add(request, id):
    cart = Cart(request)
    product = Films.objects.get(id=id)
    cart.add(product=product)
    return redirect("detail", pk=id)


@login_required
def item_clear(request, id):
    cart = Cart(request)
    product = Films.objects.get(id=id)
    cart.remove(product)
    return redirect("favorities")


@login_required
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect("favorities")


@login_required()
def cart_detail(request):
    return render(request, 'cart_detail.html')




                        # Parsing
import requests
from bs4 import BeautifulSoup


def main(request):
    url = 'https://www.kinomania.ru/news'

    def get_html(url):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.1) Gecko/2008070208 Firefox/3.0.1'
        }
        response = requests.get(url, headers=headers)
        return response.text

    def parsing_kaktus(html):
        data_list = []
        soup = BeautifulSoup(html, 'lxml')
        news = soup.find('div', class_="outer-pagelist-item").find_all('div', class_="pagelist-item")
        count = 0
        url = 'https://www.kinomania.ru'
        for new in news:
            count += 1
            try:
                title = new.find('div', class_="pagelist-item-title").find('a').text.strip()
            except:
                title = 'no title'

            try:
                lin = new.find('div', class_="pagelist-item-title").find('a').get('href')
                link = url + lin
                # print(link)
            except:
                link = 'no link'

            try:
                description = new.find('div', class_="pagelist-item-content").find('p').text.strip()
                # print(description)
            except:
                description = 'no description'
                # print(description)

            data = {'count': count, 'title': title, 'link': link, 'description': description}
            data_list.append(data)
        return data_list

    data_list = parsing_kaktus(get_html(url))
    return render(request, 'news.html', {'news': data_list})









