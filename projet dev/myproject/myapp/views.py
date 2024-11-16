from django.shortcuts import render, get_object_or_404, redirect
from .models import Author, Book, Review, Post, Commande
from django.contrib.auth.decorators import login_required

# Home Page View
def home(request):
    trending_books = Book.objects.all()[:5]  
    return render(request, 'home.html', {'trending_books': trending_books})

# Book List View
def book_list(request):
    books = Book.objects.all()

    # Recherche
    query = request.GET.get('q', '')
    if query:
        books = books.filter(titre__icontains=query)

    # Filtre par auteur
    auteur_id = request.GET.get('auteur')
    if auteur_id:
        books = books.filter(auteur_id=auteur_id)

    # Filtre par genre
    genre = request.GET.get('genre')
    if genre:
        books = books.filter(genre__icontains=genre)

    # Filtre par catégorie
    categorie_id = request.GET.get('categorie')
    if categorie_id:
        books = books.filter(categorie_id=categorie_id)

    # Récupérer les options pour les filtres
    auteurs = Author.objects.all()
    categories = Category.objects.all()

    return render(request, 'book_list.html', {
        'books': books,
        'auteurs': auteurs,
        'categories': categories,
        'query': query,
    })

# Book Detail View
def book_detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    reviews = Review.objects.filter(book=book)
    return render(request, 'book_detail.html', {'book': book, 'reviews': reviews})

# Author Detail View
def author_detail(request, author_id):
    author = get_object_or_404(Author, id=author_id)
    books_by_author = Book.objects.filter(author=author)
    return render(request, 'author_detail.html', {'author': author, 'books': books_by_author})

# Create a Review View
@login_required
def create_review(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == "POST":
        content = request.POST.get('content')
        rating = request.POST.get('rating')
        review = Review(book=book, user=request.user, content=content, rating=rating)
        review.save()
        return redirect('book_detail', book_id=book.id)
    return render(request, 'create_review.html', {'book': book})

# Post List View
def post_list(request):
    posts = Post.objects.all()
    return render(request, 'post_list.html', {'posts': posts})

# Post Detail View
def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    return render(request, 'post_detail.html', {'post': post})

# Create a Post View
@login_required
def create_post(request):
    if request.method == "POST":
        title = request.POST.get('title')
        content = request.POST.get('content')
        post = Post(user=request.user, title=title, content=content)
        post.save()
        return redirect('post_list')
    return render(request, 'create_post.html')
