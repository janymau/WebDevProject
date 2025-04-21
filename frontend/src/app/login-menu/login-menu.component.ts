import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { AuthService } from '../services/auth.service';
import { Router } from '@angular/router';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-login-menu',
  imports: [FormsModule, CommonModule],
  templateUrl: './login-menu.component.html',
  styleUrl: './login-menu.component.css'
})
export class LoginMenuComponent {
  username = '';
  password = '';
  errorMessage = '';

  constructor(private authService: AuthService,private router: Router){}

  login(){
    this.authService.login(this.username, this.password).subscribe({
      next: (response)=>{
        localStorage.setItem('access', response.access);
        localStorage.setItem('refresh', response.refresh);
        console.log('logged in');
        this.errorMessage = '';
        this.router.navigate(['main']);
      },
      error: (error)=>{
        console.error('Login error', error);
        this.errorMessage = 'Неверный логин или пароль';
      }
    })



  }
}
