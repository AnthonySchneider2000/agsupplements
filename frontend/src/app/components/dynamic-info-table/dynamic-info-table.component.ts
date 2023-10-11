import { Component, OnInit, ViewChild, Input } from '@angular/core';
import { DataService } from '../../services/data.service';
import { MatTableDataSource } from '@angular/material/table';
import { MatPaginator } from '@angular/material/paginator';
import { MatSort } from '@angular/material/sort';
import { TableDataService } from 'src/app/services/tabledata.service';
import {
  Item,
  ItemIngredient,
  Ingredient,
} from '../../services/models.service';

@Component({
  selector: 'app-dynamic-info-table',
  templateUrl: './dynamic-info-table.component.html',
  styleUrls: ['./dynamic-info-table.component.css'],
})
export class DynamicInfoTableComponent implements OnInit {
  selectedIngredients: Ingredient[] = [];
  dataSource: MatTableDataSource<any>;
  ItemData: Item[] = [];
  baseColumns: string[] = ['name', 'Price'];
  displayedColumns: string[] = ['name', 'Price'];
  ingredientColumns: string[] = [];
  customColumns: string[] = [];
  customConditions: string[] = [];
  filterValue: string = '';
  @ViewChild(MatPaginator) paginator: MatPaginator;
  @ViewChild(MatSort) sort: MatSort;

  constructor(
    private dataService: DataService,
    private tableDataService: TableDataService
  ) {
    // Subscribe to selectedIngredients$ observable
    this.tableDataService.selectedIngredients$.subscribe((ingredients) => {
      this.selectedIngredients = ingredients;
    });

    this.tableDataService.customColumns$.subscribe((customColumns) => {
      this.customColumns = customColumns;
    });

    this.tableDataService.customConditions$.subscribe((customConditions) => {
      this.customConditions = customConditions;
    });
  }

  ngOnInit(): void {
    this.getItemData();
    this.loadData();
    this.tableDataService.reloadTable$.subscribe(() => {
      // Reload table when needed
      console.log('Reloading table');
      this.loadData();
    });
  }

  loadData() {
    const outerStartTime = performance.now();
    console.log('Loading data from backend at ' + outerStartTime);
    this.dataService
      .fetchCurrentTableData(
        this.selectedIngredients,
        this.customConditions,
        this.customColumns
      )
      .subscribe((data) => {
        const startTime = performance.now();
        console.log('Data received from backend at ' + startTime);
        this.dataSource = new MatTableDataSource(data);
        this.dataSource.paginator = this.paginator;
        this.dataSource.sort = this.sort;
        this.applyFilter({ target: { value: this.filterValue } });
        this.ingredientColumns = this.selectedIngredients.map(
          (ingredient) => ingredient.name
        );

        this.displayedColumns = [
          ...this.baseColumns,
          ...this.ingredientColumns,
          ...this.customColumns,
        ];
        const endTime = performance.now();
        console.log('Data loaded at ' + endTime);
        console.log('Time to load data: ' + (endTime - startTime) + 'ms');
        console.log('Total time: ' + (endTime - outerStartTime) + 'ms');
      });
  }

  getItemData() {
    this.dataService.fetchItemData().subscribe((data) => {
      this.ItemData = data;
    });
  }
  applyFilter(event: any) {
    const filterValue = (event.target as HTMLInputElement).value;
    this.filterValue = filterValue;
    const subFilters = filterValue.split('$');
    const filterPredicates: any[] = [];
  
    subFilters.forEach((subFilter) => {
      const startsWithExclamation = subFilter.startsWith('!');
      const filterValueWithoutExclamation = startsWithExclamation
        ? subFilter.substring(1)
        : subFilter;
  
      const orConditions = filterValueWithoutExclamation.split('|'); // Split by |
  
      filterPredicates.push((data: any) => {
        const dataValue = data.name.toLowerCase(); // Replace with the correct property you want to filter by
        if (startsWithExclamation) {
          // Filter with negation
          return !orConditions.some((condition) =>
            dataValue.includes(condition)
          );
        } else {
          // Filter without negation
          return orConditions.some((condition) =>
            dataValue.includes(condition)
          );
        }
      });
    });
  
    // Combine filter predicates into a single predicate
    this.dataSource.filterPredicate = (data: any, filter: string) => {
      return filterPredicates.every((predicate) => predicate(data));
    };
  
    if (filterValue.startsWith('!')) {
      this.dataSource.filter = filterValue.substring(1).trim().toLowerCase();
    } else {
      this.dataSource.filter = filterValue.trim().toLowerCase();
    }
  }
  
  onRowClick(row: any, event: MouseEvent) {
    if (event.ctrlKey) {
      window.open(row.link, '_blank');
    } else if (event.shiftKey) {
      localStorage.setItem('selectedId', row.id.toString()); // save the selected id to localStorage
      window.location.href = '/product-page'; // navigate the current page to /product-page
    } else {
      this.dataService.fetchItemById(row.id).subscribe((data) => {
        // fetch the item data from the backend
        this.tableDataService.setSelectedItem(data); // set the selected item in the TableDataService
      });
      this.tableDataService.setSelectedId(row.id);
    }
  }
  capitalizeFirstLetter(string: string) {
    return string.charAt(0).toUpperCase() + string.slice(1);
  }
}
