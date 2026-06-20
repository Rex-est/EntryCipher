import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { GlassCardComponent } from '../../../shared/components/glass-card/glass-card.component';

@Component({
  selector: 'app-scanner',
  standalone: true,
  imports: [CommonModule, FormsModule, GlassCardComponent],
  templateUrl: './scanner.component.html'
})
export class ScannerComponent {
  ticketCode: string = '';
  statusMessage: string = '';
  isSuccess: boolean = false;

  validarTicket() {
    // Aquí luego conectaremos con tu endpoint POST /api/v1/tickets/validate/{code}
    console.log('Validando ticket:', this.ticketCode);
    
    // Simulación por ahora:
    if (this.ticketCode.length > 5) {
      this.statusMessage = "¡ACCESO AUTORIZADO!";
      this.isSuccess = true;
    } else {
      this.statusMessage = "CÓDIGO INVÁLIDO";
      this.isSuccess = false;
    }
  }
}