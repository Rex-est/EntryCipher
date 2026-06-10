import { Routes } from '@angular/router';
import { LoginComponent } from '../app/core/auth/login/login.component';
import { RegisterComponent } from './core/auth/register/register.component';
import { DashboardComponent } from './features/admin/dashboard/dashboard.component';
import { ScannerComponent } from './features/operator/scanner/scanner.component';
import { ClientDashboardComponent } from './features/client/dashboard/dashboard.component';
import { EventDetailsComponent } from './features/client/event-details/event-details.component';
import { MyTicketsComponent } from './features/client/my-tickets/my-tickets.component';
import { authGuard } from './core/guards/auth-guard';

export const routes: Routes = [
  { path: 'login', component: LoginComponent },
  { path: 'register', component: RegisterComponent },
  
  // Rutas de Admin
  { 
    path: 'admin', 
    component: DashboardComponent, 
    canActivate: [authGuard], 
    data: { role: 'ADMIN' } 
  },

  // Rutas de Operador
  { 
    path: 'scanner', 
    component: ScannerComponent, 
    canActivate: [authGuard], 
    data: { role: 'OPERATOR' } 
  },

  // Rutas de Cliente (USER)
  { 
    path: 'dashboard', 
    component: ClientDashboardComponent, 
    canActivate: [authGuard], 
    data: { role: 'USER' } 
  },
  { 
    path: 'event/:id', 
    component: EventDetailsComponent, 
    canActivate: [authGuard], 
    data: { role: 'USER' } 
  },
  { 
    path: 'my-tickets', 
    component: MyTicketsComponent, 
    canActivate: [authGuard], 
    data: { role: 'USER' } 
  },

  { path: '', redirectTo: 'login', pathMatch: 'full' },
  { path: '**', redirectTo: 'login' }
];
