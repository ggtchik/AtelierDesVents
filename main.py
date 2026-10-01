import random
import math

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.widget import Widget
from kivy.uix.scrollview import ScrollView
from kivy.graphics import Color, Line, Ellipse, Rectangle
from kivy.core.text import Label as CoreLabel

# ============================================================
#  "L’Atelier des vents" — Version Kivy / Android
# ============================================================

INSTRUMENTS = {
    "Sax alto — Mib": 3,
    "Sax baryton — Mib": -21,
    "Sax ténor — Sib": -2,
    "Sax soprano — Sib": 10,
    "Piano / instrument en Do": 0
}

NOTES_CHROMATIQUES = {
    "Do": 0, "Do#": 1, "Ré": 2, "Mi♭": 3, "Mi": 4, "Fa": 5,
    "Fa#": 6, "Sol": 7, "Sol#": 8, "La": 9, "Si♭": 10, "Si": 11
}

NOMS_NOTES = [
    "Do", "Do#", "Ré", "Mi♭", "Mi", "Fa",
    "Fa#", "Sol", "Sol#", "La", "Si♭", "Si"
]

NOTATION_ANGLO = {
    "Do": "C", "Do#": "C#", "Ré": "D", "Mi♭": "Eb", "Mi": "E", "Fa": "F",
    "Fa#": "F#", "Sol": "G", "Sol#": "G#", "La": "A", "Si♭": "Bb", "Si": "B"
}

def note_anglo(note):
    return NOTATION_ANGLO.get(note, "")

OCTAVES_REGISTRES = {
    "grave": {
        "Si♭": 2, "Si": 2, "Do": 3, "Do#": 3, "Ré": 3, "Mi♭": 3,
        "Mi": 3, "Fa": 3, "Fa#": 3, "Sol": 3, "Sol#": 3, "La": 3
    },
    "medium": {
        "Si♭": 3, "Si": 3, "Do": 4, "Do#": 4, "Ré": 4, "Mi♭": 4,
        "Mi": 4, "Fa": 4, "Fa#": 4, "Sol": 4, "Sol#": 4, "La": 4
    },
    "aigu": {
        "Si♭": 4, "Si": 4, "Do": 5, "Do#": 5, "Ré": 5, "Mi♭": 5,
        "Mi": 5, "Fa": 5, "Fa#": 5
    }
}

NIVEAUX = {
    "Débutant": {
        "notes": [
            ("Do", "grave"), ("Ré", "grave"), ("Mi♭", "grave"), ("Mi", "grave"),
            ("Fa", "grave"), ("Fa#", "grave"), ("Sol", "grave"), ("Sol#", "grave"), ("La", "grave"),
            ("Si♭", "medium"), ("Si", "medium"), ("Do", "medium"), ("Do#", "medium"),
            ("Ré", "medium"), ("Mi♭", "medium"), ("Mi", "medium"), ("Fa", "medium"),
            ("Fa#", "medium"), ("Sol", "medium"), ("Sol#", "medium"), ("La", "medium"),
            ("Si♭", "aigu"), ("Si", "aigu"), ("Do", "aigu"), ("Do#", "aigu")
        ],
        "jokers": 1
    },
    "Moyen": {
        "notes": [
            ("Do", "grave"), ("Do#", "grave"), ("Ré", "grave"), ("Mi♭", "grave"),
            ("Mi", "grave"), ("Fa", "grave"), ("Fa#", "grave"), ("Sol", "grave"),
            ("Sol#", "grave"), ("La", "grave"),
            ("Si♭", "medium"), ("Si", "medium"), ("Do", "medium"), ("Do#", "medium"),
            ("Ré", "medium"), ("Mi♭", "medium"), ("Mi", "medium"), ("Fa", "medium"),
            ("Fa#", "medium"), ("Sol", "medium"), ("Sol#", "medium"), ("La", "medium"),
            ("Si♭", "aigu"), ("Si", "aigu"), ("Do", "aigu"), ("Do#", "aigu"), ("Mi♭", "aigu")
        ],
        "jokers": 2
    },
    "Confirmé": {
        "notes": [
            ("Si♭", "grave"), ("Si", "grave"), ("Do", "grave"), ("Do#", "grave"),
            ("Ré", "grave"), ("Mi♭", "grave"), ("Mi", "grave"), ("Fa", "grave"),
            ("Fa#", "grave"), ("Sol", "grave"), ("Sol#", "grave"), ("La", "grave"),
            ("Si♭", "medium"), ("Si", "medium"), ("Do", "medium"), ("Do#", "medium"),
            ("Ré", "medium"), ("Mi♭", "medium"), ("Mi", "medium"), ("Fa", "medium"),
            ("Fa#", "medium"), ("Sol", "medium"), ("Sol#", "medium"), ("La", "medium"),
            ("Si♭", "aigu"), ("Si", "aigu"), ("Do", "aigu"), ("Do#", "aigu"),
            ("Mi♭", "aigu"), ("Mi", "aigu"), ("Fa", "aigu"), ("Fa#", "aigu")
        ],
        "jokers": 3
    }
}

PENTATONIQUES_MAJEURES = {
    "Do": ["Do", "Ré", "Mi", "Sol", "La"],
    "Do#": ["Do#", "Mi♭", "Fa", "Sol#", "Si♭"],
    "Ré": ["Ré", "Mi", "Fa#", "La", "Si"],
    "Mi♭": ["Mi♭", "Fa", "Sol", "Si♭", "Do"],
    "Mi": ["Mi", "Fa#", "Sol#", "Si", "Do#"],
    "Fa": ["Fa", "Sol", "La", "Do", "Ré"],
    "Fa#": ["Fa#", "Sol#", "Si♭", "Do#", "Mi♭"],
    "Sol": ["Sol", "La", "Si", "Ré", "Mi"],
    "Sol#": ["Sol#", "Si♭", "Do", "Mi♭", "Fa"],
    "La": ["La", "Si", "Do#", "Mi", "Fa#"],
    "Si♭": ["Si♭", "Do", "Ré", "Fa", "Sol"],
    "Si": ["Si", "Do#", "Mi♭", "Fa#", "Sol#"]
}

PENTATONIQUES_MINEURES = {
    "Do": ["Do", "Mi♭", "Fa", "Sol", "Si♭"],
    "Do#": ["Do#", "Mi", "Fa#", "Sol#", "Si"],
    "Ré": ["Ré", "Fa", "Sol", "La", "Do"],
    "Mi♭": ["Mi♭", "Fa#", "Sol#", "Si♭", "Do#"],
    "Mi": ["Mi", "Sol", "La", "Si", "Ré"],
    "Fa": ["Fa", "Sol#", "Si♭", "Do", "Mi♭"],
    "Fa#": ["Fa#", "La", "Si", "Do#", "Mi"],
    "Sol": ["Sol", "Si♭", "Do", "Ré", "Fa"],
    "Sol#": ["Sol#", "Si", "Do#", "Mi♭", "Fa#"],
    "La": ["La", "Do", "Ré", "Mi", "Sol"],
    "Si♭": ["Si♭", "Do#", "Mi♭", "Fa", "Sol#"],
    "Si": ["Si", "Ré", "Mi", "Fa#", "La"]
}

TONALITES = ["Do", "Do#", "Ré", "Mi♭", "Mi", "Fa", "Fa#", "Sol", "Sol#", "La", "Si♭", "Si"]
EXERCICES = ["Gammes", "Pentatonique", "Blues", "Arpèges", "Degrés", "Triades", "Intervalles", "Notes chromatiques", "Cercle des quintes"]
MODES = ["Majeure", "Mineure"]

INTERVALLES_GAMME_MAJEURE = [0, 2, 4, 5, 7, 9, 11, 12]
INTERVALLES_GAMME_MINEURE = [0, 2, 3, 5, 7, 8, 10, 12]

INTERVALLES_EXERCICE = {
    "Seconde mineure": 1, "Seconde majeure": 2, "Tierce mineure": 3, "Tierce majeure": 4,
    "Quarte juste": 5, "Triton": 6, "Quinte juste": 7, "Sixte mineure": 8, "Sixte majeure": 9,
    "Septième mineure": 10, "Septième majeure": 11, "Octave": 12
}

PROGRESSIONS = {
    "Tous les degrés": [1, 2, 3, 4, 5, 6, 7],
    "II – V – I": [2, 5, 1],
    "I – IV – V": [1, 4, 5],
    "I – VI – II – V": [1, 6, 2, 5],
    "I – V – VI – IV": [1, 5, 6, 4]
}

TYPES_TRIADES = ["Majeure", "Mineure", "Diminuée", "Augmentée"]
INTERVALLES_TRIADES = {
    "Majeure": [0, 4, 7], "Mineure": [0, 3, 7],
    "Diminuée": [0, 3, 6], "Augmentée": [0, 4, 8]
}

DEGRES_ROMAINS = ["I", "II", "III", "IV", "V", "VI", "VII"]
QUALITES_ACCORDS_MAJEURS = ["maj7", "m7", "m7", "maj7", "7", "m7", "m7♭5"]
QUALITES_ACCORDS_MINEURS = ["m7", "m7♭5", "maj7", "m7", "m7", "maj7", "7"]

CERCLE_MAJEUR = ["Do", "Sol", "Ré", "La", "Mi", "Si", "Fa#", "Do#", "Sol#", "Mi♭", "Si♭", "Fa"]
CERCLE_MINEUR = ["La", "Mi", "Si", "Fa#", "Do#", "Sol#", "Mi♭", "Si♭", "Fa", "Do", "Sol", "Ré"]

COULEURS_REGISTRES = {
    "grave": (0.95, 0.82, 0.36, 1),
    "medium": (0.91, 0.36, 0.45, 1),
    "aigu": (0.31, 0.56, 0.85, 1),
    "joker": (0.93, 0.93, 0.93, 1)
}

# ============================================================
# FONCTIONS MUSICALES
# ============================================================

def note_en_concert(note, octave, instrument):
    if note == "Joker" or note not in NOTES_CHROMATIQUES:
        return "—"
    indice = NOTES_CHROMATIQUES[note]
    decalage = INSTRUMENTS[instrument]
    indice_concert = indice + decalage
    octave_concert = octave
    while indice_concert < 0:
        indice_concert += 12
        octave_concert -= 1
    while indice_concert >= 12:
        indice_concert -= 12
        octave_concert += 1
    return f"{NOMS_NOTES[indice_concert]}{octave_concert}"

def trouver_octave(note):
    if note in OCTAVES_REGISTRES["medium"]:
        return OCTAVES_REGISTRES["medium"][note]
    if note in OCTAVES_REGISTRES["grave"]:
        return OCTAVES_REGISTRES["grave"][note]
    if note in OCTAVES_REGISTRES["aigu"]:
        return OCTAVES_REGISTRES["aigu"][note]
    return 4

def note_avec_intervalle(tonalite, demi_tons, octave_depart=4):
    fondamentale = NOTES_CHROMATIQUES[tonalite]
    valeur_absolue = fondamentale + demi_tons
    position = valeur_absolue % 12
    octave = octave_depart + valeur_absolue // 12
    return NOMS_NOTES[position], octave

def construire_pentatonique(tonalite, mode):
    return PENTATONIQUES_MAJEURES[tonalite] if mode == "Majeure" else PENTATONIQUES_MINEURES[tonalite]

def construire_arpege(tonalite, mode):
    f = NOTES_CHROMATIQUES[tonalite]
    t = (f + 4) % 12 if mode == "Majeure" else (f + 3) % 12
    q = (f + 7) % 12
    return [NOMS_NOTES[f], NOMS_NOTES[t], NOMS_NOTES[q]]

def calcul_blue_note(tonalite):
    return NOMS_NOTES[(NOTES_CHROMATIQUES[tonalite] + 6) % 12]

def chord_symbol(note, qualite):
    racines = {
        "Do": "C", "Do#": "C#", "Ré": "D", "Mi♭": "Eb", "Mi": "E", "Fa": "F",
        "Fa#": "F#", "Sol": "G", "Sol#": "G#", "La": "A", "Si♭": "Bb", "Si": "B"
    }
    return racines[note] + qualite

# ============================================================
# COMPOSANTS GRAPHIQUES (PORTÉE ET CERCLE)
# ============================================================

class StaffWidget(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(pos=self.update_canvas, size=self.update_canvas)
        self.notes = []

    def set_notes(self, notes):
        self.notes = notes
        self.update_canvas()

    def _indice_diatonique(self, note, octave):
        lettres = {"Do": 0, "Ré": 1, "Mi": 2, "Fa": 3, "Sol": 4, "La": 5, "Si": 6}
        for nom, idx in lettres.items():
            if note.startswith(nom):
                return octave * 7 + idx
        return octave * 7

    def update_canvas(self, *args):
        self.canvas.clear()
        if not self.notes:
            return

        with self.canvas:
            # Fond blanc/crème
            Color(0.98, 0.98, 0.96, 1)
            Rectangle(pos=self.pos, size=self.size)

            gauche = self.x + 40
            droite = self.x + self.width - 20
            espacement = 14
            y_bas = self.y + self.height / 2 + espacement * 2

            # Lignes de portée
            Color(0.2, 0.2, 0.2, 1)
            for i in range(5):
                y = y_bas - i * espacement
                Line(points=[gauche, y, droite, y], width=1)

            # Dessin simplifié des notes
            ref = 4 * 7 + 2  # Mi4
            nb_notes = len(self.notes)
            pas_x = (droite - gauche - 60) / max(1, nb_notes - 1)

            for i, item in enumerate(self.notes):
                if len(item) == 3:
                    note, _, octave = item
                else:
                    note, _ = item
                    octave = trouver_octave(note)

                x = gauche + 40 + i * pas_x

                if note == "Joker":
                    continue

                idx = self._indice_diatonique(note, octave)
                diff = idx - ref
                y = y_bas - diff * (espacement / 2)

                # Tête de note
                Color(0.15, 0.15, 0.15, 1)
                Ellipse(pos=(x - 6, y - 5), size=(12, 10))
                # Hampe
                Line(points=[x + 5, y, x + 5, y + 25], width=1.5)


class CircleOfFifthsWidget(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(pos=self.update_canvas, size=self.update_canvas)
        self.selected_tonalite = "Do"

    def set_tonalite(self, ton):
        self.selected_tonalite = ton
        self.update_canvas()

    def update_canvas(self, *args):
        self.canvas.clear()
        with self.canvas:
            Color(1, 1, 1, 1)
            Rectangle(pos=self.pos, size=self.size)

            cx = self.x + self.width / 2
            cy = self.y + self.height / 2
            rayon = min(self.width, self.height) * 0.35

            Color(0.7, 0.7, 0.7, 1)
            Line(circle=(cx, cy, rayon), width=2)

            for i, ton in enumerate(CERCLE_MAJEUR):
                angle = math.radians((i * 30) - 90)
                x = cx + rayon * math.cos(angle)
                y = cy + rayon * math.sin(angle)

                if ton == self.selected_tonalite:
                    Color(0.4, 0.7, 0.4, 1)
                else:
                    Color(0.9, 0.9, 0.9, 1)

                Ellipse(pos=(x - 22, y - 22), size=(44, 44))


# ============================================================
# APPLICATION PRINCIPALE
# ============================================================

class AtelierDesVentsApp(App):
    def build(self):
        self.mode_actuel = "Majeure"
        self.dernier_tirage = []

        root = BoxLayout(orientation='vertical')

        # ----------------------------------------------------
        # En-tête
        # ----------------------------------------------------
        header = BoxLayout(orientation='vertical', size_hint_y=None, height=70)
        with header.canvas.before:
            Color(0.06, 0.16, 0.26, 1)
            self.rect_header = Rectangle(pos=header.pos, size=header.size)
        header.bind(pos=self._update_rect, size=self._update_rect)

        title = Label(text="DU SOUFFLE À LA MUSIQUE", font_size='18sp', bold=True, color=(1, 1, 1, 1))
        subtitle = Label(text="L’Atelier des vents • Boîte à outils du musicien", font_size='12sp', color=(0.7, 0.85, 0.9, 1))
        header.add_widget(title)
        header.add_widget(subtitle)
        root.add_widget(header)

        # ----------------------------------------------------
        # Zone de Contrôles / Spinners
        # ----------------------------------------------------
        controls_scroll = ScrollView(size_hint_y=None, height=110)
        controls = GridLayout(rows=2, cols=3, spacing=5, padding=5, size_hint_x=1)

        self.spin_exercice = Spinner(text="Gammes", values=EXERCICES)
        self.spin_niveau = Spinner(text="Débutant", values=list(NIVEAUX.keys()))
        self.spin_mode = Spinner(text="Majeure", values=MODES)
        self.spin_tonalite = Spinner(text="Do", values=TONALITES)
        self.spin_option = Spinner(text="Progression", values=["Tous les degrés"])
        self.spin_instrument = Spinner(text="Sax alto — Mib", values=list(INSTRUMENTS.keys()))

        self.spin_exercice.bind(text=self.on_change)
        self.spin_niveau.bind(text=self.on_change)
        self.spin_mode.bind(text=self.on_change)
        self.spin_tonalite.bind(text=self.on_change)
        self.spin_option.bind(text=self.on_change)
        self.spin_instrument.bind(text=self.on_change)

        controls.add_widget(self.spin_exercice)
        controls.add_widget(self.spin_niveau)
        controls.add_widget(self.spin_mode)
        controls.add_widget(self.spin_tonalite)
        controls.add_widget(self.spin_option)
        controls.add_widget(self.spin_instrument)

        controls_scroll.add_widget(controls)
        root.add_widget(controls_scroll)

        # ----------------------------------------------------
        # Zone Titre de l'exercice actuel
        # ----------------------------------------------------
        self.label_info = Label(
            text="Initialisation...", font_size='15sp', bold=True,
            size_hint_y=None, height=40, color=(0.1, 0.2, 0.3, 1)
        )
        root.add_widget(self.label_info)

        # ----------------------------------------------------
        # Canvas Portée Musicale / Cercle
        # ----------------------------------------------------
        self.staff_widget = StaffWidget(size_hint_y=0.4)
        self.circle_widget = CircleOfFifthsWidget(size_hint_y=0.4)
        root.add_widget(self.staff_widget)

        # ----------------------------------------------------
        # Grille d'affichage des 8 Notes / Accord
        # ----------------------------------------------------
        self.grid_notes = GridLayout(cols=4, rows=2, spacing=5, padding=5, size_hint_y=0.35)
        self.cards = []
        for i in range(8):
            btn = Button(text="", font_size='13sp', halign='center', background_normal='')
            self.grid_notes.add_widget(btn)
            self.cards.append(btn)

        root.add_widget(self.grid_notes)

        # ----------------------------------------------------
        # Bouton Tirage
        # ----------------------------------------------------
        btn_tirage = Button(
            text="NOUVEAU TIRAGE", font_size='16sp', bold=True,
            size_hint_y=None, height=50, background_color=(0.2, 0.2, 0.2, 1)
        )
        btn_tirage.bind(on_press=lambda x: self.nouveau_tirage())
        root.add_widget(btn_tirage)

        self.nouveau_tirage()
        return root

    def _update_rect(self, instance, value):
        self.rect_header.pos = instance.pos
        self.rect_header.size = instance.size

    def on_change(self, spinner, text):
        self.mode_actuel = self.spin_mode.text
        self.nouveau_tirage()

    def nouveau_tirage(self):
        exercice = self.spin_exercice.text
        tonalite = self.spin_tonalite.text
        instrument = self.spin_instrument.text

        self.label_info.text = f"{exercice} — {tonalite} ({self.mode_actuel})"

        # Réinitialisation des cartes
        for c in self.cards:
            c.text = ""
            c.background_color = (0.9, 0.9, 0.9, 1)

        if exercice == "Notes chromatiques":
            donnees = NIVEAUX[self.spin_niveau.text]
            notes = list(donnees["notes"]) + [("Joker", "joker")] * donnees["jokers"]
            tirage = random.sample(notes, min(8, len(notes)))
            self.staff_widget.set_notes(tirage)

            for i, elem in enumerate(tirage):
                if i < 8:
                    n, reg = elem[0], elem[1]
                    octv = OCTAVES_REGISTRES.get(reg, {}).get(n, 4) if n != "Joker" else 4
                    concert = note_en_concert(n, octv, instrument)
                    self.cards[i].text = f"{n}\n{note_anglo(n)}\nUt: {concert}"
                    self.cards[i].background_color = COULEURS_REGISTRES.get(reg, (1, 1, 1, 1))

        elif exercice in ["Gammes", "Pentatonique", "Blues", "Arpèges"]:
            if exercice == "Gammes":
                interv = INTERVALLES_GAMME_MAJEURE if self.mode_actuel == "Majeure" else INTERVALLES_GAMME_MINEURE
                f = NOTES_CHROMATIQUES[tonalite]
                tirage = [(NOMS_NOTES[(f + v) % 12], None, 4 + (f + v) // 12) for v in interv]
            elif exercice == "Pentatonique":
                p = construire_pentatonique(tonalite, self.mode_actuel)
                tirage = [(n, None, 4) for n in p]
            elif exercice == "Blues":
                b = construire_pentatonique(tonalite, self.mode_actuel) + [calcul_blue_note(tonalite)]
                tirage = [(n, None, 4) for n in b]
            else: # Arpèges
                a = construire_arpege(tonalite, self.mode_actuel)
                tirage = [(n, None, 4) for n in a]

            self.staff_widget.set_notes(tirage)

            for i, elem in enumerate(tirage):
                if i < 8:
                    n = elem[0]
                    concert = note_en_concert(n, elem[2], instrument)
                    self.cards[i].text = f"{n}\n{note_anglo(n)}\nUt: {concert}"

        elif exercice == "Degrés":
            qualites = QUALITES_ACCORDS_MAJEURS if self.mode_actuel == "Majeure" else QUALITES_ACCORDS_MINEURS
            interv = INTERVALLES_GAMME_MAJEURE[:-1] if self.mode_actuel == "Majeure" else INTERVALLES_GAMME_MINEURE[:-1]
            self.staff_widget.set_notes([])

            for i in range(min(7, len(interv))):
                note, octv = note_avec_intervalle(tonalite, interv[i])
                symb = chord_symbol(note, qualites[i])
                concert = note_en_concert(note, octv, instrument)
                self.cards[i].text = f"{DEGRES_ROMAINS[i]}\n{note}\n{symb}\nUt: {concert}"

if __name__ == '__main__':
    AtelierDesVentsApp().run()
