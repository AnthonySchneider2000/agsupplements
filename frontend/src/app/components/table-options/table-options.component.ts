import { Component, Input } from '@angular/core';
import { Ingredient } from '../../services/models.service';
import { DataService } from 'src/app/services/data.service';
import { TableDataService } from 'src/app/services/tabledata.service';

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

  onIngredientSelectionChange(event: any) {
    // remove any columns that are no longer in the selected ingredients
    this.customColumns = this.customColumns.filter((column) => {
      return this.selectedIngredients.some((ingredient) => {
        return column.includes(ingredient.name);
      });
    });
    
    this.tableDataService.setCustomColumns(this.customColumns);

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
    this.customColumns.push(this.columnVar1 + '/' + this.columnVar2);
    this.tableDataService.setCustomColumns(this.customColumns);
    this.tableDataService.reloadTable();
  }

  setCustomConditions() {
    this.customConditions.push(
      this.conditionVar1 + this.operator + this.conditionVar2
    );
    this.tableDataService.setCustomConditions(this.customConditions);
    this.tableDataService.reloadTable();
  }

  clearCustomColumns() {
    this.customColumns = [];
    this.tableDataService.setCustomColumns(this.customColumns);
    this.tableDataService.reloadTable();
  }

  clearCustomConditions() {
    this.customConditions = [];
    this.tableDataService.setCustomConditions(this.customConditions);
    this.tableDataService.reloadTable();
  }
  

  // TODO: possibly include methods to remove custom columns and conditions
  // adding a new col/con visibly adds it to the page, and clicking it removes it
}
