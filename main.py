from lfi1 import LFI1, Clause


def print_choices():
    print()
    print('----------------------------------------')
    print('Les choix possibles:')
    print('[0] sortir le programme')
    print('[1] imprimmer ce catalogue')
    print('[2] insérer des nouveaux clauses')
    print('[3] exécuter la stratégie complète')
    print('[4] minimiser les clauses inser')
    print('----------------------------------------')


print_choices()

clauses = []

while True:
    print()
    print('l\'ensemble Γ: {}'.format(LFI1.clauses_str(clauses)))
    cmd = int(input('> '))
    if cmd == 0:
        break
    if cmd == 1:
        print_choices()
    elif cmd == 2:
        input_clauses = input(
            'insérer la/les clause(s) que vous voulez ajouter: (séparèes avec la vergule ",")\n>>> '
        )
        clauses = clauses + LFI1.to_clauses(input_clauses)
    elif cmd == 3:
        print()
        print('---------- strategie complete - ---------')
        LFI1.c_strategy(clauses)
    elif cmd == 4:
        clauses = LFI1.minimise(clauses)
    else:
        print('choix pas valide')
