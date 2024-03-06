import sqlite3
class Service():
    def __init__(self):
        self.conection = sqlite3.connect("vente")
        
        
    def ajouter_produit(self,id,nom,prix, rate, image):
        
        if id=="":
            return False
        else:
            
            verification = self.liste_produitById(id)
            print(verification)
            if len(verification)==0:
                with self.conection:
                    self.conection.cursor().execute(
                        f"INSERT INTO produit VALUES('{id}','{nom}', '{prix}', '{rate}','{image}')")
                return True
            else:
                return False
        

    def liste_produit(self):  
            with self.conection:  
                rows = self.conection.cursor().execute("SELECT * FROM produit").fetchall()
            return rows
        
        
    def liste_user(self):  
            with self.conection:  
                rows = self.conection.cursor().execute("SELECT * FROM user").fetchall()
            return rows    
    def liste_produitById(self, id):
        if id=="":
            return False
        else:
            with self.conection:  
                rows = self.conection.cursor().execute(f"SELECT * FROM produit where id={id}").fetchall()
            return rows