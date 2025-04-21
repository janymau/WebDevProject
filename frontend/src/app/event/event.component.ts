import { Component, OnInit } from '@angular/core';
import { EventService } from '../services/event.service';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-event',
  imports : [CommonModule, FormsModule],
  templateUrl: './event.component.html',
  styleUrls: ['./event.component.css']
})
export class EventComponent implements OnInit {
  events: any[] = []; 

  constructor(private eventService: EventService) {}

  ngOnInit(): void {
    
    this.eventService.getAllEvents().subscribe((data) => {
      this.events = data; 
    });
  }
}
