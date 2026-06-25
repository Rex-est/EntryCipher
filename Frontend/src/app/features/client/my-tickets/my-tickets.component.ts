import { Component, OnInit, inject, signal, ChangeDetectionStrategy } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router, RouterLink } from '@angular/router';
import { TicketService, TicketResponse, DynamicQRResponse } from '../../../core/services/ticket.service';
import { EventService, EventResponse } from '../../admin/services/event.service';
import { AuthService } from '../../../core/services/auth.service';
import { GlassCardComponent } from '../../../shared/components/glass-card/glass-card.component';

@Component({
  selector: 'app-my-tickets',
  standalone: true,
  imports: [CommonModule, RouterLink, GlassCardComponent],
  templateUrl: './my-tickets.component.html',
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class MyTicketsComponent implements OnInit {
  private ticketService = inject(TicketService);
  private eventService = inject(EventService);
  private authService = inject(AuthService);
  private router = inject(Router);

  tickets = signal<TicketResponse[]>([]);
  events = signal<EventResponse[]>([]);
  qrData = signal<{ [key: string]: DynamicQRResponse }>({});
  showMobileMenu = signal(false);

  ngOnInit() {
    this.ticketService.getMyTickets().subscribe(data => this.tickets.set(data));
    this.eventService.getEvents().subscribe(data => this.events.set(data));
  }

  logout() {
    this.authService.logout();
    this.router.navigate(['/login']);
  }

  getEventName(eventId: number): string {
    return this.events().find(e => e.id === eventId)?.name || 'Evento Desconocido';
  }

  generateQR(ticketCode: string) {
    this.ticketService.getDynamicQR(ticketCode).subscribe(res => {
      this.qrData.update(prev => ({ ...prev, [ticketCode]: res }));
      
      const timer = setInterval(() => {
        const currentData = this.qrData()[ticketCode];
        if (currentData && currentData.expires_in > 0) {
          this.qrData.update(prev => ({
            ...prev,
            [ticketCode]: { ...currentData, expires_in: currentData.expires_in - 1 }
          }));
        } else {
          clearInterval(timer);
          this.generateQR(ticketCode);
        }
      }, 1000);
    });
  }
}