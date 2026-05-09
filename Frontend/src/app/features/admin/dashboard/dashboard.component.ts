import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { AuthService } from '../../../core/services/auth.service'; 
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './dashboard.component.html'
})
export class DashboardComponent {
  
  // Cambiamos 'LoginComponent' por 'AuthService'
  constructor(
    private authService: AuthService, 
    private router: Router
  ) {}

  logout() {
    // El servicio es el que se encarga de borrar los tokens
    this.authService.logout(); 
    // Luego te vas al login
    this.router.navigate(['/login']);
  }
}