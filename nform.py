import itertools as it
from functools import partial
from aba import (MorphForm,
                 wellFormedArgs,
                 DepSubroutine,
                 MaxSubroutine,
                 DepOrMax,
                 ListOfForms)


class NForm(MorphForm):

    string_to_val_dict = {'zero': frozenset(),
                          'sg': frozenset({'sg'}),
                          'pl': frozenset({'sg', 'pl'}),
                          'nom': frozenset({'nom'}),
                          'acc': frozenset({'nom', 'acc'}),
                          'dat': frozenset({'nom', 'acc', 'dat'}),
                          'neu': frozenset({'neu'}),
                          'mas': frozenset({'neu', 'mas'}),
                          'fem': frozenset({'neu', 'mas', 'fem'})}

    all_values = ['zero', 'sg', 'pl', 'nom', 'acc',
                  'dat', 'neu', 'mas', 'fem']

    val_to_string_dict = {frozenset(): '∅',
                          frozenset({'sg'}): 'sg',
                          frozenset({'sg', 'pl'}): 'pl',
                          frozenset({'nom'}): 'nom',
                          frozenset({'nom', 'acc'}): 'acc',
                          frozenset({'nom', 'acc', 'dat'}): 'dat',
                          frozenset({'neu', 'mas', 'fem'}): 'fem',
                          frozenset({'neu', 'mas'}): 'mas',
                          frozenset({'neu'}): 'neu'}

    special_imm_contains_dict = {}

    feature_val_dict = {'Number': {'zero', 'sg', 'pl'},
                        'Case': {'zero', 'nom', 'acc', 'dat'},
                        'Gender': {'zero', 'neu', 'mas', 'fem'}}

    features = [f for f in feature_val_dict.keys()]
    grouped_values = [val_set for val_set in feature_val_dict.values()]

    def __init__(self, *argv):
        vals = getattr(NForm, 'all_values')
        feat_val_dic = getattr(NForm, 'feature_val_dict')
        str_val_dic = getattr(NForm, 'string_to_val_dict')
        if len(argv) > 3:
            raise Exception(f'{len(argv)} args passed to NForm,\
            which accepts at most 3')
        elif not all(v in vals for v in argv):
            raise Exception('Invalid value(s) passed to NForm')
        elif not wellFormedArgs(getattr(NForm, 'grouped_values'), argv):
            raise Exception('More than one value for a feature\
            passed to NForm')
        else:
            numb = [v for v in argv
                    if v in feat_val_dic.get('Number')
                    and not v == 'zero']
            case = [v for v in argv
                    if v in feat_val_dic.get('Case')
                    and not v == 'zero']
            gend = [v for v in argv
                    if v in feat_val_dic.get('Gender')
                    and not v == 'zero']
            if len(numb) > 0:
                self.number = str_val_dic.get(numb[0])
            else:
                self.number = frozenset()
            if len(case) > 0:
                self.case = str_val_dic.get(case[0])
            else:
                self.case = frozenset()
            if len(gend) > 0:
                self.gender = str_val_dic.get(gend[0])
            else:
                self.gender = frozenset()

    def __repr__(self):
        val_str_dic = getattr(NForm, 'val_to_string_dict')
        n = val_str_dic.get(self.number)
        c = val_str_dic.get(self.case)
        g = val_str_dic.get(self.gender)
        return f"{n}.{c}.{g}"

    def __getitem__(self, key):
        if key == 'Case':
            return self.getCase()
        elif key == 'Number':
            return self.getNumber()
        elif key == 'Gender':
            return self.getGender()
        else:
            return None

    def __hash__(self):
        return hash((self.number, self.case, self.gender))

    def valuesList(self):
        return [self.number, self.case, self.gender]

    def getNumber(self):
        return self.number

    def getCase(self):
        return self.case

    def getGender(self):
        return self.gender

    def specialImmediateContainsValue(self, value):
        dic = getattr(NForm, 'special_imm_contains_dict')
        if len(dic) == 0:
            return []
        elif value in dic:
            return dic[value]
        else:
            return []


# -------- Constraints

def MaxNum(ur: MorphForm, sr: ListOfForms) -> ListOfForms:
    fun = partial(DepOrMax, MaxSubroutine, ['Number'])
    return fun(ur, sr)


def MaxCase(ur: MorphForm, sr: ListOfForms) -> ListOfForms:
    fun = partial(DepOrMax, MaxSubroutine, ['Case'])
    return fun(ur, sr)


def DepNum(ur: MorphForm, sr: ListOfForms) -> ListOfForms:
    fun = partial(DepOrMax, DepSubroutine, ['Number'])
    return fun(ur, sr)


def DepCase(ur: MorphForm, sr: ListOfForms) -> ListOfForms:
    fun = partial(DepOrMax, DepSubroutine, ['Case'])
    return fun(ur, sr)


def MaxGender(ur: MorphForm, sr: ListOfForms) -> ListOfForms:
    fun = partial(DepOrMax, MaxSubroutine, ['Gender'])
    return fun(ur, sr)


def DepGender(ur: MorphForm, sr: ListOfForms) -> ListOfForms:
    fun = partial(DepOrMax, DepSubroutine, ['Gender'])
    return fun(ur, sr)

# num + case


def MaxNumCase(ur: MorphForm, sr: ListOfForms) -> ListOfForms:
    fun = partial(DepOrMax, MaxSubroutine, ['Number', 'Case'])
    return fun(ur, sr)


def DepNumCase(ur: MorphForm, sr: ListOfForms) -> ListOfForms:
    fun = partial(DepOrMax, DepSubroutine, ['Number', 'Case'])
    return fun(ur, sr)

# num + gender


def MaxNumGender(ur: MorphForm, sr: ListOfForms) -> ListOfForms:
    fun = partial(DepOrMax, MaxSubroutine, ['Number', 'Gender'])
    return fun(ur, sr)


def DepNumGender(ur: MorphForm, sr: ListOfForms) -> ListOfForms:
    fun = partial(DepOrMax, DepSubroutine, ['Number', 'Gender'])
    return fun(ur, sr)

# case + gender


def MaxCaseGender(ur: MorphForm, sr: ListOfForms) -> ListOfForms:
    fun = partial(DepOrMax, MaxSubroutine, ['Case', 'Gender'])
    return fun(ur, sr)


def DepCaseGender(ur: MorphForm, sr: ListOfForms) -> ListOfForms:
    fun = partial(DepOrMax, DepSubroutine, ['Case', 'Gender'])
    return fun(ur, sr)

# all three


def MaxNumCaseGender(ur: MorphForm, sr: ListOfForms) -> ListOfForms:
    fun = partial(DepOrMax, MaxSubroutine, ['Number', 'Case', 'Gender'])
    return fun(ur, sr)


def DepNumCaseGender(ur: MorphForm, sr: ListOfForms) -> ListOfForms:
    fun = partial(DepOrMax, DepSubroutine, ['Number', 'Gender', 'Case'])
    return fun(ur, sr)


nform_constraints = [MaxCase,
                     DepCase,
                     DepNum,
                     MaxNum,
                     DepGender,
                     MaxGender]

all_nform_rankings = list(it.permutations(nform_constraints))
