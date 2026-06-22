import { TestBed } from '@angular/core/testing';
import { HttpClientTestingModule, HttpTestingController } from '@angular/common/http/testing';
import { AuthService } from './auth.service';
import { environment } from '../../../environments/environment';
import { describe, it, expect, beforeEach, afterEach } from 'vitest';

describe('AuthService', () => {
  let service: AuthService;
  let httpMock: HttpTestingController;

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [HttpClientTestingModule],
      providers: [AuthService]
    });
    service = TestBed.inject(AuthService);
    httpMock = TestBed.inject(HttpTestingController);
    sessionStorage.clear();
  });

  afterEach(() => {
    httpMock.verify();
  });

  it('debe iniciar sesión y guardar el token', () => {
    const mockRes = { access_token: 'fake-token', role: 'USER' };
    const formData = new FormData();

    service.login(formData).subscribe(res => {
      expect(res).toEqual(mockRes);
      expect(sessionStorage.getItem('token')).toBe('fake-token');
      expect(sessionStorage.getItem('user_role')).toBe('USER');
    });

    const req = httpMock.expectOne(`${environment.apiUrl}/auth/login`);
    expect(req.request.method).toBe('POST');
    req.flush(mockRes);
  });

  it('debe cerrar sesión y limpiar el storage', () => {
    sessionStorage.setItem('token', 'old-token');
    sessionStorage.setItem('user_role', 'ADMIN');
    
    service.logout();
    
    expect(sessionStorage.getItem('token')).toBeNull();
    expect(sessionStorage.getItem('user_role')).toBeNull();
  });

  it('debe obtener el token correctamente', () => {
    sessionStorage.setItem('token', 'xyz');
    expect(service.getToken()).toBe('xyz');
  });

  it('debe verificar si está logueado', () => {
    expect(service.isLoggedIn()).toBe(false);
    sessionStorage.setItem('token', 'xyz');
    expect(service.isLoggedIn()).toBe(true);
  });
});
