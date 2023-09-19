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
  displayedColumns: string[] = ['name', 'description', 'price'];
  @ViewChild(MatPaginator) paginator: MatPaginator;
  @ViewChild(MatSort) sort: MatSort;

  constructor(
    private dataService: DataService,
    private tableDataService: TableDataService
  ) {}

  ngOnInit(): void {
    this.loadData();
    this.tableDataService.reloadTable$.subscribe(() => {
      // reload table
      console.log('Reloading table');
      this.loadData();
    });
  }

  loadData() {
    this.dataService.fetchItemWithIngredientsData().subscribe((data) => {
      console.log(data);
      this.dataSource = new MatTableDataSource(data);
      this.getAllIngredients();
      this.dataSource.paginator = this.paginator;
      this.dataSource.sort = this.sort;
    });
  }
  
  onIngredientSelectionChange(event: any) {
    // You can handle the selected ingredients logic here if needed
    // For example, you can add it to the selectedIngredients array
    // this.selectedIngredients.push(event.value);
  
    // Update the displayed columns without reloading the table
    this.displayedColumns = ['name', 'description', 'price', ...this.selectedIngredients.map(ingredient => ingredient.name)];
    if (this.selectedIngredients.length === 0) {
      // If no ingredients are selected, reset the table
      this.loadData();
    } else {
      // Otherwise, filter the data based on the selected ingredients
      this.filterDataByIngredients(this.selectedIngredients);
    }
  }
  
  filterDataByIngredients(selectedIngredients: Ingredient[]): void {
    if (!selectedIngredients || selectedIngredients.length === 0) {
      // If no ingredients are selected, reset the table
      this.loadData();
      return;
    }
  
    this.dataSource.data = this.dataSource.data.filter((item: ItemWithIngredients) => {
      // Check if the item has ingredients
      if (!item.ingredients || item.ingredients.length === 0) {
        console.log('Item ' + item.name + ' has no ingredients');
        return false;
      }
  
      // Extract the ingredient IDs from the item's ingredients
      const itemIngredientIds = item.ingredients.map((itemIngredient: ItemIngredient) =>
        itemIngredient.ingredient ? itemIngredient.ingredient.id : null
      );
  
      // If the item doesn't have any valid ingredient IDs, consider it as not containing the selected ingredients
      if (!itemIngredientIds.some(id => id !== null)) {
        return false;
      }
  
      // Check if all selected ingredient IDs are included in the item's ingredient IDs
      return selectedIngredients.every((ingredient: Ingredient) =>
        itemIngredientIds.includes(ingredient.id)
      );
    });
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
