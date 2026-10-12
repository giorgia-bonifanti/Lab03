from operator import attrgetter

class Strumento:
    def __init__(self, codice, tipo, marca, anno, valore):
        self.codice = codice
        self.tipo = tipo
        self.marca = marca
        self.anno_acquisto = int(anno)
        self.valore = float(valore)

    def __str__(self):       # metodo dunder per la stampa pulita dell'oggetto
        return f"[{self.codice}] {self.tipo} {self.marca}"

class Prestito:
    def __init__(self, codice_prestito, data, id_strumento, cognome_allievo):
        self.codice_prestito = codice_prestito
        self.data = data
        self.id_strumento = id_strumento
        self.cognome_allievo = cognome_allievo

    def __str__(self):
        return f"Prestito {self.codice_prestito} - Strumento {self.id_strumento} a {self.cognome_allievo}"


class DepositoStrumenti:
    def __init__(self, nome, responsabile):
        """Inizializza gli attributi e le strutture dati"""
        self.nome = nome
        self._responsabile = responsabile   #valore nascosto

        self.strumenti = {}
        self.prestiti = {}

        self.contatore_strumenti = 1
        self.contatore_prestiti = 1

    @property    ## è il getter: Permette di leggere 'responsabile' come una variabile normale
    def responsabile(self):
        return self._responsabile    # restituisce il valore nascosto
    @responsabile.setter
    def responsabile(self, nuovo_nome):
        self._responsabile = nuovo_nome    #viene aggiornato il valore nascosto con il nuovo nome


    def carica_file_strumenti(self, file_path):
        """Carica gli strumenti dal file"""
      try:
          with open(file_path, "r", encoding = "utf-8") as f:
              for riga in f:
                  riga=riga.strip()
                  if not riga:      #salta le righe vuote se ci sono
                      continue

                  parti=riga.split(",")
                  if len(parti)==5:    #ci devono essere esattamente 5 colonne
                      codice, tipo, marca, anno, valore = parti
                      codice=codice.strip()

                      nuovo_strumento= Strumento(codice, tipo.strip(), marca.strip(), anno.strip(), valore.strip())  #creazione dell' oggetto
                      self.strumenti[codice] = nuovo_strumento   #salvo tutto nel dizionario (il codice è la chiave del dizionario)

                      numero_attuale=int(codice[1:])  #estrae il numero dopo la "S"
                      #se il numero è maggiore o uguale al contatore: il contatore viene aggiornato per non avere doppioni
                      if numero_attuale >= self.contatore_strumenti:
                          self.contatore_strumenti = numero_attuale + 1

      except FileNotFoundError:
          raise FileNotFoundError("Errore: file non trovato!")


    def aggiungi_strumento(self, tipo, marca, anno_acquisto, valore):
        """Aggiunge uno strumento nel deposito: aggiunge solo nel sistema e non aggiorna il file"""
        # TO
        codice= f"S{self.contatore_strumenti}"  #racchiudo i dati in un oggetto
        self.contatore_strumenti += 1

        nuovo_strumento=Strumento(codice, tipo, marca, anno_acquisto, valore)
        self.strumenti[codice] = nuovo_strumento  #aggiungo l'oggetto creato nel dizionario

        return nuovo_strumento


    def strumenti_ordinati_per_marca(self):
        """Ordina gli strumenti per marca in ordine alfabetico"""
        return sorted(self.strumenti.values(), key=attrgetter("marca"))
        #self.strumenti.values() prende solo gli oggetti Strumento dal dizionario
        #condizione di attrgetter("marca"): ordina alafabeticamente la marca

    def nuovo_prestito(self, data, id_strumento, cognome_allievo):
        """Crea un nuovo prestito"""
        if id_strumento not in self.strumenti:
            raise Exception(f"lo strumento {id_strumento} non c'è")  #id_strumento è la chiave del dizionario

        for prestito in self.prestiti.values():  #estrae tutti i prestiti in atto per capire se lo strumento richiesto è disponibile o è gia stato prestato
            if prestito.id_strumento == id_strumento:
                raise Exception(f"lo strumento {id_strumento} è gia stato prestato")

        #genero il codice del prestito:
        codice_prestito = f"P{self.contatore_prestiti}"
        self.conatore_prestiti +=1

        #creo un nuovo oggetto e lo metto nel dizionario dei prestiti
        nuovo_p=Prestito(codice_prestito, data, id_strumento, cognome_allievo)
        self.prestiti[codice_prestito] = nuovo_p

        return nuovo_p


    def termina_prestito(self, id_prestito):
        """Termina un prestito in atto"""
       if id_prestito not in self.prestiti:
           raise Exception("prestito non trovato")

       del self.prestiti[id_prestito] #lo elimino dal dizionario dei prestiti perchè il prestito è terminato
