import { Component, Input } from '@angular/core';
import { Ingredient } from '../../services/models.service';
import { DataService } from 'src/app/services/data.service';
import { TableDataService } from 'src/app/services/tabledata.service';
import { filter } from 'rxjs';

@Component({
  selector: 'app-table-options',
  templateUrl: './table-options.component.html',
  styleUrls: ['./table-options.component.css'],
})
export class TableOptionsComponent {
  selectedIngredients: Ingredient[] = [];
  allIngredients: Ingredient[] = [];
  customColumns: string[] = [];
  customConditions: string[] = [];
  columnVar1: string = '';
  columnVar2: string = '';
  conditionVar1: string = '';
  conditionVar2: string = '';
  operator: string = '';



  constructor(
    private dataService: DataService,
    private tableDataService: TableDataService
  ) {}

  ngOnInit(): void {
    this.tableDataService.allIngredients$.subscribe((ingredients) => {
      // this.allIngredients = ingredients;
      this.getAllIngredients();
    });
  }

  usePlaceholderData() {
    //sets selected ingredients to calories and protein, sets custom columns to calories/protein, and sets custom conditions to calories > 100
    //get the ingredients from allIngredients
    this.selectedIngredients = this.allIngredients.filter((ingredient) => {
      return ingredient.name == 'Calories' || ingredient.name == 'Protein';
    });
    this.customColumns = ['Protein/Calories', 'Protein/Price', 'Calories/Price'];
    this.customConditions = ['Protein/Calories>0.1'];
    this.tableDataService.setSelectedIngredients(this.selectedIngredients);
    this.tableDataService.setCustomColumns(this.customColumns);
    this.tableDataService.setCustomConditions(this.customConditions);
    this.tableDataService.reloadTable();
  }


  filterColumns() { 
    // remove any columns that are no longer in the selected ingredients
    this.customColumns = this.customColumns.filter((column) => {
      return this.selectedIngredients.some((ingredient) => {
        return column.includes(ingredient.name);
      });
    });
    
    this.tableDataService.setCustomColumns(this.customColumns);
  }

  filterConditions() {
    // remove any conditions that are no longer in the selected ingredients or columns
    this.customConditions = this.customConditions.filter((condition) => {
      return this.selectedIngredients.some((ingredient) => {
        return condition.includes(ingredient.name);
      }) && this.customColumns.some((column) => {
        return condition.includes(column);
      });
    });

    this.tableDataService.setCustomConditions(this.customConditions);
  }

  onIngredientSelectionChange(event: any) {
    
    this.filterColumns(); // remove any columns that are no longer in the selected ingredients
    this.filterConditions(); // remove any conditions that are no longer in the selected ingredients or columns

    // Update the selected ingredients directly in the TableDataService
    this.tableDataService.setSelectedIngredients(this.selectedIngredients);

    this.tableDataService.reloadTable();
  }

  getAllIngredients() {
    this.dataService.fetchIngredientData().subscribe((data) => {
      this.allIngredients = data;
    });
  }

  setCustomColumns() {
    const customColumn = this.columnVar1 + '/' + this.columnVar2;
    if (this.customColumns.includes(customColumn)) { // don't add duplicate columns
      return;
    }
    this.customColumns.push(customColumn);
    this.tableDataService.setCustomColumns(this.customColumns);
    this.tableDataService.reloadTable();
  }

  setCustomConditions() {
    const customCondition = this.conditionVar1 + this.operator + this.conditionVar2;
    if (this.customConditions.includes(customCondition)) { // don't add duplicate conditions
      return;
    }
    this.customConditions.push(customCondition);
    this.tableDataService.setCustomConditions(this.customConditions);
    this.tableDataService.reloadTable();
  }

  clearCustomColumns() {
    this.filterConditions(); // remove any conditions that are no longer in the selected ingredients or columns
    this.customColumns = [];
    this.tableDataService.setCustomColumns(this.customColumns);
    this.tableDataService.reloadTable();
  }

  clearCustomConditions() {
    this.customConditions = [];
    this.tableDataService.setCustomConditions(this.customConditions);
    this.tableDataService.reloadTable();
  }
  
  removeColumn(index: number) {
    this.customColumns.splice(index, 1);
    this.tableDataService.setCustomColumns(this.customColumns);
    this.filterConditions(); // remove any conditions that are no longer in the columns
    this.tableDataService.reloadTable();
  }

  removeCondition(index: number) {
    this.customConditions.splice(index, 1);
    this.tableDataService.setCustomConditions(this.customConditions);
    this.tableDataService.reloadTable();
  }


}
