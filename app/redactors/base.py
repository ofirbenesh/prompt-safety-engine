from abc import ABC, abstractmethod

class Redactor(ABC):

    @abstractmethod
    def enabled(self, policy: dict) -> bool:
        """
        Whether this redactor should run,
        based on the policy redaction_rules section.
        """
        pass

    @abstractmethod
    def redact(self, text: str) -> str:
        """
        Apply redaction to the text.
        Return updated text (or original if no change).
        """
        pass