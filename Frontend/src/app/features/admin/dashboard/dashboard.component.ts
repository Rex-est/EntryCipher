import { Component, OnInit, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { AuthService } from '../../../core/services/auth.service';
import { EventService, EventResponse, EventCreate, EventZone, PricingTier } from '../services/event.service';
import { AdminService, DashboardAnalytics, Buyer } from '../services/admin.service';
import { GlassCardComponent } from '../../../shared/components/glass-card/glass-card.component';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [CommonModule, FormsModule, GlassCardComponent],
  templateUrl: './dashboard.component.html'
})
export class DashboardComponent implements OnInit {
  private eventService = inject(EventService);
  private adminService = inject(AdminService);
  private authService = inject(AuthService);
  private router = inject(Router);

  // Data
  events: EventResponse[] = [];
  analytics: DashboardAnalytics | null = null;
  buyers: Buyer[] = [];
  
  // UI State
  activeTab: 'dashboard' | 'events' | 'users' = 'dashboard';
  showCreatorModal = false;
  showMobileMenu = false;
  currentStep = 1;

  // Formulario Avanzado para nuevo evento
  newEvent: EventCreate = {
    name: '',
    description: '',
    category: 'Concierto',
    location: '',
    date: '',
    zones: []
  };

  ngOnInit() {
    this.refreshData();
  }

  refreshData() {
    this.loadEvents();
    this.loadAnalytics();
    this.loadBuyers();
  }

  loadEvents() {
    this.eventService.getEvents().subscribe(data => this.events = data);
  }

  loadAnalytics() {
    this.adminService.getAnalytics().subscribe(data => this.analytics = data);
  }

  loadBuyers() {
    this.adminService.getBuyers().subscribe(data => this.buyers = data);
  }

  toggleUserStatus(buyer: Buyer) {
    this.adminService.toggleUserStatus(buyer.id).subscribe({
      next: (res) => {
        buyer.is_active = res.is_active;
      },
      error: (err) => console.error('Error toggling status:', err)
    });
  }

  // --- Creator Logic ---
  openCreator() {
    this.showCreatorModal = true;
    this.currentStep = 1;
    this.newEvent = {
      name: '', description: '', category: 'Concierto', location: '', date: '', zones: []
    };
  }

  nextStep() { this.currentStep++; }
  prevStep() { this.currentStep--; }

  addZone() {
    const newZone: EventZone = {
      name: '', total_capacity: 0, is_numbered: false, tiers: []
    };
    this.newEvent.zones?.push(newZone);
  }

  removeZone(index: number) {
    this.newEvent.zones?.splice(index, 1);
  }

  addTier(zone: EventZone) {
    const newTier: PricingTier = {
      name: '', price: 0, stock_limit: 0, is_active: true
    };
    zone.tiers.push(newTier);
  }

  onCreateEvent() {
    this.eventService.createEvent(this.newEvent).subscribe({
      next: (res) => {
        this.events.push(res);
        this.showCreatorModal = false;
        this.refreshData();
      },
      error: (err) => console.error('Error:', err)
    });
  }

  logout() {
    this.authService.logout();
    this.router.navigate(['/login']);
  }
}
