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

  constructor(
    private dataService: DataService,
    private tableDataService: TableDataService
  ) {}

  ngOnInit(): void {
    this.getAllIngredients();
  }

  onIngredientSelectionChange(event: any) {
    // Update the selected ingredients directly in the TableDataService
    this.tableDataService.setSelectedIngredients(this.selectedIngredients);
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
}
