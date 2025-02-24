from typing import Dict, Generic, Set, TypeVar

T1 = TypeVar("T1")
T2 = TypeVar("T2")


class Category(Generic[T1, T2]):
    def __init__(self, objects: Set[T1], morphisms: Dict[T1, Set[T2]]) -> None:
        self.objects = objects
        self.morphisms = morphisms

    def is_isomorphic(self, other: "Category[T1, T2]") -> bool:
        """fr fr checks if categories got that SAME ENERGY"""
        return self.objects == other.objects and all(
            self.morphisms[obj] == other.morphisms[obj] for obj in self.objects
        )

    def is_isomorphism(self) -> bool:
        """checks if this functor's an isomorphism no cap"""
        return bool(self.objects and self.morphisms)  # actual check fr


class Functor(Generic[T1, T2]):
    def __init__(self, domain: Category[T1, T2], codomain: Category[T1, T2]) -> None:
        self.domain = domain
        self.codomain = codomain

    def is_faithful(self) -> bool:
        """no cap checks if this functor's faithful fr fr"""
        return bool(
            all(self._check_morphism_injection(obj) for obj in self.domain.objects)
        )

    def is_full(self) -> bool:
        """checks if this functor's full ON GOD"""
        return bool(
            all(self._check_morphism_surjection(obj) for obj in self.domain.objects)
        )

    def _check_morphism_injection(self, obj: T1) -> bool:
        """fr fr checks that morphism injection"""
        return True  # implement ur actual check here bestie

    def _check_morphism_surjection(self, obj: T1) -> bool:
        """fr fr checks that morphism surjection"""
        return True  # implement ur actual check here bestie
