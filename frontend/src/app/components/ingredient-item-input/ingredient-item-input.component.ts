import { Component } from '@angular/core';
import { DataService } from '../../services/data.service';
import { TableDataService } from 'src/app/services/tabledata.service';
import { MatSelectModule } from '@angular/material/select';
import {
  ItemWithIngredients,
  ItemIngredient,
  Ingredient,
} from '../../services/models.service';

@Component({
  selector: 'app-ingredient-item-input',
  templateUrl: './ingredient-item-input.component.html',
  styleUrls: ['./ingredient-item-input.component.css'],
})
// manipulates data for the ItemWithIngredients table
// can create and delete items and ingredients
export class IngredientItemInputComponent {
  allIngredients: Ingredient[] = [];
  inputIngredients: Ingredient[] = [];
  ingredient: Ingredient = {
    id: 0,
    name: '',
    description: '',
    price: 1.0,
  };
  item: ItemWithIngredients = {
    id: 0,
    name: '',
    description: '',
    price: 0,
    link: '',
    ingredients: [],
  };
  servings: number = 1;

  constructor(
    private dataService: DataService,
    private tableDataService: TableDataService
  ) {}

  ngOnInit(): void {
    this.tableDataService.selectedId$.subscribe((id) => {
      this.item.id = id;
    });
    this.tableDataService.selectedItem$.subscribe((item) => {
      this.item = item;
    });
    this.dataService.fetchIngredientData().subscribe((data) => {
      this.allIngredients = data;
    });
  }

  addItem() {
    if (this.inputIngredients.length > 0) {
      for (let ingredient of this.inputIngredients) {
        const mass = prompt('Enter mass of ' + ingredient.name + ' in grams');
        this.item.ingredients.push({
          id: ingredient.id,
          ingredient: ingredient,
          mass: Number(mass) * this.servings,
        });
      }
    }

    this.dataService
      .addItemWithIngredientsToDatabase(this.item)
      .subscribe((data) => {
        this.tableDataService.reloadTable();
      });
    this.resetData();
  }

  updateItem() {
    if (this.inputIngredients.length > 0) {
      for (let ingredient of this.inputIngredients) {
        const mass = prompt('Enter mass of ' + ingredient.name + ' in grams');
        this.item.ingredients.push({
          id: ingredient.id,
          ingredient: ingredient,
          mass: Number(mass) * this.servings,
        });
      }
    }

    this.dataService.updateItem(this.item).subscribe((data) => {
      this.tableDataService.reloadTable();
    });

    this.resetData();
  }

  deleteItem() {
    this.dataService
      .deleteItemWithIngredientsFromDatabase(this.item.id)
      .subscribe((data) => {
        this.tableDataService.reloadTable();
      });
    this.resetData();
  }

  blacklistItem() {
    this.dataService.blacklistItem(this.item.id).subscribe((data) => {
      this.tableDataService.reloadTable();
    });
  }

  addIngredient() {
    this.dataService
      .addIngredientToDatabase(
        this.ingredient.name,
        this.ingredient.description,
        this.ingredient.price
      )
      .subscribe((data) => {
        this.getAllIngredients();
        this.tableDataService.setAllIngredients(this.allIngredients);
        this.resetData();
      });
  }

  deleteIngredient() {
    this.dataService
      .deleteIngredientFromDatabase(this.ingredient.id)
      .subscribe((data) => {
        this.allIngredients = this.allIngredients.filter(
          (ingredient) => ingredient.id !== this.ingredient.id
        );
        this.tableDataService.setAllIngredients(this.allIngredients);
        this.resetData();
      });
  }

  getAllIngredients() {
    this.dataService.fetchIngredientData().subscribe((data) => {
      this.allIngredients = data;
    });
  }

  resetData() {
    this.ingredient.description = '';
    this.ingredient.name = '';
    this.ingredient.price = 1.0;
    this.ingredient.id = 0;
    this.item.name = '';
    this.item.description = '';
    this.item.price = 0;
    this.item.link = '';
    this.item.ingredients = [];
    this.inputIngredients = [];
    this.servings = 1;
  }
}
