import { Component } from '@angular/core';
import { DataService } from 'src/app/services/data.service';
import { TableDataService } from 'src/app/services/tabledata.service';

@Component({
  selector: 'app-selected-items',
  templateUrl: './selected-items.component.html',
  styleUrls: ['./selected-items.component.css']
})
export class SelectedItemsComponent {
  selectedIds: number[] = [];
  selectedItems: any[] = [];

  constructor(
    private dataService: DataService,
    private tableDataService: TableDataService
  ) {
    this.tableDataService.selectedIds$.subscribe((ids) => {
      this.selectedIds = ids;
      this.getItems();
    });

  }

  getItems() {
    this.selectedItems = [];
    for(let id of this.selectedIds) {
      this.dataService.fetchItemById(id).subscribe((item) => {
        this.selectedItems.push(item);
      });
    }
  }

  removeItem(id: number) {
    this.selectedIds.splice(this.selectedIds.indexOf(id), 1);
    this.tableDataService.setSelectedIds(this.selectedIds);
  }
}
