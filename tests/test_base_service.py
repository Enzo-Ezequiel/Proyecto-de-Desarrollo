"""Tests unitarios de BaseService con InMemoryRepository."""

import pytest

from app.core.exceptions import ResourceNotFoundException
from app.core.repository import InMemoryRepository
from app.models.base_model import BaseEntity
from app.services.base_service import BaseService


class MockEntity(BaseEntity):
    """Entidad de prueba para BaseService."""

    def __init__(self, nombre: str = "test", **kwargs):
        super().__init__(**kwargs)
        self.nombre = nombre


@pytest.fixture
def service() -> BaseService[MockEntity]:
    """BaseService con repositorio en memoria."""
    return BaseService[MockEntity](InMemoryRepository[MockEntity]())


@pytest.mark.unit
def test_create_agrega_entidad(service):
    """create() agrega una entidad al repositorio."""
    import asyncio

    async def _ejercitar():
        entity = MockEntity(nombre="doc1")
        result = await service.create(entity)
        assert result.nombre == "doc1"
        assert result.id is not None

    asyncio.run(_ejercitar())


@pytest.mark.unit
def test_get_by_id_existe(service):
    """get_by_id() retorna la entidad cuando existe."""
    import asyncio

    async def _ejercitar():
        entity = MockEntity(nombre="buscar")
        await service.create(entity)

        encontrada = await service.get_by_id(entity.id)
        assert encontrada is not None
        assert encontrada.nombre == "buscar"

    asyncio.run(_ejercitar())


@pytest.mark.unit
def test_get_by_id_no_existe(service):
    """get_by_id() retorna None cuando no existe."""
    import asyncio

    async def _ejercitar():
        result = await service.get_by_id("id-falso")
        assert result is None

    asyncio.run(_ejercitar())


@pytest.mark.unit
def test_get_all_vacio(service):
    """get_all() retorna lista vacía cuando no hay entidades."""
    import asyncio

    async def _ejercitar():
        result = await service.get_all()
        assert result == []

    asyncio.run(_ejercitar())


@pytest.mark.unit
def test_get_all_con_entidades(service):
    """get_all() retorna todas las entidades."""
    import asyncio

    async def _ejercitar():
        await service.create(MockEntity(nombre="a"))
        await service.create(MockEntity(nombre="b"))

        todas = await service.get_all()
        assert len(todas) == 2
        nombres = {e.nombre for e in todas}
        assert nombres == {"a", "b"}

    asyncio.run(_ejercitar())


@pytest.mark.unit
def test_update_entidad_existente(service):
    """update() actualiza una entidad existente."""
    import asyncio

    async def _ejercitar():
        entity = MockEntity(nombre="original")
        await service.create(entity)

        entity.nombre = "modificado"
        await service.update(entity)

        encontrada = await service.get_by_id(entity.id)
        assert encontrada.nombre == "modificado"

    asyncio.run(_ejercitar())


@pytest.mark.unit
def test_update_entidad_no_existente_lanza_excepcion(service):
    """update() lanza ResourceNotFoundException si la entidad no existe."""
    import asyncio

    async def _ejercitar():
        entity = MockEntity(nombre="fantasma")
        with pytest.raises(ResourceNotFoundException):
            await service.update(entity)

    asyncio.run(_ejercitar())


@pytest.mark.unit
def test_delete_entidad_existente(service):
    """delete() elimina una entidad existente y retorna True."""
    import asyncio

    async def _ejercitar():
        entity = MockEntity(nombre="borrable")
        await service.create(entity)

        resultado = await service.delete(entity.id)
        assert resultado is True

        assert await service.get_by_id(entity.id) is None

    asyncio.run(_ejercitar())


@pytest.mark.unit
def test_delete_entidad_no_existente(service):
    """delete() retorna False cuando la entidad no existe."""
    import asyncio

    async def _ejercitar():
        resultado = await service.delete("id-falso")
        assert resultado is False

    asyncio.run(_ejercitar())


@pytest.mark.unit
def test_count_vacio(service):
    """count() retorna 0 cuando no hay entidades."""
    import asyncio

    async def _ejercitar():
        assert await service.count() == 0

    asyncio.run(_ejercitar())


@pytest.mark.unit
def test_count_con_entidades(service):
    """count() retorna el número correcto de entidades."""
    import asyncio

    async def _ejercitar():
        await service.create(MockEntity(nombre="a"))
        await service.create(MockEntity(nombre="b"))
        await service.create(MockEntity(nombre="c"))

        assert await service.count() == 3

    asyncio.run(_ejercitar())
