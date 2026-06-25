import { TestBed } from '@angular/core/testing';
import { ClientDashboardComponent } from './dashboard.component';
import { EventService } from '../../admin/services/event.service';
import { AuthService } from '../../../core/services/auth.service';
import { of, throwError } from 'rxjs';
import { provideRouter, Router } from '@angular/router';
import { describe, it, expect, beforeEach, vi } from 'vitest';

describe('ClientDashboardComponent', () => {
  let component: ClientDashboardComponent;
  let eventServiceMock: any;

  beforeEach(async () => {
    eventServiceMock = {
      getEvents: vi.fn().mockReturnValue(of([
        { 
          id: 1, 
          name: 'Concierto Rock', 
          category: 'Concierto', 
          price: 50, 
          date: '2026-12-01',
          zones: [
            { name: 'VIP', tiers: [{ price: 100 }, { price: 80 }] },
            { name: 'General', tiers: [{ price: 40 }] }
          ] 
        }
      ]))
    };

    await TestBed.configureTestingModule({
      imports: [ClientDashboardComponent],
      providers: [
        { provide: EventService, useValue: eventServiceMock },
        { provide: AuthService, useValue: { logout: vi.fn() } },
        provideRouter([])
      ]
    }).compileComponents();

    const fixture = TestBed.createComponent(ClientDashboardComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('debe calcular el precio mínimo correctamente de las zonas', () => {
    const event = component.events()[0];
    const minPrice = component.getMinPrice(event);
    expect(minPrice).toBe(40);
  });

  it('debe usar el precio base si no hay zonas (Legacy)', () => {
    const legacyEvent = { id: 2, name: 'Legacy', price: 25, zones: [] } as any;
    const minPrice = component.getMinPrice(legacyEvent);
    expect(minPrice).toBe(25);
  });

  it('debe formatear la fecha correctamente', () => {
    const dateStr = '2026-10-15T12:00:00';
    const formatted = component.formatDate(dateStr);
    expect(formatted).toContain('15');
    expect(formatted.toLowerCase()).toContain('octubre');
  });

  it('debe manejar error al cargar eventos', () => {
    const consoleSpy = vi.spyOn(console, 'error').mockImplementation(() => {});
    eventServiceMock.getEvents.mockReturnValue(throwError(() => new Error('Error')));
    
    // Forzamos reinicio de ngOnInit
    component.ngOnInit();
    
    expect(component.error()).toContain('No se pudieron cargar los eventos');
    expect(component.loading()).toBe(false);
    consoleSpy.mockRestore();
  });

  it('debe manejar lista vacía de eventos', () => {
    eventServiceMock.getEvents.mockReturnValue(of([]));
    component.ngOnInit();
    expect(component.events().length).toBe(0);
    expect(component.loading()).toBe(false);
  });

  it('debe navegar al login al cerrar sesión', async () => {
    const authService = TestBed.inject(AuthService);
    const router = TestBed.inject(Router);
    const navigateSpy = vi.spyOn(router, 'navigate');
    
    component.logout();
    
    expect(authService.logout).toHaveBeenCalled();
    expect(navigateSpy).toHaveBeenCalledWith(['/login']);
  });
});
