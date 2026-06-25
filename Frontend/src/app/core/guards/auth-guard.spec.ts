import { TestBed } from '@angular/core/testing';
import { Router } from '@angular/router';
import { authGuard } from './auth-guard';
import { ActivatedRouteSnapshot, RouterStateSnapshot } from '@angular/router';
import { describe, it, expect, beforeEach, vi } from 'vitest';

describe('authGuard', () => {
  let router: Router;

  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [
        { provide: Router, useValue: { navigate: vi.fn() } }
      ]
    });
    router = TestBed.inject(Router);
    sessionStorage.clear();
  });

  it('debe bloquear el acceso si no hay token', () => {
    const route = { data: {} } as any;
    const state = {} as RouterStateSnapshot;
    
    const result = TestBed.runInInjectionContext(() => authGuard(route, state));
    
    expect(result).toBe(false);
    expect(router.navigate).toHaveBeenCalledWith(['/login']);
  });

  it('debe permitir acceso si el rol coincide', () => {
    sessionStorage.setItem('token', 'fake-token');
    sessionStorage.setItem('user_role', 'ADMIN');
    
    const route = { data: { role: 'ADMIN' } } as any;
    const state = {} as RouterStateSnapshot;
    
    const result = TestBed.runInInjectionContext(() => authGuard(route, state));
    
    expect(result).toBe(true);
  });

  it('debe bloquear acceso si el rol NO coincide', () => {
    sessionStorage.setItem('token', 'fake-token');
    sessionStorage.setItem('user_role', 'USER'); // Rol equivocado
    
    const route = { data: { role: 'ADMIN' } } as any;
    const state = {} as RouterStateSnapshot;
    
    const result = TestBed.runInInjectionContext(() => authGuard(route, state));
    
    expect(result).toBe(false);
    expect(router.navigate).toHaveBeenCalledWith(['/login']);
  });
});
