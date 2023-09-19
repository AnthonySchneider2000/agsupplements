// data.service.ts
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { ItemIngredient, Item, ItemWithIngredients, Ingredient } from './models.service';
@Injectable({
  providedIn: 'root',
})
export class DataService {
  constructor(private http: HttpClient) {}

  fetchItemBaseData(): Observable<any> {
    return this.http.get<Item[]>('http://localhost:8000/backend/get-item/');
  }

  fetchItemWithIngredientsData(): Observable<ItemWithIngredients[]> {
    return this.http.get<ItemWithIngredients[]>('http://localhost:8000/backend/get-item-with-ingredients/');
  }
  
  fetchIngredientData(): Observable<any> {
    return this.http.get<Ingredient[]>('http://localhost:8000/backend/get-ingredient/');
  }





  addItemToDatabase(name: string, description: string, price: number): Observable<any> {
    const apiUrl = 'http://localhost:8000/backend/create-item/';
    const requestBody = {
      name: name,
      description: description,
      price: price,
    };
    return this.http.post(apiUrl, requestBody);
  }

  deleteItemFromDatabase(id: number): Observable<any> {
    const apiUrl = 'http://localhost:8000/backend/delete-item/' + id + '/';
    return this.http.delete(apiUrl);
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

  addItemWithIngredientsToDatabase(name: string, description: string, price: number, ingredients: ItemIngredient[]): Observable<any> {
    const apiUrl = 'http://localhost:8000/backend/create-item-with-ingredients/';
    console.log(ingredients);
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


}
