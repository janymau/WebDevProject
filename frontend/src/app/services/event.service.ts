import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class EventService {

  private apiUrl = 'http://127.0.0.1:8000/api/events/'; // URL для получения всех событий

  constructor(private http: HttpClient) {}

  // Получение списка всех событий
  getAllEvents(): Observable<any[]> {
    return this.http.get<any[]>(this.apiUrl);
  }
}
