"""An OT grammar for morphological exponence in inflectional paradigms.

This module provides the tools to define classes that represent
morphological objects (that is, bundles of feature-value pairs), as
instances of the superclass MorphForm.  MorphForm defines the crucial
notion of containment between forms that underlies the theory.

This module also provides a form of OT Eval and Con, that takes
objects that instantiate a subclass of MorphForm as candidates.  Con
consists exclusively of Max and Dep constraints.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or (at
your option) any later version.  This program is distributed in the
hope that it will be useful, but WITHOUT ANY WARRANTY; without even
the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR
PURPOSE. See the GNU General Public License for more details.  You
should have received a copy of the GNU General Public License along
with this program. If not, see <http://www.gnu.org/licenses/>.

"""

__authors__ = ["Stanislao Zompì", "Enrico Flor"]
__contact__ = "zompi@mit.edu"
__copyright__ = "Copyright 2023, Stanislao Zompì"
__date__ = "2023/08/01"
__deprecated__ = False
__email__ = "zompi@mit.edu"
__license__ = "GPLv3"
__maintainer__ = "Stanislao Zompì"
__status__ = "Production"
__version__ = "0.0.1"

import textwrap
from collections import defaultdict
import itertools as it
import more_itertools as mit
from abc import abstractmethod
from typing import TypeAlias, Callable



# -------- Define MorphForm

ListOfValues: TypeAlias = list[set[str]]


def wellFormedArgs(group_vals: ListOfValues, *argv: str) -> bool:
    if len(argv) == 1:
        return True
    for a in argv:
        for b in argv:
            for val_list in group_vals:
                if not a == 'zero' and not b == 'zero' \
                   and not a == b and a in val_list \
                   and b in val_list:
                    return False
    return True


class MorphForm:

    def __init__(self, *values):
        return self

    @abstractmethod
    def valuesList(self):
        raise NotImplementedError

    def getValues(self):
        return self.valuesList()

    # re: type hint as str see https://stackoverflow.com/a/41135046/15080452
    def contains(self, other: 'MorphForm') -> bool:
        '''Return True iff SELF contains OTHER.

        Both SELF and OTHER are MorphForms.  This function returns
        True iff SELF and OTHER are instances of the same class c and
        for every feature f defined of the class c, the the value SELF
        assigns to f is an (improper superset) of the value OTHER
        assigns to f.

        This function returns False if SELF and OTHER are identical
        (containment is thus defined as an irreflexive relation).

        '''
        if self == other:
            return False
        elif not type(self) == type(self):
            raise Exception('Containment is only defined\
            between objects of the same class.')
        for t in list(zip(self.getValues(), other.getValues())):
            if not t[0].issuperset(t[1]):
                return False
        return True

    def __eq__(self, other):
        if type(self) == type(other):
            return self.getValues() == other.getValues()

    def __str__(self):
        return self.__repr__()

    def __lt__(self, other):
        return other.contains(self)

    def isUnderspecified(self):
        '''Return True iff any feature of SELF has the empty set as a
        value.
        '''
        vals = self.allValues()
        # remember: underspecified value is the empty set!
        return any(map(lambda v: len(v) == 0, vals))

    def containment(self, other: 'MorphForm') -> bool:
        '''Return True iff SELF and OTHER are in a containment
        relation.'''
        return self.contains(other) or other.contains(self)

    def getSpecialImmediateContainsValue(self, value):
        return self.specialImmediateContainsValue(value)

    @abstractmethod
    def specialImmediateContainsValue(self, value):
        raise NotImplementedError

    def nonImmediateContains(self, other: 'MorphForm') -> bool:
        '''Return True if SELF contains OTHER but not immediately.

        "Not immediately" means that there exists MorphForms that
        contain OTHER and are contained by SELF, and are distinct from
        either.

        This function will look up the value of
        special_imm_contains_dict for the class the SELF and OTHER
        instantiate so that special cases of immediate containment
        that override the set theoretic definition (immediate
        containment being, in set theoretic terms, difference being a
        singleton set) are taken into consideration.

        '''
        if not self.contains(other):
            return False
        diffs = 0
        for t in list(zip(self.getValues(), other.getValues())):
            # if this value of other is contained in the special
            # dictionary as one possible value for the key that is the
            # value of self, then just increment diff of one *as if
            # the set difference between t[0] and t[1] was 1*.
            if t[1] in self.getSpecialImmediateContainsValue(t[0]):
                diffs += 1
            else:
                diffs += len(t[0].difference(t[1]))
        return diffs > 1

    def nonImmediateContainment(self, other: 'MorphForm') -> bool:
        return self.nonImmediateContains(other) or\
            other.nonImmediateContains(self)

    def immediateContains(self, other: 'MorphForm') -> bool:
        return self.contains(other) and\
            not self.nonImmediateContains(other)

    def immediateContainment(self, other: 'MorphForm') -> bool:
        return self.immediateContains(other) or\
            other.immediateContains(self)

    def isBetween(self, form1: 'MorphForm',
                  form2: 'MorphForm') -> bool:
        return (self.contains(form1) and form2.contains(self)) or \
            (self.contains(form2) and form1.contains(self))


ListOfForms: TypeAlias = list[MorphForm]
Partition: TypeAlias = list[list[MorphForm]]


def getBottom(forms: ListOfForms) -> ListOfForms:
    inds = [f for f, x in enumerate(forms) if x == min(forms)]
    return [forms[i] for i in inds]


def getTop(forms: ListOfForms) -> ListOfForms:
    inds = [f for f, x in enumerate(forms) if x == max(forms)]
    return [forms[i] for i in inds]


def partitionIsWellFormed(partition: Partition,
                          number_of_forms: int,
                          type_form: type) -> bool:
    flat = [form for cell in partition for form in cell]
    total_forms = len(flat)
    if total_forms > number_of_forms:
        print(f"Found {total_forms} forms: too many!")
        return False
    elif total_forms < number_of_forms:
        print(f"Found {total_forms} forms: too few!")
        return False
    for f in flat:
        if not isinstance(f, type_form):
            print(f"Not all members are valid objects of {type_form} class")
            return False
    if total_forms > len(set(flat)):
        print(f"Duplicate {type_form}s found!")
        return False
    for c in partition:
        if len(c) > len(set(c)):
            print(f"Cell with duplicate {type_form}s found!")
            return False
    return True



# -------- Properties of Partitions

def getPaths(form1: MorphForm,
             form2: MorphForm,
             list_of_forms: ListOfForms) -> list[ListOfForms]:
    '''Return all paths that connect two forms.

    FORM1 and FORM2 are MorphForms and are the two ends of the path.
    LIST_OF_FORMS is a list of MorphForms.  Return a list that
    contains all paths connecting FORM1 and FORM2 made out of forms in
    LIST_OF_FORMS, if any.

    '''
    if not form1.containment(form2):
        return []
    domain = list(set([f for f in list_of_forms
                       if f.isBetween(form1, form2)]
                      + [form1, form2]))
    bottom = getBottom([form1, form2])[0]
    top = getTop([form1, form2])[0]
    if form1.immediateContainment(form2):
        return [bottom, top]

    def getExtensions(path: ListOfForms,
                      top: MorphForm,
                      forms: ListOfForms) -> ListOfForms:
        out = []
        last = path[-1]
        exts = [f for f in forms
                if f.immediateContains(last) and top.contains(f)]
        for e in exts:
            out.append(path + [e])
        return out

    paths_traversed = [[bottom]]
    while True:
        extended = []
        for p in paths_traversed:
            if top.contains(p[-1]):  # you're done if you already reached top
                exts = getExtensions(p, top, domain)
                for e in exts:
                    extended.append(e)
        if extended == paths_traversed or len(extended) == 0:
            # you did no progress: get out
            break
        else:
            paths_traversed = extended
    if paths_traversed == [[bottom]]:
        return []
    else:
        return [p[1:] for p in paths_traversed]


def isBadCell(cell: ListOfForms) -> bool:
    '''Return True if CELL is a bad cell.

    CELL is a list of MorphForms.  It is bad if it contains two forms
    x and y that are in a containment relation but are not connected
    by a path of forms in CELL.
    '''
    containment_pairs = []
    for f in cell:
        for g in cell:
            if g.nonImmediateContains(f):
                containment_pairs.append((f, g))
    for p in containment_pairs:
        paths = getPaths(p[0], p[1], cell)
        if len(paths) == 0:
            return True
    return False


def isAba(partition: Partition) -> bool:
    '''Return True if PARTITION contains a bad cell.

    PARTITION is a list of lists of MorphForms.  A cell is bad if it
    verifies the predicate isBadCell.
    '''
    is_aba = False
    for cell in partition:
        if len(cell) > 1:
            is_aba = isBadCell(cell)
            break
    return is_aba


# -------- Constraints


FeatureValue: TypeAlias = set[str]


def DepSubroutine(ur_value: FeatureValue,
                  sr_value: FeatureValue) -> int:
    '''Return Dep of two values.

    The return is the cardinality of the difference between the union
    of UR_VALUE and SR_VALUE and UR_VALUE.

    '''
    return len(ur_value.union(sr_value).difference(ur_value))


def MaxSubroutine(ur_value: FeatureValue,
                  sr_value: FeatureValue) -> int:
    '''Return Max of two values.

    The return is the cardinality of the difference between the union
    of UR_VALUE and SR_VALUE and SR_VALUE.

    '''
    return len(ur_value.union(sr_value).difference(sr_value))


def DepOrMax(constr: Callable[FeatureValue, FeatureValue],
             features: list[str],
             ur: MorphForm,
             candidates: ListOfForms) -> ListOfForms:
    best_so_far = None
    winners = []
    for form in candidates:
        form_score = []
        for i in features:
            ur_val = ur[i]
            sr_val = form[i]
            form_score.append(constr(ur_val, sr_val))
        total_score = sum(form_score)
        if best_so_far is None:
            winners.append(form)
            best_so_far = total_score
        elif total_score > best_so_far:
            # this form loses
            pass
        elif total_score == best_so_far:
            # we tie with the current best, add this to the winners
            winners.append(form)
        else:
            # we found one that is better than all so far, get rid of
            # old winners
            winners = [form]
            best_so_far = total_score
    return winners


def printRanking(ranking):
    return tuple(map(lambda f: f.__name__, ranking))


# -------- Eval


def otEval(rank: list[callable],
           ur_form: MorphForm,
           candidates: ListOfForms) -> ListOfForms:
    '''Return list of winning candidates given constraint ranking RANK
    and input form UR_FORM (a MorphForm).  RANK is a list of
    constraints sorted by decreasing priority.  CANDIDATES is a list
    of MorphForms from which the winners are selected.
    '''
    for constraint in rank:
        if len(candidates) > 1:
            candidates = constraint(ur_form, candidates)
        else:
            break
    return candidates


def areSamePartitions(part1: Partition,
                      part2: Partition) -> bool:
    '''Return True iff PART1 and PART2, which are lists of lists of
    MorphForms, represent the same partition.
    '''
    s1 = set(map(frozenset, part1))
    s2 = set(map(frozenset, part2))
    return len(s1.difference(s2)) == len(s2.difference(s1)) == 0


def getWinnerPartition(rank,
                       ur_forms: ListOfForms,
                       sr_forms: ListOfForms) -> Partition:
    '''Given a list of constraints RANK, and two lists of MorphForms
    UR_FORMS and SR_FORMS, return the winner partition (a list of
    lists of MorphForms).

    Deriving the winner partition involves finding the winner(s)
    otEval assigns to each form in UR_FORMS, given RANK and choosing
    from SR_FORMS.  Given the list of results so obtained, the list is
    partitioned under equivalence (not just between MorphForms, but
    between lists thereof if need be).  Such partition is the return
    value of this function.
    '''
    winners = dict()
    for ur in ur_forms:
        winners[ur] = otEval(rank, ur, sr_forms)
    temp_dict = {k: str(v) for k, v in winners.items()}
    res = defaultdict(list)
    for key, val in sorted(temp_dict.items()):
        res[val].append(key)
    return list(res.values())


def generateForms(type_of_form, *values):
    dic = getattr(type_of_form, 'feature_val_dict')
    all_args = [f for f in it.product(*list(dic.values()))]
    if len(values) > 0 and isinstance(values[0], list):
        values = values[0]
    if len(values) == 0:
        args = all_args
    else:
        args = []
        for a in all_args:
            if len(set(a).intersection(set(values))) == 0:
                args.append(a)
    return [type_of_form(*f) for f in args]


def findVocabularyRankingPairs(type_of_form,
                               ur_partition,
                               rankings,
                               list_values_to_exclude=[],
                               stop=True,
                               output_file=None,
                               header=""):
    '''Given a UR_PARTITION (a list of lists of MorhForm of type
    TYPE_OF_FORM), and a list of rankings (each ranking is a tuple of
    constraints), find all the pairs of vocabulary (a list that
    contains as many MorphForms as UR_PARTITION cells) and rankings
    such that the generated output partitions the space of all
    possible TYPE_OF_FORMS in the same way UR_PARTITION does.

    Optionally, pass a list of feature values as strings (congruent
    with the definition of the class TYPE_OF_FORM) to be ignored in
    the generation of candidates, as the value of
    LIST_VALUES_TO_EXCLUDE.

    By default, as soon as one "good" ranking is found for a
    vocabulary, this function moves to another vocabulary.  To change
    this default pass False as the value of STOP.

    The return value of this function is a list of tuples of
    vocabulary and ranking.  This function optionally pretty prints
    this return value on a file whose name you can pass as a string as
    the value of OUTPUT_FILE, whose (optional) header is the string
    passed as the value of HEADER.
    '''
    sforms = generateForms(type_of_form, list_values_to_exclude)
    urs = [form for cell in ur_partition for form in cell]
    vocab_list = list(it.combinations(sforms, len(ur_partition)))
    success_pairs = []
    vocab_number = len(vocab_list)
    vocab_counter = 1
    success_counter = 0
    for vocab in vocab_list:
        print(f"Testing {vocab_counter}/{vocab_number} vocabularies,\
        {success_counter} good ones found...", end='\r')
        good_ranks = []
        for rank in rankings:
            wpart = getWinnerPartition(rank, urs, vocab)
            if areSamePartitions(wpart, ur_partition):
                good_ranks.append(printRanking(rank))
                if stop:
                    break
        vocab_counter += 1
        if len(good_ranks) > 0:
            success_pairs.append((vocab, good_ranks))
            success_counter += 1
    print('\n')
    if len(success_pairs) == 0:
        print("No luck...")
    else:
        print(f"Found {len(success_pairs)} successes!")
    # --- SIDE EFFECT ---
    if output_file is not None:
        with open(output_file, 'w') as f:
            f.write(header)
            f.write(f'{vocab_number} vocabularies tested')
            if stop:
                f.write(' (only one winning ranking per vocabulary reported)')
            f.write('\n')
            if len(list_values_to_exclude) > 0:
                f.write(f'Feature values excluded: {list_values_to_exclude}\n')
            f.write('Partition:\n')
            for c in ur_partition:
                f.write(textwrap.fill(str(c), 70))
                f.write('\n ---\n')
            f.write('\n\n')
            f.write(f'{len(success_pairs)} winning vocabularies found:\n')
            for i in success_pairs:
                f.write('==========\n')
                f.write(str(i[0]))
                f.write('\n-----\n')
                for r in i[1]:
                    f.write(str(r))
                    f.write('\n')
    # -------------------
    return success_pairs
