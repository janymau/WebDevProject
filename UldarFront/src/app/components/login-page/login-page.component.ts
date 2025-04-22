import { Component, OnInit } from '@angular/core';
import { ServiceService } from 'src/app/services/service.service';
import { Location } from '@angular/common';
import { Router } from '@angular/router';

@Component({
  selector: 'app-login-page',
  templateUrl: './login-page.component.html',
  styleUrls: ['./login-page.component.css']
})
export class LoginPageComponent implements OnInit {

  email='';
  password='';
  logged=false;
  error=false;

  constructor(private _service:ServiceService,
              private location:Location,
              private router: Router) { }

  ngOnInit(): void {
    const access=localStorage.getItem('access');
    if (access) this.logged=true;
    if (this.logged) {
      this.router.navigateByUrl('questions').then()
    }
  }
  login(){
    this._service.login(this.email,this.password).subscribe(
      (data)=>{
        this.logged=true;
        localStorage.setItem('access',data.access);
        this.email='';
        this.password='';
        location.reload();
      },
      (error)=>{
        this.error=true;
        console.log("Error(");
      }
    )
  }

}