import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model


    def fillDDsYears(self, dd: ft.Dropdown()):
        years= self._model.getAllYears()
        for y in years:
            dd.options.append(ft.dropdown.Option(text=y))

    def handleBuildGraph(self, e):
        ymin = self._view._ddYear1.value
        ymax = self._view._ddYear1.value

        if ymin is None or ymax is None:
            self._view.create_alert("Seleziona entrambi i rating")
            return

        if ymin > ymax:
            self._view.create_alert("Il voto minimo non può essere maggiore del voto massimo.")
            return

        self._model.creaGrafo(ymin, ymax)
        n, m = self._model.getGraphDetails()
        self._view._txt_result.controls.clear()
        self._view._txt_result.controls.append(
            ft.Text(f"Grafo correttamente creato! "
                    f"Il grafo è costituito di {n} nodi e {m} archi")
        )
        self._view.update_page()

    def handlePrintDetails(self, e):
        pass

    def handleCercaDreamChampionship(self, e):
        pass


