// data.service.ts
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { ItemIngredient, Item, Ingredient } from './models.service';
import { HttpHeaders } from '@angular/common/http';
@Injectable({
  providedIn: 'root',
})
export class DataService {
  constructor(private http: HttpClient) {}

  fetchItemData(): Observable<Item[]> {
    return this.http.get<Item[]>(
      'http://localhost:8000/backend/get-all-items/'
    );
  }

  fetchIngredientData(): Observable<any> {
    return this.http.get<Ingredient[]>(
      'http://localhost:8000/backend/get-all-ingredients/'
    );
  }

  fetchCurrentTableData(
    selectedIngredients: Ingredient[],
    conditions: string[],
    columns: string[]
  ): Observable<any> {
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

  fetchItemById(id: number): Observable<Item> {
    const apiUrl = 'http://localhost:8000/backend/get-item-by-id/' + id + '/';
    return this.http.get<Item>(apiUrl);
  }

  addIngredientToDatabase(ingredient: Ingredient): Observable<any> {
    const apiUrl = 'http://localhost:8000/backend/create-ingredient/';
    const requestBody = {
      name: ingredient.name,
      description: ingredient.description,
      price: ingredient.price,
      units: ingredient.units,
    };
    return this.http.post(apiUrl, requestBody);
  }

  deleteIngredientFromDatabase(id: number): Observable<any> {
    const apiUrl =
      'http://localhost:8000/backend/delete-ingredient/' + id + '/';
    return this.http.delete(apiUrl);
  }

  deleteIngredientByNameFromDatabase(name: string): Observable<any> {
    const apiUrl =
      'http://localhost:8000/backend/delete-ingredient-by-name/' + name + '/';
    return this.http.delete(apiUrl);
  }

  addItemToDatabase(item: Item): Observable<any> {
    const apiUrl = 'http://localhost:8000/backend/create-item/';
    const requestBody = {
      name: item.name,
      description: item.description,
      price: item.price,
      link: item.link,
      ingredients: item.ingredients,
      servings: item.servings,
      tags: item.tags,
    };
    return this.http.post(apiUrl, requestBody);
  }

  deleteItemFromDatabase(id: number): Observable<any> {
    const apiUrl = 'http://localhost:8000/backend/delete-item/' + id + '/';
    return this.http.delete(apiUrl);
  }

  updateItem(item: Item): Observable<any> {
    const apiUrl = 'http://localhost:8000/backend/update-item/' + item.id + '/';
    const requestBody = {
      name: item.name,
      description: item.description,
      price: item.price,
      link: item.link,
      ingredients: item.ingredients,
      servings: item.servings,
      tags: item.tags,
    };
    return this.http.put(apiUrl, requestBody);
  }

  blacklistItem(id: number): Observable<any> {
    const apiUrl = 'http://localhost:8000/backend/blacklist-item/' + id + '/';
    return this.http.post(apiUrl, {});
  }
}
