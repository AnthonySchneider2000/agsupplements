import { Injectable } from '@angular/core';
import { Subject, BehaviorSubject } from 'rxjs';
import { Ingredient } from './models.service';

@Injectable({
  providedIn: 'root',
})
export class TableDataService {
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
  
}
