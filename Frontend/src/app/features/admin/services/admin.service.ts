import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../../../environments/environment';

export interface DashboardAnalytics {
  total_sales: number;
  revenue: number;
  active_events: number;
  sales_velocity: { date: string, sales: number }[];
}

export interface Buyer {
  id: number;
  email: string;
  dni: string;
  is_active: boolean;
}

@Injectable({
  providedIn: 'root'
})
export class AdminService {
  private http = inject(HttpClient);
  private apiUrl = `${environment.apiUrl}/admin`;

  getAnalytics(): Observable<DashboardAnalytics> {
    return this.http.get<DashboardAnalytics>(`${this.apiUrl}/analytics`);
  }

  getBuyers(): Observable<Buyer[]> {
    return this.http.get<Buyer[]>(`${this.apiUrl}/buyers`);
  }

  toggleUserStatus(userId: number): Observable<any> {
    return this.http.post(`${this.apiUrl}/users/${userId}/toggle-status`, {});
  }
}
