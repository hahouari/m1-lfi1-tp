from terme import Terme
from equation import Equation
from typing import List


class Regle:
    def valider_suppression(equations: List[Equation], index: int):
        gauche, droite = equations[index].split()
        return gauche == droite

    def valider_decomposition(equations: List[Equation], index: int):
        gauche, droite = equations[index].split()
        return gauche.type == droite.type == 'Fonction'

    def valider_orientation(equations: List[Equation], index: int):
        gauche, droite = equations[index].split()
        return droite.type == 'Variable' and gauche.type != 'Variable'

    def valider_elimination(equations: List[Equation], index: int):
        gauche, _ = equations[index].split()
        pre_equations = equations[:index] + equations[index+1:]
        return gauche.type == 'Variable' and Regle.verifier_occurence(pre_equations, gauche)

    def supprimer(equations: List[Equation], index: int):
        equations.pop(index)
        return equations

    def decomposer(equations: List[Equation], index: int):
        gauche, droite = equations[index].split()

        if gauche.match == droite.match:
            if len(gauche.sous_termes) == len(droite.sous_termes):
                equations.pop(index)
                for g_terme, d_terme in zip(reversed(gauche.sous_termes), reversed(droite.sous_termes)):
                    equations.insert(index, Equation(g_terme, d_terme))
                return equations
            return -1
        return -2

    def orienter(equations: List[Equation], index: int):
        gauche, droite = equations[index].split()
        equations.pop(index)
        equations.insert(index, Equation(droite, gauche))
        return equations

    def eliminer(equations: List[Equation], index: int):
        gauche, droite = equations[index].split()
        if droite.type == 'Fonction' and gauche.verifier_occurence(droite.sous_termes):
            return -1
        pre_equations = equations[:index] + equations[index+1:]
        Regle.__terme_remplaceur(pre_equations, gauche, droite)
        return equations

    def verifier_occurence(equations: List[Equation], terme: Terme):
        """
        detects if a term is in one of the equations sent
        """
        if len(equations) == 0:
            return False

        equation = equations[0]
        if equation.gauche == terme or equation.droite == terme:
            return True

        if equation.gauche.type == 'Fonction':
            if terme.verifier_occurence(equation.gauche.sous_termes):
                return True
        if equation.droite.type == 'Fonction':
            if terme.verifier_occurence(equation.droite.sous_termes):
                return True
        return Regle.verifier_occurence(equations[1:], terme)

    def __params_remplaceur(sous_termes: List[Terme], old_terme: Terme, new_terme: Terme):
        new_sous_termes: List[Terme] = []
        for terme in sous_termes:
            new_sous_termes.append(
                new_terme if terme == old_terme else terme
            )
            if terme.type == 'Fonction':
                terme.sous_termes = Regle.__params_remplaceur(
                    terme.sous_termes, old_terme, new_terme
                )
        return new_sous_termes

    def __terme_remplaceur(equations: List[Equation], old_terme: Terme, new_terme: Terme):
        """
        used on the 4th rule where every occurance of the old term is replaced with new term
        """
        if len(equations) == 0:
            return

        equation = equations[0]
        if equation.gauche == old_terme:
            equation.gauche = new_terme
        elif equation.gauche.type == 'Fonction':
            equation.gauche.sous_termes = Regle.__params_remplaceur(
                equation.gauche.sous_termes, old_terme, new_terme
            )
        if equation.droite == old_terme:
            equation.droite = new_terme
        elif equation.droite.type == 'Fonction':
            equation.droite.sous_termes = Regle.__params_remplaceur(
                equation.droite.sous_termes, old_terme, new_terme
            )
        Regle.__terme_remplaceur(equations[1:], old_terme, new_terme)
