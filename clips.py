"""Integration for CLIPS-style propositional logic."""



##### Classes #####



class CLIPS:
    """General class for all self-contained CLIPS instances."""

    def __init__(self):
        self.facts = []
        self.rules = []


    def RULE(self):
        """Create a new logical relation."""


    def ASSERT(self):
        """Declare a new fact."""


    def RETRACT(self):
        """Retract an asserted fact."""


    def RESOLUTION(self):
        """Run resolution on the entire database to a depth of `n`. If not provided runs until no more relations found."""


    def IMPLIES(self):
        """Logical implication."""


    def NOT(self):
        """Logical negation."""


    def DECLARE(self):
        """Declare a Boolean variable."""


    def RESET(self):
        """Reset the current CLIPS instance."""
        self.facts = []
        self.rules = []
