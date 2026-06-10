import { Component, OnInit, inject, signal, ChangeDetectionStrategy } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, Router, RouterLink } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { EventService, EventResponse } from '../../admin/services/event.service';
import { TicketService } from '../../../core/services/ticket.service';
import { AuthService } from '../../../core/services/auth.service';

@Component({
  selector: 'app-event-details',
  imports: [CommonModule, FormsModule, RouterLink],
  templateUrl: './event-details.component.html',
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class EventDetailsComponent implements OnInit {
  private route = inject(ActivatedRoute);
  private router = inject(Router);
  private eventService = inject(EventService);
  private ticketService = inject(TicketService);
  private authService = inject(AuthService);

  event = signal<EventResponse | null>(null);
  selectedZone = signal<any>(null);
  purchaseSuccess = signal(false);
  purchaseError = signal('');

  ngOnInit() {
    const id = this.route.snapshot.paramMap.get('id');
    if (id) {
      this.eventService.getEvents().subscribe(events => {
        this.event.set(events.find(e => e.id === +id) || null);
      });
    }
  }

  logout() {
    this.authService.logout();
    this.router.navigate(['/login']);
  }

  getActivePrice(zone: any): number {
    if (!zone.tiers || zone.tiers.length === 0) return 0;
    return Math.min(...zone.tiers.map((t: any) => t.price));
  }

  buyTicket() {
    const currentEvent = this.event();
    const currentZone = this.selectedZone();
    if (!currentEvent || !currentZone) return;

    this.purchaseError.set('');
    this.ticketService.buyTicket({
      event_id: currentEvent.id,
      zone_id: currentZone.id
    }).subscribe({
      next: () => {
        this.purchaseSuccess.set(true);
        setTimeout(() => this.router.navigate(['/my-tickets']), 2000);
      },
      error: (err) => {
        this.purchaseError.set(err.error?.detail || 'Error en la compra');
      }
    });
  }
}