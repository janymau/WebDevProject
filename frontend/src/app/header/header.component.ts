import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
@Component({
  selector: 'app-header',
  standalone: true,
  imports: [CommonModule, RouterModule],
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.css']
})
export class HeaderComponent {
  isLoggedIn = true; // временно для демонстрации
  username = 'Uldar';
  userAvatarUrl = 'assets/avatar.png'; // заглушка

  constructor(private router: Router) {}

  goHome() {
    this.router.navigate(['/']);
  }

  goLogin() {
    this.router.navigate(['/login']);
  }

  goSignup() {
    this.router.navigate(['/register']);
  }

  logout() {
    // сюда вставь логику logout
    this.isLoggedIn = false;
    this.router.navigate(['/login']);
  }
}
