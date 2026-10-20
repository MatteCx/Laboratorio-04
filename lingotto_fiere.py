from csv import reader
from logging import exception
from operator import itemgetter

class stand:
    def __init__(self, idS, mq, padiglione, prezzoBase, infoExtra):
        self.__idS = idS
        self.__mq = mq
        self.__padiglione = padiglione
        self.__prezzoBase = prezzoBase
        self.__infoExtra = infoExtra
        self.__assigned = None
        if self.__infoExtra is None:
            self.__prezzo = float(self.__prezzoBase)
        elif self.__infoExtra.isalpha():
            self.__prezzo = float(self.__prezzoBase*1.30)
        elif self.__infoExtra.isdigit():
            self.__prezzo = float(self.__prezzoBase *(1+0.07*int(self.__infoExtra)))
        self.__prezzo = round(self.__prezzo, 2)

    def __str__(self):
        if self.__assigned is None: disp = "Disponibile"
        else: disp = "Non Disponibile"
        if self.__infoExtra is None:
            return f"{self.__idS:<3}: Standard | {self.__mq:^4} mq - Padiglione {self.__padiglione:^3} - Prezzo {self.__prezzo:>8}€ - {disp}"
        elif self.__infoExtra.isdigit():
            return f"{self.__idS:<3}: Premium  | {self.__mq:^4} mq - Padiglione {self.__padiglione:^3} - Prezzo {self.__prezzo:>8}€ - {"Prese aggiuntive:" + str(self.__infoExtra):<25} - {disp}"
        else:
            return f"{self.__idS:<3}: Premium  | {self.__mq:^4} mq - Padiglione {self.__padiglione:^3} - Prezzo {self.__prezzo:>8}€ - {"Posizione:" + self.__infoExtra:<25} - {disp}"

    def available(self):
        if self.__assigned is None: return True
        else: return False

    def assign(self, Espositore):
        self.__assigned = Espositore

    def __lt__(self, other):
        return self.__prezzo < other.__prezzo

    @property
    def idS(self):
        return self.__idS
    def prezzo(self):
        return self.__prezzo

class Espositore:
    def __init__(self, idE, nome, cognome):
        self.__idE = idE
        self.__nome = nome
        self.__cognome = cognome
        self.__assignedStand = None

    def freeToRent(self):
        if self.__assignedStand is None: return True
        else: return False

    def rent(self, Stand):
        self.__assignedStand = Stand

    def __str__(self):
        if self.__assignedStand is None:
            return f"{self.__idE:^20}|{self.__nome:>10} {self.__cognome:<10}|"
        else:
            return f"{self.__idE:^20}|{self.__nome:>10} {self.__cognome:<10}|{self.__assignedStand.idS:^20}"

    @property
    def idE(self):
        return self.__idE

class LingottoFiere:
    def __init__(self, nome):
        """Inizializza gli attributi e le strutture dati"""
        # TODO --------DONE----------
        self.__nome = nome
        self.__stand = []
        self.__espositori = []
        self.__registroAssegnazioni = []

    @property
    def nome(self):
        return self.__nome
    @nome.setter
    def nome(self, nome):
        self.__nome = nome

    """Aggiungere setter e getter se necessari"""
    # TODO --------DONE----------

    def carica_file_dati(self, file_path):
        """Carica i dati (stand ed espositori) dal file"""
        # TODO ---------DONE---------
        try:
            with open(file_path, "r") as file_raw:
                file = reader(file_raw, delimiter=",")
                for riga in file:
                    if riga[0][0] == "S":
                        if len(riga) == 4:
                            self.__stand.append(stand(idS=riga[0], mq=float(riga[1]), padiglione=int(riga[2]), prezzoBase=float(riga[3]), infoExtra=None))
                        else:
                            self.__stand.append(stand(idS=riga[0], mq=float(riga[1]), padiglione=int(riga[2]), prezzoBase=float(riga[3]), infoExtra=riga[4]))
                    elif riga[0][0] == "E":
                        self.__espositori.append(Espositore(riga[0], riga[1], riga[2]))
                    else:
                        print(f"Nel file sono presenti dati non validi che verranno ignorati")
        except Exception as e:
            print(e)

    def assegna_stand_a_espositore(self, codice_stand, codice_espositore):
        """Associa uno stand a un espositore"""
        # TODO ----------DONE----------
        stend = [s for s in self.__stand if s.idS == codice_stand]
        esp =  [e for e in self.__espositori if e.idE == codice_espositore]
        if stend == []: raise Exception(f"Codice Stand non valido")
        if esp == []: raise Exception(f"Codice Esposito non valido")

        stend = stend[0]
        esp = esp[0]

        if not stend.available(): raise Exception(f"Stend non disponibile")
        elif not esp.freeToRent(): raise Exception(f"Espositore non disponibile")

        self.__registroAssegnazioni.append((stend, esp))
        esp.rent(stend)
        stend.assign(esp)

    def elenca_espositori(self):
        """Stampa l'elenco degli espositori mostrando, per ognuno, lo stand a cui è associato, quando applicabile """
        # TODO --------DONE-----------
        print(f"{"CODICE ESPOSITORE":^20}|{"NOME":>10} {"COGNOME":<10}|{"STEND (SE PRESENTE)":^20}")
        for esp in self.__espositori:
            print(esp)

    def stand_ordinati_per_prezzo(self):
        """Restituisce la lista ordinata degli stand in base al prezzo"""
        # TODO -------------DONE--------------
        return sorted(stand for stand in self.__stand)
