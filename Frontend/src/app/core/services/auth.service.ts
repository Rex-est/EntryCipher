import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from '../../../environments/environment';
import { tap } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private http = inject(HttpClient);
  private apiUrl = environment.apiUrl;

  login(formData: FormData) {
    return this.http.post(`${this.apiUrl}/auth/login`, formData).pipe(
      tap((res: any) => {
        localStorage.setItem('token', res.access_token);
        localStorage.setItem('user_role', res.role);
      })
    );
  }

  register(userData: any) {
    return this.http.post(`${this.apiUrl}/auth/register`, userData);
  }

  logout() {
    localStorage.removeItem('token');
    localStorage.removeItem('user_role');
  }

  getToken(): string | null {
    return localStorage.getItem('token');
  }

  isLoggedIn(): boolean {
    return !!this.getToken();
  }
}