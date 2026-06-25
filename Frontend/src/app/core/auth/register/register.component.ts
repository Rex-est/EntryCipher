import { Component, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router, RouterModule } from '@angular/router';
import { AuthService } from '../../services/auth.service';
import { GlassCardComponent } from '../../../shared/components/glass-card/glass-card.component';

@Component({
  selector: 'app-register',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterModule, GlassCardComponent],
  templateUrl: './register.component.html'
})
export class RegisterComponent {
  private authService = inject(AuthService);
  private router = inject(Router);

  user = {
    email: '',
    password: '',
    full_name: '',
    dni: ''
  };

  errorMessage = '';
  loading = false;

  onRegister() {
    this.loading = true;
    this.errorMessage = '';
    
    this.authService.register(this.user).subscribe({
      next: () => {
        this.router.navigate(['/login'], { queryParams: { registered: true } });
      },
      error: (err) => {
        this.errorMessage = err.error?.detail || 'Error al registrar usuario';
        this.loading = false;
      }
    });
  }
}
