import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  private http = inject(HttpClient);
  private apiUrl = 'http://localhost:8000'; // FastAPI default port

  getHealth(): Observable<any> {
    return this.http.get(`${this.apiUrl}/`);
  }
}
