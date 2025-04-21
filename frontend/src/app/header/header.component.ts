import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';

@Component({
  selector: 'app-header',
  imports: [CommonModule],
  templateUrl: './header.component.html',
  styleUrl: './header.component.css'
})
export class HeaderComponent {
  username = 'Bezdar666';
  isLoggedIn = true; // или false
  userAvatarUrl = 'https://i.pravatar.cc/150?img=3'; // или твой URL
}
