import { Component, OnInit, ViewChild, Input } from '@angular/core';
import { DataService } from '../../services/data.service';
import { MatTableDataSource } from '@angular/material/table';
import { MatPaginator } from '@angular/material/paginator';
import { MatSort } from '@angular/material/sort';
import { TableDataService } from 'src/app/services/tabledata.service';
import {
  ItemWithIngredients as Item,
  ItemIngredient,
  Ingredient,
} from '../../services/models.service';

@Component({
  selector: 'app-dynamic-info-table',
  templateUrl: './dynamic-info-table.component.html',
  styleUrls: ['./dynamic-info-table.component.css'],
})
export class DynamicInfoTableComponent implements OnInit {
  allIngredients: Ingredient[] = [];
  selectedIngredients: Ingredient[] = [];
  dataSource: MatTableDataSource<any>;
  ItemData: Item[] = [];
  baseColumns: string[] = ['name', 'price'];
  displayedColumns: string[] = ['name', 'price'];
  ingredientColumns: string[] = [];
  customColumns: string[] = [];
  customConditions: string[] = [];
  showCostRatio: boolean = false; // Initialize with default value
  filterValue: string = '';
  @ViewChild(MatPaginator) paginator: MatPaginator;
  @ViewChild(MatSort) sort: MatSort;

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
      if (this.selectedIngredients.length > 0) {
        this.filterData();
      }
    });

    this.tableDataService.customColumns$.subscribe((customColumns) => {
      this.customColumns = customColumns;
      // When customColumns change, reload the data
      if (this.selectedIngredients.length > 0) {
        this.filterData();
      }
    });

    this.tableDataService.customConditions$.subscribe((customConditions) => {
      this.customConditions = customConditions;
      console.log(this.customConditions);
      // When customConditions change, reload the data
      this.filterData();
    });
  }

  ngOnInit(): void {
    this.getAllIngredients();
    this.getItemData();
    this.loadData();
    this.tableDataService.reloadTable$.subscribe(() => {
      // Reload table when needed
      console.log('Reloading table');
      this.loadData();
    });
  }

  loadData() {
    this.dataService
      .fetchCurrentTableData(
        this.selectedIngredients,
        this.customConditions,
        this.customColumns
      )
      .subscribe((data) => {
        this.dataSource = new MatTableDataSource(data);
        this.dataSource.paginator = this.paginator;
        this.dataSource.sort = this.sort;
        this.dataSource.filter = this.filterValue.trim().toLowerCase();
      });
  }

  filterData() {
    this.loadData();
    this.ingredientColumns = this.selectedIngredients.map(
      (ingredient) => ingredient.name
    );

    this.displayedColumns = [
      ...this.baseColumns,
      ...this.ingredientColumns,
      ...this.customColumns,
    ];

    // Apply showCostRatio filter
    if (this.showCostRatio) {
      this.displayedColumns = [
        ...this.baseColumns,
        ...this.ingredientColumns,
        ...this.selectedIngredients.map(
          (ingredient) => ingredient.name + ' Cost Ratio'
        ),
      ];
    }
  }

  getAllIngredients() {
    this.dataService.fetchIngredientData().subscribe((data) => {
      this.allIngredients = data;
      this.tableDataService.setAllIngredients(this.allIngredients);
    });
  }

  getItemData() {
    this.dataService.fetchItemWithIngredientsData().subscribe((data) => {
      this.ItemData = data;
    });
  }

  applyFilter(event: any) {
    const filterValue = (event.target as HTMLInputElement).value;
    this.filterValue = filterValue;
    this.dataSource.filter = filterValue.trim().toLowerCase();
  }
  onRowClick(row: any, event: MouseEvent) {
    if (event.ctrlKey) {
      window.open(row.link, '_blank');
    } else {
      this.tableDataService.setSelectedId(row.id);
    }
  }
  capitalizeFirstLetter(string: string) {
    return string.charAt(0).toUpperCase() + string.slice(1);
  }
}
