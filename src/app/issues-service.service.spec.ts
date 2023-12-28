import { TestBed } from '@angular/core/testing';

import { IssuesServiceService } from './issues-service.service';

describe('IssuesServiceService', () => {
  beforeEach(() => TestBed.configureTestingModule({}));

  it('should be created', () => {
    const service: IssuesServiceService = TestBed.get(IssuesServiceService);
    expect(service).toBeTruthy();
  });
});
