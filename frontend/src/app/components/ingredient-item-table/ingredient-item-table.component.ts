import { Component, OnInit, ViewChild, Input } from '@angular/core';
import { DataService } from '../../services/data.service';
import { MatTableDataSource } from '@angular/material/table';
import { MatPaginator } from '@angular/material/paginator';
import { MatSort } from '@angular/material/sort';
import { TableDataService } from 'src/app/services/tabledata.service';
import {
  ItemWithIngredients,
  ItemIngredient,
  Ingredient,
} from '../../services/models.service';

@Component({
  selector: 'app-ingredient-item-table',
  templateUrl: './ingredient-item-table.component.html',
  styleUrls: ['./ingredient-item-table.component.css'],
})
export class IngredientItemTableComponent implements OnInit {
  allIngredients: Ingredient[] = [];
  selectedIngredients: Ingredient[] = [];
  dataSource: MatTableDataSource<any>;
  baseColumns: string[] = ['name', 'description', 'price'];
  displayedColumns: string[] = ['name', 'description', 'price'];
  showCostRatio: boolean = false; // Initialize with default value
  @ViewChild(MatPaginator) paginator: MatPaginator;
  @ViewChild(MatSort) sort: MatSort;

  originalData: ItemWithIngredients[] = [];

  constructor(
    private dataService: DataService,
    private tableDataService: TableDataService
  ) {
    // Subscribe to selectedIngredients$ and showCostRatio$ observables
    this.tableDataService.selectedIngredients$.subscribe((ingredients) => {
      this.selectedIngredients = ingredients;
      // When selectedIngredients change, update the columns and filter data
      this.filterData();
    });

    this.tableDataService.showCostRatio$.subscribe((costRatio) => {
      this.showCostRatio = costRatio;
      // When showCostRatio changes, reload the data
    });
  }

  ngOnInit(): void {
    this.loadData();
    this.tableDataService.reloadTable$.subscribe(() => {
      // Reload table when needed
      console.log('Reloading table');
      this.loadData();
    });
  }

  loadData() {
    this.getAllIngredients();
    this.dataService.fetchItemWithIngredientsData().subscribe((data) => {
      this.dataSource = new MatTableDataSource(data);
      this.originalData = data; // Store the original data
      this.dataSource.paginator = this.paginator;
      this.dataSource.sort = this.sort;
      this.filterData(); // Apply filters after loading data
    });
  }

  filterData() {
    let filteredData = this.originalData;

    // Apply selectedIngredients filter
    if (this.selectedIngredients.length > 0) {
      filteredData = filteredData.filter((item) => {
        const itemIngredientIds = item.ingredients.map((itemIngredient) =>
          itemIngredient.ingredient ? itemIngredient.ingredient.id : null
        );
        return this.selectedIngredients.every((ingredient) =>
          itemIngredientIds.includes(ingredient.id)
        );
      });
    }

    // Apply showCostRatio filter
    if (this.showCostRatio) {
      // Add logic here to filter based on cost ratio if needed
      // Example: filteredData = filteredData.filter((item) => item.someCondition);
    }

    this.dataSource.data = filteredData;
    this.displayedColumns = [...this.baseColumns, ...this.selectedIngredients.map((ingredient) => ingredient.name)];

  }

  getIngredientMass(item: ItemWithIngredients, ingredient: Ingredient) {
    const itemIngredient = item.ingredients.find(
      (itemIngredient) => itemIngredient.ingredient.id === ingredient.id
    );
    return itemIngredient ? itemIngredient.mass : 0;
  }

  getAllIngredients() {
    this.dataService.fetchIngredientData().subscribe((data) => {
      this.allIngredients = data;
      console.log(this.allIngredients);
    });
  }

  applyFilter(event: any) {
    const filterValue = (event.target as HTMLInputElement).value;
    this.dataSource.filter = filterValue.trim().toLowerCase();
  }
  onRowClick(row: any) {
    this.tableDataService.setSelectedId(row.id);
  }
  capitalizeFirstLetter(string: string) {
    return string.charAt(0).toUpperCase() + string.slice(1);
  }
}
