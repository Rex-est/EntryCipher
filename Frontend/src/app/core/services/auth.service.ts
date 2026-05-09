import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from '../../../environments/environment';
import { tap } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private apiUrl = environment.apiUrl;

  constructor(private http: HttpClient) {}

  login(formData: FormData) {
    return this.http.post(`${this.apiUrl}/auth/login`, formData).pipe(
      tap((res: any) => {
        // Guardamos los datos importantes en el navegador
        localStorage.setItem('token', res.access_token);
        localStorage.setItem('user_role', res.role);
      })
    );
  }

    logout() {
  localStorage.removeItem('token');
  localStorage.removeItem('user_role');
}
}