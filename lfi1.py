import re


class Clause:
    def __init__(self, formule='', lits=set(), op=''):
        self.op = op if op else Clause.__op(formule)
        assert self.op in ['+', None]
        if len(formule):
            formule = Clause.__treat(formule)
            self.lits = set(formule.split(self.op)) if len(formule) else set()
        else:
            self.lits = set(lits)

    def __op(formule: str):
        match = re.search(r'\*|\+', formule)
        return match.group() if match else None

    def __treat(formule: str):
        return re.sub(r'[ ]+|\(|\)', '', formule)

    def __str__(self):
        clause = ' {} '.format(self.op).join(
            self.lits) if self.op else self.lits
        clause = clause.replace('-', '¬')
        clause = clause.replace('+', '∨')
        return clause


class LFI1:
    def resolve(clause1: Clause, clause2: Clause):
        assert all([
            clause.op in ['+', None] for clause in [clause1, clause2]
        ])
        clause_resolu = Clause(op='+')
        lits = clause1.lits.union(clause2.lits)
        for lit in lits:
            opposite_lit = lit[1:] if lit[0] == '-' else '-{}'.format(lit)
            if opposite_lit not in lits:
                clause_resolu.lits.add(lit)
        return clause_resolu

    def resolve_all(clauses1: list, clauses2: list):
        clauses_resolu = list()
        for clause1 in clauses1:
            for clause2 in clauses2:
                resolvant = LFI1.resolve(clause1, clause2)
                if len(resolvant.lits):
                    clauses_resolu.append(resolvant)

        # remove repeated clauses
        lits = set(map(lambda clause: tuple(clause.lits), clauses_resolu))
        clauses_resolu = list(map(
            lambda lit: Clause(lits=set(lit), op='+'), lits
        ))

        return clauses_resolu

    def clauses_str(clauses: list):
        return ', '.join(
            set(map(lambda clause: str(clause), clauses))
        ) if len(clauses) > 1 else clauses[0] if len(clauses) else '∅'

    def minimise(clauses: list):
        # remove repeated clauses
        lits = set(map(lambda clause: tuple(clause.lits), clauses))
        clauses = list(map(
            lambda lit: Clause(lits=set(lit), op='+'), lits
        ))
        # remove supersets
        mini_clauses = list(filter(lambda clause: [
            clause.lits.issuperset(clause_copy.lits) for clause_copy in clauses
        ].count(True) == 1, clauses))

        return mini_clauses

    def to_clauses(input_clauses: str):
        return list(map(lambda clause: Clause(clause), input_clauses.split(',')))

    def c_strategy(delta: list, theta=list(), k=0, force_stop=False):
        union_delta_theta = delta + theta
        resolvants = LFI1.resolve_all(delta, union_delta_theta)

        if k == 0:
            print('{:<2} {:<35} {:<30} {:<35} {:<42}'.format(
                'k', '∆_k', 'Θ_k', '∆_k ∪ Θ_k', 'Resolvants'
            ))

        print('{:<2} {:<35} {:<30} {:<35} {:<42}'.format(
            k,
            LFI1.clauses_str(delta),
            LFI1.clauses_str(theta),
            LFI1.clauses_str(union_delta_theta),
            LFI1.clauses_str(resolvants)
        ))

        if len(delta) == 0 or force_stop:
            print()
            if force_stop:
                print(
                    'l\'Algorithme a été arrêté forcément, car il n\'y a pas un progrès en ∆_k, k= {}.'.format(
                        k
                    )
                )
            else:
                print('l\'Algorithme a fini avec succès, k= {}.'.format(k))
            return

        # exclude union_delta_theta from resolvants
        ex_lits = list(map(lambda clause: clause.lits, union_delta_theta))
        delta_k_plus_1 = list(filter(
            lambda clause: not any([
                ex_lit.issubset(clause.lits) for ex_lit in ex_lits
            ]), resolvants
        ))

        # exclude delta_k_plus_1 from union_delta_theta
        ex_lits = list(map(lambda clause: clause.lits, delta_k_plus_1))
        theta_k_plus_1 = list(filter(
            lambda clause: not any([
                ex_lit.issubset(clause.lits) for ex_lit in ex_lits
            ]), union_delta_theta
        ))

        LFI1.c_strategy(
            delta_k_plus_1,
            theta_k_plus_1,
            k+1,
            force_stop=delta_k_plus_1 == delta
        )

        pass
