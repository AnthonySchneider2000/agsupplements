import { Component } from '@angular/core';
import { DataService } from '../../services/data.service';
import { TableDataService } from 'src/app/services/tabledata.service';
import {MatSelectModule} from '@angular/material/select';
import { ItemWithIngredients, ItemIngredient, Ingredient } from '../../services/models.service';

@Component({
  selector: 'app-ingredient-item-input',
  templateUrl: './ingredient-item-input.component.html',
  styleUrls: ['./ingredient-item-input.component.css'],
})
// manipulates data for the ItemWithIngredients table
// can create and delete items and ingredients
export class IngredientItemInputComponent {
  id: number = 0;
  name: string = '';
  description: string = '';
  price: number = 0;
  allIngredients: Ingredient[] = [];
  itemIngredients: ItemIngredient[] = [];
  ingredient: Ingredient = {
    id: 0,
    name: '',
    description: '',
    price: 1.0,
  };
  mass: number = 0;
  
  
  constructor(private dataService: DataService, private tableDataService: TableDataService) { }

  ngOnInit(): void {
    this.tableDataService.selectedId$.subscribe((id) => {
      this.id = id;
    });
    this.getAllIngredients();
  }

  addItemWithIngredients() {
    this.dataService.addItemWithIngredientsToDatabase(this.name, this.description, this.price, this.itemIngredients).subscribe((data) => {
      this.tableDataService.reloadTable();
    });
  }

  deleteItemWithIngredients() {
    this.dataService.deleteItemWithIngredientsFromDatabase(this.id).subscribe((data) => {
      this.tableDataService.reloadTable();
    });
  }

  addIngredient() {
    this.dataService.addIngredientToDatabase(this.ingredient.name, this.ingredient.description, this.ingredient.price).subscribe((data) => {
      this.tableDataService.reloadTable();
    });
  }

  deleteIngredient() {
    this.dataService.deleteIngredientFromDatabase(this.ingredient.id).subscribe((data) => {
      this.tableDataService.reloadTable();
    });
  }

  getAllIngredients() {
    this.dataService.fetchIngredientData().subscribe((data) => {
      this.allIngredients = data;
    });
  }

  addIngredientToItem() {
    this.itemIngredients.push({
      id: 0,
      item: {
        id: 0,
        name: '',
        description: '',
        price: 0,
        ingredients: [],
      },
      ingredient: this.ingredient,
      mass: this.mass,
    });
  }

}
