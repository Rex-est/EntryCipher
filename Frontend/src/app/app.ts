import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet],
  templateUrl: './app.html',
  styleUrl: './app.css'
})
// 👇 Fíjate que diga AppComponent
export class AppComponent {
  title = 'SafeTicket-Frontend';
}