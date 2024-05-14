import flet as ft
from model.model import Model
from UI.view import View
from model.nerc import Nerc


class Controller:
    def __init__(self, view: View, model: Model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._idMap = {}
        self.fillIDMap()
        self._NERC_id = None
        self._maxH = None
        self._maxY = None

    def handleWorstCase(self, e):
        try:
            int(self._maxH)
            int(self._maxY)
        except ValueError:
            self._view.create_alert("I valori delle ore e degli anni devono essere numeri interi")
            return
        sol_best, persone_coinvolete, tot_ore = self._model.worstCase(self._NERC_id, self._maxY, self._maxH)
        self._view._txtOut.controls.append(ft.Text(f"Totale persone coinvolte: {persone_coinvolete}"))
        self._view._txtOut.controls.append(ft.Text(f"Totale ore di disservizio: {tot_ore}"))
        for evento in sol_best:
            self._view._txtOut.controls.append(ft.Text(evento))
        self._view.update_page()

    def fillDD(self):
        nercList = self._model.listNerc

        for n in nercList:
            self._view._ddNerc.options.append(ft.dropdown.Option(n))
        self._view.update_page()

    def fillIDMap(self):
        values = self._model.listNerc
        for v in values:
            self._idMap[v.value] = v

    def setNERC(self, e):
        value = self._view._ddNerc.value
        self._NERC_id = self._model.trova_id_NERC(value)

    def setMaxH(self, e):
        self._maxH = self._view._txtHours.value

    def setMaxY(self, e):
        self._maxY = self._view._txtYears.value

