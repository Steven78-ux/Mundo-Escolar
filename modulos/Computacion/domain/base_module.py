"""Contrato base para todos los módulos del sistema."""

from abc import ABC, abstractmethod


class BaseModule(ABC):
    """Define una interfaz mínima para módulos independientes."""

    @abstractmethod
    def run(self) -> None:
        """Inicia el ciclo principal del módulo."""
        raise NotImplementedError
