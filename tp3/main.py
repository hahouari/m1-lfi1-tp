#!/bin/python3

from typing import List
from terme import Terme
from analyse import Analyse
from unification import Unification
from equation import Equation
from PyQt5.QtGui import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QMargins

import sys


class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.setWindowTitle("Master 1 - LFI 1 - TP 4")

        g_layout = QHBoxLayout()
        l_layout = QVBoxLayout()
        l_layout.setContentsMargins(QMargins(0, 0, 4, 0))
        self.ops_layout = QVBoxLayout()
        self.ops_layout.setContentsMargins(QMargins())
        r_layout = QVBoxLayout()
        r_layout.setContentsMargins(QMargins())

        ops_label = QLabel("Inserer les deux termes:", self)
        l_layout.addWidget(ops_label)

        self.ops_left_inputs = []
        self.ops_right_inputs = []
        self.drop_btns = []

        ops_widget = QWidget(self)
        ops_widget.setLayout(self.ops_layout)
        l_layout.addWidget(ops_widget)

        self.insert_new_op()

        table_label = QLabel("La table des termes classifiées:", self)

        self.validate_btn = QPushButton(
            QIcon('./icons/validate.png'),
            ' &Valider',
            self
        )
        self.validate_btn.setFixedWidth(80)
        self.validate_btn.clicked.connect(self.on_validate)

        self.terms_table_holder = QPlainTextEdit()
        self.terms_table_holder.setReadOnly(True)

        valid_layout = QHBoxLayout()
        valid_layout.setContentsMargins(QMargins())
        valid_layout.addWidget(table_label)
        valid_layout.addWidget(self.validate_btn)

        valid_widget = QWidget(self)
        valid_widget.setLayout(valid_layout)
        l_layout.addWidget(valid_widget)

        l_layout.addWidget(self.terms_table_holder)

        l_widget = QWidget(self)
        l_widget.setLayout(l_layout)

        unification_label = QLabel("La table de l'unification:", self)
        self.unification_holder = QPlainTextEdit()
        self.unification_holder.setReadOnly(True)

        r_layout.addWidget(unification_label)
        r_layout.addWidget(self.unification_holder)

        r_widget = QWidget(self)
        r_widget.setLayout(r_layout)

        g_layout.addWidget(l_widget)
        g_layout.addWidget(r_widget)

        g_widget = QWidget(self)
        g_widget.setLayout(g_layout)

        self.setCentralWidget(g_widget)

    def insert_new_op(self):
        self.ops_left_inputs.append(QLineEdit(self))
        self.ops_right_inputs.append(QLineEdit(self))

        op_layout = QHBoxLayout()
        op_layout.setContentsMargins(QMargins())
        op_layout.addWidget(self.ops_left_inputs[-1])
        op_layout.addWidget(QLabel("=", self))
        op_layout.addWidget(self.ops_right_inputs[-1])

        op_widget = QWidget(self)
        op_widget.setLayout(op_layout)
        self.ops_layout.addWidget(op_widget)

    def on_validate(self):
        equations = []
        self.terms_table_holder.setPlainText('')

        for left_input, right_input in zip(self.ops_left_inputs, self.ops_right_inputs):
            if not left_input.text() or not right_input.text():
                self.terms_table_holder.insertPlainText(
                    '---------------------------------------------------\n' +
                    'Attention!! Une partie vide est détectée, donc celle l\'équation est ignorée.\n' +
                    '---------------------------------------------------\n'
                )
                continue

            liste_gauche = Analyse.analyse_lexical(left_input.text())
            liste_droite = Analyse.analyse_lexical(right_input.text())

            liste_gauche = Analyse.termes_separateur(liste_gauche)
            liste_droite = Analyse.termes_separateur(liste_droite)

            liste_gauche = Analyse.analyse_syntaxique(liste_gauche)
            liste_droite = Analyse.analyse_syntaxique(liste_droite)

            if len(liste_gauche) != len(liste_droite):
                self.terms_table_holder.insertPlainText(
                    '---------------------------------------------------\n' +
                    'Attention!! La partie gauche et partie droite n\'avons pas le même nombre des termes' +
                    ', donc le nombre minimum est gardé.\n' +
                    '---------------------------------------------------\n'
                )

            liste_min = min(len(liste_gauche), len(liste_droite))

            for gauche, droite in zip(liste_gauche[:liste_min], liste_droite[:liste_min]):
                equation = Equation(gauche, droite)
                equations.append(equation)

            self.terms_table_holder.insertPlainText(
                '---------------------------------------------------\n'
                '1er partie: ----------\n' +
                (Terme.terms_table(liste_gauche) or '<Pas des termes>\n') +
                '2eme partie: ----------\n' +
                (Terme.terms_table(liste_droite) or '<Pas des termes>\n')
            )

        unification = Unification(equations)
        self.unification_holder.setPlainText(unification.moteur_unification())


app = QApplication(sys.argv)
window = MainWindow()
window.resize(750, 500)
window.move(80, 100)
window.show()

app.exec_()
