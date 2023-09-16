// data.service.ts
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class DataService {
  constructor(private http: HttpClient) {}

  fetchData(): Observable<any> { //to be removed, replaced by fetchItemBaseData
    return this.http.get("http://localhost:8000/backend/get-item/");
  }


  fetchItemBaseData(): Observable<any> {
    return this.http.get('http://localhost:8000/backend/get-item/');
  }

  fetchItemWithIngredientsData(): Observable<any> {
    return this.http.get('http://localhost:8000/backend/get-item-with-ingredients/');
  }



  addDataToDatabase(name: string, description: string, price: number): Observable<any> {
    const apiUrl = 'http://localhost:8000/backend/create-item/';
    const requestBody = {
      name: name,
      description: description,
      price: price,
    };
    return this.http.post(apiUrl, requestBody);
  }

  deleteDataFromDatabase(id: number): Observable<any> {
    const apiUrl = 'http://localhost:8000/backend/delete-item/' + id + '/';
    return this.http.delete(apiUrl);
  }
}
