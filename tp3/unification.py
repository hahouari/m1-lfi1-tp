from regle import Regle
from typing import List
from terme import Terme
from equation import Equation


class Unification:
    def __init__(self, equations: List[Equation]) -> None:
        self.equations = equations
        self.origin_eqs = equations.copy()
        self.feedback = ', '.join(map(
            lambda eq: str(eq), equations
        )) + '\n' if len(equations) > 0 else ''
        self.erreur = False

    def __str__(self):
        if len(self.feedback) == 0:
            return ''

        if len(self.equations) == 0:
            return '{}<Pas des équations>\n'.format(self.feedback)

        str_termes = '— {}, nous obtenons: '.format(self.feedback)
        str_termes += ', '.join(map(
            lambda eq: str(eq),
            self.equations
        )) + '.\n'

        if self.erreur:
            str_termes += '— Donc l\'équation(s) {} n\'a pas de solution.'.format(', '.join(map(
                lambda eq: str(eq), self.origin_eqs
            )) if len(self.origin_eqs) > 0 else '')

        return str_termes

    def __params_verifier_erreur(self, sous_termes: List[Terme]):
        if len(sous_termes) == 0:
            return False

        for terme in sous_termes:
            if terme.erreur:
                return True
            if terme.type == 'Fonction':
                if self.__params_verifier_erreur(
                    terme.sous_termes
                ):
                    return True
        return self.__params_verifier_erreur(sous_termes[1:])

    def verifier_erreur(self, equations: List[Equation]) -> bool:
        """
        applée par moteur de l'unification, vérifie que il n'y a pas des erreurs avant aller a l'unification
        """
        if len(equations) == 0:
            return False

        equation = equations[0]
        if equation.gauche.erreur or equation.droite.erreur:
            return True
        if equation.gauche.type == 'Fonction':
            if self.__params_verifier_erreur(equation.gauche.sous_termes):
                return True
        if equation.droite.type == 'Fonction':
            if self.__params_verifier_erreur(equation.droite.sous_termes):
                return True
        return self.verifier_erreur(equations[1:])

    def moteur_unification(self):
        # check any syntaxic errors generated before proceeding
        try:
            assert not self.verifier_erreur(self.equations)
        except AssertionError:
            return 'Il y\'a une erreur dans l\'analyse syntaxique'

        unif_process_msg = self.feedback

        while len(self.feedback) and not self.erreur:
            self.__unif_iter()
            unif_process_msg += str(self)

        return unif_process_msg

    def __unif_iter(self):
        self.feedback = ''

        for equation, index in zip(self.equations, range(1, len(self.equations) + 1)):
            if Regle.valider_suppression(self.equations, index-1):
                self.feedback = 'Par suppression'
                self.equations = Regle.supprimer(self.equations, index-1)
                return
            elif Regle.valider_decomposition(self.equations, index-1):
                resultat = Regle.decomposer(self.equations, index-1)
                if type(resultat) is list:
                    self.feedback = 'Par décomposition'
                    self.equations = resultat
                else:
                    self.erreur = True
                    self.feedback = 'L’équation {} engendre un échec de décomposition'.format(
                        equation
                    )
                    if resultat == -1:
                        self.feedback += ', nombre de paramètres n\'est pas le même'
                    if resultat == -2:
                        self.feedback += ', les noms des fonctions ne sont pas le même'
                return
            elif Regle.valider_orientation(self.equations, index-1):
                self.feedback = 'Par orientation'
                self.equations = Regle.orienter(self.equations, index-1)
                return
            elif Regle.valider_elimination(self.equations, index-1):
                resultat = Regle.eliminer(self.equations, index-1)
                if type(resultat) is list:
                    self.feedback = 'Par élimination de {}'.format(
                        equation.gauche
                    )
                    self.equations = resultat
                else:
                    self.erreur = True
                    self.feedback = 'L’équation {} engendre un échec d\'élimination'.format(
                        equation
                    )
                    if resultat == -1:
                        self.feedback += ', {} ne doit pas être dans la partie droite'.format(
                            equation.gauche
                        )
                return
