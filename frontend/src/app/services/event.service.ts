import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Event } from '../event/event.model'; // поправь путь если модель в другой папке

@Injectable({
  providedIn: 'root'
})
export class EventService {
  private apiUrl = 'http://127.0.0.1:8000/api/events/';

  constructor(private http: HttpClient) {}

  // Получение списка всех событий
  getAllEvents(): Observable<Event[]> {
    return this.http.get<Event[]>(this.apiUrl);
  }

  // Подать заявку на участие
  joinEvent(eventId: number): Observable<any> {
    return this.http.post(`${this.apiUrl}${eventId}/join/`, {});
  }

  // Получение одного события (если нужно для страницы "Подробнее")
  getEventById(eventId: number): Observable<Event> {
    return this.http.get<Event>(`${this.apiUrl}${eventId}/`);
  }
}
