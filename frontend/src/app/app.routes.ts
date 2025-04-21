import { Routes } from '@angular/router';
import { MainPageComponent } from './main-page/main-page.component';
import { LoginMenuComponent } from './login-menu/login-menu.component';
import { RegisterMenuComponent } from './register-menu/register-menu.component';
import { AuthGuard } from './services/guard.service';  // Импортируйте ваш AuthGuard
import { EventComponent } from './event/event.component';

export const routes: Routes = [
    { path: '', component: LoginMenuComponent },
    { path: 'main', component: MainPageComponent, canActivate: [AuthGuard] },  // Добавляем Guard
    { path: 'register', component: RegisterMenuComponent },
    {path: 'events', component:EventComponent , canActivate: [AuthGuard] }
];
