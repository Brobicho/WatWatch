from PySide6.QtWidgets import (
    QWidget, QFileDialog, QVBoxLayout, QLabel,
    QPushButton, QLineEdit, QSpinBox, QListWidget, QListWidgetItem,
    QComboBox, QProgressBar, QTextEdit
)
from PySide6.QtCore import QThread, Signal

from api_clients import fetch_senscritique_collection, get_sc_global_rating
from recommender import get_recommendations
from visualization import show_bokeh
from file_utils import save_suggestions_to_xls


CATEGORIES = [
    "Film", "Série", "Court-métrage d'animation", "Long-métrage d'animation",
    "Émission TV", "Drama", "Documentaire", "Spectacle", "Album",
    "Court-métrage", "Moyen-métrage", "Manga", "Dessin animé",
    "Comics", "BD Franco-Belge", "Jeu"
]


class WorkerThread(QThread):
    """Background thread for processing with progress updates."""
    progress = Signal(int, int)
    status = Signal(str)
    finished_with_result = Signal(object)
    error = Signal(str)
    
    def __init__(self, username, n_suggestions, categories, model, output_file):
        super().__init__()
        self.username = username
        self.n_suggestions = n_suggestions
        self.categories = categories
        self.model = model
        self.output_file = output_file
    
    def run(self):
        try:
            self.status.emit("Récupération de la collection SensCritique...")
            
            def progress_callback(current, total):
                self.progress.emit(current, total)
            
            collection = fetch_senscritique_collection(self.username, progress_callback)
            self.status.emit(f"✓ {len(collection)} œuvres récupérées")
            
            self.status.emit("Recherche de suggestions...")
            self.progress.emit(0, 0)
            recos = get_recommendations(collection, self.n_suggestions, self.categories, self.model)
            self.status.emit(f"✓ {len(recos)} suggestions trouvées")
            
            self.status.emit("Récupération des notes SensCritique...")
            total_recos = len(recos)
            for i, reco in enumerate(recos):
                title = reco["title"]
                reco["rating_sc_global"] = get_sc_global_rating(title)
                self.progress.emit(i + 1, total_recos)
            
            self.status.emit("✓ Notes récupérées")
            
            if self.output_file:
                self.status.emit("Sauvegarde du fichier Excel...")
                save_suggestions_to_xls(recos, self.output_file)
                self.status.emit(f"✓ Fichier sauvegardé : {self.output_file}")
            
            self.finished_with_result.emit(recos)
            
        except Exception as e:
            self.error.emit(str(e))


class App(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("WatWatcher")
        self.setStyleSheet("""
            QWidget {
                background: #202124;
                color: white;
                font-size: 15px;
            }
            QPushButton {
                background: #3c4043;
                padding: 8px;
                border-radius: 6px;
            }
            QPushButton:hover {
                background: #5f6368;
            }
            QProgressBar {
                border: 2px solid #3c4043;
                border-radius: 5px;
                text-align: center;
                background: #2d2d2d;
            }
            QProgressBar::chunk {
                background-color: #4285f4;
                border-radius: 3px;
            }
            QTextEdit {
                background: #2d2d2d;
                border: 1px solid #3c4043;
                border-radius: 5px;
                padding: 5px;
            }
        """)

        layout = QVBoxLayout()

        self.user_input = QLineEdit()
        self.user_input.setPlaceholderText("Nom d'utilisateur SensCritique…")
        layout.addWidget(QLabel("Nom d'utilisateur"))
        layout.addWidget(self.user_input)

        layout.addWidget(QLabel("Nombre de suggestions"))
        self.nb_spin = QSpinBox()
        self.nb_spin.setMinimum(1)
        self.nb_spin.setMaximum(50)
        self.nb_spin.setValue(10)
        layout.addWidget(self.nb_spin)

        layout.addWidget(QLabel("Modèle OpenAI"))
        self.model_combo = QComboBox()
        self.model_combo.addItems(["gpt-4.1-mini", "gpt-4.1", "gpt-5.1"])
        layout.addWidget(self.model_combo)

        layout.addWidget(QLabel("Catégories"))
        self.cat_list = QListWidget()
        self.cat_list.setSelectionMode(QListWidget.MultiSelection)
        for c in CATEGORIES:
            item = QListWidgetItem(c)
            item.setSelected(True)
            self.cat_list.addItem(item)
        layout.addWidget(self.cat_list)

        self.output_file = None
        btn_out = QPushButton("Choisir fichier XLS de sortie…")
        btn_out.clicked.connect(self.select_output)
        layout.addWidget(btn_out)

        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)

        layout.addWidget(QLabel("Statut :"))
        self.log_display = QTextEdit()
        self.log_display.setReadOnly(True)
        self.log_display.setMaximumHeight(150)
        layout.addWidget(self.log_display)

        self.btn_run = QPushButton("Rechercher")
        self.btn_run.clicked.connect(self.run_all)
        layout.addWidget(self.btn_run)

        self.setLayout(layout)
        self.worker = None

    def select_output(self):
        fn, _ = QFileDialog.getSaveFileName(self, "Choisir fichier XLS", "", "Fichiers Excel (*.xlsx)")
        if fn:
            self.output_file = fn

    def run_all(self):
        username = self.user_input.text().strip()
        if not username:
            self.log("❌ Veuillez entrer un nom d'utilisateur")
            return

        n = self.nb_spin.value()
        model = self.model_combo.currentText()
        cats = [item.text() for item in self.cat_list.selectedItems()]

        self.btn_run.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        self.log_display.clear()
        
        self.worker = WorkerThread(username, n, cats, model, self.output_file)
        self.worker.progress.connect(self.on_progress)
        self.worker.status.connect(self.log)
        self.worker.finished_with_result.connect(self.on_finished)
        self.worker.error.connect(self.on_error)
        self.worker.start()
    
    def on_progress(self, current, total):
        if total > 0:
            self.progress_bar.setMaximum(total)
            self.progress_bar.setValue(current)
        else:
            self.progress_bar.setMaximum(0)
            self.progress_bar.setValue(0)
    
    def log(self, message):
        self.log_display.append(message)
    
    def on_finished(self, recos):
        self.progress_bar.setVisible(False)
        self.btn_run.setEnabled(True)
        self.log("\n✅ Terminé ! Affichage des résultats...")
        show_bokeh(recos)
    
    def on_error(self, error_msg):
        self.progress_bar.setVisible(False)
        self.btn_run.setEnabled(True)
        self.log(f"\n❌ Erreur : {error_msg}")
