from typing import Annotated

from fastapi import Depends

from app.auth import get_admin_user, get_current_active_user
from app.models.usuario import Usuario

CurrentUser = Annotated[Usuario, Depends(get_current_active_user)]
AdminUser = Annotated[Usuario, Depends(get_admin_user)]
