from database.DAO import DAO
import copy

class Model:
    def __init__(self):
        self._tot_ore_outages = None
        self._solBest = []
        self._listNerc = None
        self._listEvents = None
        self.loadNerc()
        self._anno_inizio = -1
        self._max_persone_coinvolte = -1
        self._tot_ore_bo = -1


    def worstCase(self, nerc, maxY, maxH):
        self._solBest = []
        self._anno_inizio = -1
        self._tot_ore_bo = -1
        self._max_persone_coinvolte = -1
        self._listEvents = None
        self._tot_ore_outages = None
        self.loadEvents(nerc)
        self.ricorsione([], maxY, maxH, self._listEvents)
        return self._solBest, self._max_persone_coinvolte, self._tot_ore_outages

    def ricorsione(self, parziale, maxY, maxH, lista_eventi):
        if self._tot_ore_bo > int(maxH):
            evento = parziale.pop()
            self._tot_ore_bo -= (evento.date_event_finished-evento.date_event_began).total_seconds()/3600
            persone_coinvolte = self._conta_persone(parziale)
            if persone_coinvolte > self._max_persone_coinvolte:
                self._solBest = copy.deepcopy(parziale)
                self._max_persone_coinvolte = persone_coinvolte
                self._tot_ore_outages = self._somma_ore_parziale(parziale)
                print(self._solBest)
        else:
            for blackout in lista_eventi:
                if self._condizioni_rispettate(parziale, blackout, maxY):
                    parziale.append(blackout)
                    self._tot_ore_bo += (blackout.date_event_finished-blackout.date_event_began).total_seconds()/3600
                    self.ricorsione(parziale, maxY, maxH, lista_eventi)
            if len(parziale) != 0:
                ev = parziale.pop()
                self._tot_ore_bo -= (ev.date_event_finished - ev.date_event_began).total_seconds() / 3600
    def _condizioni_rispettate(self, parziale, blackout, maxY):
        if len(parziale) == 0:
            self._anno_inizio = blackout.date_event_began.year
            return True
        elif parziale[-1].date_event_began < blackout.date_event_began and (blackout.date_event_began.year > self._anno_inizio and (blackout.date_event_began.year - self._anno_inizio) < int(maxY)):
            return True
        return False

    def _conta_persone(self, parziale):
        n_persone = 0
        for blackout in parziale:
            n_persone += blackout.customers_affected
        return n_persone


    def loadEvents(self, nerc):
        self._listEvents = DAO.getAllEvents(nerc)

    def loadNerc(self):
        self._listNerc = DAO.getAllNerc()

    def trova_id_NERC(self, nerc_value):
        for nerc in self._listNerc:
            if nerc.value == nerc_value:
                return nerc.id

    @property
    def listNerc(self):
        return self._listNerc

    def _somma_ore_parziale(self, parziale):
        somma_ore = 0
        for bo in parziale:
            somma_ore += (bo.date_event_finished-bo.date_event_began).total_seconds()/3600
        return somma_ore

