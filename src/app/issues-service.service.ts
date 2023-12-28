import { Injectable } from '@angular/core';
import {HttpClient, HttpHeaders} from '@angular/common/http';
import {Observable} from 'rxjs';
import { UserInfo } from './Userinfo';


@Injectable({
  providedIn: 'root'
})
export class IssuesServiceService {

  constructor(private http: HttpClient) { }

  /*This function makes a call to the backend server , passing the owner name and reponame as aruments in the request*/
  fetchOpenIssuesCount(user: UserInfo): Observable<any> {
      
      return this.http.get(`http://127.0.0.1:5000/issues?owner=${user.owner}&reponame=${user.repositoryName}`);

  }
}
