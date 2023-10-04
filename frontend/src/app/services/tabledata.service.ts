import { Injectable } from '@angular/core';
import { Subject, BehaviorSubject } from 'rxjs';
import { Ingredient, ItemWithIngredients } from './models.service';

@Injectable({
  providedIn: 'root',
})
export class TableDataService {
  private baseItem: ItemWithIngredients = {
    id: 0,
    name: '',
    description: '',
    price: 0,
    link: '',
    servings: 0,
    ingredients: [],
  };



  private reloadTableSubject = new Subject<void>();

  // Observable for reloading the table
  reloadTable$ = this.reloadTableSubject.asObservable();

  // Method to trigger table reload
  reloadTable() {
    this.reloadTableSubject.next();
  }

  private selectedIdSubject = new Subject<number>();

  // Observable for getting the selected id
  selectedId$ = this.selectedIdSubject.asObservable();

  setSelectedId(id: number) {
    this.selectedIdSubject.next(id);
  }
  
  private selectedItemSubject = new BehaviorSubject<ItemWithIngredients>(this.baseItem);

  // Observable for getting the selected item
  selectedItem$ = this.selectedItemSubject.asObservable();

  setSelectedItem(item: ItemWithIngredients) {
    this.selectedItemSubject.next(item);
  }

  private selectedIngredientsSubject = new BehaviorSubject<Ingredient[]>([]);

  // Observable for getting the selected ingredients
  selectedIngredients$ = this.selectedIngredientsSubject.asObservable();

  setSelectedIngredients(selectedIngredients: Ingredient[]) {
    this.selectedIngredientsSubject.next(selectedIngredients);
  }

  private showCostRatioSubject = new BehaviorSubject<boolean>(false);

  // Observable for getting the showCostRatio
  showCostRatio$ = this.showCostRatioSubject.asObservable();

  setShowCostRatio(showCostRatio: boolean) {
    this.showCostRatioSubject.next(showCostRatio);
  }

  private customColumnsSubject = new BehaviorSubject<string[]>([]);
  // Observable for getting the customColumns
  customColumns$ = this.customColumnsSubject.asObservable();

  setCustomColumns(customColumns: string[]) {
    this.customColumnsSubject.next(customColumns);
  }

  private customConditionsSubject = new BehaviorSubject<string[]>([]);
  // Observable for getting the customConditions
  customConditions$ = this.customConditionsSubject.asObservable();

  setCustomConditions(customConditions: string[]) {
    this.customConditionsSubject.next(customConditions);
  }

  private allIngredientsSubject = new BehaviorSubject<Ingredient[]>([]);
  // Observable for getting the allIngredients
  allIngredients$ = this.allIngredientsSubject.asObservable();

  setAllIngredients(allIngredients: Ingredient[]) {
    this.allIngredientsSubject.next(allIngredients);
  }
  
  
}
