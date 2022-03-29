import itertools
import collections
from msilib.schema import Component


class Chemical:
    def __init__(self, name: str, amount: int):
        self.name = name
        self.amount = amount

    def has_enough(self, component: "Chemical") -> bool:
        return self == component and self.amount >= component.amount

    def copy(self, ratio: int = 1) -> "Chemical":
        return Chemical(self.name, self.amount * ratio)

    def __eq__(self, other: "Chemical") -> bool:
        return self.name == other.name

    def __ge__(self, other: "Chemical") -> bool:
        return self.has_enough(other)

    def __sub__(self, amount: int) -> "Chemical":
        self.amount -= amount
        return self

    def __mul__(self, amount: int) -> "Chemical":
        self.amount *= amount
        return self

    def __str__(self) -> str:
        return f"{self.name}={self.amount}"

    def __repr__(self) -> str:
        return self.__str__()


class ChemicalGroup:
    def __init__(self, **kwargs):
        self.chemicals = collections.OrderedDict()
        for name, amount in kwargs.items():
            self.chemicals[name] = Chemical(name, amount)

    def from_list(chemicals: list) -> "ChemicalGroup":
        group = ChemicalGroup()
        for chemical in chemicals:
            group.chemicals[chemical.name] = chemical.copy(1)
        return group

    def has(self, chemical: Chemical) -> bool:
        return chemical.name in self.chemicals

    def __iter__(self) -> str:
        for name in self.chemicals:
            yield name

    def __getitem__(self, name: str) -> Chemical:
        return self.chemicals[name]

    def values(self) -> Chemical:
        for chemical in self.chemicals.values():
            yield chemical

    def items(self) -> tuple:
        for name, chemical in self.chemicals.items():
            yield (name, chemical)

    def __add__(self, chemical: Chemical) -> "ChemicalGroup":
        if self.has(chemical):
            self.chemicals[chemical.name] += chemical
        else:
            self.chemicals[chemical.name] = chemical
        return self

    def __sub__(self, chemical: Chemical) -> "ChemicalGroup":
        self.chemicals[chemical.name] -= chemical.amount
        if self.chemicals[chemical.name].amount == 0:
            self.chemicals.pop(chemical.name)
        elif self.chemicals[chemical.name].amount < 0:
            raise ValueError
        return self

    def __len__(self) -> int:
        return len(self.chemicals)

    def __str__(self):
        return "; ".join(repr(chemical) for chemical in self.chemicals.values())

    def __repr__(self) -> str:
        return self.__str__()


class ChemicalDefinition:
    def __init__(self, name: str, amount: int):
        self.name = name
        self.amount = amount  # Created with the minimal amount of the mixture
        self.base = False  # Comes from a ChemMaster ( Hydrogen )
        # Comes from exterior sources ( Welding Fuel )
        self.alternative = False
        self.components = None  # Comes from a mixture ( Ammonia )

    # Next multiple of the amount wanted
    def minimal(self, amount_wanted: int) -> int:
        if amount_wanted % self.amount != 0:
            return amount_wanted + self.amount - (amount_wanted % self.amount)
        else:
            return amount_wanted

    # Ratio of minimal for reaction
    def ratio(self, chemical_numerator: Chemical) -> int:
        for component in self.components.values():
            if chemical_numerator == component:
                return chemical_numerator.amount // component.amount

    def can_react(self, chemicals: dict, temperature=20):
        if self.base or self.alternative:
            return False

        valid_chems = 0
        for chemical, amount in chemicals.items():
            if chemical not in self.components:
                continue
            if amount < self.components[chemical]:
                continue
            valid_chems += 1

        return valid_chems == len(self.components)

    def __iter__(self) -> str:
        for name in self.components:
            yield name

    def __getitem__(self, name: str) -> Chemical:
        return self.components[name]

    def values(self) -> Chemical:
        for chemical in self.components.values():
            yield chemical

    def items(self) -> tuple:
        for name, chemical in self.components.items():
            yield (name, chemical)

    def __len__(self) -> int:
        return len(self.components)

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return self.__str__()


def add_base(name: str) -> ChemicalDefinition:
    chem = ChemicalDefinition(name, 1)
    chem.base = True
    return chem


def add_composite(name: str, amount: int, **kwargs) -> ChemicalDefinition:
    chem = ChemicalDefinition(name, amount)
    chem.components = ChemicalGroup(**kwargs)
    return chem


def add_alternative(name: str) -> ChemicalDefinition:
    chem = ChemicalDefinition(name, 1)
    chem.alternative = True
    return chem


CHEMICALS = {
    "carbon": add_base("carbon"),
    "hydrogen": add_base("hydrogen"),
    "oxygen": add_base("oxygen"),
    "nitrogen": add_base("nitrogen"),
    "weldingfuel": add_alternative("weldingfuel"),
    "ammonia": add_composite("ammonia", 3, hydrogen=3, nitrogen=1),
    "oil": add_composite("oil", 3, carbon=1, hydrogen=1, weldingfuel=1)
}

def get_reaction(reagents: ChemicalGroup) -> Chemical:
    def check_has_reagent(reagent: Chemical, components: ChemicalGroup):
        for _, component in components.items():
            if reagent >= component:
                return True
        return False

    for chemical in CHEMICALS.values():
        if chemical.base or chemical.alternative:
            continue

        if len(reagents) != len(chemical):
            continue

        chem_possible = True
        for _, reagent in reagents.items():
            if not check_has_reagent(reagent, chemical):
                chem_possible = False
                break

        if chem_possible:
            return chemical

    return None


class Container:
    def __init__(self, **kwargs):
        self.chemicals = ChemicalGroup(**kwargs)

    def simulate(self) -> bool:
        def check_reaction(chemicals: list, length: int) -> set:
            reactions = set()
            for reaction in itertools.combinations(chemicals, length):
                result = get_reaction(
                    ChemicalGroup.from_list(reaction))
                if result:
                    reactions.add(result)
            return reactions

        possible_reactions_set = set()
        for comb_length in range(1, 1 + len(self.chemicals)):
            possible_reactions_set.update(check_reaction(
                self.chemicals.values(), comb_length))

        if len(possible_reactions_set) == 0:
            return False

        possible_reactions_index = []
        for possible_reaction in possible_reactions_set:
            for index, chemical in reversed(list(enumerate(self.chemicals))):
                if chemical in possible_reaction:
                    possible_reactions_index.append((index, possible_reaction))
                    break

        first_reaction = sorted(possible_reactions_index)[0][1]

        ratio = None
        removal_list = []
        for chemical in self.chemicals.values():
            if chemical.name not in first_reaction:
                continue
            if ratio == None:
                ratio = first_reaction.ratio(chemical)
            else:
                ratio = min(ratio, first_reaction.ratio(chemical))
            removal_list.append(first_reaction[chemical.name].copy())
        
        for chemical in removal_list:
            chemical *= ratio

        for removed_chem in removal_list:
            self.chemicals -= removed_chem
           
        self.chemicals += Chemical(first_reaction.name, first_reaction.amount * ratio)
        print(self.chemicals)

        # new_chemicals = [
        #     chemical for chemical in self.chemicals if chemical.amount > 0]
        # new_chemicals.append(
        #     Component(first_reaction.name, first_reaction.amount * ratio))

        # print(new_chemicals)

        # for group in all_list:
        #     print(group, possible_reactions(group))

        # print(all_list)
        # for chemical in self.chemicals:
        #     possible_list += possible_reactions(chemical[0], chemical[1])

        # possible_list = set(
        #     [chemical for chemical in possible_list if possible_list.count(chemical) > 1])


a = Container(hydrogen=5+12, weldingfuel=5, carbon=5, nitrogen=4)
a.simulate()
a.simulate()
a.simulate()

# a = ["a", "b"]

# groups = []
# groups += itertools.combinations(a, 1)
# groups += itertools.combinations(a, 2)

# for comb_length in range(1, 1 + len(a)):
#     print(list(itertools.combinations(a, comb_length)))

# print(list(itertools.combinations(a, 1)))
# print(list(itertools.combinations(a, 2)))
# print(list(itertools.combinations(a, 3)))
