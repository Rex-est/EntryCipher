import { Routes } from '@angular/router';
import { LoginComponent } from '../app/core/auth/login/login.component';
import { DashboardComponent } from './features/admin/dashboard/dashboard.component';
import { ScannerComponent } from './features/operator/scanner/scanner.component';

export const routes: Routes = [
  { path: 'login', component: LoginComponent },
  { path: 'admin', component: DashboardComponent },   // <--- Agregado
  { path: 'scanner', component: ScannerComponent }, // <--- Agregado
  { path: '', redirectTo: 'login', pathMatch: 'full' },
  { path: '**', redirectTo: 'login' } // Por si escriben cualquier cosa
];