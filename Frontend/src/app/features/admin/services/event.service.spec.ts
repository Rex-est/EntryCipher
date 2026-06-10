import { TestBed } from '@angular/core/testing';
import { HttpClientTestingModule, HttpTestingController } from '@angular/common/http/testing';
import { EventService } from './event.service';
import { environment } from '../../../../environments/environment';
import { describe, it, expect, beforeEach, afterEach } from 'vitest';

describe('EventService', () => {
  let service: EventService;
  let httpMock: HttpTestingController;

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [HttpClientTestingModule],
      providers: [EventService]
    });
    service = TestBed.inject(EventService);
    httpMock = TestBed.inject(HttpTestingController);
  });

  afterEach(() => {
    httpMock.verify();
  });

  it('debe obtener la lista de eventos', () => {
    const mockEvents = [{ id: 1, name: 'Evento 1', location: 'Lugar 1', date: '2026-01-01' }];

    service.getEvents().subscribe(events => {
      expect(events).toEqual(mockEvents);
    });

    const req = httpMock.expectOne(`${environment.apiUrl}/events/`);
    expect(req.request.method).toBe('GET');
    req.flush(mockEvents);
  });

  it('debe crear un evento', () => {
    const newEvent = { name: 'Nuevo', location: 'Lugar', date: '2026-01-01' } as any;
    const mockRes = { ...newEvent, id: 99 };

    service.createEvent(newEvent).subscribe(res => {
      expect(res.id).toBe(99);
    });

    const req = httpMock.expectOne(`${environment.apiUrl}/events/`);
    expect(req.request.method).toBe('POST');
    req.flush(mockRes);
  });
});
