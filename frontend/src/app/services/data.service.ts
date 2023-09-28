// data.service.ts
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { ItemIngredient, ItemWithIngredients, Ingredient } from './models.service';
import { HttpHeaders } from '@angular/common/http';
@Injectable({
  providedIn: 'root',
})
export class DataService {
  constructor(private http: HttpClient) {}

  fetchItemWithIngredientsData(): Observable<ItemWithIngredients[]> {
    return this.http.get<ItemWithIngredients[]>('http://localhost:8000/backend/get-item-with-ingredients/');
  }
  
  fetchIngredientData(): Observable<any> {
    return this.http.get<Ingredient[]>('http://localhost:8000/backend/get-ingredient/');
  }

  fetchCurrentTableData(selectedIngredients: Ingredient[], conditions: string[], columns: string[]): Observable<any> {
    const apiUrl = 'http://localhost:8000/backend/get-current-table-data/';
    const requestBody = {
      selectedIngredients: selectedIngredients,
      conditions: conditions,
      columns: columns,
    };

    console.log('Sending request to backend - current table data');
    // console.log(requestBody);

    return this.http.post(apiUrl, requestBody);
  }

  fetchFilteredTableData(selectedIngredients: Ingredient[], showCostRatio: boolean): Observable<any> {
    const apiUrl = 'http://localhost:8000/backend/get-filtered-table-data/';
    const requestBody = {
      selectedIngredients: selectedIngredients,
      showCostRatio: showCostRatio,
    };

    console.log('Sending request to backend - filtered table data');
    // console.log(requestBody);

    return this.http.post(apiUrl, requestBody);
  }






  addIngredientToDatabase(name: string, description: string, price: number): Observable<any> {
    const apiUrl = 'http://localhost:8000/backend/create-ingredient/';
    const requestBody = {
      name: name,
      description: description,
      price: price,
    };
    return this.http.post(apiUrl, requestBody);
  }

  deleteIngredientFromDatabase(id: number): Observable<any> {
    const apiUrl = 'http://localhost:8000/backend/delete-ingredient/' + id + '/';
    return this.http.delete(apiUrl);
  }

  deleteIngredientByNameFromDatabase(name: string): Observable<any> {
    const apiUrl = 'http://localhost:8000/backend/delete-ingredient-by-name/' + name + '/';
    return this.http.delete(apiUrl);
  }

  addItemWithIngredientsToDatabase(name: string, description: string, price: number, ingredients: ItemIngredient[], link: string): Observable<any> {
    const apiUrl = 'http://localhost:8000/backend/create-item-with-ingredients/';
    const requestBody = {
      name: name,
      description: description,
      price: price,
      ingredients: ingredients,
    };
    return this.http.post(apiUrl, requestBody);
  }

  deleteItemWithIngredientsFromDatabase(id: number): Observable<any> {
    const apiUrl = 'http://localhost:8000/backend/delete-item-with-ingredients/' + id + '/';
    return this.http.delete(apiUrl);
  }

  //send a list of item ingredients to the backend and receive a list of cost ratios
  getIngredientCostRatioList(ingredients: ItemIngredient[]): Observable<any> {
    const apiUrl = 'http://localhost:8000/backend/get-ingredient-cost-ratio-list/';
    const requestBody = {
      ingredients: ingredients,
    };
    return this.http.post(apiUrl, requestBody);
  }


  blacklistItem(id: number): Observable<any> {
    const apiUrl = 'http://localhost:8000/backend/blacklist-item/' + id + '/';
    return this.http.post(apiUrl, {});
  }
  
}
