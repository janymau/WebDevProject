import { Component } from '@angular/core';
import { HeaderComponent } from '../header/header.component';
import { EventComponent } from '../event/event.component';

@Component({
  selector: 'app-main-page',
  imports: [HeaderComponent, EventComponent],
  templateUrl: './main-page.component.html',
  styleUrl: './main-page.component.css'
})
export class MainPageComponent {

}
