import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../../../environments/environment';

export interface PricingTier {
  name: string;
  price: number;
  stock_limit: number;
  start_date?: string;
  end_date?: string;
  is_active: boolean;
}

export interface EventZone {
  id?: number; // Añadido para identificación en el front
  name: string;
  total_capacity: number;
  is_numbered: boolean;
  tiers: PricingTier[];
}

export interface EventCreate {
  name: string;
  description?: string;
  category?: string;
  location: string;
  date: string;
  banner_url?: string;
  max_tickets_per_user?: number; // Añadido
  start_presale_date?: string;
  start_sale_date?: string;
  end_publish_date?: string;
  terms_and_conditions?: string;
  social_links?: string;
  capacity?: number; // Legacy
  price?: number;    // Legacy
  zones?: EventZone[];
}

export interface EventResponse extends EventCreate {
  id: number;
}

@Injectable({
  providedIn: 'root'
})
export class EventService {
  private http = inject(HttpClient);
  private apiUrl = `${environment.apiUrl}/events/`;

  getEvents(): Observable<EventResponse[]> {
    return this.http.get<EventResponse[]>(this.apiUrl);
  }

  createEvent(event: EventCreate): Observable<EventResponse> {
    return this.http.post<EventResponse>(this.apiUrl, event);
  }
}
