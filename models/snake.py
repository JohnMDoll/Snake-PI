class Snake():
    """defines snake dictionary objects"""
    def __init__(self, id, name, owner_id, species_id, gender, color, species_name = None):
        self.id = id
        self.name = name
        self.owner_id = owner_id
        self.species_id = species_id
        self.gender = gender
        self.color = color
        self.species_name = species_name
