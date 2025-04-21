import { Component } from '@angular/core';
import { AuthService } from '../services/auth.service';
import { Router } from '@angular/router';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-register-menu',
  imports: [CommonModule, FormsModule],
  templateUrl: './register-menu.component.html',
  styleUrl: './register-menu.component.css'
})
export class RegisterMenuComponent {
  form = {
    username: '',
    password: '',
    first_name: '',
    last_name: '',
    age: 0,
    phoneNumber: ''
    };

  message = '';
  errorMessage = '';

  constructor(private authService: AuthService, private router: Router) {}

  register() {
    console.log('Отправляемые данные:', this.form);
    this.authService.register(this.form).subscribe({
      next: () => {
        this.message = 'Регистрация успешна!';
        this.errorMessage = '';
        this.router.navigate(['/']); 
      },
      error: (err) => {
        console.error(err);
        this.message = '';
        this.errorMessage = 'Ошибка регистрации. Проверьте введённые данные.';
      }
    });
  }
}
