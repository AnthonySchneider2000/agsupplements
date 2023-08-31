// data.service.ts
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class DataService {
  constructor(private http: HttpClient) {}

  fetchData(): Observable<any> {
    const data = this.http.get("http://localhost:8000/backend/get-dummy-data/");
    console.log("In service:");
    console.log(data);
    return data;
  }
}
