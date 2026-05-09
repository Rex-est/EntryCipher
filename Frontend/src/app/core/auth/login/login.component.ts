import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { AuthService } from '../../services/auth.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './login.component.html',
  styleUrls: []
})
export class LoginComponent {
  // Modelo para el formulario
  credentials = {
    email: '',
    password: ''
  };

  errorMessage: string = '';

  constructor(private authService: AuthService, private router: Router) {}

 onLogin() {
    const formData = new FormData();
    formData.append('username', this.credentials.email);
    formData.append('password', this.credentials.password);

    this.authService.login(formData).subscribe({
      // Agregamos ": any" para que TypeScript no se queje
      next: (res: any) => {
        console.log('¡Acceso concedido!');
        const role = localStorage.getItem('user_role');
        
        // Redirección simple según rol
        if (role === 'ADMIN') this.router.navigate(['/admin']);
        else if (role === 'OPERATOR') this.router.navigate(['/scanner']);
        else this.router.navigate(['/my-tickets']);
      },
      error: (err: any) => {
        this.errorMessage = 'Credenciales inválidas';
        console.error(err);
      }
    });
  }

  logout() {
  localStorage.removeItem('token');
  localStorage.removeItem('user_role');
}
}