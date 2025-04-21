import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { EventService } from '../services/event.service';
import { Event } from './event.model'; // путь поправь при необходимости
import { Router } from '@angular/router';

@Component({
  selector: 'app-event',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './event.component.html',
  styleUrls: ['./event.component.css']
})
export class EventComponent implements OnInit {
  events: Event[] = [];

  constructor(private eventService: EventService, private router: Router) {}

  ngOnInit(): void {
    this.eventService.getAllEvents().subscribe((data: Event[]) => {
      this.events = data;
    });
  }

  goToDetails(eventId: number) {
    this.router.navigate(['/events', eventId]);
  }

  applyToEvent(eventId: number) {
    this.eventService.joinEvent(eventId).subscribe({
      next: () => alert('Заявка отправлена!'),
      error: err => alert(err.error?.error || 'Ошибка')
    });
  }
}
