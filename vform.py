import itertools as it
from functools import partial
from aba import (MorphForm,
                 wellFormedArgs,
                 DepSubroutine,
                 MaxSubroutine,
                 DepOrMax,
                 ListOfForms)


class VForm(MorphForm):

    string_to_val_dict = {'zero': frozenset(),
                          'part': frozenset({'part'}),
                          'auth': frozenset({'part', 'auth'}),
                          'addr': frozenset({'part', 'addr'}),
                          'pl': frozenset({'pl'})}

    all_values = ['zero', 'pl', 'part', 'auth', 'addr']

    val_to_string_dict = {frozenset(): '∅',
                          frozenset({'pl'}): 'pl',
                          frozenset({'part'}): 'part',
                          frozenset({'part', 'auth'}): 'auth',
                          frozenset({'part', 'addr'}): 'addr'}

    feature_val_dict = {'Person': {'zero', 'part', 'auth', 'addr'},
                        'Number': {'zero', 'pl'}}

    features = [f for f in feature_val_dict.keys()]
    grouped_values = [val_set for val_set in feature_val_dict.values()]

    special_imm_contains_dict = {frozenset({'part', 'auth'}): [frozenset()],
                                 frozenset({'part', 'addr'}):  [frozenset()]}

    def __init__(self, *argv):
        vals = getattr(VForm, 'all_values')
        feat_val_dic = getattr(VForm, 'feature_val_dict')
        str_val_dic = getattr(VForm, 'string_to_val_dict')
        if len(argv) > 2:
            raise Exception(f'{len(argv)} args passed to VForm,\
            which accepts at most 2')
        elif not all(v in vals for v in argv):
            raise Exception('Invalid value(s) passed to VForm')
        elif not wellFormedArgs(argv):
            raise Exception('More than one value for a feature\
            passed to VForm')
        else:
            numb = [v for v in argv
                    if v in feat_val_dic.get('Number')
                    and not v == 'zero']
            pers = [v for v in argv
                    if v in feat_val_dic.get('Person')
                    and not v == 'zero']
            if len(numb) > 0:
                self.number = str_val_dic.get(numb[0])
            else:
                self.number = frozenset()
            if len(pers) > 0:
                self.person = str_val_dic.get(pers[0])
            else:
                self.person = frozenset()

    def __repr__(self):
        val_str_dic = getattr(VForm, 'val_to_string_dict')
        n = val_str_dic.get(self.number)
        p = val_str_dic.get(self.person)
        return f"{n}.{p}"

    def __getitem__(self, key):
        if key == 'Number':
            return self.getNumber()
        elif key == 'Person':
            return self.getPerson()
        else:
            return None

    def __hash__(self):
        return hash((self.number, self.person))

    def valuesList(self):
        return [self.number, self.person]

    def getNumber(self):
        return self.number

    def getPerson(self):
        return self.person

    def specialImmediateContainsValue(self, value):
        dic = getattr(VForm, 'special_imm_contains_dict')
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


def DepNum(ur: MorphForm, sr: ListOfForms) -> ListOfForms:
    fun = partial(DepOrMax, DepSubroutine, ['Number'])
    return fun(ur, sr)


def MaxPers(ur: MorphForm, sr: ListOfForms) -> ListOfForms:
    fun = partial(DepOrMax, MaxSubroutine, ['Person'])
    return fun(ur, sr)


def DepPers(ur: MorphForm, sr: ListOfForms) -> ListOfForms:
    fun = partial(DepOrMax, DepSubroutine, ['Person'])
    return fun(ur, sr)


vform_constraints = [MaxPers,
                     DepPers,
                     DepNum,
                     MaxNum]

vform_rankings = list(it.permutations(vform_constraints))
