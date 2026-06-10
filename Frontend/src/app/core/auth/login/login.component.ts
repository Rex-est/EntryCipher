import { Component, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { AuthService } from '../../services/auth.service';
import { Router, RouterModule } from '@angular/router';

@Component({
  selector: 'app-login',
  imports: [CommonModule, FormsModule, RouterModule],
  templateUrl: './login.component.html',
  styleUrls: []
})
export class LoginComponent {
  private authService = inject(AuthService);
  private router = inject(Router);

  // Modelo para el formulario
  credentials = {
    email: '',
    password: ''
  };

  errorMessage: string = '';

  onLogin() {
    const formData = new FormData();
    formData.append('username', this.credentials.email);
    formData.append('password', this.credentials.password);

    this.authService.login(formData).subscribe({
      next: () => {
        console.log('¡Acceso concedido!');
        const role = localStorage.getItem('user_role');
        
        // Redirección según rol
        if (role === 'ADMIN') this.router.navigate(['/admin']);
        else if (role === 'OPERATOR') this.router.navigate(['/scanner']);
        else this.router.navigate(['/dashboard']);
      },
      error: (err: any) => {
        this.errorMessage = 'Credenciales inválidas';
        console.error(err);
      }
    });
  }
}