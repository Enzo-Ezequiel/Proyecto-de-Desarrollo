"""
Servicio de Usuarios: Contiene la lógica de negocio para gestionar usuarios.

Principios aplicados:
- Single Responsibility: Solo maneja operaciones de usuarios.
- DRY: Extiende BaseService para reutilizar CRUD común.
- Fail-fast: Valida datos tempranamente.
"""

from typing import Callable, List, Optional
from uuid import UUID

from app.core.exceptions import DuplicateResourceException
from app.models import User

from .base_service import BaseService


class UserService(BaseService[User]):
    """
    Servicio para gestionar usuarios en la aplicación.

    Proporciona métodos específicos de negocio para usuarios como búsqueda
    por email, activación/desactivación, etc.
    """

    def get_by_email(self, email: str) -> Optional[User]:
        """
        Busca un usuario por su correo electrónico.

        Args:
            email: El correo electrónico del usuario.

        Returns:
            El usuario si existe, None en caso contrario.
        """
        for user in self._repository.values():
            if user.email.lower() == email.lower():
                return user
        return None

    def email_exists(self, email: str) -> bool:
        """
        Verifica si un correo electrónico ya está registrado.

        Args:
            email: El correo a verificar.

        Returns:
            True si el email existe, False en caso contrario.
        """
        return self.get_by_email(email) is not None

    def get_active_users(self) -> List[User]:
        """
        Obtiene todos los usuarios activos.

        Returns:
            Lista de usuarios activos.
        """
        return [user for user in self.get_all() if user.is_active]

    def _apply_user_state_change(
        self, user_id: UUID, state_setter: Callable[[User], None]
    ) -> Optional[User]:
        """
        Helper para aplicar cambios de estado a un usuario.

        Consolidahizo el patrón repetido de obtener usuario → cambiar estado → actualizar.

        Args:
            user_id: El ID del usuario.
            state_setter: Función que aplica el cambio de estado al usuario.

        Returns:
            El usuario con el estado aplicado, o None si no existe.
        """
        user = self.get_by_id(str(user_id))
        if user:
            state_setter(user)
            self.update(user)
        return user

    def deactivate_user(self, user_id: UUID) -> Optional[User]:
        """
        Desactiva un usuario por su ID.

        Args:
            user_id: El ID del usuario a desactivar.

        Returns:
            El usuario desactivado, o None si no existe.
        """
        return self._apply_user_state_change(user_id, lambda u: u.deactivate())

    def activate_user(self, user_id: UUID) -> Optional[User]:
        """
        Activa un usuario por su ID.

        Args:
            user_id: El ID del usuario a activar.

        Returns:
            El usuario activado, o None si no existe.
        """
        return self._apply_user_state_change(user_id, lambda u: u.activate())

    def create_user(
        self,
        email: str,
        full_name: str,
        description: Optional[str] = None,
    ) -> User:
        """
        Crea un nuevo usuario.

        Args:
            email: Correo del usuario.
            full_name: Nombre completo del usuario.
            description: Descripción opcional del usuario.

        Returns:
            El usuario creado.

        Raises:
            DuplicateResourceException: Si el email ya existe.
            ValidationException: Si los datos son inválidos.
        """
        if self.email_exists(email):
            raise DuplicateResourceException("Usuario", f"email={email}")

        user = User(
            email=email,
            full_name=full_name,
            description=description,
        )
        return self.create(user)
