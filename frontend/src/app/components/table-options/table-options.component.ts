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
  showCostRatio: boolean = false;
  allIngredients: Ingredient[] = [];
  customColumns: string[] = [];
  customConditions: string[] = [];
  columnVar1: string = '';
  columnVar2: string = '';
  conditionVar1: string = '';
  conditionVar2: string = '';
  operator: string = '';
  customColumnOptions: string[] = [
    'Price',
  ];


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
    // Update the selected ingredients directly in the TableDataService
    this.tableDataService.setSelectedIngredients(this.selectedIngredients);
    this.customColumnOptions = ["Price", ...this.selectedIngredients.map((ingredient) => ingredient.name)];
  }

  onShowCostRatioChange(event: any) {
    // Update the showCostRatio directly in the TableDataService
    this.tableDataService.setShowCostRatio(this.showCostRatio);
  }

  getAllIngredients() {
    this.dataService.fetchIngredientData().subscribe((data) => {
      this.allIngredients = data;
    });
  }

  setCustomColumns() {
    this.customColumns.push(this.columnVar1 + '/' + this.columnVar2);
    this.tableDataService.setCustomColumns(this.customColumns);
  }

  setCustomConditions() {
    this.customConditions.push(
      this.conditionVar1 + this.operator + this.conditionVar2
    );
    this.tableDataService.setCustomConditions(this.customConditions);
  }

  clearCustomColumns() {
    this.customColumns = [];
    this.tableDataService.setCustomColumns(this.customColumns);
  }

  clearCustomConditions() {
    this.customConditions = [];
    this.tableDataService.setCustomConditions(this.customConditions);
  }
  

  // TODO: possibly include methods to remove custom columns and conditions
  // adding a new col/con visibly adds it to the page, and clicking it removes it
}
