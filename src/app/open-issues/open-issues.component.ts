import { Component, OnInit } from '@angular/core';
import {IssuesServiceService} from '../issues-service.service';
import {UserInfo} from '../Userinfo'

@Component({
  selector: 'app-open-issues',
  templateUrl: './open-issues.component.html',
  styleUrls: ['./open-issues.component.css']
})
export class OpenIssuesComponent implements OnInit {


  userInfo: UserInfo = new UserInfo();
  inputURL: String = '';
  outputScreen:boolean = false;
  inputScreen:boolean = true;


  constructor(private issueServiceService: IssuesServiceService) { }

  ngOnInit() {}

  /*This function takes in the incoming input github public repo link and extracts arguments owner and reponame to send it to backend*/
  getRequestParams() {
    
     var url = this.inputURL.split('/');
     var length = url.length;
      
     this.userInfo.repositoryName = url[length -1];
     this.userInfo.owner = url[length -2];
       
     console.log(this.userInfo.repositoryName);
     console.log(this.userInfo.owner)
     this.fetchOpenIssuesCount(this.userInfo);

  }


  /*This function makes call to the service class to hit backend, and processes incoming response to display on UI*/
  fetchOpenIssuesCount(userInfo: UserInfo) {

    this.issueServiceService.fetchOpenIssuesCount(userInfo).subscribe (

      response => {
              this.userInfo.issueCount = response;
              this.outputScreen = true;
              this.inputScreen = false;

      },
      error => console.log('error', error)

    );
    };


    goBack() {
      this.outputScreen = false;
      this.inputScreen = true;
    };

  }


