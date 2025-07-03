import asyncio  #Importa la librería asíncrona
import aiohttp  #Librería asíncrona para hacer peticiones HTTP
import sys      #Para leer argumentos desde consola

API_LIST_URL = "https://pokeapi.co/api/v2/pokemon?limit=150"
SEPARATOR = "-" * 40

async def fetch_json(session: aiohttp.ClientSession, url: str):
    """Hace GET y devuelve el JSON."""
    async with session.get(url, timeout=10) as resp:
        resp.raise_for_status()
        return await resp.json()

async def fetch_pokemon_detail(session, meta):
    """Devuelve información de los Pokémon."""
    data = await fetch_json(session, meta["url"])
    return {
        "id": data["id"],
        "name": data["name"],
        "types": [t["type"]["name"] for t in data["types"]],
        "height": data["height"],
        "weight": data["weight"],
    }

async def main():
    #Leer tipo de Pokemón desde consola
    tipo_filtro = sys.argv[1].lower() if len(sys.argv) > 1 else None

    async with aiohttp.ClientSession() as session:
        #Lista de los Pokémon
        lista = await fetch_json(session, API_LIST_URL)
        metas = lista["results"]

        #Obtener información de los Pokémon
        detalles = await asyncio.gather(
            *(fetch_pokemon_detail(session, m) for m in metas)
        )

        #Si existe el tipo de filtro, filtrar los Pokémon
        if tipo_filtro:
            detalles = [p for p in detalles if tipo_filtro in p["types"]]

        #Mostrar mensaje si no hay resultados
        if not detalles:
            print(f"No se encontraron Pokémon del tipo '{tipo_filtro}'.")
            return

        #Imprimir información de los Pokémon
        for p in detalles:
            print(SEPARATOR)
            print(f"ID: {p['id']}")
            print(f"Nombre: {p['name'].capitalize()}")
            print(f"Tipos: {', '.join(p['types'])}")
            print(f"Altura: {p['height']}")
            print(f"Peso: {p['weight']}")
        print(SEPARATOR)

if __name__ == "__main__":
    asyncio.run(main())