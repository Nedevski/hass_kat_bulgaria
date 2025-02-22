"""KAT Bulgaria Client Wrapper."""

from kat_bulgaria.obligations import KatApi


class KatClient(KatApi):
    """KAT Client Manager."""

    person_name: str
    person_egn: str
    person_license_number: str

    def __init__(self, name: str, egn: str, license_number: str) -> None:
        """Initialize client."""
        super().__init__()

        self.person_name = name
        self.person_egn = egn
        self.person_license_number = license_number

    async def validate_credentials(self):
        """Validate EGN/License Number."""
        return await super().validate_credentials(
            self.person_egn, self.person_license_number
        )

    async def get_obligations(self):
        """Get obligations."""
        return await super().get_obligations(
            self.person_egn, self.person_license_number
        )
