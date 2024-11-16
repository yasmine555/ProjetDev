from django.db import models
from django.contrib.auth.models import User

class Utilisateur(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nom = models.CharField(max_length=100)
    adresse = models.CharField(max_length=255)
    mot_de_passe = models.CharField(max_length=100)

    def inscrire(self):
        #INSCRIRE function
        pass

    def seconnecter(self):
        # Login function 
        pass

    def modifierprofile(self):
        # profile modification function
        pass

    def ajouteraupanier(self, livre):
        # Add to cart function
        pass

    def consulterlivre(self, livre):
        # consulter livre function
        pass

    def passercommande(self, panier):
        # passer commande function
        pass


class Author(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    datenaissance = models.DateField()
    origine = models.CharField(max_length=100)
    biographie = models.TextField()

    def AfficherInfoAuteur(self):
        # afficher info function
        pass


class Category(models.Model):
    nom = models.CharField(max_length=100)

    def __str__(self):
        return self.nom


class Book(models.Model):
    titre = models.CharField(max_length=100)
    auteur = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='livres')
    genre = models.CharField(max_length=50)
    prix = models.DecimalField(max_digits=5, decimal_places=2)
    description = models.TextField()
    note = models.IntegerField()
    categorie = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='livres')

    def __str__(self):
        return self.titre

    def ConsulterDetails(self):
        # Consult book functions 
        pass

    def AjouterCommentaire(self, utilisateur, texte):
        # Add comment functions
        Review.objects.create(utilisateur=utilisateur, livre=self, texte=texte)


class Commande(models.Model):
    utilisateur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, related_name='commandes')
    DateCommande = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20)
    Livres = models.ManyToManyField(Book, related_name='commandes')

    def Afficherdetails(self):
        # Show order functions
        pass

    def AnnulerCommande(self):
        # Cancel order functions
        pass


class Panier(models.Model):
    utilisateur = models.OneToOneField(Utilisateur, on_delete=models.CASCADE, related_name='panier')
    livres = models.ManyToManyField(Book, related_name='paniers')

    def AjouterLivre(self, livre):
        self.livres.add(livre)

    def SupprimerLivre(self, livre):
        self.livres.remove(livre)

    def ValiderCommande(self):
        # Valider commande function
        pass


class Review(models.Model):
    utilisateur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, related_name='commentaires')
    livre = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='commentaires')
    texte = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def AfficherCommentaire(self):
        # show comments function
        pass
