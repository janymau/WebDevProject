import { Component, OnInit } from '@angular/core';
import { EventService } from '../services/event.service';

@Component({
  selector: 'app-event-list',
  templateUrl: './event-list.component.html',
  styleUrls: ['./event-list.component.css']
})
export class EventComponent implements OnInit {
  events: any[] = []; // Массив для хранения всех событий

  constructor(private eventService: EventService) {}

  ngOnInit(): void {
    // Получаем все события при загрузке компонента
    this.eventService.getAllEvents().subscribe((data) => {
      this.events = data; // Заполняем массив events данными из API
    });
  }
}
