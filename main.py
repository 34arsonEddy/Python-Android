from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.gridlayout import MDGridLayout
from kivy.properties import StringProperty
from kivy.core.window import Window
from kivymd.uix.screenmanager import MDScreenManager
from kivy.lang import Builder
from kivy.factory import Factory
from service import *
from kivymd.uix.filemanager import MDFileManager
import os
from kivymd.toast import toast
from kivymd.uix.screen import MDScreen
from kivymd.uix.snackbar import MDSnackbar,MDSnackbarCloseButton,MDSnackbarActionButton
from kivymd.uix.label import MDLabel 

class Menu(MDScreen):
    pass 
class Login(MDScreen):
    pass 
class Dialog(MDDialog):
    image = StringProperty()
    price = StringProperty()
    rate = StringProperty()
class FormProduit(MDScreen):
    pass
class PanierViewer(MDScreen):
    pass

class Vente(MDApp):
    panier = []
    logged = False
    dialog = None
    service = Service()
    sm = MDScreenManager()
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.manager_open = False
        self.file_manager = MDFileManager(
        exit_manager=self.exit_manager, select_path=self.select_path)
    def verifcation_login(self):
        if self.logged==False:
            self.sm.current = 'login'
        else:
            self.sm.current = 'menu'  
               
    def file_manager_open(self):
        self.file_manager.show(os.path.expanduser("~"))
        self.manager_open = True
        
    def exit_manager(self, *args):
        self.manager_open = False
        self.file_manager.close()
    
    def select_path(self, path: str):
        
        self.exit_manager()
        self.formProduit.ids.pathImage.text = path
        
        
    def build(self):
        Window.size = [350,600]
        self.screen = Builder.load_file("main.kv")
        self.menu = Builder.load_file("menu.kv")
        self.login = Builder.load_file("login.kv")
        Builder.load_file("panierViewer.kv")
        Builder.load_file("ajoutProduit.kv")
        self.panierViewer = PanierViewer()
        self.formProduit = FormProduit()
        self.sm.add_widget(self.screen)
        self.sm.add_widget(Menu())
        self.sm.add_widget(Login())
        self.sm.add_widget(self.formProduit)
        self.sm.add_widget(self.panierViewer)
        
        
        self.bottom_sheet = self.screen.ids.bottom_sheet 
        self.title = 'vente en ligne'
        self.theme_cls.primary_palette = "Pink"
        
        return self.sm
    
    def show_custom_bottom_sheet(self,id,image,prix,rate):
        
        customSheet = Factory.ContentCustomSheet()
        customSheet.id = id
        customSheet.image = image
        customSheet.prix = prix
        customSheet.rate = rate
        bottom_sheet = self.screen.ids.bottom_sheet
        content_container = self.screen.ids.content_container
        content_container.clear_widgets()
        content_container.add_widget(customSheet)
        if not self.dialog:
            bottom_sheet.open()
    
       
    def on_start(self):
        service = Service()
        #insertion du contenu dans screenHome
        listeProduit = service.liste_produit()
        contenuGrid = self.screen.ids.contenuGrid
        contenuGrid.clear_widgets()
        for produit in listeProduit:
            elementCard = Factory.ElementCard() 
            elementCard.id = str(produit[0])
            elementCard.nom = str(produit[1])
            elementCard.prix = str(produit[2])
            elementCard.rate = str(produit[3])
            elementCard.image = str(produit[4])
            contenuGrid.add_widget(elementCard)
            
          
            
    def verification_login(self,nomUser, motDePasse):

        service = Service()
        for user in service.liste_user():
            
            if nomUser==user[1] and motDePasse==user[3]:
                self.sm.current="menu"
                toast("Connexion réussi")
                self.logged = True
                
            else:
                toast("Connexion echoué")   
                
    def ajouter_produit(self,id,nom,prix,rate, image):
        if self.service.ajouter_produit(id, nom, prix, rate, image)==True:
            toast('réussi')
            self.sm.current = "home"
            
        else:
            self.snackbar = MDSnackbar(
                MDLabel(
                    text="verifier tous les champs",
                    theme_text_color="Custom",
                    text_color="#393231"
                )
                ,
                y=24,
                pos_hint={"center_x": 0.5},
                size_hint_x=0.9,
                md_bg_color="#E8D8D7",
                )
            self.snackbar.open()   
        
    def ajouter_panier(self, id_produit):
        
        box = self.panierViewer.ids.box
        existe = False
        for p in self.panier:
            if p == id_produit:
                existe = True
            
        if existe:
            toast("ce produit est dejà dans le panier")
        else:
            
            self.panier.append(id_produit) 
            box.clear_widgets()
            for panier in self.panier:
                produit = self.service.liste_produitById(panier)
                for p in produit:
                    listePanier = Factory.ListePanier()
                    listePanier.id = str(p[0])
                    listePanier.nom = str(p[1])
                    listePanier.prix = str(p[2])
                    listePanier.image = str(p[4])
                    box.add_widget(listePanier)
            toast("ajouté") 
            
        print(self.panier)
    def supprimer_panier(self, id):
        box = self.panierViewer.ids.box
        box.clear_widgets()
        for panier in self.panier:
            if panier == id:
                self.panier.remove(panier)
            else:                           
                produit = self.service.liste_produitById(panier)
                for p in produit:
                    listePanier = Factory.ListePanier()
                    print(produit)
                    listePanier.id = str(p[0])
                    listePanier.nom = str(p[1])
                    listePanier.prix = str(p[2])
                    listePanier.image = str(p[4])
                    box.add_widget(listePanier)
        toast("supprimé")    
    def snackbar_close(self, *args):
        self.snackbar.dismiss()
             
    
Vente().run()
