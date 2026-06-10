import { inject } from '@angular/core';
import { CanActivateFn, Router } from '@angular/router';

export const authGuard: CanActivateFn = (route, state) => {
  const router = inject(Router);
  const token = localStorage.getItem('token');
  const userRole = localStorage.getItem('user_role');

  if (!token) {
    router.navigate(['/login']);
    return false;
  }

  // Si la ruta requiere un rol específico (definido en 'data.role')
  const requiredRole = route.data?.['role'];
  
  if (requiredRole && userRole !== requiredRole) {
    // Si el rol no coincide, lo mandamos al login o a una página de acceso denegado
    // Por simplicidad, al login
    router.navigate(['/login']);
    return false;
  }

  return true;
};
