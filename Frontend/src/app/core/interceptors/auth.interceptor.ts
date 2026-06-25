import { HttpInterceptorFn, HttpErrorResponse } from '@angular/common/http';
import { inject } from '@angular/core';
import { Router } from '@angular/router';
import { catchError, throwError } from 'rxjs';
import { AuthService } from '../services/auth.service';

export const authInterceptor: HttpInterceptorFn = (req, next) => {
  const authService = inject(AuthService);
  const router = inject(Router);
  const token = authService.getToken();

  let authReq = req;
  if (token) {
    authReq = req.clone({
      setHeaders: { Authorization: `Bearer ${token}` }
    });
  }

  return next(authReq).pipe(
    catchError((error: HttpErrorResponse) => {
      if (error.status === 401) {
        // Mensaje específico del backend para multisesión
        const detail = error.error?.detail;
        if (detail && detail.includes('otro dispositivo')) {
          alert('🚫 SESIÓN CERRADA: Se ha detectado un nuevo inicio de sesión en otro dispositivo. Por seguridad, esta sesión se cerrará.');
        } else {
          // Opcional: mensaje general para otros casos de 401
          console.warn('Sesión expirada o no autorizada');
        }

        authService.logout();
        router.navigate(['/login']);
      }
      return throwError(() => error);
    })
  );
};