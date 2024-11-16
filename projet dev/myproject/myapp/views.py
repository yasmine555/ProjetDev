from django.shortcuts import render, get_object_or_404, redirect
from .models import Author, Book, Review, Category, Commande
from django.contrib.auth.decorators import login_required
import requests

# Home Page View
def home(request):
    trending_books = Book.objects.all()[:5]  
    return render(request, 'home.html', {'trending_books': trending_books})

def fetch_books_from_api():
    api_url = 'https://www.googleapis.com/books/v1/volumes?q=python+programming'
    response = requests.get(api_url)

    if response.status_code == 200:
        data = response.json()
        books = data.get('items', [])

        for book_data in books:
            volume_info = book_data.get('volumeInfo', {})

            # Récupération des données de l'API
            title = volume_info.get('title', 'Titre inconnu')
            author_name = ', '.join(volume_info.get('authors', ['Auteur inconnu']))
            description = volume_info.get('description', 'Pas de description')
            cover_image_url = volume_info.get('imageLinks', {}).get('thumbnail', '')
            genre = ', '.join(volume_info.get('categories', ['Genre inconnu']))

            # Création ou récupération de l'auteur
            author, created = Author.objects.get_or_create(
                nom=author_name,
                defaults={'prenom': '', 'datenaissance': None, 'origine': '', 'biographie': 'N/A'}
            )

            # Création ou récupération de la catégorie
            category, created = Category.objects.get_or_create(nom=genre)

            # Ajout du livre à la base de données
            Book.objects.create(
                titre=title,
                auteur=author,
                genre=genre,
                prix=0.00,  # Par défaut
                description=description,
                note=0,  # À adapter si l’API fournit des notes
                categorie=category,
                cover_image_url=cover_image_url
            )

# Book List View
def book_list(request):
    # Récupère tous les livres
    books = Book.objects.all()

    # Recherche par titre
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

    # Données pour les filtres
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
#def post_list(request):
    #posts = Post.objects.all()
    #return render(request, 'post_list.html', {'posts': posts})

# Post Detail View
#def post_detail(request, post_id):
    #post = get_object_or_404(Post, id=post_id)
    #return render(request, 'post_detail.html', {'post': post})

# Create a Post View
#@login_required
#def create_post(request):
    #if request.method == "POST":
        #title = request.POST.get('title')
        #content = request.POST.get('content')
        #post = Post(user=request.user, title=title, content=content)
        #post.save()
        #return redirect('post_list')
    #return render(request, 'create_post.html')
