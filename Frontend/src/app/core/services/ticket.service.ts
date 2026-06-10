import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../../environments/environment';

export interface TicketPurchase {
  event_id: number;
  zone_id: number;
}

export interface TicketResponse {
  id: number;
  ticket_code: string;
  event_id: number;
  zone_id: number;
  price_paid: number;
  purchased_at: string;
  is_used: boolean;
}

export interface DynamicQRResponse {
  dynamic_token: string;
  expires_in: number;
}

@Injectable({
  providedIn: 'root'
})
export class TicketService {
  private http = inject(HttpClient);
  private apiUrl = `${environment.apiUrl}/tickets/`;

  buyTicket(data: TicketPurchase): Observable<TicketResponse> {
    return this.http.post<TicketResponse>(`${this.apiUrl}buy`, data);
  }

  getMyTickets(): Observable<TicketResponse[]> {
    return this.http.get<TicketResponse[]>(`${this.apiUrl}my-tickets`);
  }

  getDynamicQR(ticketCode: string): Observable<DynamicQRResponse> {
    return this.http.get<DynamicQRResponse>(`${this.apiUrl}generate-qr/${ticketCode}`);
  }
}
