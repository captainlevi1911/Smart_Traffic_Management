from dataclasses import dataclass, field


@dataclass
class ValidationResult:
    """
    Stores the outcome of dataset validation.
    """

    # Overall validation status.
    passed: bool = True

    # Stores validation errors.
    errors: list[str] = field(default_factory=list)

    # Stores validation warnings.
    warnings: list[str] = field(default_factory=list)

    def add_error(self, message: str) -> None:
        """
        Add an error to the validation report.
        """

        self.passed = False
        self.errors.append(message)

    def add_warning(self, message: str) -> None:
        """
        Add a warning to the validation report.
        """

        self.warnings.append(message)