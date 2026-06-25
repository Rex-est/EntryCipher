import { Component, OnInit, inject, signal, ChangeDetectionStrategy } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink, Router } from '@angular/router';
import { EventService, EventResponse } from '../../admin/services/event.service';
import { AuthService } from '../../../core/services/auth.service';
import { GlassCardComponent } from '../../../shared/components/glass-card/glass-card.component';

@Component({
  selector: 'app-client-dashboard',
  standalone: true,
  imports: [CommonModule, RouterLink, GlassCardComponent],
  templateUrl: './dashboard.component.html',
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class ClientDashboardComponent implements OnInit {
  private eventService = inject(EventService);
  private authService = inject(AuthService);
  private router = inject(Router);

  events = signal<EventResponse[]>([]);
  loading = signal(true);
  error = signal('');
  showMobileMenu = signal(false);

  ngOnInit() {
    this.eventService.getEvents().subscribe({
      next: (data) => {
        this.events.set(data);
        this.loading.set(false);
      },
      error: (err) => {
        console.error('Error fetching events:', err);
        this.error.set('No se pudieron cargar los eventos. Por favor, intenta de nuevo más tarde.');
        this.loading.set(false);
      }
    });
  }

  logout() {
    this.authService.logout();
    this.router.navigate(['/login']);
  }

  getMinPrice(ev: EventResponse): number {
    if (!ev.zones || ev.zones.length === 0) return ev.price || 0;
    
    const prices = ev.zones
      .filter(z => z.tiers && z.tiers.length > 0)
      .flatMap(z => z.tiers.map(t => t.price));
    
    if (prices.length === 0) return ev.price || 0;
    return Math.min(...prices);
  }

  formatDate(dateStr: string): string {
    if (!dateStr) return '';
    try {
      const date = new Date(dateStr);
      return date.toLocaleDateString('es-ES', { day: '2-digit', month: 'long' });
    } catch {
      return dateStr;
    }
  }
}