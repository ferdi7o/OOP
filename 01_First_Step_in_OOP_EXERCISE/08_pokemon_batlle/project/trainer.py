from typing import List
from project.pokemon import Pokemon


class Trainer:
    def __init__(self, name: str):
        self.name = name
        self.pokemons: List[Pokemon] = [] # podskazka! che izpolzva list ot pokemon class

    def add_pokemon(self, pokemon: Pokemon) -> str:
        if pokemon in self.pokemons:
            return "This pokemon is already caught"
        self.pokemons.append(pokemon)
        return f"Caught {pokemon.pokemon_details()}" # izvikme ot pokemon pokemon_details motda

    def release_pokemon(self, pokemon_name: str) -> str:
        # for pok in self.pokemons:
        #     if pok.name == pokemon_name:
        #         self.pokemons.remove(pok)
        #         return f"You have released {pokemon_name}"
        pokemon_to_release = next((p for p in self.pokemons if p.name == pokemon_name), None)
        if pokemon_to_release:
            self.pokemons.remove(pokemon_to_release)
            return f"You have released {pokemon_name}" # dopulnitelna informacia ama trudna za sega :D
        return "Pokemon is not caught"

    def trainer_data(self) -> str:
        result = [f"Pokemon Trainer {self.name}",
                  f"Pokemon count {len(self.pokemons)}"]
        for p in self.pokemons:
            result.append(f"- {p.pokemon_details()}") # metod za detaylite izvikame

        return "\n".join(result)

#TestCode