import { Component } from '@angular/core';
import { DataService } from '../../services/data.service';
import { TableDataService } from 'src/app/services/tabledata.service';

@Component({
  selector: 'app-ingredient-item-input',
  templateUrl: './ingredient-item-input.component.html',
  styleUrls: ['./ingredient-item-input.component.css'],
})
export class IngredientItemInputComponent {
  name: string = '';
  description: string = '';
  price: number;
  id: number;
  
  constructor(private dataService: DataService, private tableDataService: TableDataService) { }

  ngOnInit(): void {
    this.tableDataService.selectedId$.subscribe((id) => {
      this.id = id;
    });
  }

  async handleAddDataToDatabase() {
    if (this.name) {
      try {
        await this.dataService.addDataToDatabase(this.name, this.description, this.price).toPromise();
        console.log('Data added successfully');
        // Reload the table data
        this.tableDataService.reloadTable();
      } catch (error) {
        console.error('Error adding data:', error);
      }
    } else {
      console.log('No name provided');
    }
  }

  async handleDeleteDataFromDatabase() {
    if (this.id) {
      try {
        await this.dataService.deleteDataFromDatabase(this.id).toPromise();
        console.log('Data deleted successfully');
        // Reload the table data
        this.tableDataService.reloadTable();
      } catch (error) {
        console.error('Error deleting data:', error);
      }
    } else {
      console.log('No id provided');
    }
  }
  


}
