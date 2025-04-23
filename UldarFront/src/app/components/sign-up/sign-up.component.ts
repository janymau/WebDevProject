import { Component, OnInit } from '@angular/core';
import { AbstractControl, FormBuilder, FormControl, FormGroup, Validators } from '@angular/forms';
import { ServiceService } from '../../services/service.service';
import Validation from '../../utils/validation';
import { Router } from '@angular/router';

@Component({
  selector: 'app-sign-up',
  templateUrl: './sign-up.component.html',
  styleUrls: ['./sign-up.component.css']
})
export class SignUpComponent implements OnInit {

  form: FormGroup = new FormGroup({});
  submitted = false;

  constructor(
    private formBuilder: FormBuilder,
    private service: ServiceService,
    private router: Router
  ) {}

  ngOnInit(): void {
    this.form = this.formBuilder.group(
      {
        firstname: ['', Validators.required],
        lastname: ['', Validators.required],
        age: ['', Validators.required],
        username: [
          '',
          [Validators.required, Validators.minLength(6), Validators.maxLength(20)]
        ],
        email: ['', [Validators.required, Validators.email]],
        password: [
          '',
          [Validators.required, Validators.minLength(6), Validators.maxLength(40)]
        ],
        confirmPassword: ['', Validators.required],
      },
      {
        validators: [Validation.match('password', 'confirmPassword')]
      }
    );
  }

  get f(): { [key: string]: AbstractControl } {
    return this.form.controls;
  }

  onSubmit(): void {
    this.submitted = true;

    if (this.form.invalid) return;

    const data = {
      email: this.form.get('email')?.value,
      username: this.form.get('username')?.value,
      first_name: this.form.get('firstname')?.value,
      last_name: this.form.get('lastname')?.value,
      password: this.form.get('password')?.value,
      password2: this.form.get('confirmPassword')?.value, 
      age: this.form.get('age')?.value,
    };

    this.service.register(data).subscribe({
      next: (response) => {
        console.log('Registration success', response);
        this.router.navigateByUrl('/login'); 
      },
      error: (error) => {
        console.error('Registration failed', error);
      }
    });
  }

  onReset(): void {
    this.submitted = false;
    this.form.reset();
  }
}
