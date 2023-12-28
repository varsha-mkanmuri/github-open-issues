import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { OpenIssuesComponent } from './open-issues/open-issues.component';

import {HttpClientModule} from '@angular/common/http';
import {FormsModule} from '@angular/forms';
import { IssuesServiceService } from './issues-service.service';


@NgModule({
  declarations: [
    AppComponent,
    OpenIssuesComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule,
    FormsModule
  ],
  providers: [IssuesServiceService],
  bootstrap: [AppComponent]
})
export class AppModule { }
