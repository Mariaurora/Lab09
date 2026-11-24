

from database.parco_DAO import ParcoDAO
from database.escursione_DAO import EscursioneDAO
from database.punto_interesse_DAO import PuntoInteresseDAO



class Model:
    def __init__(self):
        self.escursioni_map = {} # Mappa ID escursione -> oggetti Escursione
        self.punti_interesse_map = {} # Mappa ID punto di interesse -> oggetti PuntoInteresse

        self._pacchetto_ottimo = []
        self._valore_ottimo: int = -1
        self._costo = 0

        # TODO: Aggiungere eventuali altri attributi

        # Caricamento
        self.load_escursioni()
        self.load_punti_interesse()
        self.load_relazioni()

    @staticmethod
    def load_parchi():
        """ Restituisce tutti i parchi disponibili """
        return ParcoDAO.get_parchi()

    def load_escursioni(self):
        """ Carica tutte le escursioni in un dizionario [id, Escursione]"""
        self.escursioni_map = EscursioneDAO.get_escursioni()

    def load_punti_interesse(self):
        """ Carica tutti i punti di interesse in un dizionario [id, PuntoInteresse]"""
        self.punti_interesse_map = PuntoInteresseDAO.get_punti_interesse()

    def load_relazioni(self):
        """
            Interroga il database per ottenere tutte le relazioni fra escursioni e punti di interesse e salvarle nelle strutture dati
            Collega escursione <-> punti di interesse.
            --> Ogni Escursione ha un set di PuntoInteresse.
            --> Ogni PuntoInteresse ha un set di Escursioni.
        """
        for dizionario in EscursioneDAO.get_escursioni_punti_interesse():
           id_escursione=dizionario["id_escursione"]
           id_punto_interesse=dizionario["id_punto_interesse"]
           for punto in self.punti_interesse_map:
               punto_riferimento=self.punti_interesse_map[punto]
               for escursione in self.escursioni_map:
                   escursione_riferimento=self.escursioni_map[escursione]
                   if id_escursione == escursione and id_punto_interesse==punto:
                       punto_riferimento.escursioni.add(escursione_riferimento)
                       escursione_riferimento.punti_interesse.add(punto_riferimento)

    def genera_pacchetto(self, id_parco: str, max_giorni: int = None, max_budget: float = None):
        """
        Calcola il pacchetto di escursioni ottimale per un parco rispettando i vincoli di durata, budget e punti di interesse unici.
        :param id_parco: id del parco
        :param max_giorni: numero massimo di giorni (può essere None --> nessun limite)
        :param max_budget: costo massimo del pacchetto (può essere None --> nessun limite)

        :return: self._pacchetto_ottimo (una lista di oggetti Escursione)
        :return: self._costo (il costo del pacchetto)
        :return: self._valore_ottimo (il voto complessivo dei visitatori per il pacchetto)
        """
        self._pacchetto_ottimo = []
        self._costo = 0
        self._valore_ottimo = -1

        # TODO
        self._ricorsione(0,[],0,0,0,set( ),id_parco,max_giorni, max_budget)
        return self._pacchetto_ottimo, self._costo, self._valore_ottimo

    def _ricorsione(self, start_index: int, pacchetto_parziale: list, durata_corrente: int, costo_corrente: float, valore_corrente: int, punti_usati: set ,parco_selezionato : str, max_giorni, max_budget):
        """ Algoritmo di ricorsione che deve trovare il pacchetto che massimizza il voto complessivo dei visitatori"""

        # TODO: è possibile cambiare i parametri formali della funzione se ritenuto opportuno

        if valore_corrente> self._valore_ottimo:
            self._pacchetto_ottimo =pacchetto_parziale.copy()
            self._valore_ottimo = valore_corrente
            self._costo=costo_corrente

        for i in range(start_index, len(self.escursioni_map)):
            escursione = list(self.escursioni_map.keys())[i]
            escursione_corrente = self.escursioni_map[escursione]
            if escursione_corrente.id_parco == parco_selezionato:
                punti_validi = True
                for punto in escursione_corrente.punti_interesse:
                    if punto in punti_usati:
                        punti_validi = False
                        break
                nuova_durata = durata_corrente + escursione_corrente.durata_giorni
                nuovo_costo = costo_corrente + escursione_corrente.costo

                if (punti_validi is True and (max_giorni is None or nuova_durata <= max_giorni) and (max_budget is None or nuovo_costo <= max_budget)):
                    nuovo_valore = valore_corrente
                    for punto in escursione_corrente.punti_interesse:
                        nuovo_valore += punto.voto_visitatori
                    pacchetto_parziale.append(escursione_corrente)
                    punti_usati.update(escursione_corrente.punti_interesse)
                    self._ricorsione( i + 1,pacchetto_parziale,nuova_durata, nuovo_costo,nuovo_valore,punti_usati,parco_selezionato,max_giorni,max_budget)
                    pacchetto_parziale.pop()

                    for punto in escursione_corrente.punti_interesse:
                        punti_usati.remove(punto)








